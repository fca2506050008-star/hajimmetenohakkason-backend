from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
	password: str
	email: str

class TodoUpdate(BaseModel):
	title: Optional[str] = None
	content: Optional[str] = None
