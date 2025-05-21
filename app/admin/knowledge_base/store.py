from typing import List
from bson import ObjectId
from app.admin.knowledge_base.schemas import KnowledgeBaseDocument
from app.database import database

knowledge_base_collection = database.get_collection("knowledge_base")

# object store collection
object_store_collection = database.get_collection("object_store")


async def add_document(document_data: dict) -> KnowledgeBaseDocument:
    result = await knowledge_base_collection.insert_one(document_data)
    return await get_document(str(result.inserted_id))


async def get_document(id: str) -> KnowledgeBaseDocument:
    document = await knowledge_base_collection.find_one({"_id": ObjectId(id)})
    return KnowledgeBaseDocument.model_validate(document)


async def list_documents() -> List[KnowledgeBaseDocument]:
    documents = await knowledge_base_collection.find().to_list()
    return [KnowledgeBaseDocument.model_validate(doc) for doc in documents]


async def edit_document(document_id: str, document_data: dict):
    await knowledge_base_collection.update_one(
        {"_id": ObjectId(document_id)}, {"$set": document_data}
    )


async def delete_document(document_id: str):
    await knowledge_base_collection.delete_one({"_id": ObjectId(document_id)})


async def upload_document_file(document_file: bytes):
    result = await object_store_collection.insert_one({"file": document_file})
