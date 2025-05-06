import requests
import os

api_key = "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"  # Replace with your actual Groq API key
api_url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

transcript_text = """
Machine learning is a lot more than just learning. It's also about understanding and reasoning.
Today, we will learn about the basics of machine learning.
Humans learn from past experiences, and machines follow instructions. But if we train machines on past data, they can learn and act faster.
Machine learning builds predictive models from data and improves as more data is fed in.
There are three main types of machine learning: supervised, unsupervised, and reinforcement learning.
Machine learning is widely used in healthcare, fraud detection, social media analysis, and e-commerce.
"""

prompt = f"""
You are a helpful assistant. Read the following content and generate 5 concise flashcard-style questions and answers. Make sure the answers are accurate and short.

Content:
\"\"\"
{transcript_text}
\"\"\"

Format:
Q1: <question>?
Answer: <short answer>

Q2: ...
"""

data = {
    "model": "llama3-8b-8192",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.3
}

try:
    response = requests.post(api_url, headers=headers, json=data)
    print("✅ Status Code:", response.status_code)
    print("📨 Response:", response.text)
except Exception as e:
    print("❌ Error:", e)
