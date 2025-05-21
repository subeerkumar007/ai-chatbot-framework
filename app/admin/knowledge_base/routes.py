from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from app.admin.knowledge_base import store
from app.admin.knowledge_base.schemas import KnowledgeBaseDocument
from typing import Annotated

router = APIRouter(prefix="/knowledge-base", tags=["knowledge-base"])

@router.post("/documents")
async def upload_document(
    document_title: Annotated[str, Form()],
    document_type: Annotated[str, Form()],
    document_content: Annotated[str, Form()],
    file: UploadFile = File(None)
):
    """Upload a document to the knowledge base"""
    if not document_content and not file:
        raise HTTPException(
            status_code=400,
            detail="Either content or file must be provided"
        )


    document = KnowledgeBaseDocument(
        document_title=document_title,
        document_type=document_type,
        document_content=document_content
    )

    # If file is provided,store it in object store
    if file:
        content = await file.read()
        content = content.decode("utf-8")
        title = file.filename

        file_id = store.upload_document_file(content)
        document.object_store_id = file_id


    # TODO: Implement vector store integration
    # placeholder for vector store integration
    # vector_store_id = await vector_store.add_document(content)
    # document.vector_store_id = vector_store_id

    return await store.add_document(document.model_dump(exclude={"id": True}))

@router.get("/documents")
async def list_documents():
    """List all documents in the knowledge base"""
    return await store.list_documents()

@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Get a document from the knowledge base"""
    return await store.get_document(document_id)

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document from the knowledge base"""
    return await store.delete_document(document_id)