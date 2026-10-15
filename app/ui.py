import requests
import streamlit as st

st.set_page_config(page_title="AI Support Ticket Triage", page_icon="🎫", layout="centered")
st.title("🎫 AI Support Ticket Triage")
st.caption("Classify support requests, estimate urgency, and draft a first response.")

with st.form("ticket_form"):
    subject = st.text_input("Ticket subject", placeholder="e.g. Charged twice for my subscription")
    message = st.text_area("Customer message", height=160, placeholder="Describe the customer's issue...")
    tier = st.selectbox("Customer tier", ["standard", "premium", "enterprise"])
    submitted = st.form_submit_button("Triage ticket", type="primary", use_container_width=True)

if submitted:
    if len(subject.strip()) < 3 or len(message.strip()) < 5:
        st.error("Enter a subject (at least 3 characters) and message (at least 5 characters).")
    else:
        try:
            with st.spinner("Analyzing ticket..."):
                response = requests.post("http://127.0.0.1:8000/triage", json={"subject": subject, "message": message, "customer_tier": tier}, timeout=10)
                response.raise_for_status()
                result = response.json()
            c1, c2 = st.columns(2)
            c1.metric("Category", result["category"].replace("_", " ").title())
            c2.metric("Priority", result["priority"].upper())
            if result["needs_human_review"]:
                st.warning("Human review recommended before sending a reply or taking action.")
            st.subheader("Suggested response")
            st.text_area("Draft (review before sending)", value=result["suggested_response"], height=130)
            st.caption(result["rationale"])
        except requests.RequestException:
            st.error("Could not connect to the API. Start it first with: uvicorn app.main:app --reload")

st.divider()
st.caption("Demo project: suggestions are heuristic, not an automated decision. Review all drafts before sending.")
