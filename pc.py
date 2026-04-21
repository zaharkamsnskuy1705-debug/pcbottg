import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
USER_ID = 1073348110

API_URL = "https://ngrok.com/docs/errors/err_ngrok_4018"  # <-- встав сюди свій ngrok

last_action = "Нема дій"


# ---------------- STATUS ----------------

def stats():
    try:
        r = requests.get(f"{API_URL}/status", timeout=3).json()
        return r["cpu"], r["ram"], r["disk"], True
    except:
        return 0, 0, 0, False


# ---------------- MENU ----------------

def menu():
    global last_action

    cpu, ram, disk, online = stats()
    status = "🟢 Онлайн" if online else "🔴 Офлайн"

    text = f"""
🖥 CONTROL PANEL

📡 Статус: {status}
🔥 CPU: {cpu}%
🧠 RAM: {ram}%
💾 Disk: {disk}%

🧾 Остання дія: {last_action}
"""

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Оновити", callback_data="refresh")],

        [InlineKeyboardButton("⚡ Увімкнути ПК", callback_data="wake")],
        [InlineKeyboardButton("⛔ Вимкнути ПК", callback_data="shutdown")],
        [InlineKeyboardButton("🔁 Перезавантажити ПК", callback_data="restart")],

        [InlineKeyboardButton("🎮 Steam", callback_data="steam")]
    ])

    return text, kb


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_action

    if update.effective_user.id != USER_ID:
        return

    last_action = "Панель відкрита"

    text, kb = menu()
    await update.message.reply_text(text, reply_markup=kb)


# ---------------- BUTTONS ----------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_action

    q = update.callback_query

    if q.from_user.id != USER_ID:
        await q.answer("Нема доступу")
        return

    await q.answer()
    d = q.data

    # 🔄 refresh
    if d == "refresh":
        text, kb = menu()
        await q.edit_message_text(text, reply_markup=kb)

    # ⚡ wake (wake-on-lan)
    elif d == "wake":
        last_action = "Спроба увімкнення (WOL)"
        text, kb = menu()
        await q.edit_message_text(text, reply_markup=kb)

    # ⛔ shutdown
    elif d == "shutdown":
        try:
            requests.get(f"{API_URL}/shutdown")
            last_action = "ПК вимкнено"
        except:
            last_action = "Помилка вимкнення"

        text, kb = menu()
        await q.edit_message_text(text, reply_markup=kb)

    # 🔁 restart
    elif d == "restart":
        try:
            requests.get(f"{API_URL}/restart")
            last_action = "ПК перезавантажено"
        except:
            last_action = "Помилка рестарту"

        text, kb = menu()
        await q.edit_message_text(text, reply_markup=kb)

    # 🎮 steam
    elif d == "steam":
        try:
            requests.get(f"{API_URL}/steam")
            last_action = "Steam запущено"
        except:
            last_action = "Помилка запуску Steam"

        text, kb = menu()
        await q.edit_message_text(text, reply_markup=kb)


# ---------------- RUN ----------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🟢 BOT RUNNING...")
app.run_polling()
