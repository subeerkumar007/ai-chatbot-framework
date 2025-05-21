"use client";

import React, { useState, useEffect, useCallback } from "react";
import {
  listDocuments,
  uploadDocument,
  deleteDocument,
  KnowledgeBaseDocument,
} from "@/app/services/knowledgeBase";
import { useSnackbar } from "@/app/components/Snackbar/SnackbarContext";
import { TrashIcon } from "@heroicons/react/24/outline";
import { Modal, Button } from "flowbite-react";

const DocumentModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (title: string, content: string, file: File | null, type: "file" | "text") => void;
  isLoading: boolean;
}> = ({ isOpen, onClose, onSubmit, isLoading }) => {
  const [documentType, setDocumentType] = useState<"file" | "text">("text");
  const [file, setFile] = useState<File | null>(null);
  const [documentTitle, setTitle] = useState("");
  const [documentContent, setContent] = useState("");

  useEffect(() => {
    if (!isOpen) {
      setTitle("");
      setContent("");
      setFile(null);
      setDocumentType("text");
    }
  }, [isOpen]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const isValid = documentTitle.trim() !== "" && (documentType === "text" ? documentContent.trim() !== "" : !!file);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(documentTitle, documentContent, file, documentType);
  };

  return (
    <Modal show={isOpen} onClose={onClose}>
      <Modal.Header>Add Document</Modal.Header>
      <Modal.Body>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Document Type</label>
            <select
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value as "file" | "text")}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="text">Text</option>
              <option value="file">File</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input
              type="text"
              placeholder="Document Title"
              value={documentTitle}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>

          {documentType === "text" ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Content</label>
              <textarea
                placeholder="Enter document content"
                value={documentContent}
                onChange={(e) => setContent(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 min-h-[100px]"
                required
              />
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">File</label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4">
                <input
                  type="file"
                  onChange={handleFileChange}
                  className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                  required
                />
              </div>
            </div>
          )}
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button type="submit" disabled={!isValid} onClick={handleSubmit} className="w-full bg-green-500 text-white">
          {isLoading ? "Uploading..." : "Upload Document"}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

const KnowledgeBasePage: React.FC = () => {
  const [documents, setDocuments] = useState<KnowledgeBaseDocument[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { addSnackbar } = useSnackbar();

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = useCallback(async () => {
    try {
      const docs = await listDocuments();
      setDocuments(docs);
    } catch (error) {
      addSnackbar("Failed to load documents", "error");
    }
  }, [addSnackbar]);

  const handleSubmit = async (title: string, content: string, file: File | null, type: "file" | "text") => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append("document_title", title);
      formData.append("document_type", type);

      if (type === "file" && file) {
        formData.append("file", file);
      } else if (type === "text") {
        formData.append("document_content", content);
      }

      await uploadDocument(formData);
      addSnackbar("Document uploaded successfully", "success");
      setIsModalOpen(false);
      fetchDocuments();
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || "Failed to upload document";
      addSnackbar(errorMessage, "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (documentId: string) => {
    if (window.confirm("Are you sure you want to delete this document?")) {
      try {
        await deleteDocument(documentId);
        addSnackbar("Document deleted successfully", "success");
        fetchDocuments();
      } catch (error) {
        addSnackbar("Failed to delete document", "error");
      }
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-semibold text-gray-800">Knowledge Base</h1>
          <p className="text-gray-600 mt-1">Manage your chatbot's knowledge base documents</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-200"
        >
          Add Document
        </button>
      </div>

      <div className="grid gap-4">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:border-green-200 transition-colors duration-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-gray-800">{doc.document_title}</h3>
                <p className="text-sm text-gray-500 mt-1">
                  Type: {doc.document_type} | Created: {new Date(doc.created_at).toLocaleDateString()}
                </p>
              </div>
              <button onClick={() => handleDelete(doc.id)} className="p-2 text-gray-400 hover:text-red-500">
                <TrashIcon className="w-5 h-5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      <DocumentModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
};

export default KnowledgeBasePage;
