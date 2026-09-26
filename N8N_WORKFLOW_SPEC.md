# N8N Workflow Specification

## Project: PrimeHomes Realty Lead Bot

**Document:** `N8N_WORKFLOW_SPEC.md`  
**Version:** 1.0  
**Status:** Ready for Implementation  
**System:** PrimeHomes Realty Lead Bot  
**Primary Automation Platform:** n8n  
**Backend:** FastAPI  
**Database:** PostgreSQL  
**Frontend:** React  
**AI:** LLM-based extraction and response generation  
**Secondary Reporting:** Google Sheets

---

# 1. Purpose

This document defines the n8n workflows responsible for automating lead processing, qualification, sales notifications, follow-ups, Google Sheets synchronization, and error handling for the PrimeHomes Realty Lead Bot.

n8n acts as the **workflow orchestration layer**.

It connects:

```text
Customer
   ↓
React Frontend
   ↓
FastAPI
   ↓
n8n
   ↓
AI
   ↓
FastAPI / PostgreSQL
   ↓
Lead Qualification
   ↓
Sales Team
   ↓
Follow-up
```

n8n should coordinate business processes but should not become the primary database or business-logic engine.

---

# 2. Architecture

```text
                         CUSTOMER
                            │
                            ▼
                     React Frontend
                            │
                            ▼
                         FastAPI
                            │
                            ▼
                       n8n Webhook
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
          AI Processing          Existing Lead Data
                │                       │
                └───────────┬───────────┘
                            ▼
                    Merge Lead Data
                            │
                            ▼
                    Validate Information
                            │
                            ▼
                    Lead Qualification
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
              HOT/WARM              COLD
                 │                     │
                 ▼                     │
           Notify Sales               │
                 │                     │
                 └──────────┬──────────┘
                            ▼
                  Generate Response
                            │
                            ▼
                      Save Message
                            │
                            ▼
                     Return Response
```

---

# 3. n8n Responsibilities

n8n is responsible for:

- Receiving automation requests from FastAPI.
- Orchestrating AI processing.
- Calling FastAPI endpoints.
- Checking lead context.
- Validating workflow data.
- Determining which workflow branch should execute.
- Triggering lead qualification.
- Triggering sales notifications.
- Scheduling follow-ups.
- Synchronizing selected lead data to Google Sheets.
- Handling workflow failures.
- Recording workflow activity.

n8n is **not** responsible for:

- Being the primary database.
- Storing the complete application state.
- Directly modifying PostgreSQL tables unless explicitly required.
- Implementing authentication for customers.
- Implementing application authorization.
- Making unsupported property availability claims.
- Inventing property information.
- Making irreversible business decisions that belong in FastAPI.
- Replacing the backend API.

---

# 4. Workflow Naming Convention

All workflows should use the following naming convention:

```text
PRH-[FUNCTION]
```

Where `PRH` means PrimeHomes Realty.

Current workflows:

| Workflow ID | Workflow Name | Purpose |
|---|---|---|
| `PRH-LEAD-PROCESS-MESSAGE` | Process Customer Message | Main lead-processing workflow |
| `PRH-LEAD-QUALIFY` | Qualify Lead | Calculate lead score |
| `PRH-LEAD-NOTIFY-SALES` | Notify Sales Team | Alert sales about important leads |
| `PRH-FOLLOWUP-REMINDER` | Follow-up Reminder | Handle scheduled follow-ups |
| `PRH-SHEET-SYNC-LEAD` | Sync Lead to Google Sheets | Reporting/operational synchronization |
| `PRH-ERROR-HANDLER` | Workflow Error Handler | Central workflow error handling |

---

# 5. General Workflow Principles

Every workflow should follow these principles:

1. Validate incoming data.
2. Use stable IDs.
3. Avoid duplicate processing.
4. Keep PostgreSQL as the source of truth.
5. Use FastAPI for application-level data operations.
6. Validate AI output before saving it.
7. Do not trust external input blindly.
8. Record important workflow activities.
9. Handle failures without losing customer messages.
10. Make workflows easy to debug.
11. Keep node names descriptive.
12. Avoid unnecessary workflow complexity.

---

# 6. Workflow 1: PRH-LEAD-PROCESS-MESSAGE

## 6.1 Purpose

This is the primary workflow.

It processes an incoming customer message, extracts useful lead information, updates the lead, determines whether additional information is required, qualifies the lead when possible, generates an appropriate response, and returns the response to FastAPI.

---

## 6.2 Trigger

### Trigger Type

n8n Webhook.

Example:

```text
POST /webhook/lead/process-message
```

FastAPI sends a request to this webhook.

---

# 7. Input Schema

Example input:

```json
{
  "event_id": "evt_123456",
  "lead_id": "lead_123",
  "conversation_id": "conv_123",
  "message_id": "msg_123",
  "customer_message": "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million.",
  "channel": "web",
  "timestamp": "2026-09-12T10:30:00Z"
}
```

---

# 8. Input Fields

| Field | Required | Description |
|---|---:|---|
| `event_id` | Yes | Unique event identifier |
| `lead_id` | Yes | Lead identifier |
| `conversation_id` | Yes | Conversation identifier |
| `message_id` | Yes | Customer message identifier |
| `customer_message` | Yes | Raw customer message |
| `channel` | Yes | Source channel |
| `timestamp` | Yes | Event timestamp |

Possible channels:

```text
web
whatsapp
instagram
facebook
manual
api
```

---

# 9. Main Workflow

```text
Webhook
   ↓
Validate Input
   ↓
Check Idempotency
   ↓
Get Lead Context
   ↓
Get Conversation History
   ↓
Prepare AI Input
   ↓
AI Extraction
   ↓
Validate AI Output
   ↓
Merge Lead Information
   ↓
Update Lead
   ↓
Check Missing Information
   ↓
Information Missing?
   │
   ├── YES
   │     ↓
   │  Generate Clarification
   │     ↓
   │  Save Response
   │     ↓
   │  Return Response
   │
   └── NO
         ↓
      Qualify Lead
         ↓
      HOT?
       │
       ├── YES → Notify Sales
       │
       └── NO
             ↓
       Generate Response
             ↓
       Save Response
             ↓
       Return Response
```

---

# 10. Node Specification

## Node 1 — Webhook

**Name:**

```text
01 - Receive Lead Message
```

**Type:**

Webhook

**Method:**

```text
POST
```

**Purpose:**

Receive a new customer message from FastAPI.

---

## Node 2 — Validate Input

**Name:**

```text
02 - Validate Input
```

**Type:**

Code / validation node

Validate:

```text
event_id
lead_id
conversation_id
message_id
customer_message
channel
timestamp
```

If required information is missing:

```text
Stop workflow
→ Return validation error
```

---

# 11. Node 3 — Check Idempotency

**Name:**

```text
03 - Check Idempotency
```

Purpose:

Prevent the same customer message from being processed multiple times.

Check whether:

```text
event_id
```

or:

```text
message_id
```

has already been processed.

FastAPI endpoint:

```http
GET /api/v1/events/{event_id}
```

Possible result:

```json
{
  "processed": true
}
```

If already processed:

```text
Stop workflow
→ Return existing result
```

If not processed:

```text
Continue
```

---

# 12. Node 4 — Get Lead Context

**Name:**

```text
04 - Get Lead Context
```

FastAPI:

```http
GET /api/v1/leads/{lead_id}
```

Retrieve:

```text
customer_name
email
phone
intent
transaction_type
property_type
bedrooms
location
budget
timeline
lead_status
lead_score
lead_classification
```

---

# 13. Node 5 — Get Conversation History

**Name:**

```text
05 - Get Conversation History
```

FastAPI:

```http
GET /api/v1/conversations/{conversation_id}/messages
```

Retrieve the recent conversation.

The workflow should not send an unnecessarily large conversation history to the AI.

Recommended:

```text
Last 10–20 relevant messages
```

---

# 14. Node 6 — Prepare AI Input

**Name:**

```text
06 - Prepare AI Input
```

Create a structured AI request.

Example:

```json
{
  "customer_message": "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million.",
  "existing_lead": {
    "name": null,
    "email": null,
    "phone": null,
    "intent": null,
    "property_type": null,
    "bedrooms": null,
    "location": null,
    "budget_max": null,
    "timeline": null
  },
  "conversation_history": []
}
```

---

# 15. Node 7 — AI Extraction

**Name:**

```text
07 - AI Extract Lead Information
```

**Purpose:**

Understand the customer's message and extract structured information.

AI should identify:

- Intent
- Transaction type
- Property type
- Bedrooms
- Location
- Budget
- Currency
- Timeline
- Customer name
- Email
- Phone
- Missing information
- Confidence

---

# 16. Expected AI Output

The AI must return structured JSON.

Example:

```json
{
  "intent": "BUY",
  "transaction_type": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": null,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": null,
  "customer_name": null,
  "email": null,
  "phone": null,
  "missing_fields": [
    "timeline",
    "phone"
  ],
  "confidence": 0.96
}
```

---

# 17. Node 8 — Validate AI Output

**Name:**

```text
08 - Validate AI Output
```

The workflow must validate:

- JSON structure
- Allowed enum values
- Numeric fields
- Confidence range
- Required keys
- No unexpected dangerous instructions
- No fabricated property information

Example validation:

```text
confidence >= 0
confidence <= 1
```

Budget must be numeric.

Bedrooms must be numeric when provided.

---

# 18. AI Validation Failure

If AI output is invalid:

```text
AI Output
   ↓
Validation Failed
   ↓
Retry AI once
   ↓
Validate Again
```

If it still fails:

```text
Record Error
   ↓
Do Not Modify Lead
   ↓
Return Safe Fallback Response
```

Example fallback:

```text
Thanks for your message. We'd like to help you find the right property. Could you please provide a few more details about what you're looking for?
```

---

# 19. Node 9 — Merge Lead Information

**Name:**

```text
09 - Merge Lead Data
```

Existing lead data should not be unnecessarily overwritten.

Example:

```text
Existing location:
Lekki

New AI location:
Lekki Phase 1
```

The application should determine whether the new value should replace the old value.

General rule:

```text
New confirmed information
        ↓
Update existing information
```

Do not replace known information with:

```text
null
unknown
uncertain
```

---

# 20. Node 10 — Update Lead

**Name:**

```text
10 - Update Lead
```

FastAPI:

```http
PATCH /api/v1/leads/{lead_id}
```

Example:

```json
{
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN"
}
```

FastAPI remains responsible for database persistence.

---

# 21. Node 11 — Check Missing Information

**Name:**

```text
11 - Check Missing Information
```

Required information depends on the lead intent.

For a buying lead, useful fields include:

```text
name
phone
property_type
location
budget
timeline
```

Not every field must always be available before responding.

---

# 22. Required Information Rules

### Buying

Recommended:

```text
property_type
location
budget
timeline
contact information
```

### Renting

Recommended:

```text
property_type
location
budget
timeline
contact information
```

### Land

Recommended:

```text
location
budget
purpose
timeline
contact information
```

### Selling

Recommended:

```text
property_type
location
estimated value
contact information
```

---

# 23. Node 12 — Information Missing?

**Name:**

```text
12 - Information Missing?
```

Type:

```text
IF
```

Branches:

```text
YES
NO
```

---

# 24. Missing Information Branch

If important information is missing:

```text
Check Missing Information
        ↓
Generate Clarification
        ↓
Save Assistant Message
        ↓
Return Response
```

Example customer response:

```text
Thanks! A 3-bedroom apartment around Lekki with a budget of ₦80 million sounds good.

To help us narrow down suitable options, when are you hoping to move or complete the purchase?
```

The question should request only the most useful missing information instead of overwhelming the customer.

---

# 25. Node 13 — Generate Clarification

**Name:**

```text
13 - Generate Clarification
```

The AI should generate a short, natural customer response.

Requirements:

- Friendly
- Professional
- Concise
- Helpful
- No fabricated listings
- No fabricated prices
- No false promises

---

# 26. Node 14 — Save Assistant Response

**Name:**

```text
14 - Save Assistant Response
```

FastAPI:

```http
POST /api/v1/messages
```

Example:

```json
{
  "conversation_id": "conv_123",
  "sender_type": "ASSISTANT",
  "message": "When are you hoping to complete the purchase?",
  "message_type": "TEXT"
}
```

---

# 27. Node 15 — Return Response

**Name:**

```text
15 - Return Response
```

Return:

```json
{
  "success": true,
  "lead_id": "lead_123",
  "response": "When are you hoping to complete the purchase?",
  "lead_status": "IN_PROGRESS"
}
```

---

# 28. Complete Lead Branch

When sufficient information exists:

```text
Information Complete
        ↓
Calculate Lead Score
        ↓
Classify Lead
        ↓
HOT?
        ↓
Notify Sales if required
        ↓
Generate Customer Response
        ↓
Save Response
        ↓
Return Response
```

---

# 29. Workflow 2: PRH-LEAD-QUALIFY

## Purpose

Calculate the lead score and classification.

---

## Trigger

This workflow may be triggered:

```text
PRH-LEAD-PROCESS-MESSAGE
```

or manually through FastAPI.

---

# 30. Qualification Flow

```text
Receive Lead
    ↓
Validate Lead
    ↓
Calculate Score
    ↓
Determine Classification
    ↓
Save Score History
    ↓
Update Lead
    ↓
Return Result
```

---

# 31. Lead Scoring

Current scoring model:

| Category | Points |
|---|---:|
| Intent | 20 |
| Property Requirement | 15 |
| Location | 15 |
| Budget | 20 |
| Timeline | 20 |
| Contact Information | 10 |
| **Total** | **100** |

---

# 32. Qualification Rules

Example:

### Intent

```text
Clear buying/renting/selling intent = 20
Unclear intent = 0–10
```

### Property Requirement

```text
Property type + relevant details = 15
Partial information = 5–10
Missing = 0
```

### Location

```text
Specific location = 15
General area = 5–10
Missing = 0
```

### Budget

```text
Clear budget = 20
Approximate budget = 10–15
Missing = 0
```

### Timeline

```text
Immediate = 20
Within 1 month = 20
Within 3 months = 15
Researching = 5
Unknown = 0
```

### Contact

```text
Phone + email = 10
One contact method = 5
None = 0
```

---

# 33. Lead Classification

```text
80–100 → HOT
60–79  → WARM
30–59  → COLD
0–29   → UNQUALIFIED
```

Example:

```json
{
  "lead_id": "lead_123",
  "score": 85,
  "classification": "HOT"
}
```

---

# 34. Save Score History

FastAPI:

```http
POST /api/v1/leads/{lead_id}/qualify
```

The system should retain qualification history.

Example:

```json
{
  "score": 85,
  "classification": "HOT",
  "reason": "Clear buying intent, specific property requirement, budget and timeline provided."
}
```

---

# 35. Workflow 3: PRH-LEAD-NOTIFY-SALES

## Purpose

Notify the sales team when a lead becomes important enough to require human attention.

---

# 36. Trigger

The workflow is triggered when:

```text
lead_classification == HOT
```

---

# 37. Flow

```text
Receive HOT Lead
       ↓
Get Lead Details
       ↓
Generate Sales Summary
       ↓
Send Notification
       ↓
Record Notification Activity
```

---

# 38. Node Specification

### Node 1

```text
01 - Receive HOT Lead
```

Input:

```json
{
  "lead_id": "lead_123"
}
```

### Node 2

```text
02 - Get Lead Details
```

FastAPI:

```http
GET /api/v1/leads/{lead_id}
```

### Node 3

```text
03 - Generate Sales Summary
```

Example:

```text
🔥 HOT LEAD

Name: John
Intent: Buying
Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80M
Timeline: Within 1 month

Recommended action:
Contact customer as soon as possible.
```

### Node 4

```text
04 - Send Sales Notification
```

The initial MVP may support one notification channel.

Possible options:

```text
Email
Slack
WhatsApp
Telegram
```

The exact integration should be selected during implementation based on the client's available tools.

### Node 5

```text
05 - Record Notification
```

FastAPI:

```http
POST /api/v1/activities
```

Record:

```text
lead_id
activity_type
notification_channel
timestamp
status
```

---

# 39. Workflow 4: PRH-FOLLOWUP-REMINDER

## Purpose

Automatically remind the sales team about leads requiring follow-up.

---

# 40. Trigger

Use:

```text
Schedule Trigger
```

Example:

```text
Every 15 minutes
```

For the MVP, this is sufficient.

---

# 41. Flow

```text
Schedule Trigger
       ↓
Find Due Follow-ups
       ↓
Loop Through Follow-ups
       ↓
Get Lead
       ↓
Generate Reminder
       ↓
Notify Sales
       ↓
Mark Follow-up Processed
       ↓
Record Activity
```

---

# 42. Find Due Follow-ups

FastAPI:

```http
GET /api/v1/follow-ups?status=DUE
```

The backend determines which follow-ups are due.

n8n should not directly query application tables unless there is a specific technical reason.

---

# 43. Follow-up Reminder

Example:

```text
Follow-up Reminder

Lead: John
Lead Type: HOT
Requirement: 3-bedroom apartment in Lekki
Budget: ₦80M

Follow-up was due today.

Please contact the customer.
```

---

# 44. Workflow 5: PRH-SHEET-SYNC-LEAD

## Purpose

Synchronize selected lead information to Google Sheets for reporting and simple operational visibility.

Google Sheets is **not the source of truth**.

PostgreSQL remains the source of truth.

---

# 45. Trigger

This workflow may be triggered after:

```text
Lead Created
```

or:

```text
Lead Updated
```

---

# 46. Flow

```text
Receive Lead Event
       ↓
Get Lead Data
       ↓
Find Existing Sheet Row
       ↓
Row Exists?
    │
    ├── YES → Update Row
    │
    └── NO  → Create Row
       ↓
Record Sync Status
```

---

# 47. Google Sheet Columns

Recommended initial columns:

| Column |
|---|
| Lead ID |
| Date Created |
| Name |
| Phone |
| Email |
| Intent |
| Transaction Type |
| Property Type |
| Bedrooms |
| Location |
| Budget |
| Currency |
| Timeline |
| Lead Score |
| Classification |
| Lead Status |
| Assigned Salesperson |
| Last Contact |
| Next Follow-up |
| Updated At |

---

# 48. Duplicate Prevention

Never create a new Google Sheets row simply because a workflow runs again.

Use:

```text
Lead ID
```

as the unique identifier.

Workflow:

```text
Lead ID
   ↓
Search Sheet
   ↓
Found?
 ├── YES → Update
 └── NO  → Create
```

---

# 49. Workflow 6: PRH-ERROR-HANDLER

## Purpose

Handle workflow failures without silently losing customer information.

---

# 50. Error Flow

```text
Workflow Error
      ↓
Capture Error
      ↓
Identify Workflow
      ↓
Identify Lead/Event
      ↓
Record Error
      ↓
Retry if Safe
      ↓
Notify Admin if Required
```

---

# 51. Error Categories

### Validation Error

Example:

```text
Missing lead_id
```

Action:

```text
Do not retry automatically.
Record error.
Return clear error.
```

### Temporary API Error

Example:

```text
FastAPI unavailable
```

Action:

```text
Retry.
```

### AI Failure

Example:

```text
AI timeout
```

Action:

```text
Retry once.
```

### Google Sheets Failure

Action:

```text
Do not block the main lead workflow.
Record sync failure.
Retry later.
```

---

# 52. Retry Strategy

Keep retry logic simple.

Recommended:

```text
Attempt 1
   ↓
Failure
   ↓
Wait
   ↓
Attempt 2
   ↓
Failure
   ↓
Record failure
```

Do not create complex retry chains for the MVP.

---

# 53. Idempotency

Idempotency is required for important workflows.

Primary identifiers:

```text
event_id
message_id
lead_id
```

Example:

```text
event_id = evt_123
```

If n8n receives the same event twice:

```text
First request:
Process

Second request:
Detect already processed
→ Do not duplicate message
→ Do not duplicate lead update
→ Do not duplicate notification
```

---

# 54. FastAPI ↔ n8n Contract

FastAPI should call n8n using a defined webhook contract.

Example:

```http
POST /webhook/lead/process-message
Content-Type: application/json
```

Body:

```json
{
  "event_id": "evt_123",
  "lead_id": "lead_123",
  "conversation_id": "conv_123",
  "message_id": "msg_123",
  "customer_message": "I need a 2 bedroom apartment in Ikeja.",
  "channel": "web",
  "timestamp": "2026-09-12T10:30:00Z"
}
```

---

# 55. n8n Response Contract

Successful processing:

```json
{
  "success": true,
  "lead_id": "lead_123",
  "response": "What budget range are you considering?",
  "lead_score": 45,
  "classification": "COLD",
  "status": "IN_PROGRESS"
}
```

---

# 56. Error Response

Example:

```json
{
  "success": false,
  "error": {
    "code": "WORKFLOW_PROCESSING_ERROR",
    "message": "Unable to process the customer message."
  }
}
```

Do not expose internal stack traces to the customer.

---

# 57. AI Integration Rules

n8n may call the configured AI provider.

AI should receive:

```text
Current customer message
Relevant conversation history
Existing lead information
Allowed fields
Instructions
```

AI should return:

```text
Structured JSON
```

The AI should not return arbitrary application commands.

---

# 58. AI Safety Rules

The AI must not:

- Invent available properties.
- Invent prices.
- Invent discounts.
- Confirm property availability without backend verification.
- Promise appointments without confirmation.
- Modify database records directly.
- Assign sales staff.
- Delete leads.
- Change lead ownership.
- Expose internal system information.

---

# 59. Property Availability

If a customer asks:

```text
Do you have a 3-bedroom apartment in Lekki?
```

The AI should not automatically say:

```text
Yes, we have one available.
```

unless availability has been verified.

Safe response:

```text
I'd be happy to help you find a suitable 3-bedroom apartment in Lekki. Let me confirm the available options for you.
```

---

# 60. Credentials

n8n credentials should be configured using n8n's credential system.

Possible credentials:

```text
FastAPI API credential
AI provider credential
Google Sheets credential
Notification provider credential
```

Credentials must not be hardcoded into workflow nodes.

---

# 61. Environment Variables

Recommended environment variables:

```env
N8N_HOST=
N8N_PORT=
N8N_PROTOCOL=

FASTAPI_BASE_URL=
FASTAPI_API_KEY=

AI_API_KEY=

GOOGLE_SHEETS_ID=

SALES_NOTIFICATION_EMAIL=

WEBHOOK_SECRET=
```

Actual secrets must be stored outside Git.

---

# 62. Webhook Authentication

The FastAPI → n8n webhook should use a simple shared secret or API credential.

Example:

```text
Authorization: Bearer <WEBHOOK_SECRET>
```

n8n validates the credential before processing the request.

---

# 63. Logging

Important workflow events should be logged.

Example:

```text
Workflow started
Workflow completed
AI extraction completed
Lead updated
Lead qualified
Sales notification sent
Google Sheets sync completed
Workflow failed
```

Avoid logging sensitive customer information unnecessarily.

---

# 64. Node Naming Convention

Use numbered nodes.

Example:

```text
01 - Receive Lead Message
02 - Validate Input
03 - Check Idempotency
04 - Get Lead Context
05 - Get Conversation History
06 - Prepare AI Input
07 - AI Extract Lead Information
08 - Validate AI Output
09 - Merge Lead Data
10 - Update Lead
11 - Check Missing Information
12 - Information Missing?
13 - Generate Clarification
14 - Save Assistant Response
15 - Qualify Lead
16 - HOT Lead?
17 - Notify Sales
18 - Generate Customer Response
19 - Save Response
20 - Return Response
```

This makes debugging easier.

---

# 65. Workflow Data Format

Use consistent JSON throughout the workflow.

Example internal structure:

```json
{
  "event": {
    "id": "evt_123",
    "type": "CUSTOMER_MESSAGE"
  },
  "lead": {
    "id": "lead_123",
    "name": null,
    "phone": null,
    "email": null
  },
  "conversation": {
    "id": "conv_123"
  },
  "message": {
    "id": "msg_123",
    "text": "I need a 3 bedroom apartment in Lekki."
  },
  "ai": {
    "intent": "BUY",
    "property_type": "APARTMENT",
    "bedrooms": 3,
    "location": "Lekki",
    "budget_max": null,
    "timeline": null,
    "confidence": 0.94
  },
  "qualification": {
    "score": 45,
    "classification": "COLD"
  }
}
```

---

# 66. Workflow State

n8n execution data should not be treated as the permanent application state.

Permanent state belongs in PostgreSQL.

Example:

```text
n8n execution
    ↓
Temporary workflow state

PostgreSQL
    ↓
Permanent business state
```

---

# 67. Customer Response Strategy

The AI response should:

1. Acknowledge the customer.
2. Use information already provided.
3. Ask for the most important missing information.
4. Avoid asking unnecessary questions.
5. Keep responses conversational.
6. Avoid repeating questions already answered.

Example:

Customer:

```text
I need a 3-bedroom apartment in Lekki for ₦80m.
```

Bad response:

```text
What type of property are you looking for?
What location?
What budget?
How many bedrooms?
```

Better:

```text
Thanks! You're looking for a 3-bedroom apartment in Lekki with a budget of about ₦80 million.

When are you hoping to complete the purchase?
```

---

# 68. Human Handoff

A lead should be eligible for human handoff when:

```text
HOT
```

or when the customer explicitly asks for a human.

Examples:

```text
"I want to speak with an agent."
"Can someone call me?"
"Please connect me to your salesperson."
```

Workflow:

```text
Customer Requests Human
        ↓
Set Lead Status
        ↓
Notify Sales
        ↓
Continue Customer Response
```

---

# 69. Lead Statuses

Recommended statuses:

```text
NEW
IN_PROGRESS
QUALIFIED
CONTACTED
FOLLOW_UP
CONVERTED
LOST
CLOSED
```

The exact status transitions should remain controlled by FastAPI/business rules.

---