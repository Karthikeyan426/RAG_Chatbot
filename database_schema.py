from sqlmodel import SQLModel, Field, Column
from datetime import datetime, timezone
from pgvector.sqlalchemy import VECTOR
from uuid import UUID, uuid4

class users(SQLModel, table = True):
    id: str = Field(primary_key = True, default = None)
    password: str = Field(nullable = False)

class docs(SQLModel, table = True):
    id: UUID = Field(primary_key = True, default_factory = uuid4)
    doc_name: str = Field(unique = True, nullable = False)
    uploaded_at: datetime = Field(default_factory = datetime.now(timezone.utc))
    user_id: str = Field(foreign_key = "users.id")

class chunks(SQLModel, table = True):
    id: UUID = Field(primary_key = True, default_factory = uuid4)
    doc_id: UUID = Field(foreign_key = "docs.id")
    content: str = Field(nullable = False)
    embedding: list[float] = Field(sa_column = Column(VECTOR(384)), nullable = False)

class chats(SQLModel, table = True):
    id: UUID = Field(primary_key = True, default_factory = uuid4)
    user_id: str = Field(foreign_key = "users.id")
    doc_id: UUID = Field(foreign_key = "docs.id")
    question_content: str = Field(nullable = False)
    question_embedding: list[float] = Field(nullable = True, sa_column = Column(VECTOR(384)))
    response_content: str = Field(nullable = False)
