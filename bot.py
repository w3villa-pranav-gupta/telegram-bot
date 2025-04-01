import requests
import json
import time
import random  # Import random for shuffling
from datetime import datetime
from telegram import Bot
import os
from dotenv import load_dotenv
import asyncio
import schedule
import re  # Added for regex handling

# Load environment variables
load_dotenv()

# Get environment variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not all([TOKEN, CHAT_ID, GEMINI_API_KEY]):
    raise ValueError("One or more environment variables are missing. Please check your .env file.")

# Gemini API URL
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Set to keep track of asked questions
asked_questions = set()

async def fetch_questions():
    """Fetch four unique quiz questions with explanations using the Gemini API."""
    prompt = """
    Generate four unique multiple-choice technical questions commonly asked in interviews. 
    take help from geeks for geeks,interviewbit,leetcode, and other interview preparation sites.
    The questions should be related to one of the following topics: DBMS, OS, DSA, React, JavaScript, 
    C, C++, Python, Algorithms, Data Structures, Networking, Software Engineering (medium level). 
    Return a **valid JSON** object only with the following structure for each question:
    Generate a challenging multiple-choice quiz question for advanced MERN stack developers.
    Instructions:
    - The question should focus on advanced DBMS, OS, DSA, React, JavaScript, 
    C, C++, Python, Algorithms, Data Structures, Networking, Software Engineering topics.
    - Provide 4 distinct options, each not exceeding 100 characters.
    - Specify the correct answer by its index (0-based).
    - Include a brief explanation (up to 200 characters) of the correct answer.
    - Vary topics across different areas of Ruby and Rails, avoiding repetition of subjects like Lambda and Proc.

      Example:
    {
      "question": "What is the purpose of `useEffect` hook in React?",
      "options": [
        "Execute code after render",
        "Handle routing",
        "Manage background jobs",
        "Define middleware"
      ],
      "correct_option_id": 0,
      "explanation": "`useEffect` runs side effects in function components, often for tasks like fetching data or subscribing to events after the component renders."
    }

    Ensure the response is **valid JSON** without extra text, explanations, or formatting issues.
    """

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            print("Raw API Response:", json.dumps(result, indent=2))  # Debugging

            text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            print("Extracted Text:", text)  # Debugging

            # Remove Markdown code block (```json ... ```)
            text = re.sub(r"```json\n(.*?)\n```", r"\1", text, flags=re.DOTALL).strip()

            # Convert text to JSON
            questions_data = json.loads(text)

            questions = []
            for question_data in questions_data:
                question = question_data.get("question", "").strip()
                options = question_data.get("options", [])
                correct_option_id = question_data.get("correct_option_id", None)
                explanation = question_data.get("explanation", "No explanation provided.")[:200]  # Trim explanation to 200 chars

                if question and options and correct_option_id is not None:
                    questions.append((question, options, correct_option_id, explanation))

            if len(questions) == 4:
                return questions
            else:
                print("Error: Less than four questions returned.")
                return []

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing response (Attempt {attempt+1}): {e}")
            time.sleep(2 ** attempt)  # Exponential backoff

    print("Failed after multiple attempts.")
    return []

async def send_questions(questions):
    """Send each question as a Telegram poll with a one-minute interval."""
    bot = Bot(token=TOKEN)

    # Shuffle questions for randomization
    random.shuffle(questions)

    for question, options, correct_option_id, explanation in questions:
        # Check if the question has already been asked
        if question in asked_questions:
            print("Question already asked, skipping...")
            continue  # Skip to the next question if it's already been asked

        # Add the question to the set of asked questions
        asked_questions.add(question)

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
            print(f"✅ Quiz sent at {datetime.now()}: {question}")
            await asyncio.sleep(60)  # Wait for 1 minute before sending the next question
        except Exception as e:
            print(f"Telegram API Error: {e}")

async def job():
    """Fetch questions and send them."""
    questions = await fetch_questions()
    if questions:
        await send_questions(questions)
    else:
        print("No questions to send.")

# Schedule the job to run every 4 minutes (to allow for 4 questions to be sent)
schedule.every(4).minutes.do(lambda: asyncio.create_task(job()))

print("Bot started...")

# Keep the script running
async def main():
    while True:
        try:
            schedule.run_pending()
            await asyncio.sleep(1)  # Use async sleep
        except Exception as e:
            print(f"Error: {e}")
            continue

# Run the async event loop properly
asyncio.run(main())