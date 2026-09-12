# Frontend (React)

React application for the Real Estate Lead Bot.

## Structure (target)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   ├── chat/
│   │   ├── leads/
│   │   ├── dashboard/
│   │   └── followups/
│   ├── pages/
│   │   ├── customer/
│   │   ├── auth/
│   │   └── dashboard/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   ├── utils/
│   └── app/
├── package.json
└── README.md
```

## Responsibilities

- Customer chat interface
- Lead form (optional progressive collection)
- Sales dashboard
- Lead list, details, filtering, assignment
- Follow-up management UI

All business logic and data access go through the FastAPI backend. The frontend must never talk directly to the database or AI provider.

## Quick Start (once implemented)

```bash
cd frontend
npm install
npm run dev
```
