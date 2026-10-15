"""Rule-based ticket triage with an optional LLM-ready response layer."""
from __future__ import annotations
from typing import Any

CATEGORIES = {
    "billing": ["invoice", "charged", "payment", "refund", "billing", "subscription", "receipt", "price"],
    "technical_issue": ["error", "bug", "crash", "not working", "failed", "failure", "login", "loading", "broken", "issue"],
    "account_access": ["password", "locked out", "sign in", "signin", "login", "2fa", "verification", "access"],
    "feature_request": ["feature", "please add", "would be great", "request", "suggestion", "support for"],
    "shipping": ["delivery", "shipment", "tracking", "package", "order", "arrived", "shipping"],
    "general_inquiry": [],
}

URGENT_TERMS = ["data breach", "hacked", "security breach", "can't access", "cannot access", "outage", "all users", "production down", "urgent", "asap"]
HIGH_TERMS = ["charged twice", "double charged", "refund", "unable to login", "can't log in", "cannot log in", "crash", "lost data", "not working"]


def triage_ticket(subject: str, message: str, customer_tier: str = "standard") -> dict[str, Any]:
    text = f"{subject} {message}".lower()
    scores = {category: sum(1 for term in terms if term in text) for category, terms in CATEGORIES.items()}
    category = max(scores, key=scores.get)
    if scores[category] == 0:
        category = "general_inquiry"

    if any(term in text for term in URGENT_TERMS):
        priority = "critical"
    elif any(term in text for term in HIGH_TERMS):
        priority = "high"
    elif any(term in text for term in ["when will", "how do i", "how can i", "question", "wondering"]):
        priority = "low"
    else:
        priority = "medium"

    if customer_tier.lower() in {"enterprise", "premium"} and priority in {"medium", "high"}:
        priority = "high"

    response_templates = {
        "billing": "Thanks for contacting us about your billing concern. We'll review the charge and payment details. If applicable, please share the invoice or transaction reference—never send full card details.",
        "technical_issue": "Sorry you're running into this issue. Please share the steps that led to it, any error message, and your device/browser details so we can investigate.",
        "account_access": "We can help you regain access. Please use the official password-reset flow first. For your security, don't send passwords or verification codes in this ticket.",
        "feature_request": "Thanks for the suggestion. We've captured your feedback for review. If you can share the workflow this would improve, it will help us evaluate the request.",
        "shipping": "Thanks for reaching out about your order. Please share your order number or tracking reference so we can check the latest delivery status.",
        "general_inquiry": "Thanks for contacting support. Could you share a little more detail about what you're trying to do and what outcome you expected? We'll be happy to help.",
    }
    rationale = f"Matched category keywords for {category.replace('_', ' ')}; priority was estimated from urgency and impact language."
    return {
        "category": category,
        "priority": priority,
        "suggested_response": response_templates[category],
        "rationale": rationale,
        "needs_human_review": priority == "critical" or category == "general_inquiry",
    }
