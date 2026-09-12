# Backend (FastAPI)

Python + FastAPI backend for the Real Estate Lead Bot.

## Structure (target)

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── leads.py
│   │       ├── conversations.py
│   │       ├── messages.py
│   │       ├── followups.py
│   │       └── health.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   └── db/
├── tests/
├── requirements.txt
└── README.md
```

## Responsibilities

- API endpoints
- Request / response validation
- Authentication & authorization
- Business logic
- Database operations (via SQLAlchemy)
- Lead, conversation, message, and follow-up management

Automation workflows belong in `n8n/`, not here.

## Quick Start (once implemented)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
