# Database

PostgreSQL is the system of record.

## Contents (planned)

- SQLAlchemy models (or migration sources)
- Alembic migrations
- Seed data scripts
- Schema documentation references

## Core Tables (from specification)

- `users`
- `roles`
- `leads`
- `conversations`
- `messages`
- `lead_scores`
- `lead_assignments`
- `follow_ups`
- `activities`
- `integration_syncs`

See `docs/Database & Data Model Specification.md` for the full schema design.

## Local Development

Use the `postgres` service from the root `docker-compose.yml`:

```bash
docker compose up -d postgres
```

Connection string example (matches docker-compose defaults):

```
postgresql://relb:relb_secret@localhost:5432/real_estate_leads
```
