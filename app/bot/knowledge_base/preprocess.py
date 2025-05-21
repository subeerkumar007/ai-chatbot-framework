import tempfile
from typing import List
from langchain.schema import Document
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
from app.admin.knowledge_base.schemas import KnowledgeBaseDocument


class KnowledgeBasePreprocessor:
    """Handles preprocessing of documents for the knowledge base."""

    SUPPORTED_TYPES = [
        "text/plain",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    DOC_LOADER_MAPPING = {
        "text/plain": TextLoader,
        "application/pdf": PyPDFLoader,
        "application/msword": UnstructuredWordDocumentLoader,
    }

    @staticmethod
    async def process(documents: List[KnowledgeBaseDocument]) -> List[Document]:
        """Process a list of documents and convert them to LangChain documents.

        Args:
            documents: List of KnowledgeBaseDocument objects to process

        Returns:
            List of processed LangChain Document objects
        """
        processed_docs = []

        for doc in documents:
            # Process based on document type
            if doc.document_type == "text/plain":
                # Process text directly
                processed_docs.append(
                    Document(
                        page_content=doc.content,
                        metadata={
                            "source": doc.source,
                            "title": doc.title,
                            "doc_id": str(doc.id),
                        },
                    )
                )
            elif doc.content_type in SUPPORTED_TYPES:
                file_contents = await self.preprocess_document_file(doc.content)
                processed_docs.extend(file_contents)

        return processed_docs

    async def preproces_document_file(self, document_file: bytes) -> List[Document]:
        """Preprocess a document file and convert it to LangChain documents.
        Args:
            document_file: Binary content of the document file
        Returns:
            List of processed LangChain Document objects
        """

        # Create temporary file for binary content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(document_file.binary_content)
            temp_file_path = temp_file.name

        # Load based on file type
        if doc.content_type not in self.DOC_LOADER_MAPPING:
            raise ValueError(f"Unsupported file type: {doc.content_type}")

        loader = self.DOC_LOADER_MAPPING[doc.content_type](temp_file_path)

        loaded_docs = loader.load()

        # Add metadata to each page/section
        for loaded_doc in loaded_docs:
            loaded_doc.metadata.update(
                {"source": doc.source, "title": doc.title, "doc_id": str(doc.id)}
            )
            processed_docs.append(loaded_doc)
        return processed_docs
