from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from app.database import ObjectIdField

class KnowledgeBaseDocument(BaseModel):
    id: ObjectIdField = Field(validation_alias="_id", default=None)
    document_type: str  # pdf/doc/text
    document_title: str  # filename/text title
    document_content: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    vector_store_id: Optional[str] = None 
    object_store_id: Optional[ObjectIdField] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)