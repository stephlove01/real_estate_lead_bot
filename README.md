# Real Estate Lead Bot

An AI-powered real estate lead management and qualification system designed to help real estate companies automatically receive, understand, qualify, store, and manage potential customers.

---

## 1. Project Overview

The Real Estate Lead Bot is a small automated business system for real estate companies.

The system acts like a digital receptionist.

When a potential customer sends a property enquiry, the system can:

1. Receive the customer's message.
2. Understand the customer's intent.
3. Extract important information.
4. Validate the information.
5. Store the lead.
6. Calculate the lead score.
7. Classify the lead as HOT, WARM, or COLD.
8. Generate an appropriate response.
9. Notify the sales team when necessary.
10. Track the lead's progress.
11. Support sales follow-up.

The goal is to combine **Frontend, Backend, AI, Database, and Automation** into one complete system.

---

# 2. Example Business

For this project, we will use a fictional real estate company:

**PrimeHomes Realty**

PrimeHomes Realty advertises residential properties and receives enquiries from potential customers through online channels.

Example customer messages:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million."

> "Do you have any 2-bedroom apartments in Ikeja?"

> "I need land around Ibadan, preferably below ₦20 million."

> "Hello, I want to buy a house."

The Real Estate Lead Bot will process these enquiries automatically.

---

# 3. Problem Statement

Real estate companies may receive many enquiries every day.

Manually processing every enquiry can result in:

* Slow responses.
* Missed leads.
* Poor lead organization.
* Difficulty identifying high-value customers.
* Repetitive work for sales teams.
* Inconsistent follow-up.
* Poor visibility into lead progress.

The Real Estate Lead Bot is designed to reduce these problems through automation and AI.

---

# 4. Project Goals

The system should be able to:

* Receive property enquiries.
* Understand customer intent.
* Extract customer and property information.
* Validate submitted information.
* Store leads.
* Qualify leads.
* Score leads.
* Categorize leads.
* Respond to customers.
* Notify sales representatives.
* Track lead status.
* Support follow-up.
* Provide a foundation for future automation.

---

# 5. Lead Information

The system will attempt to collect the following information.

## Customer Information

* Name
* Email
* Phone number

## Property Information

* Property type
* Number of bedrooms
* Location
* Budget
* Buy or rent

## Customer Intent

* Buying
* Renting
* Selling
* Land
* Property enquiry

## Timeline

* Immediately
* Within 1 month
* Within 3 months
* Just researching

---

# 6. High-Level Architecture

```text
                    CUSTOMER
                       |
                       v
              +------------------+
              |    FRONTEND      |
              | Chat / Lead Form |
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
                       |
                       v
                   FOLLOW-UP
```

---

# 7. Technology Stack

## Frontend

Initial frontend technologies:

* HTML
* CSS
* JavaScript

The frontend will provide:

* Chat interface.
* Lead form.
* Customer interaction.
* API communication.
* Display of bot responses.

A frontend framework may be introduced later if required.

---

## Backend

Backend technologies:

* Python
* FastAPI

The backend will be responsible for:

* Receiving requests.
* Validating data.
* Business logic.
* API endpoints.
* Communication with other system components.

Example endpoints:

```text
POST /api/leads
GET /api/leads/{id}
POST /api/chat
```

The exact endpoints may change during development.

---

## Automation

Automation platform:

* n8n

n8n will handle:

* Workflow orchestration.
* AI processing.
* Database operations.
* Notifications.
* Lead routing.
* Follow-up automation.
* External integrations.

---

## AI

AI will be responsible for:

* Understanding natural language.
* Extracting customer requirements.
* Classifying leads.
* Generating responses.
* Summarizing conversations.

AI will not replace the entire system.

It will act as one intelligent component inside the larger system.

---

## Database

The initial development database will be:

* SQLite

A production database such as PostgreSQL may be introduced later.

---

# 8. AI Lead Extraction

Customers do not always provide information in a structured form.

For example:

```text
Hi, I'm looking for a 3-bedroom apartment around Lekki.
My budget is about ₦80 million and I want to buy within
the next two months.
```

The AI should extract:

```json
{
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "intent": "buying",
  "timeline": "2 months"
}
```

The structured information can then be used by the automation system.

---

# 9. Lead Qualification

Lead qualification determines how valuable or urgent a lead may be.

Example:

### Lead A

> "I'm just browsing."

### Lead B

> "I'm interested in buying next year."

### Lead C

> "I have ₦100 million and want a 4-bedroom apartment in Lekki this month."

Lead C should receive a higher priority.

---

# 10. Lead Scoring

The educational version of the system will use a simple scoring model.

| Condition     | Points |
| ------------- | -----: |
| Phone number  |    +10 |
| Budget        |    +20 |
| Location      |    +15 |
| Property type |    +15 |
| Buying soon   |    +25 |
| Clear requ    |        |
