import secrets
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User, Workspace, WorkspaceMember, AuditLog
from security import hash_password, verify_password, create_access_token, get_current_user
from schemas.workspace_schemas import RegisterRequest, LoginRequest, AuthResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    email_clean = req.email.strip().lower()
    existing = (await db.execute(select(User).where(User.email == email_clean))).scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="An account with this email address already exists."
        )
    
    user_id = f"usr_{secrets.token_hex(8)}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    new_user = User(
        id=user_id,
        email=email_clean,
        hashed_password=hash_password(req.password),
        full_name=req.full_name or email_clean.split('@')[0],
        created_at=now_iso
    )
    db.add(new_user)
    
    # Automatically provision initial private workspace for this merchant
    ws_id = f"ws_{secrets.token_hex(6)}"
    workspace = Workspace(
        id=ws_id,
        name="My Pilot Store",
        owner_id=user_id,
        currency="USD",
        is_synthetic=False,
        created_at=now_iso
    )
    db.add(workspace)
    
    member = WorkspaceMember(
        id=f"mem_{secrets.token_hex(6)}",
        workspace_id=ws_id,
        user_id=user_id,
        role="admin",
        joined_at=now_iso
    )
    db.add(member)
    
    # Audit trail
    log = AuditLog(
        id=f"log_{secrets.token_hex(8)}",
        workspace_id=ws_id,
        user_id=user_id,
        action="user_registered",
        details={"email": email_clean, "workspace_id": ws_id},
        timestamp=now_iso
    )
    db.add(log)
    
    await db.commit()
    await db.refresh(new_user)
    
    token = create_access_token({"sub": user_id, "email": email_clean})
    
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            created_at=new_user.created_at
        )
    )

@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    email_clean = req.email.strip().lower()
    user = (await db.execute(select(User).where(User.email == email_clean))).scalars().first()
    
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password. Please verify your credentials."
        )
    
    token = create_access_token({"sub": user.id, "email": user.email})
    
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at
        )
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(user: User = Depends(get_current_user)):
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at
    )
