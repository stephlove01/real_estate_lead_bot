# Real Estate Lead Bot

An AI-powered real estate lead management and qualification system designed to help real estate companies automatically receive, understand, qualify, store, and manage potential customers.

**Example Client:** PrimeHomes Realty

---

## Project Status

- **Phase:** Implementation Preparation / Scaffolding
- **Documentation:** Complete (being consolidated into `docs/`)
- **Application Code:** Scaffolding complete

See [`docs/TASK.md`](docs/TASK.md) for the full task tracker.

---

## High-Level Architecture

```text
                    CUSTOMER
                       |
                       v
              +------------------+
              |  REACT FRONTEND  |
              | Chat / Dashboard |
              +--------+---------+
                       |
                       v
              +------------------+
              |     FASTAPI      |
              |  BACKEND / API   |
              +--------+---------+
                       |
                       v
              +------------------+
              |       n8n        |
              | Automation Engine|
              +--------+---------+
                       |
             +---------+---------+
             |         |         |
             v         v         v
           AI      DATABASE   NOTIFICATION
             |         |         |
             +---------+---------+
                       |
                       v
                 SALES TEAM
```

---

## Technology Stack

| Layer          | Technology              |
|----------------|-------------------------|
| Frontend       | React                   |
| Backend        | Python + FastAPI        |
| Database       | PostgreSQL              |
| Automation     | n8n                     |
| AI             | LLM (provider TBD)      |
| Reporting      | Google Sheets (secondary) |

---

## Repository Structure

```text
real_estate_lead_bot/
├── frontend/                 # React application
├── backend/                  # FastAPI application
├── n8n/                      # Workflow definitions
├── database/                 # Migrations, seeds, schema notes
├── tests/                    # Cross-cutting / E2E tests
├── docs/                     # Specification documents (consolidation in progress)
├── .env.example
├── .gitignore
├── docker-compose.yml        # Local Postgres + n8n
├── LICENSE
└── README.md
```

### Specification Documents

Core documents are being moved into `docs/`. Currently available there:

- [`docs/TASK.md`](docs/TASK.md) — Project task tracker
- [`docs/LEAD_QUALIFICATION_SPEC.md`](docs/LEAD_QUALIFICATION_SPEC.md) — Scoring & classification

The larger specification files (PRD, Architecture, Database, API, AI, UI-UX, Deployment, Development Setup, Testing) still live at the repository root and will be moved into `docs/` next to keep the root clean while preserving exact content.

---

## Quick Start (Local Development)

### 1. Clone & Environment

```bash
git clone https://github.com/stephlove01/real_estate_lead_bot.git
cd real_estate_lead_bot
cp .env.example .env
# Edit .env with your values
```

### 2. Start infrastructure

```bash
docker compose up -d
```

This starts:

- PostgreSQL on `localhost:5432`
- n8n on `localhost:5678`

### 3. Backend (once implemented)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend (once implemented)

```bash
cd frontend
npm install
npm run dev
```

---

## Development Principles

1. **Keep it simple** — do not introduce unnecessary technologies.
2. **Build incrementally** — one working slice at a time.
3. **Clear responsibilities** — React = UI, FastAPI = business logic + API, n8n = orchestration, SQL = system of record, AI = language understanding only.
4. **AI is not the source of truth** — always validate AI output before persisting.
5. **Test as you go**.

See `DEVELOPMENT_SETUP.md` and `docs/TASK.md` for the recommended implementation order.

---

## License

MIT — see [LICENSE](LICENSE).
