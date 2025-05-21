import { API_BASE_URL } from "./base";

export interface KnowledgeBaseDocument {
    id: string;
    document_type: string;
    document_title: string;
    document_content: string;
    created_at: string;
    updated_at: string;
    vector_store_id?: string;
}

export const  uploadDocument = async (formData: FormData) => {
    const response = await fetch(`${API_BASE_URL}knowledge-base/documents`, {
        method: 'POST',
        body: formData,
      });
    return response.json();
}

export const  listDocuments =async () => {
    const response = await fetch(`${API_BASE_URL}knowledge-base/documents`);
    return response.json();
}

export const deleteDocument = async (documentId: string) => {
    const response = await fetch(`${API_BASE_URL}knowledge-base/documents/${documentId}`, {method: 'DELETE'});
    return response.json();
}