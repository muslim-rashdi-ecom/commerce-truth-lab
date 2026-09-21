import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DEFAULT_SQLITE_PATH = os.path.join(DATA_DIR, "demo.db")
DB_PATH = DEFAULT_SQLITE_PATH


raw_db_url = os.getenv("DATABASE_URL", "").strip()

if raw_db_url:
    # Normalize postgres connection strings for asyncpg
    if raw_db_url.startswith("postgres://"):
        DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif raw_db_url.startswith("postgresql://") and not raw_db_url.startswith("postgresql+"):
        DATABASE_URL = raw_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif raw_db_url.startswith("sqlite://") and not raw_db_url.startswith("sqlite+"):
        DATABASE_URL = raw_db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    else:
        DATABASE_URL = raw_db_url
else:
    DATABASE_URL = f"sqlite+aiosqlite:///{DEFAULT_SQLITE_PATH}"

# Configure engine kwargs depending on dialect
engine_kwargs = {"echo": False}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_async_engine(DATABASE_URL, **engine_kwargs)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
