# 🤖 AI Usage Note - Smart Ticket Deduplicator

## 📌 Overview
This project uses Artificial Intelligence techniques to identify and group duplicate support tickets based on semantic similarity.

---

## 🧠 AI/ML Techniques Used

### 1. Sentence Embeddings
- Model: `all-MiniLM-L6-v2` (Sentence Transformers)
- Purpose: Converts ticket text into numerical vectors (embeddings)
- Benefit: Understands meaning, not just keywords

---

### 2. Similarity Measurement
- Method: Cosine Similarity
- Used to compare two ticket embeddings
- Output range: 0 (no similarity) to 1 (exact match)

---

### 3. Duplicate Detection Logic
- If similarity > 0.65 → Verified Duplicate
- If 0.45 – 0.65 → Potential Match
- If < 0.45 → Not a Duplicate

---

### 4. LLM Verification Layer (Simulated)
- Mimics an AI model (like GPT/Llama)
- Adds explanation for similarity decisions
- Helps in interpreting results in human language

---

## ⚙️ Technologies Used
- Python
- Sentence Transformers
- NumPy
- Streamlit
- SQLite (for ticket storage)

---

## 🎯 Purpose
To reduce duplicate support tickets and improve efficiency in customer support systems using AI-based semantic matching.