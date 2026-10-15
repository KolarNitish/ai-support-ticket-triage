# AI Support Ticket Triage

A small portfolio project that helps a support team triage incoming tickets. It predicts a category, estimates urgency, drafts a first response, and flags cases that should be reviewed by a human.


## Demo

![AI Support Ticket Triage demo](screenshots/ticket-triage-demo.png)

**Live Demo:** https://ai-support-ticket-triage-icskytjilkhzmobgc3zkzk.streamlit.app/

**GitHub:** https://github.com/KolarNitish/ai-support-ticket-triage

## Features

- Ticket categories: billing, technical issue, account access, feature request, shipping, and general inquiry
- Priority estimation: low, medium, high, or critical
- Customer-tier escalation for premium and enterprise customers
- Suggested response draft with safety reminders
- FastAPI REST API with request validation and interactive Swagger docs
- Streamlit UI for a quick demo
- Pytest unit tests

> **Transparency:** This version uses explainable keyword-based rules so it works without paid API keys. It is an AI-support workflow prototype, not a trained machine-learning model. Always review suggested priorities and responses before taking action.

## Requirements

Python 3.10 or newer recommended.

## Setup

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `\.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

From the project root:

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation. Health check: `http://127.0.0.1:8000/health`.

## Run the Streamlit UI

Keep the API running in one terminal. In a second terminal, activate the same virtual environment and run:

```bash
streamlit run app/ui.py
```

## Example API request

```bash
curl -X POST "http://127.0.0.1:8000/triage" \
  -H "Content-Type: application/json" \
  -d '{"subject":"Charged twice for my subscription","message":"I was charged twice this month and need a refund.","customer_tier":"standard"}'
```

Example response:

```json
{
  "category": "billing",
  "priority": "high",
  "suggested_response": "Thanks for contacting us about your billing concern. We'll review the charge and payment details. If applicable, please share the invoice or transaction reference—never send full card details.",
  "rationale": "Matched category keywords for billing; priority was estimated from urgency and impact language.",
  "needs_human_review": false
}
```

## Run tests

```bash
pytest -q
```

## Suggested next improvements

- Replace keyword rules with a labeled-ticket classifier and evaluate precision/recall
- Add a database for ticket history and agent feedback
- Add authentication and role-based access
- Add an optional LLM provider for better summaries and response drafts, with redaction and validation
- Track category and priority accuracy on a held-out dataset

## Repository structure

```text
ai-support-ticket-triage/
├── app/
│   ├── main.py          # FastAPI endpoints and validation
│   ├── triage.py        # Classification, priority, response drafts
│   └── ui.py            # Streamlit demo interface
├── tests/
│   └── test_triage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Resume bullet (use after you have run and tested it)

**AI Support Ticket Triage | Python, FastAPI, Pydantic, Streamlit**
- Built a support-ticket triage prototype that categorizes requests, estimates urgency, drafts first-response suggestions, and flags critical cases for human review.
- Exposed validated REST endpoints with FastAPI and created an interactive Streamlit interface; added pytest coverage for ticket classification and escalation rules.
