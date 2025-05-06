import streamlit as st
from summarizer import (
    get_transcript,
    summarize_transcript,
    generate_flashcards_from_transcript
)

# Page config
st.set_page_config(page_title="QUICKFLICKS: YouTube Summariser", layout="centered")

# Custom CSS for animations and dark theme
st.markdown("""
    <style>
        body {
            background-color: #0f0f0f;
        }
        .title {
            font-size: 3em;
            font-weight: 800;
            color: #ff4c60;
            text-align: center;
        }
        .subtitle {
            font-size: 1.2em;
            text-align: center;
            color: #ccc;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 1.5em;
            margin-top: 30px;
            color: #f39c12;
        }
        .flashcard {
            background-color: #111;
            border: 1px solid #444;
            padding: 1rem;
            margin-bottom: 10px;
            border-radius: 10px;
            color: #fff;
            box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.05);
            transition: transform 0.3s ease;
        }
        .flashcard:hover {
            transform: scale(1.02);
        }
        .expander-header {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="title">🎬 QUICKFLICKS: YOUTUBE VIDEO SUMMARISER</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">📥 Paste a YouTube link to get a summary and interactive flashcards</div>', unsafe_allow_html=True)

# Input field
video_url = st.text_input("🔗 Enter YouTube Video URL")

if st.button("📝 Generate"):
    with st.spinner("⏳ Fetching transcript..."):
        transcript = get_transcript(video_url)

    if transcript.startswith("❌ Error"):
        st.error(transcript)
    else:
        with st.spinner("🧠 Summarizing..."):
            summary = summarize_transcript(transcript)

        st.markdown('<div class="section-title">📄 Video Summary</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='flashcard'>{summary}</div>", unsafe_allow_html=True)

        with st.spinner("📚 Generating flashcards..."):
            flashcards_text = generate_flashcards_from_transcript(transcript)

        if flashcards_text.startswith("Error") or flashcards_text.startswith("❌"):
            st.error(flashcards_text)
        else:
            st.markdown('<div class="section-title">🧠 Flashcard Questions</div>', unsafe_allow_html=True)
            for line in flashcards_text.strip().split("\n\n"):
                if line.strip():
                    parts = line.split("\n")
                    if len(parts) == 2:
                        question = parts[0].strip()
                        answer = parts[1].replace("Answer:", "").strip()
                        with st.expander(f"❓ {question}", expanded=False):
                            st.markdown(f"<div class='flashcard'><strong>Answer:</strong> {answer}</div>", unsafe_allow_html=True)
