# Real Estate Lead Bot
## Product Requirements Document (PRD)

**Product:** Real Estate Lead Bot  
**Example Client:** PrimeHomes Realty  
**Document:** Product Requirements Document  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** September 2026

---

## 1. Executive Summary

Real Estate Lead Bot is an AI-powered lead capture, qualification, and follow-up system designed for real estate businesses.

The system receives messages from potential customers, understands their property requirements, extracts relevant information, qualifies the lead, stores the lead, generates an appropriate response, and notifies the sales team when human follow-up is required.

The product will combine:

- React for the frontend
- Python + FastAPI for the backend
- n8n for workflow orchestration and integrations
- An LLM for natural-language understanding and response generation
- SQL database for persistent business data
- Google Sheets for operational visibility and reporting
- Notification and messaging integrations for sales follow-up

The system is designed as a **real software product**, not simply as an n8n automation.

---

# 2. Problem Statement

Real estate businesses receive potential customers through different channels such as:

- WhatsApp
- Instagram
- Facebook
- Website forms
- Telegram
- Email
- Phone enquiries

Many enquiries are handled manually.

This creates several problems:

1. Leads may be missed.
2. Sales representatives may respond slowly.
3. Important customer information may not be collected.
4. Sales teams may not know which leads are most valuable.
5. Follow-ups may be forgotten.
6. Lead information may be stored inconsistently.
7. Business owners may have poor visibility into their leads.
8. Sales teams spend time repeatedly asking basic qualification questions.

The Real Estate Lead Bot aims to solve these problems through automated lead capture, AI-assisted qualification, structured data storage, and automated follow-up workflows.

---

# 3. Product Vision

Build a reliable AI-powered real estate lead management system that helps businesses:

> **Capture more leads, understand them faster, prioritize valuable opportunities, and follow up consistently.**

The system should allow a potential customer to communicate naturally while the platform converts the conversation into structured business information.

---

# 4. Product Goals

## 4.1 Primary Goals

The system must:

1. Capture potential real estate customers.
2. Understand customer messages.
3. Extract relevant customer information.
4. Extract property requirements.
5. Identify customer intent.
6. Determine purchase/rental timeline.
7. Qualify leads.
8. Assign a lead score.
9. Store lead information.
10. Generate useful responses.
11. Notify sales representatives.
12. Support human follow-up.
13. Track lead status.
14. Maintain conversation history.
15. Reduce repetitive manual work.

---

## 4.2 Business Goals

The product should help real estate businesses:

- Increase response speed.
- Reduce missed leads.
- Improve lead qualification.
- Increase sales-team productivity.
- Improve follow-up consistency.
- Identify high-value leads faster.
- Maintain centralized lead records.
- Improve visibility into sales opportunities.

---

# 5. Non-Goals

The MVP will NOT attempt to:

- Replace human sales representatives completely.
- Automatically close property sales.
- Make legal decisions.
- Provide legal advice.
- Guarantee property availability.
- Invent property listings.
- Invent prices.
- Automatically negotiate contracts.
- Process payments.
- Replace professional real estate agents.

The AI is an assistant and automation component, not the final authority for business decisions.

---

# 6. Target Users

## 6.1 Potential Customer / Lead

A person interested in:

- Buying property
- Renting property
- Buying land
- Selling property
- Asking about available properties

They should be able to communicate naturally without filling a long form.

---

## 6.2 Sales Representative

The sales representative needs to:

- Receive qualified leads.
- View customer requirements.
- See lead score.
- See lead status.
- Review conversation history.
- Follow up with customers.
- Update lead status.

---

## 6.3 Sales Manager

The sales manager needs to:

- Monitor incoming leads.
- Identify high-value leads.
- Monitor sales activity.
- Track lead progression.
- Review team performance.

---

## 6.4 Business Administrator

The administrator manages:

- System configuration.
- Users.
- Integrations.
- Lead data.
- Workflow configuration.
- AI configuration.

---

# 7. Primary User Journey

The expected customer journey is:

```text
Customer
   ↓
Lead Bot / Chat Interface
   ↓
FastAPI Backend
   ↓
n8n Workflow
   ↓
AI Processing
   ↓
Information Extraction
   ↓
Lead Qualification
   ↓
Lead Score
   ↓
SQL Database
   ↓
Sales Notification
   ↓
Human Follow-up
   ↓
Lead Status Updates
   ↓
Conversion
```

---

# 8. Core Product Workflow

The system should follow this general process:

```text
1. Receive customer message
2. Validate incoming data
3. Identify/create conversation
4. Process customer message
5. Extract structured information
6. Identify customer intent
7. Identify property requirements
8. Determine timeline
9. Check missing information
10. Calculate lead score
11. Save/update lead
12. Generate customer response
13. Send response
14. Notify sales team when necessary
15. Track lead status
16. Schedule or trigger follow-up
```

---

# 9. Lead Intake

The system must be able to receive customer enquiries.

Example:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million."

The system should identify:

```text
Property Type: Apartment
Bedrooms: 3
Location: Lekki
Budget: ₦80,000,000
Intent: Buying
```

If the customer provides their name:

```text
Name: Customer Name
```

If they provide contact information:

```text
Phone: Customer Phone
Email: Customer Email
```

The system should not ask questions for information that has already been provided.

---

# 10. Customer Information Extraction

The system should attempt to extract:

- Full name
- Email
- Phone number
- Preferred contact method

Example:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+2348000000000"
}
```

All extracted information must be validated before being stored.

---

# 11. Property Requirement Extraction

The system should extract relevant property requirements.

Possible fields include:

- Property type
- Number of bedrooms
- Number of bathrooms
- Preferred location
- Budget
- Currency
- Buy or rent
- Land size
- Property features
- Preferred amenities

Example:

```json
{
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "currency": "NGN",
  "transaction_type": "buy"
}
```

---

# 12. Customer Intent Classification

The system should identify the primary intent of the customer.

Supported MVP intents:

```text
BUY
RENT
SELL
LAND
PROPERTY_ENQUIRY
GENERAL_ENQUIRY
UNKNOWN
```

Example:

> "I need land around Ibadan."

Intent:

```text
LAND
```

Example:

> "Do you have a two-bedroom apartment in Ikeja?"

Intent:

```text
PROPERTY_ENQUIRY
```

---

# 13. Timeline Detection

The system should identify how soon the customer intends to act.

Supported values:

```text
IMMEDIATE
WITHIN_1_MONTH
WITHIN_3_MONTHS
RESEARCHING
UNKNOWN
```

Example:

> "I need to move into the apartment next month."

Timeline:

```text
WITHIN_1_MONTH
```

---

# 14. Lead Qualification

The system should determine whether a lead has enough information to be considered qualified.

Qualification may consider:

- Clear intent
- Budget
- Location
- Property type
- Timeline
- Contact information
- Specific requirements

Example:

A lead saying:

> "I want to buy a house."

may be considered incomplete.

The bot should ask an appropriate follow-up question such as:

> "Absolutely. What location and budget range are you considering?"

---

# 15. Lead Scoring

The system should assign a numerical or categorical score to leads.

Example categories:

```text
HIGH
MEDIUM
LOW
```

A numerical score may also be used.

Example:

```text
80-100 → High
50-79  → Medium
0-49   → Low
```

Potential scoring factors:

### Intent

Buying property may receive a higher score than general browsing.

### Budget

Higher or clearly defined budgets may increase the score.

### Timeline

Customers ready to purchase soon should receive higher priority.

### Requirement clarity

Specific requirements indicate stronger intent.

### Contact availability

A lead with valid contact information can be easier for the sales team to follow up with.

---

# 16. Lead Score Example

Customer:

> "I want to buy a 4-bedroom house in Lekki. My budget is ₦150 million and I want to buy within the next month. My phone number is 08000000000."

Possible result:

```text
Lead Score: 92
Lead Priority: HIGH
```

Reason:

- Buying intent is clear.
- Property requirement is specific.
- Location is known.
- Budget is known.
- Timeline is short.
- Contact information is available.

---

# 17. Missing Information Handling

The AI should determine what important information is missing.

For example:

Customer:

> "I want to rent an apartment."

Missing:

- Location
- Bedroom requirement
- Budget
- Timeline

The bot should not ask all questions at once unless necessary.

It should ask the most useful next question.

Example:

> "Sure. Which area are you looking to rent in?"

After receiving the location, it can continue gathering the remaining information.

---

# 18. AI Response Generation

The AI should generate responses that are:

- Helpful
- Concise
- Professional
- Natural
- Relevant
- Clear
- Customer-friendly

The AI should avoid unnecessary long responses.

---

# 19. AI Guardrails

The AI must NOT:

- Invent property listings.
- Invent prices.
- Invent availability.
- Invent customer information.
- Claim a property exists when the database has not confirmed it.
- Promise property availability.
- Make unauthorized financial decisions.
- Make legal claims.
- Misrepresent itself.

If information is unavailable, the AI should clearly communicate that.

Example:

> "I can help you with that. Let me collect a few details so our property team can recommend suitable options."

---

# 20. AI as an Assistant

The AI should not be treated as the source of truth.

The system must separate:

### Probabilistic tasks

Handled by AI:

- Understanding natural language.
- Extracting intent.
- Extracting requirements.
- Generating responses.
- Identifying missing information.

### Deterministic tasks

Handled by application/business logic:

- Lead scoring rules.
- Data validation.
- Database persistence.
- Authentication.
- Authorization.
- Lead status transitions.
- Business rules.
- Property availability checks.

---

# 21. Structured AI Output

AI responses should preferably be returned in structured JSON.

Example:

```json
{
  "intent": "BUY",
  "customer": {
    "name": null,
    "email": null,
    "phone": null
  },
  "property": {
    "type": "apartment",
    "bedrooms": 3,
    "location": "Lekki",
    "budget": 80000000
  },
  "timeline": "WITHIN_3_MONTHS",
  "missing_information": [
    "phone"
  ],
  "confidence": 0.94
}
```

The backend must validate the AI output before using it.

---

# 22. Lead Storage

The system should store leads in a SQL database.

The SQL database will be the **system of record** for core business information.

Core information includes:

- Lead
- Customer
- Conversation
- Message
- Property requirement
- Lead score
- Lead status
- Assignment
- Follow-up
- Timestamps

---

# 23. Google Sheets

Google Sheets may be used for:

- Operational visibility
- Reporting
- Sales-team access
- Lightweight exports
- External business workflows

However:

> **Google Sheets must not be treated as the authoritative source of truth for core lead data.**

The SQL database remains the primary source of truth.

n8n can synchronize relevant information between the database and Google Sheets.

---

# 24. Lead Status

The system should support a lead lifecycle.

Initial statuses:

```text
NEW
CONTACTED
QUALIFIED
FOLLOW_UP
VIEWING
NEGOTIATION
CONVERTED
LOST
CLOSED
```

Example:

```text
NEW
 ↓
CONTACTED
 ↓
QUALIFIED
 ↓
VIEWING
 ↓
NEGOTIATION
 ↓
CONVERTED
```

---

# 25. Sales Notification

When a lead meets predefined qualification criteria, the system should notify the sales team.

Example:

```text
🔥 HIGH-VALUE LEAD

Name: John Doe
Intent: Buy
Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80M
Timeline: Within 1 month
Score: 91
Status: Qualified
```

Possible notification channels:

- Telegram
- Email
- Slack
- WhatsApp
- Internal dashboard

The MVP may begin with one notification channel.

---

# 26. Lead Assignment

Qualified leads should be assignable to sales representatives.

The system should support:

- Manual assignment.
- Automatic assignment.
- Assignment by location.
- Assignment by property type.
- Assignment by sales representative availability.

Automatic assignment rules may be added after the MVP.

---

# 27. Sales Follow-Up

The system should support follow-up workflows.

Possible follow-up events:

```text
New Lead
↓
Initial Contact
↓
Follow-up Reminder
↓
Property Recommendation
↓
Property Viewing
↓
Negotiation
↓
Conversion
```

n8n can be used to automate reminders and notifications.

---

# 28. Conversation History

The system should maintain conversation history.

Each conversation should contain:

- Customer
- Channel
- Messages
- Timestamp
- Intent
- Extracted requirements
- Lead status

This allows sales representatives to understand the customer's previous interaction with the bot.

---

# 29. Frontend Requirements

The React frontend should provide a clean and professional user experience.

The frontend may include:

### Customer interface

- Chat interface
- Message input
- Conversation history
- Bot responses
- Lead/contact information

### Sales dashboard

- Lead list
- Lead details
- Lead score
- Lead status
- Customer requirements
- Conversation history
- Assignment
- Follow-up information

---

# 30. Backend Requirements

FastAPI will serve as the primary application backend.

Responsibilities include:

- REST API
- Authentication
- Authorization
- Input validation
- Business logic
- Database access
- Lead management
- Conversation management
- Lead scoring
- AI service integration
- n8n webhook integration
- Error handling

---

# 31. n8n Responsibilities

n8n will be used primarily for orchestration and integrations.

Responsibilities may include:

- Receiving webhook events.
- Calling AI services.
- Sending notifications.
- Updating Google Sheets.
- Sending follow-up reminders.
- Connecting external services.
- Triggering workflows.
- Routing events.
- Executing scheduled processes.

n8n should not become the location for all business logic.

---

# 32. Code Responsibilities

Application code should handle areas where deterministic software logic is more appropriate.

Examples:

- Authentication.
- Authorization.
- Validation.
- Lead scoring.
- Database operations.
- API endpoints.
- Business rules.
- Data transformations.
- Custom integrations.
- Complex calculations.

---

# 33. Architecture

The high-level architecture is:

```text
                    CUSTOMER
                       │
                       ▼
              ┌─────────────────┐
              │ React Frontend  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ FastAPI Backend │
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       ┌────────────┐      ┌─────────────┐
       │ SQL DB     │      │     n8n     │
       └────────────┘      └──────┬──────┘
                                  │
                           ┌──────┴──────┐
                           │             │
                           ▼             ▼
                        ┌─────┐    ┌────────────┐
                        │ AI  │    │ Integrations│
                        └─────┘    └────────────┘
                                       │
                                       ▼
                                Google Sheets
                                Notifications
```

---

# 34. Component Responsibilities

## React

Responsible for:

- UI
- User interaction
- State presentation
- API communication

React should not contain sensitive business logic.

---

## FastAPI

Responsible for:

- API layer
- Business logic
- Authentication
- Validation
- Database access
- Security

---

## n8n

Responsible for:

- Workflow orchestration
- Integrations
- Notifications
- Scheduled workflows
- External service communication

---

## AI

Responsible for:

- Natural language understanding
- Information extraction
- Classification
- Response generation

---

## SQL Database

Responsible for:

- Persistent storage
- Lead records
- Customer records
- Conversations
- Messages
- Status
- Follow-up information

---

# 35. Functional Requirements

## FR-001 — Lead Intake

The system must accept customer enquiries.

---

## FR-002 — Message Processing

The system must process incoming customer messages.

---

## FR-003 — Customer Extraction

The system must extract available customer information.

---

## FR-004 — Property Extraction

The system must extract property requirements.

---

## FR-005 — Intent Classification

The system must identify customer intent.

---

## FR-006 — Timeline Detection

The system must identify customer purchase/rental timeline where possible.

---

## FR-007 — Missing Information Detection

The system must identify important missing information.

---

## FR-008 — Lead Qualification

The system must determine whether the lead meets qualification criteria.

---

## FR-009 — Lead Scoring

The system must calculate a lead score.

---

## FR-010 — Lead Persistence

The system must store lead information in the SQL database.

---

## FR-011 — AI Response

The system must generate an appropriate customer response.

---

## FR-012 — Sales Notification

The system must notify the sales team when predefined conditions are met.

---

## FR-013 — Lead Assignment

The system should support assigning leads to sales representatives.

---

## FR-014 — Follow-Up

The system should support automated follow-up reminders.

---

## FR-015 — Lead Status

The system must support lead status tracking.

---

## FR-016 — Conversation History

The system must maintain customer conversation history.

---

# 36. Non-Functional Requirements

## 36.1 Performance

The system should provide fast responses under normal operating conditions.

Target:

```text
API response:
< 500ms excluding external AI/workflow processing where practical
```

AI response time may vary depending on the selected model and external services.

---

## 36.2 Reliability

The system should:

- Handle external API failures.
- Retry appropriate operations.
- Avoid duplicate lead creation.
- Preserve important data.
- Log failures.

---

## 36.3 Scalability

The architecture should allow future growth in:

- Number of leads.
- Number of users.
- Number of conversations.
- Number of integrations.
- Number of sales representatives.

---

## 36.4 Security

The system must:

- Protect authentication credentials.
- Protect API keys.
- Validate incoming data.
- Restrict unauthorized access.
- Use environment variables for secrets.
- Avoid storing secrets in GitHub.
- Apply appropriate authorization.

---

## 36.5 Maintainability

The codebase should:

- Use clear architecture.
- Use modular components.
- Have clear naming conventions.
- Include documentation.
- Include tests.
- Avoid unnecessary complexity.

---

# 37. Error Handling

The system should handle:

### AI Failure

If the AI service fails:

```text
AI Failure
↓
Log error
↓
Retry if appropriate
↓
Fallback response or human escalation
```

### Database Failure

The system should not report a successful lead creation if persistence failed.

### n8n Failure

Failed workflows should be logged and retried where appropriate.

### External Integration Failure

External API failures should not silently corrupt lead data.

---

# 38. Idempotency

The system should prevent duplicate processing.

For example, if the same webhook event is delivered twice, the system should avoid creating two identical leads.

Each relevant event should have an identifier such as:

```text
event_id
```

The system can use this to detect previously processed events.

---

# 39. Data Integrity

The system must ensure:

- Required fields are validated.
- IDs are unique.
- Dates are valid.
- Monetary values are stored correctly.
- AI output is validated.
- Database relationships remain consistent.

---

# 40. Authentication and Authorization

The production system should support authentication for internal users.

Possible roles:

```text
ADMIN
MANAGER
SALES_REP
```

Example permissions:

### ADMIN

Can:

- Manage users.
- Manage integrations.
- View all leads.
- Modify configuration.

### MANAGER

Can:

- View team leads.
- Assign leads.
- Monitor performance.

### SALES_REP

Can:

- View assigned leads.
- Update lead status.
- Add follow-up notes.

---

# 41. Data Privacy

The system may process personal information such as:

- Names
- Phone numbers
- Email addresses
- Property requirements
- Conversations

The system should:

- Minimize unnecessary data collection.
- Protect stored information.
- Restrict access.
- Avoid exposing customer information unnecessarily.
- Follow applicable data-protection requirements.

---

# 42. MVP Scope

The first version should focus on the essential workflow.

### MVP includes:

- Customer chat interface.
- React frontend.
- FastAPI backend.
- SQL database.
- Lead creation.
- Customer information extraction.
- Property requirement extraction.
- Intent classification.
- Timeline detection.
- Lead scoring.
- AI response generation.
- n8n workflow orchestration.
- Google Sheets synchronization.
- Sales notification.
- Lead status.
- Conversation history.

---

# 43. MVP Exclusions

The MVP will initially exclude:

- Payment processing.
- Complex CRM integration.
- Advanced property recommendation engine.
- Automated contract generation.
- Advanced analytics.
- Multi-company tenancy.
- Advanced sales forecasting.
- Voice assistant.
- Full WhatsApp Business API integration if configuration is not yet available.

These can be considered future enhancements.

---

# 44. Future Features

Potential future versions may include:

### Property Matching

Automatically match leads with suitable properties.

### Property Database

Store available properties directly in the platform.

### WhatsApp Integration

Connect the system to WhatsApp.

### Instagram Integration

Process Instagram enquiries.

### Facebook Integration

Process Facebook enquiries.

### Voice AI

Allow customers to interact through voice.

### Advanced Analytics

Provide:

- Conversion rate
- Lead source performance
- Sales representative performance
- Average response time
- Lead-to-sale time

### AI Sales Assistant

Help sales representatives draft:

- Follow-up messages
- Property recommendations
- Customer responses

---

# 45. Success Metrics

The product should eventually measure:

## Lead Capture Rate

Percentage of enquiries successfully captured.

## Response Time

Average time between customer message and response.

## Qualification Rate

Percentage of leads successfully qualified.

## Follow-Up Rate

Percentage of qualified leads receiving follow-up.

## Conversion Rate

Percentage of leads that become customers.

## Sales Productivity

Reduction in repetitive manual work.

## Lead Processing Accuracy

Accuracy of extracted information and classifications.

---

# 46. MVP Acceptance Criteria

The MVP will be considered successful when:

### AC-001

A customer can send a message through the interface.

### AC-002

The backend receives and validates the message.

### AC-003

The message can be processed through n8n.

### AC-004

The AI extracts relevant customer information.

### AC-005

The AI extracts property requirements.

### AC-006

The AI identifies customer intent.

### AC-007

The system identifies missing information.

### AC-008

The system calculates a lead score.

### AC-009

The lead is stored in the SQL database.

### AC-010

The system generates a customer response.

### AC-011

The customer receives the response.

### AC-012

Qualified leads trigger a sales notification.

### AC-013

Relevant information can be synchronized to Google Sheets.

### AC-014

Sales representatives can view lead information.

### AC-015

Lead status can be updated.

### AC-016

Conversation history can be retrieved.

### AC-017

Duplicate events do not create duplicate records.

### AC-018

Failures are logged and handled appropriately.

---

# 47. Product Principles

The following principles guide development.

## Principle 1 — AI is not the source of truth

AI can interpret information but should not be trusted blindly for deterministic business operations.

---

## Principle 2 — Database is the source of truth

Core business data belongs in the SQL database.

---

## Principle 3 — n8n is the orchestrator

n8n should coordinate workflows and integrations rather than contain the entire application.

---

## Principle 4 — Backend owns business logic

Important business rules should live in the backend/application layer.

---

## Principle 5 — Validate external input

All external data must be validated before entering the system.

---

## Principle 6 — Human-in-the-loop

The system should escalate important or uncertain situations to humans.

---

## Principle 7 — Design for failure

External APIs, AI services, workflows, and integrations can fail.

The system must be designed to recover gracefully.

---

## Principle 8 — Security by default

Secrets should never be committed to GitHub.

Sensitive operations must require appropriate authentication and authorization.

---

## Principle 9 — Build incrementally

The product should be developed in small, testable stages.

---

# 48. High-Level Domain Model

The core entities are expected to include:

```text
Customer
   │
   └── Conversation
          │
          └── Message

Customer
   │
   └── Lead
          │
          ├── Property Requirement
          ├── Lead Score
          ├── Lead Status
          ├── Assignment
          └── Follow-up
```

---

# 49. Initial Lead Object

A conceptual lead object may look like:

```json
{
  "id": "lead_123",
  "customer_id": "customer_123",
  "intent": "BUY",
  "status": "QUALIFIED",
  "score": 87,
  "priority": "HIGH",
  "property_requirement": {
    "property_type": "apartment",
    "bedrooms": 3,
    "location": "Lekki",
    "budget": 80000000,
    "currency": "NGN",
    "transaction_type": "buy"
  },
  "timeline": "WITHIN_1_MONTH",
  "created_at": "2026-09-12T10:00:00Z",
  "updated_at": "2026-09-12T10:05:00Z"
}
```

This is a conceptual model only. The final database schema will be defined in the Database Design document.

---

# 50. Development Approach

Development should happen in controlled phases.

## Phase 1 — Requirements

Deliver:

- PRD
- User stories
- Acceptance criteria

---

## Phase 2 — System Design

Deliver:

- System architecture
- Data flow
- Component responsibilities
- Integration boundaries

---

## Phase 3 — Technical Design

Deliver:

- Database schema
- API specification
- Backend architecture
- Authentication strategy

---

## Phase 4 — Frontend

Build:

- React application
- Chat interface
- Dashboard
- Lead views

---

## Phase 5 — Backend

Build:

- FastAPI application
- API endpoints
- Database models
- Business logic
- Validation

---

## Phase 6 — n8n

Build:

- Lead processing workflow
- AI workflow
- Notification workflow
- Google Sheets integration
- Follow-up workflows

---

## Phase 7 — AI

Implement:

- Extraction
- Classification
- Qualification support
- Response generation
- Guardrails
- Structured output validation

---

## Phase 8 — Testing

Test:

- Frontend
- Backend
- Database
- AI output
- n8n workflows
- Integrations
- Failure scenarios

---

## Phase 9 — Optimization

Improve:

- Performance
- Reliability
- User experience
- AI accuracy
- Observability
- Security

---

# 51. Definition of Done

A feature is considered complete when:

- Requirements are understood.
- Implementation is complete.
- Code follows project architecture.
- Input validation exists.
- Error handling exists.
- Tests are written where appropriate.
- The feature has been manually tested.
- Documentation is updated.
- No secrets are committed.
- The implementation does not violate established architecture.

---

# 52. Open Questions

The following decisions will be finalized during technical design:

1. Which SQL database will be used?
2. Which LLM provider will be used?
3. Which messaging channels will be supported in the MVP?
4. Which authentication system will be used?
5. Which notification channel will be used first?
6. How will sales representatives be assigned?
7. What exact lead scoring formula will be used?
8. Which property data source will be used?
9. Will the application be deployed to the cloud during the MVP?
10. What level of analytics is required?

These questions should be resolved before implementation of the affected components.

---

# 53. Recommended Initial Technical Direction

The recommended architecture is:

```text
Frontend
React
   ↓
Backend
FastAPI
   ↓
SQL Database
   ↓
n8n
   ↓
AI + Integrations
```

The backend should remain the primary application boundary.

n8n should be treated as an orchestration and integration layer.

The database should remain the authoritative source of business data.

---

# 54. Engineering Boundary

The system should maintain a clear separation:

```text
┌──────────────────────────────┐
│           React              │
│ Presentation / User Interface│
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           FastAPI            │
│ API + Business Logic         │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐   ┌─────────────┐
│ SQL Database│   │     n8n     │
│ Source Truth│   │ Orchestrator│
└─────────────┘   └──────┬──────┘
                         │
                         ▼
                    ┌─────────┐
                    │   AI    │
                    │Language │
                    └─────────┘
```

This separation is important for maintainability, testing, security, and future scaling.

---

# 55. Documentation Roadmap

This PRD is the first product document.

The next documents should be:

```text
01-product/
├── PRD.md
└── USER_STORIES.md

02-architecture/
├── SYSTEM_ARCHITECTURE.md
└── DATA_FLOW.md

03-technical/
├── TECHNICAL_DESIGN.md
├── API_SPECIFICATION.md
└── DATABASE_DESIGN.md

04-ai/
├── AI_AGENT_SPECIFICATION.md
├── PROMPTS.md
└── AI_EVALUATION.md

05-frontend/
└── UI_UX_SPECIFICATION.md

06-automation/
└── N8N_WORKFLOW_ARCHITECTURE.md

07-testing/
└── TEST_STRATEGY.md

08-decisions/
└── ADR.md
```

---

# 56. Final Product Principle

The Real Estate Lead Bot should be developed as a **real software product**, not simply as an automation workflow.

The architecture must therefore maintain clear boundaries between:

```text
User Interface
      ↓
Application Backend
      ↓
Business Logic
      ↓
Database
      ↓
Workflow Orchestration
      ↓
AI + External Integrations
```

Each component should have a clearly defined responsibility.

The objective is to build a system that is:

- Reliable
- Maintainable
- Secure
- Testable
- Scalable
- AI-assisted
- Human-supervised
- Business-focused

---

## Document Status

**Version:** 1.0  
**Status:** Draft  
**Owner:** Product / Engineering  
**Project:** Real Estate Lead Bot  
**Example Client:** PrimeHomes Realty

**Next Document:** `docs/02-architecture/SYSTEM_ARCHITECTURE.md`