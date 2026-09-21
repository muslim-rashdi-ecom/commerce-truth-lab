from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import health, upload, demo, auth, workspace, merchant_upload, merchant_audit
from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Commerce Truth Lab API",
    description="Evidence-first e-commerce audit API. All demo data is synthetic.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

