from pydantic import BaseModel
from datetime import datetime

from typing import Optional


class IssueSchema(BaseModel):
    id: int
    created_at: datetime
    avtomat_number: int
    address: str
    issue: Optional[str] = None
    comment: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None


class IssuesSchema(BaseModel):
    issues: list[IssueSchema]
