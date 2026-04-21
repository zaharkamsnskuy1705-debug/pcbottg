import os
import psutil
import platform
import subprocess

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
USER_ID = 1073348110

PC_IP = "192.168.0.107"

last_action = "Нема дій"


# ---------------- SAFE ----------------

def safe_run(cmd):
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print("CMD ERROR:", e)


def is_online():
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(
            ["ping", param, "1", PC_IP],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except:
        return False


def stats():
    try:
        return (
            psutil.cpu_percent(),
            psutil.virtual_memory().percent,
            psutil.disk_usage("/").percent
        )
    except:
        return (0, 0, 0)


# ---------------- MENU ----------------

def menu():
    try:
        status = "🟢 Онлайн" if is_online() else "🔴 Офлайн"
        cpu, ram, disk = stats()

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
            [InlineKeyboardButton("⚡ Wake", callback_data="wake")],
            [InlineKeyboardButton("⛔ Shutdown", callback_data="shutdown")],
            [InlineKeyboardButton("🔁 Restart", callback_data="restart")],
            [InlineKeyboardButton("🎮 Steam", callback_data="steam")],
        ])

        return text, kb

    except Exception as e:
        print("MENU ERROR:", e)
        return "⚠️ Помилка меню", None


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_action

    try:
        if update.effective_user.id != USER_ID:
            return

        last_action = "Панель відкрита"

        text, kb = menu()
        await update.message.reply_text(text, reply_markup=kb)

    except Exception as e:
        print("START ERROR:", e)


# ---------------- BUTTON ----------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_action

    try:
        q = update.callback_query

        if q.from_user.id != USER_ID:
            await q.answer("Нема доступу")
            return

        await q.answer()
        d = q.data

        if d == "refresh":
            text, kb = menu()
            await q.edit_message_text(text, reply_markup=kb)

        elif d == "wake":
            last_action = "Wake signal"
        
        elif d == "shutdown":
            safe_run("shutdown /s /t 0")
            last_action = "Shutdown (може не працювати на Railway)"

        elif d == "restart":
            safe_run("shutdown /r /t 0")
            last_action = "Restart (може не працювати)"

        elif d == "steam":
            safe_run("start steam://open/main")
            last_action = "Steam (тільки Windows)"

        text, kb = menu()
        await q.edit_message_text(text, reply_markup=kb)

    except Exception as e:
        print("BUTTON ERROR:", e)


# ---------------- RUN ----------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("🟢 BOT STABLE RUNNING...")
    app.run_polling()


if __name__ == "__main__":
    main()
