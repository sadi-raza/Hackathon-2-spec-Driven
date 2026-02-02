from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('title', 'description', mode='before')
    @classmethod
    def trim_whitespace(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError('Cannot be empty or whitespace only')
        return v

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v):
        if not v:
            raise ValueError('Title cannot be empty')
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

    @field_validator('title', 'description', mode='before')
    @classmethod
    def trim_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class TaskToggle(BaseModel):
    completed: bool


class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    createdAt: str  # ISO 8601
    updatedAt: str  # ISO 8601
    userId: int

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    task: TaskSchema


class TaskListResponse(BaseModel):
    tasks: List[TaskSchema]
    total: int


class TaskDeleteResponse(BaseModel):
    message: str