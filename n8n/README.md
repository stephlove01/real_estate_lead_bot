# n8n Workflows

Automation and orchestration layer for the Real Estate Lead Bot.

## Structure

```text
n8n/
├── workflows/
│   ├── lead-process-message.json
│   ├── lead-qualify.json
│   ├── lead-notify-sales.json
│   ├── followup-reminder.json
│   └── error-handler.json
└── README.md
```

## Workflow Naming Convention

- `PRH-LEAD-PROCESS-MESSAGE`
- `PRH-LEAD-QUALIFY`
- `PRH-LEAD-NOTIFY-SALES`
- `PRH-FOLLOWUP-REMINDER`
- `PRH-ERROR-HANDLER`
- `PRH-SHEET-SYNC-LEAD` (optional)

## Responsibilities

- Workflow orchestration
- AI processing calls
- Notifications
- Google Sheets synchronization (secondary)
- Scheduled follow-up reminders
- Error handling and retries

n8n is **not** the system of record. All authoritative data lives in PostgreSQL via FastAPI.
