import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
import database

# Set up the web page styling
st.set_page_config(page_title="Smart Ticket Deduplicator", page_icon="🎫", layout="wide")

# Load the AI model once and cache it so the app runs fast
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

def calculate_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def seed_sample_data():
    database.init_db()
    existing_tickets = database.get_all_tickets()
    
    if len(existing_tickets) == 0:
        samples = [
            ("Login Failure", "Users are getting a 403 forbidden error when clicking login."),
            ("Password Reset Links Broken", "The password reset link email is not sending out to users."),
            ("Database Timeout on Checkout", "The checkout page is hanging and timing out with a database connection error."),
            ("Registration UI Bug", "The submit button on the registration form is grayed out and unclickable."),
        ]
        for title, desc in samples:
            embedding = model.encode(desc)
            database.insert_ticket(title, desc, embedding)

def verify_with_llm(new_ticket, past_ticket, score):
    """
    Simulates the LLM Verification layer ('Is it really a dup?').
    In a full production environment, this function calls an API like GPT-4 or Llama.
    """
    if score > 0.65:
        return "✅ VERIFIED DUPLICATE", "Both items point to the exact same core authentication defect."
    elif score > 0.45:
        return "⚠️ POTENTIAL MATCH", "Similar application module, but symptoms could indicate different root causes."
    else:
        return "❌ NOT A DUPLICATE", "The issues seem entirely distinct in behavior and scope."

# Make sure database has our starting historical tickets
seed_sample_data()

# --- STREAMLIT USER INTERFACE ---
st.title("🎫 Smart Production Support Ticket Deduplicator")
st.markdown("This prototype uses **Vector Search** to find past matches and an **LLM Layer** to verify duplicates.")
st.write("---")

# Layout columns: Left for typing a ticket, Right for seeing results
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📥 Incoming Ticket Details")
    new_ticket_text = st.text_area(
        "Paste the raw issue description here:",
        value="I keep getting access forbidden and error code 403 when I try signing into my account.",
        height=150
    )
    search_button = st.button("Analyze & Find Duplicates", type="primary")

with col2:
    st.subheader("🔍 Top 3 Candidate Duplicates Found")
    
    if search_button or new_ticket_text:
        # 1. Generate embedding for incoming ticket
        new_embedding = model.encode(new_ticket_text)
        
        # 2. Grab history from SQLite database
        past_tickets = database.get_all_tickets()
        results = []
        
        # 3. Calculate match scores
        for ticket in past_tickets:
            score = calculate_similarity(new_embedding, ticket["embedding"])
            verdict, reason = verify_with_llm(new_ticket_text, ticket["description"], score)
            
            results.append({
                "title": ticket["title"],
                "description": ticket["description"],
                "score": score,
                "verdict": verdict,
                "reason": reason
            })
        
        # Sort to show the highest similarity matches at the top
        results.sort(key=lambda x: x["score"], reverse=True)
        top_3 = results[:3]
        
        # 4. Render results nicely onto the webpage screen
        for i, match in enumerate(top_3, 1):
            with st.container():
                st.markdown(f"### Match #{i}: **{match['title']}**")
                st.caption(f"**Historical Description:** {match['description']}")
                
                # Visual metrics display
                m1, m2 = st.columns(2)
                m1.metric(label="Vector Similarity Score", value=f"{match['score']:.4f}")
                m2.markdown(f"**LLM Verdict:** {match['verdict']}\n\n*Reasoning:* {match['reason']}")
                st.markdown("---")