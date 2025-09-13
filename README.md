# MailingList Bot

A Telegram bot for reminders and scheduled notifications built with **Aiogram** and **APScheduler**.

---

## 🚀 Features

- 🕒 **Scheduled Reminders**
  - Users receive timely notifications.
  - Supports recurring and one-time reminders.

- 🤖 **Telegram Bot**
  - Built with **Aiogram 3.x**.
  - Handles multiple users concurrently.

- 🗄️ **Database**
  - MySQL support via **SQLAlchemy**, **PyMySQL**, or **aiomysql**.
  - Supports migrations with **Alembic**.

- ⚡ **Async & Efficient**
  - Fully asynchronous using **aiohttp**, **aiofiles**, and async DB drivers.

- 🔒 **Configuration**
  - Environment variables via `.env`.

---

## ⚙️ Installation

```bash
git clone https://github.com/Oleg21345/MailingList.git
cd MailingList
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
