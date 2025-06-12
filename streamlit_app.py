import streamlit as st
from datetime import datetime
from bible_loader import load_bible
from hypothesis_engine import generate_hypothesis
from rag_engine import RAGEngine
from memory_store import load_memory, save_hypothesis


def run():
    st.set_page_config(page_title="Logos Researcher", layout="wide")
    st.title("📖 Logos Researcher")

    bible = load_bible()
    rag = RAGEngine(bible)
    memory = load_memory()

    col1, col2 = st.columns(2)
    with col1:
        st.header("The Sanctuary")
        query = st.text_input("Ask a question or enter a verse")
        manual_ref = st.text_input("Manual verse lookup (e.g., Genesis 1:1)")
        verses = []
        if query:
            verses = rag.search(query)
        if manual_ref:
            try:
                book, rest = manual_ref.split()
                chapter, verse = rest.split(":")
                text = bible[book][chapter][int(verse) - 1]
                verses.append({"reference": manual_ref, "text": text})
            except Exception:
                st.warning("Verse not found")
        for v in verses:
            st.markdown(f"**{v['reference']}**: {v['text']}")

    with col2:
        st.header("The Lab")
        if query or manual_ref:
            prompt = query or manual_ref
            hypothesis = generate_hypothesis(prompt)
            st.text_area("Hypothesis", hypothesis, height=200)
            if st.button("Refine Hypothesis"):
                hypothesis = generate_hypothesis(hypothesis)
                st.text_area("Refined Hypothesis", hypothesis, height=200)
            if st.button("Link to Science"):
                st.json([
                    {"title": "Photon Properties", "abstract": "Study on light.", "field": "Physics"},
                    {"title": "Vibration Theory", "abstract": "Frequency and creation", "field": "Physics"},
                ])
            if st.button("Save Thread"):
                save_hypothesis({
                    "verse": manual_ref or verses[0]['reference'] if verses else "",
                    "question": prompt,
                    "hypothesis": hypothesis,
                    "timestamp": datetime.utcnow().isoformat(),
                })
                st.success("Saved")

    st.header("Conversation Thread")
    for item in memory:
        st.markdown(f"{item['timestamp']} - {item['verse']} - {item['question']}")
        st.markdown(item['hypothesis'])
