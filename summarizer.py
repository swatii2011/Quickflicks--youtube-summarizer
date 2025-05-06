import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import textwrap

# Load Groq API Key (make sure it's set in your environment or paste directly)
GROQ_API_KEY = "xxxxx"  # Replace with your Groq API key
GROQ_MODEL = "llama3-8b-8192"


def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    elif "youtube" in parsed_url.hostname:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    return None


def get_transcript(video_url):
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            return "❌ Error: Invalid YouTube URL"
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        return f"❌ Error fetching transcript: {str(e)}"


def summarize_transcript(transcript_text):
    prompt = f"""
Summarize the following transcript in 2 short paragraphs.
Focus on the core concepts of machine learning discussed in the transcript such as types of learning, how it's applied, and real-world use cases. Avoid repeating or listing too many examples.

Transcript:
\"\"\"{transcript_text}\"\"\"
"""
    return query_groq(prompt)


def generate_flashcards_from_transcript(transcript_text):
    prompt = f"""
You are a flashcard generator.

Given the following transcript from a video, generate 5 educational flashcard-style questions and answers that help a student study the material. Make sure the questions are specific and the answers are clear.

Format:
Q1: ...
Answer: ...

Transcript:
\"\"\"{transcript_text}\"\"\"
"""
    return query_groq(prompt)


def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"
