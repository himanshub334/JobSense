# JobSense

Full-stack job discovery demo: React/Vite UI, FastAPI API, PostgreSQL + pgvector, Redis, Celery, hybrid lexical/vector ranking, daily ingestion, run history, evaluation metrics.

## Start
`cp .env.example .env` then `docker compose up --build`
UI: http://localhost:5173 | API docs: http://localhost:8000/docs

Demo postings are seeded on startup. Celery Beat refreshes the corpus daily at 05:00 UTC; use **Run ingestion** for a manual refresh. Replace `backend/app/source.py` with a public/licensed feed adapter before production. Respect source terms and rate limits.

## Design notes
Stable source IDs and SHA-256 hashes skip unchanged postings. Changed postings are schema-validated, embedded in batches and upserted; disappeared postings are deactivated. Search combines PostgreSQL full-text rank and pgvector cosine similarity using reciprocal-rank fusion, then applies hard metadata filters. Runs record counts, low-volume warnings and estimated cost. The no-key demo uses deterministic feature-hash vectors and rule-based extraction; configure OpenAI-compatible credentials for model-based extraction/embeddings. The local fallback is not a production semantic embedding model.

Production checklist: auth, Alembic migrations, provider-specific ingestion adapters, monitoring, secrets management, backups, retention policy, and versioned embedding migrations.
