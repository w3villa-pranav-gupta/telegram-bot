# 📌 Telegram Quiz Bot

## 🚀 Features

1️⃣ ⏳ **Sends One Question Every 2 Hours** – Ensures a steady and engaging quiz experience.  
2️⃣ 🔄 **Fetches Fresh Questions Every 3rd Question** – Ensures continuous variety in questions.  
3️⃣ 🧠 **Unique Questions Every Time** – Avoids repeating previous 24 questions (last 6 batches).  
4️⃣ 🤖 **Uses Gemini AI for Question Generation** – High-quality, random, and diverse technical questions.  
5️⃣ 📚 **Covers Multiple Tech Topics** – DBMS, OS, DSA, React, JavaScript, Python, C++, and more.  
6️⃣ 🎯 **Multiple-Choice Quiz Format** – Each question has 4 answer choices.  
7️⃣ ✅ **Auto-Validated Answer** – Displays the correct answer after the poll ends.  
8️⃣ 📖 **Provides Brief Explanations** – Each question includes a simple explanation.  
9️⃣ ⚡ **Smart Randomization** – Uses AI temperature control for maximum uniqueness.  
🔟 🔔 **Real-Time Polls in Telegram** – Users can vote on answers directly in Telegram.  
1️⃣1️⃣ 📡 **Fully Automated** – Runs 24/7 with scheduled execution.  
1️⃣2️⃣ 🔐 **Secure & Reliable** – Uses environment variables to protect sensitive data.  
1️⃣3️⃣ 🌍 **Open-Source & Customizable** – Easily adaptable for different question styles.  

---

## 🚀 How to Set Up & Run the Telegram Quiz Bot

Follow these steps to install dependencies, configure, and run the bot on your system.

### ✅ Prerequisites
Before running the bot, ensure you have the following installed:

- ✅ **Python 3.8+** – Required to execute the script.
- ✅ **pip** – Python package manager (comes with Python).
- ✅ **Required Python Libraries**: Install them using the following command:

```bash
pip install requests python-dotenv python-telegram-bot schedule asyncio
```

---

### ⚙️ Setup Instructions

#### 1️⃣ Clone or Download the Repository

```bash
git clone https://github.com/your-repo-name/telegram-quiz-bot.git
cd telegram-quiz-bot
```

#### 2️⃣ Create a `.env` File and Add Your API Keys

Inside the project folder, create a `.env` file and add the following:

```ini
TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
GEMINI_API_KEY=your_gemini_api_key
```

📌 **Where to Get These Keys?**
- **TOKEN** → Get from [BotFather](https://t.me/botfather) on Telegram.
- **CHAT_ID** → Get your chat ID using a Telegram bot.
- **GEMINI_API_KEY** → Get from [Google AI's Gemini API](https://ai.google.dev/).

---

#### 3️⃣ Run the Bot

```bash
python bot.py
```

#### 4️⃣ Bot Starts Running! 🎉
You will see logs in the terminal indicating that the bot is sending questions every 2 hours.

---

## 🔄 How the Bot Works?

- Every **2 hours**, a new technical quiz question is sent as a **Telegram poll**.
- After the **3rd question**, the bot fetches **4 fresh unique questions** from the Gemini API.
- The bot ensures **no duplicate questions** from the last **6 batches (24 questions total).**
- **Fully automated!** Runs continuously without manual intervention.

---

📢 **Contributions & Feedback**
Feel free to fork, modify, or contribute to improve this bot! 🚀
