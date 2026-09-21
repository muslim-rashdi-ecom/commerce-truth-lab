import os
from typing import List

# Insecure/Default blacklist that must never be accepted in production
INSECURE_SECRETS_BLACKLIST = {
    "ctl_production_secret_key_change_in_env_2026",
    "ctl_salt_987654321",
    "secret",
    "changeme",
    "password",
    "test",
    "default",
    "admin",
    "12345678",
}

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower().strip()
RAW_DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
RAW_JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "").strip()
RAW_PSEUDONYMIZATION_SALT = os.getenv("PSEUDONYMIZATION_SALT", "").strip()
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "https://commerce-truth-lab.vercel.app").strip()


def validate_production_config():
    """
    Strict validation for production mode.
    Fails fast with RuntimeError on application startup if any required secret or database is insecure/missing.
    """
    if ENVIRONMENT == "production":
        # 1. Database validation: Must be PostgreSQL, never SQLite
        if not RAW_DATABASE_URL:
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: DATABASE_URL must be set in production."
            )
        if "sqlite" in RAW_DATABASE_URL.lower():
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: SQLite is strictly forbidden in production. Use PostgreSQL (psycopg)."
            )
        if not (
            RAW_DATABASE_URL.startswith("postgresql://")
            or RAW_DATABASE_URL.startswith("postgres://")
            or RAW_DATABASE_URL.startswith("postgresql+psycopg://")
            or RAW_DATABASE_URL.startswith("postgresql+asyncpg://")
        ):
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: Production DATABASE_URL must be a valid PostgreSQL connection string."
            )

        # 2. JWT secret validation
        if not RAW_JWT_SECRET_KEY:
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: JWT_SECRET_KEY must be set in production."
            )
        if len(RAW_JWT_SECRET_KEY) < 32:
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: Production JWT_SECRET_KEY must be at least 32 characters long."
            )
        if RAW_JWT_SECRET_KEY.lower() in INSECURE_SECRETS_BLACKLIST:
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: Default or weak JWT_SECRET_KEY is forbidden in production."
            )

        # 3. Salt validation
        if not RAW_PSEUDONYMIZATION_SALT:
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: PSEUDONYMIZATION_SALT must be set in production."
            )
        if len(RAW_PSEUDONYMIZATION_SALT) < 16:
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: Production PSEUDONYMIZATION_SALT must be at least 16 characters long."
            )
        if RAW_PSEUDONYMIZATION_SALT.lower() in INSECURE_SECRETS_BLACKLIST:
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: Default or weak PSEUDONYMIZATION_SALT is forbidden in production."
            )

        # 4. Frontend origin
        if not FRONTEND_ORIGIN or FRONTEND_ORIGIN == "*":
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: Wildcard or empty FRONTEND_ORIGIN is forbidden in production."
            )


# Execute validation on import if in production
validate_production_config()


def get_jwt_secret_key() -> str:
    if ENVIRONMENT == "production":
        return RAW_JWT_SECRET_KEY
    return RAW_JWT_SECRET_KEY or "dev_jwt_secret_key_non_production_only_1234567890"


def get_pseudonymization_salt() -> str:
    if ENVIRONMENT == "production":
        return RAW_PSEUDONYMIZATION_SALT
    return RAW_PSEUDONYMIZATION_SALT or "dev_salt_non_prod_1234567890"


def get_allowed_cors_origins() -> List[str]:
    if ENVIRONMENT == "production":
        # Strictly the deployed frontend origin in production
        return [FRONTEND_ORIGIN]
    
    # Local dev origins
    origins = [
        FRONTEND_ORIGIN,
        "http://localhost:5173",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
    ]
    # Deduplicate while preserving order
    return list(dict.fromkeys(origins))
