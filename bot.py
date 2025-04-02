import requests
import json
import random
import re
import asyncio
import schedule
import os
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not all([TOKEN, CHAT_ID, GEMINI_API_KEY]):
    raise ValueError("Missing environment variables!")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
asked_questions = set()
question_queue = []

async def fetch_questions():
    prompt = """
     Generate four unique multiple-choice technical questions for freshers and 2-year experienced candidates.  
Take reference from GeeksforGeeks, InterviewBit, LeetCode, W3Schools, and similar sites.  

Topics: DBMS, OS, DSA, React, JavaScript, C, C++, Python, Algorithms, Data Structures, Networking, Software Engineering.  

Instructions:  
- Questions should not repeat; generate fresh ones every time.  
- Provide 4 distinct answer options (≤100 characters each).  
- Mark the correct option using a 0-based index.  
- Give a simple, easy-to-understand explanation (≤200 characters). 

Example:
{
  "question": "What is the purpose of `useEffect` in React?",
  "options": [
    "Execute code after render",
    "Handle routing",
    "Manage background jobs",
    "Define middleware"
  ],
  "correct_option_id": 0,
  "explanation": "`useEffect` runs side effects in function components, such as fetching data after rendering."
}

Ensure the output is **valid JSON** without extra text or formatting issues.
    """
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 1.2}}
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        text = re.sub(r"```json\n(.*?)\n```", r"\1", text, flags=re.DOTALL).strip()
        questions_data = json.loads(text)
        questions = []
        for q in questions_data:
            question = q.get("question", "").strip()
            if question in asked_questions: continue
            options = q.get("options", [])
            correct_option_id = q.get("correct_option_id")
            explanation = q.get("explanation", "No explanation provided.")[:200]
            if question and options and correct_option_id is not None:
                questions.append((question, options, correct_option_id, explanation))
        return questions if len(questions) == 4 else []
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"API Error: {e}")
        return []

async def send_question():
    global question_queue
    bot = Bot(token=TOKEN)
    if not question_queue:
        question_queue = await fetch_questions()
    if not question_queue:
        print("No questions available.")
        return
    question, options, correct_option_id, explanation = question_queue.pop(0)
    asked_questions.add(question)
    if len(asked_questions) > 24:
        asked_questions.pop()
    try:
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            explanation=explanation,
            is_anonymous=False
        )
        print(f"Sent at {datetime.now()}: {question}")
        if len(question_queue) == 1:
            question_queue = await fetch_questions()
    except Exception as e:
        print(f"Telegram Error: {e}")

schedule.every(2).hours.do(lambda: asyncio.create_task(send_question()))
print("Bot started...")

async def main():
    while True:
        try:
            schedule.run_pending()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Loop error: {e}")

asyncio.run(main())
