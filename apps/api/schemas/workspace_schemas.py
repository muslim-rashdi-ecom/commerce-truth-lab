from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=5, description="Merchant email address")
    password: str = Field(..., min_length=8, description="Password minimum 8 characters")
    full_name: Optional[str] = ""

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=5)
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.strip().lower()


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class CreateWorkspaceRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    currency: str = Field("USD", min_length=3, max_length=3)

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    owner_id: Optional[str] = None
    currency: str
    is_synthetic: bool
    created_at: str
    order_count: int = 0
    finding_count: int = 0
    data_completeness_pct: float = 0.0
    latest_audit_status: Optional[str] = "not_run"

class StageUploadResponse(BaseModel):
    upload_id: str
    file_name: str
    source_type: str
    detected_headers: List[str]
    suggested_mappings: Dict[str, str]
    preview_rows: List[Dict[str, Any]]
    row_count: int
    warnings: List[str]
    errors: List[str]
    pseudonymized_fields: List[str]

class CommitUploadRequest(BaseModel):
    upload_id: str
    mappings: Dict[str, str]

class CommitUploadResponse(BaseModel):
    success: bool
    source_type: str
    imported_rows: int
    message: str

class RunAuditResponse(BaseModel):
    audit_id: str
    status: str
    evaluated_orders: int
    total_findings: int
    healthy_controls_count: int
    completed_at: str

AuditRunResponse = RunAuditResponse


class AuditLogResponse(BaseModel):
    id: str
    action: str
    details: Any
    timestamp: str
