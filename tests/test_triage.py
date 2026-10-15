from app.triage import triage_ticket


def test_billing_and_high_priority():
    result = triage_ticket("Charged twice", "I was charged twice and need a refund")
    assert result["category"] == "billing"
    assert result["priority"] == "high"


def test_security_issue_is_critical():
    result = triage_ticket("Possible data breach", "Our account may have been hacked")
    assert result["priority"] == "critical"
    assert result["needs_human_review"] is True


def test_unknown_ticket_needs_review():
    result = triage_ticket("Hello", "I have a question about something")
    assert result["category"] == "general_inquiry"
    assert result["needs_human_review"] is True


def test_enterprise_customer_escalation():
    result = triage_ticket("Account settings", "Can you help me with this?", "enterprise")
    assert result["priority"] == "high"
