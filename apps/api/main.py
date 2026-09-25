from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import ENVIRONMENT, get_allowed_cors_origins
from routers import health, upload, demo, auth, workspace, merchant_upload, merchant_audit, benchmarks
from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # In development and test environments, auto-create tables
    # In production, schema is strictly managed by Alembic migrations
    if ENVIRONMENT != "production":
        with engine.begin() as conn:
            Base.metadata.create_all(conn)
    yield


app = FastAPI(
    title="Commerce Truth Lab API",
    description="Evidence-first e-commerce audit API. All demo data is synthetic.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(demo.router)
app.include_router(auth.router)
app.include_router(workspace.router)
app.include_router(merchant_upload.router)
app.include_router(merchant_audit.router)
app.include_router(benchmarks.router)
