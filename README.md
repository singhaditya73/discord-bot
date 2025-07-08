# Cryptic Hunt Discord Bot

A custom-built Discord bot designed for managing and automating cryptic hunt events on Discord servers. This bot handles question flow, answer checking, leaderboard tracking, and smooth interaction for participants.

## 🚀 Features

- Automated question flow for cryptic levels
- Answer validation and level progression
- Leaderboard system to track participant progress
- Admin commands for monitoring and controlling the event
- Easy-to-use and beginner-friendly setup

## 🔧 Tech Stack

- **Language**: Python
- **Library**: discord.py
- **Hosting**: Can be hosted locally or on cloud platforms like Replit, Heroku, or Railway

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/singhaditya73/discord-bot.git
   cd discord-bot
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Create a .env File
Add your Discord bot token and other secrets:

env
Copy
Edit
DISCORD_TOKEN=your_bot_token_here
Run the Bot

bash
Copy
Edit
python bot.py
📂 Folder Structure
bash
Copy
Edit
discord-bot/
│
├── bot.py                # Main bot logic
├── questions.json        # List of cryptic questions and answers
├── leaderboard.json      # Tracks user progress
├── requirements.txt      # Dependencies
└── .env                  # Your bot token (keep this secret)
