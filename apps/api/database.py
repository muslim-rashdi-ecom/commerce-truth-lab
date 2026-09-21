import os
import ssl
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import ENVIRONMENT, RAW_DATABASE_URL


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_SQLITE_PATH = os.path.join(DATA_DIR, "demo.db")
DB_PATH = DEFAULT_SQLITE_PATH

# Vercel production uses PostgreSQL and its deployed filesystem is read-only.
# Only create the local SQLite directory for development/test environments.
if not RAW_DATABASE_URL or RAW_DATABASE_URL.startswith("sqlite"):
    if ENVIRONMENT != "production":
        os.makedirs(DATA_DIR, exist_ok=True)


def _normalize_database_url(raw_db_url: str) -> str:
    """Normalize PostgreSQL URLs to Vercel-compatible pure-Python pg8000."""
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql+pg8000://", 1)
    elif raw_db_url.startswith("postgresql://"):
        raw_db_url = raw_db_url.replace("postgresql://", "postgresql+pg8000://", 1)
    elif raw_db_url.startswith("postgresql+asyncpg://"):
        raw_db_url = raw_db_url.replace("postgresql+asyncpg://", "postgresql+pg8000://", 1)
    elif raw_db_url.startswith("postgresql+psycopg://"):
        raw_db_url = raw_db_url.replace("postgresql+psycopg://", "postgresql+pg8000://", 1)

    if raw_db_url.startswith("postgresql+pg8000://"):
        parsed = urlsplit(raw_db_url)
        query = [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True)
                 if key not in {"sslmode", "channel_binding"}]
        return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))
    return raw_db_url


if RAW_DATABASE_URL:
    if RAW_DATABASE_URL.startswith("sqlite") and ENVIRONMENT == "production":
        raise RuntimeError("SQLite is strictly forbidden in production. Use PostgreSQL (pg8000).")
    DATABASE_URL = _normalize_database_url(RAW_DATABASE_URL)
else:
    if ENVIRONMENT == "production":
        raise RuntimeError("DATABASE_URL must be configured with PostgreSQL in production.")
    DATABASE_URL = f"sqlite:///{DEFAULT_SQLITE_PATH}"


engine_kwargs = {"echo": False}
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
elif DATABASE_URL.startswith("postgresql+pg8000"):
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 5
    engine_kwargs["max_overflow"] = 5
    connect_args["ssl_context"] = ssl.create_default_context()
if connect_args:
    engine_kwargs["connect_args"] = connect_args

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=Session)
Base = declarative_base()


class AsyncSessionCompat:
    """Async-shaped adapter over a sync SQLAlchemy session."""

    def __init__(self, session: Session):
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self._session.close()

    async def execute(self, *args, **kwargs):
        return self._session.execute(*args, **kwargs)

    async def scalar(self, *args, **kwargs):
        return self._session.scalar(*args, **kwargs)

    async def commit(self):
        self._session.commit()

    async def rollback(self):
        self._session.rollback()

    async def refresh(self, instance, *args, **kwargs):
        self._session.refresh(instance, *args, **kwargs)

    async def delete(self, instance):
        self._session.delete(instance)

    def add(self, instance):
        self._session.add(instance)

    def add_all(self, instances):
        self._session.add_all(instances)


class AsyncSessionFactory:
    def __call__(self):
        return AsyncSessionCompat(SessionLocal())


AsyncSessionLocal = AsyncSessionFactory()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
