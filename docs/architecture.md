# Architecture

## Monorepo
```text
commerce-truth-lab-v1/
  apps/
    api/
    web/
  packages/
    engine/
    shared/
  data/
  tests/
```

## Data Flow
Upload -> Parsing -> DB -> Engine Evaluation -> Results

## Database
SQLite for demo. SQLAlchemy ORM mappings.

## Tech
- FastAPI, Pydantic v2
- Next.js (frontend)
