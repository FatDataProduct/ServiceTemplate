from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

#https://docs.pydantic.dev/


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class Amodel(BaseModel):
    app_id: int
    hash_id: str
    phone_number: str = '+7999999999'
    session_name: Optional[str] = None

class Dialog(BaseModel):
    id: int
    name: str
    type: str

class ExportRequest(BaseModel):
    session_name: Optional[str]
    dialog_ids: List[int]
