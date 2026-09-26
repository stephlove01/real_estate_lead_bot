# n8n Workflow Specification — Real Estate Lead Bot

## 1. Document Overview

**Project:** PrimeHomes Realty — Real Estate Lead Bot  
**Component:** n8n Automation Workflow  
**Version:** 1.0  
**Purpose:** Define the automation workflow responsible for receiving leads, processing customer messages with AI, extracting lead information, qualifying and scoring leads, storing lead data, generating responses, notifying the sales team, and supporting follow-up.

## 2. Workflow Objective

The n8n workflow acts as the **automation and orchestration layer** between the frontend/backend application, AI services, database, and sales team.

The workflow should:

1. Receive a customer message from the backend.
2. Validate the incoming request.
3. Send the customer message to the AI for analysis.
4. Extract structured lead information.
5. Classify the customer's intent.
6. Determine the customer's buying/renting timeline.
7. Calculate a lead score.
8. Assign a lead temperature.
9. Store the lead in the database.
10. Generate an appropriate customer response.
11. Return the response to the backend.
12. Notify the sales team when appropriate.
13. Create follow-up tasks for qualified leads.
14. Track changes to the lead over time.

## 3. High-Level Architecture

```text
Customer
   │
   ▼
Frontend Chat Interface
   │
   ▼
Python FastAPI Backend
   │
   ▼
n8n Webhook
   │
   ▼
AI Processing
   │
   ├── Extract Customer Information
   ├── Extract Property Requirements
   ├── Identify Intent
   └── Identify Timeline
   │
   ▼
Lead Qualification
   │
   ▼
Lead Scoring
   │
   ├── HOT
   ├── WARM
   └── COLD
   │
   ▼
MySQL Database
   │
   ├──────────────► Sales Notification
   │
   └──────────────► Follow-up System
   │
   ▼
Generate Customer Response
   │
   ▼
FastAPI Backend
   │
   ▼
Frontend
   │
   ▼
Customer
```

## 4. Main n8n Workflow

```text
Webhook
   ↓
Validate Input
   ↓
Prepare Lead Data
   ↓
AI Lead Analysis
   ↓
Parse AI Output
   ↓
Calculate Lead Score
   ↓
Determine Lead Temperature
   ↓
Save Lead to MySQL
   ↓
Generate Customer Response
   ↓
Check Lead Priority
   ↓
Notify Sales Team
   ↓
Return Response
```

## 5. Node Specification

### Node 1 — Webhook Trigger

**Node Type:** Webhook

**Purpose:** Receive lead information from the FastAPI backend.

**HTTP Method:**

```text
POST
```

**Example Endpoint:**

```text
/webhook/real-estate-lead
```

**Example Request:**

```json
{
  "session_id": "session_12345",
  "message": "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million.",
  "name": "Amina Yusuf",
  "email": "amina@example.com",
  "phone": "08012345678"
}
```

**Required Fields:**

```text
session_id
message
```

**Optional Fields:**

```text
name
email
phone
```

### Node 2 — Validate Input

**Node Type:** IF / Code / Set

**Purpose:** Ensure the incoming request contains the minimum information required for processing.

**Validation Rules:**

- `message` exists
- `message` is not empty
- `session_id` exists

**If valid:** Continue to AI processing.

**If invalid:** Return an error response.

**Example error:**

```json
{
  "success": false,
  "message": "Please provide a message so we can assist you."
}
```

### Node 3 — Prepare Lead Data

**Node Type:** Set / Edit Fields

**Purpose:** Create a consistent data structure before sending information to the AI.

**Fields:**

```text
session_id
message
name
email
phone
received_at
source
```

**Example:**

```json
{
  "session_id": "session_12345",
  "message": "I need a 3-bedroom apartment in Lekki.",
  "name": "Amina Yusuf",
  "email": "amina@example.com",
  "phone": "08012345678",
  "source": "website",
  "received_at": "2026-09-26T16:00:00Z"
}
```

### Node 4 — AI Lead Analysis

**Node Type:** AI / LLM

**Purpose:** Understand the customer's natural-language message and convert it into structured information.

The AI should identify:

**Customer Information**

```text
name
email
phone
```

**Property Requirements**

```text
property_type
bedrooms
location
budget
```

**Intent**

Possible values:

```text
buying
renting
selling
land
property_enquiry
unknown
```

**Timeline**

Possible values:

```text
immediately
within_1_month
within_3_months
researching
unknown
```

**Requirements**

The AI should also identify the customer's specific requirements.

Example:

```text
"3-bedroom apartment around Lekki"
```

### Node 5 — AI Structured Output

The AI must return valid JSON.

**Expected format:**

```json
{
  "customer": {
    "name": null,
    "email": null,
    "phone": null
  },
  "property": {
    "property_type": "apartment",
    "bedrooms": 3,
    "location": "Lekki",
    "budget": 80000000
  },
  "intent": "buying",
  "timeline": "unknown",
  "requirements": [
    "3-bedroom apartment",
    "Lekki"
  ],
  "missing_information": [
    "timeline"
  ]
}
```

The AI must not invent information that the customer did not provide.

Unknown information should be returned as:

```text
null
```

or:

```text
unknown
```

### Node 6 — Parse AI Output

**Node Type:** Structured Output Parser / Code

**Purpose:** Convert the AI response into structured fields that n8n can use.

Extract:

```text
customer_name
customer_email
customer_phone

property_type
bedrooms
location
budget

intent
timeline
requirements
missing_information
```

### Node 7 — Lead Qualification

**Node Type:** Code / Set

**Purpose:** Determine whether the lead contains enough information to be considered qualified.

A lead becomes more complete when it contains:

- Contact information
- Property type
- Location
- Budget
- Timeline
- Clear buying/renting intent

Example:

```text
Name ✓
Phone ✓
Property type ✓
Location ✓
Budget ✓
Timeline ✓
Intent ✓
```

### Node 8 — Lead Scoring

**Node Type:** Code

**Purpose:** Assign a numerical score to the lead based on available information and buying intent.

| Lead Information | Points |
|---|---:|
| Phone number | +10 |
| Budget provided | +20 |
| Location provided | +15 |
| Property type provided | +15 |
| Buying/renting timeline is soon | +25 |
| Clear requirements | +15 |

**Maximum score:**

```text
100
```

### Lead Temperature

```text
80–100 → HOT
50–79  → WARM
0–49   → COLD
```

**HOT:** Clear requirements, budget, location, contact information, strong intent, and short timeline.

**WARM:** Genuine interest but some important information or urgency is missing.

**COLD:** Limited information, general enquiry, researching, or no clear timeline.

### Node 9 — MySQL Database Storage

**Node Type:** MySQL

**Purpose:** Store lead information for retrieval, follow-up, and reporting.

**Database:** MySQL

**Suggested lead table fields:**

```text
id
session_id
name
email
phone
property_type
bedrooms
location
budget
intent
timeline
requirements
lead_score
lead_temperature
status
source
created_at
updated_at
```

### Lead Status

Initial status:

```text
new
```

Possible future statuses:

```text
new
contacted
qualified
viewing_scheduled
negotiating
converted
lost
```

### Node 10 — Generate Customer Response

**Node Type:** AI

**Purpose:** Generate a helpful response based on the information extracted from the customer.

The response should:

- Be conversational
- Be professional
- Avoid pretending to know property availability unless the database confirms it
- Ask for missing information
- Guide the customer toward the next step
- Avoid asking for information the customer already provided

**Example customer message:**

```text
Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million.
```

**Example response:**

```text
Thanks for reaching out to PrimeHomes Realty. I understand you're looking for a 3-bedroom apartment around Lekki with a budget of about ₦80 million.

I'd be happy to help you narrow down suitable properties. When are you looking to purchase — immediately, within the next month, or later?
```

### Node 11 — Check Lead Priority

**Node Type:** IF / Switch

Check:

```text
lead_temperature
```

**HOT:** Send notification to sales immediately.

**WARM:** Store the lead and optionally notify sales.

**COLD:** Store the lead and continue normal conversation.

### Node 12 — Sales Notification

**Node Type:** Telegram / Email / Slack / WhatsApp API

**Purpose:** Notify the sales team when a qualified lead requires attention.

**Example HOT lead notification:**

```text
🔥 NEW HOT LEAD

Name: Amina Yusuf
Phone: 08012345678

Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80,000,000

Intent: Buying
Timeline: Within 1 month

Lead Score: 95
Temperature: HOT

Action:
Contact the lead as soon as possible.
```

### Node 13 — Return Response to Backend

**Node Type:** Respond to Webhook

The workflow returns structured information to the FastAPI backend.

**Example response:**

```json
{
  "success": true,
  "message": "Thanks for reaching out to PrimeHomes Realty. When are you looking to purchase?",
  "lead": {
    "score": 75,
    "temperature": "WARM",
    "status": "new"
  }
}
```

The backend then sends the response to the frontend.

## 6. Complete Main Workflow

```text
                    ┌──────────────────┐
                    │ Customer Message │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ FastAPI Backend │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Webhook Trigger │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Validate Input  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Prepare Data    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ AI Lead Analysis│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Parse AI Output │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Lead Qualify    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Lead Scoring    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Lead Temperature│
                    └────────┬────────┘
                             │
                  ┌──────────┼──────────┐
                  │          │          │
                 HOT        WARM       COLD
                  │          │          │
                  ▼          ▼          ▼
             Notify Sales  Optional   Continue
                          Notify
                  └──────────┬──────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ MySQL Database  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ AI Response     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Respond Webhook │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ FastAPI Backend │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Frontend Chat   │
                    └─────────────────┘
```

## 7. Follow-Up Workflow

The project should have a separate workflow for follow-up.

**Trigger:**

```text
Schedule Trigger
```

Example:

```text
Every day at 9:00 AM
```

**Workflow:**

```text
Schedule Trigger
      ↓
Get Leads From MySQL
      ↓
Find Leads Requiring Follow-Up
      ↓
Check Lead Status
      ↓
Generate Follow-Up Message
      ↓
Send Message
      ↓
Update Follow-Up Status
```

### Follow-Up Rules

**New lead:** Follow up after 24 hours.

**HOT lead:** Follow up sooner if sales has not contacted the lead.

**WARM lead:** Follow up after 1–3 days.

**Researching lead:** Follow up later with useful property information.

## 8. Lead Conversation History

The system should eventually maintain conversation history.

Suggested table:

```text
conversations
```

Fields:

```text
id
lead_id
session_id
sender
message
timestamp
```

Sender values:

```text
customer
bot
sales
```

This allows the AI to understand previous messages instead of treating every message as a new conversation.

## 9. Error Handling

The workflow should handle failures gracefully.

Possible errors:

```text
Invalid request
AI failure
Invalid AI JSON
Database failure
Notification failure
Timeout
Missing required field
```

**Error handling flow:**

```text
Main Workflow
      │
      ▼
Process Request
      │
      ├── Success → Continue
      │
      └── Error → Error Handler
                       │
                       ├── Log Error
                       ├── Notify Admin
                       └── Return Friendly Message
```

The customer should never receive technical error messages such as:

```text
500 Internal Server Error
JSON parsing failed
Database connection refused
```

Instead:

```text
Sorry, I'm having trouble processing your request right now. Please try again in a moment.
```

## 10. Security Requirements

The workflow should:

- Validate incoming requests.
- Avoid exposing API keys.
- Store credentials in n8n Credentials.
- Avoid putting secrets directly inside Code nodes.
- Validate AI output.
- Sanitize user input where appropriate.
- Protect webhook endpoints.
- Use HTTPS when deployed publicly.
- Restrict database credentials.
- Avoid exposing internal database information to customers.

## 11. Environment Variables

Sensitive configuration should be stored outside workflow logic.

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD

AI_API_KEY

N8N_WEBHOOK_URL
```

**Never commit secrets to GitHub.**

## 12. Testing Requirements

### Test 1 — Complete Buying Lead

```text
Hi, I'm looking for a 3-bedroom apartment in Lekki. My budget is ₦80 million and I want to buy within the next month. My phone number is 08012345678.
```

**Expected:**

```text
Intent: buying
Property: apartment
Bedrooms: 3
Location: Lekki
Budget: ₦80m
Timeline: within_1_month
Temperature: HOT
```

### Test 2 — Property Enquiry

```text
Do you have any 2-bedroom apartments in Ikeja?
```

**Expected:**

```text
Intent: property_enquiry
Property: apartment
Bedrooms: 2
Location: Ikeja
Budget: unknown
Timeline: unknown
```

The bot should ask for missing information.

### Test 3 — Land

```text
I need land around Ibadan, preferably below ₦20 million.
```

**Expected:**

```text
Intent: land
Property: land
Location: Ibadan
Budget: ₦20m
```

### Test 4 — General Enquiry

```text
Hello, I want to buy a house.
```

**Expected:**

```text
Intent: buying
Property: house
Location: unknown
Budget: unknown
Timeline: unknown
```

The bot should ask useful follow-up questions.

## 13. Success Criteria

The n8n system will be considered functional when:

- A customer can send a message from the frontend.
- FastAPI receives the message.
- FastAPI sends the message to n8n.
- n8n processes the message.
- AI extracts lead information.
- The lead receives a score.
- The lead receives a temperature.
- The lead is stored in MySQL.
- AI generates an appropriate response.
- The response is returned to the frontend.
- HOT leads trigger a sales notification.
- Follow-up information can be stored and retrieved.
- Errors are handled without exposing technical details.

## 14. Future Integrations

The workflow can later be extended to support:

- WhatsApp Business API
- Telegram
- Email
- Instagram
- Facebook Messenger
- Google Sheets
- CRM systems
- Calendar scheduling
- Property inventory database
- Google Maps
- Sales dashboards
- Analytics
- Automated property recommendations

## 15. Recommended Development Order

### Phase 1 — Basic Connection

```text
FastAPI
   ↓
n8n Webhook
   ↓
Response
```

### Phase 2 — AI

```text
Webhook
   ↓
AI
   ↓
Structured JSON
   ↓
Response
```

### Phase 3 — Lead Processing

```text
Webhook
   ↓
AI Extraction
   ↓
Qualification
   ↓
Scoring
```

### Phase 4 — Database

```text
AI
   ↓
Scoring
   ↓
MySQL
```

### Phase 5 — Customer Response

```text
MySQL
   ↓
AI Response
   ↓
FastAPI
   ↓
Frontend
```

### Phase 6 — Sales Notification

```text
Lead Score
   ↓
IF / Switch
   ↓
HOT?
   ↓
Sales Notification
```

### Phase 7 — Follow-Up

```text
Schedule Trigger
   ↓
MySQL
   ↓
Find Leads
   ↓
AI Follow-Up
   ↓
Send Message
   ↓
Update Database
```

## 16. Final n8n Workflow Architecture

The completed automation system should consist of at least two workflows.

### Workflow 1 — Lead Processing

```text
Webhook
→ Validate
→ Prepare Data
→ AI Extraction
→ Parse JSON
→ Qualify
→ Score
→ Temperature
→ MySQL
→ AI Response
→ Sales Notification
→ Respond to Webhook
```

### Workflow 2 — Lead Follow-Up

```text
Schedule Trigger
→ MySQL
→ Find Follow-Up Leads
→ AI Follow-Up Message
→ Send Message
→ Update Lead
```

## 17. Project Principle

> **Use n8n for orchestration and integrations, AI for understanding and generation, Python/FastAPI for application logic and API control, MySQL for persistent data, and the frontend for customer interaction.**

This separation makes the Real Estate Lead Bot easier to build, test, maintain, and expand.
