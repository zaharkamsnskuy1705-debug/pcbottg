from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = 1073348110


def menu():
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Статус", callback_data="refresh")],
        [InlineKeyboardButton("⛔ Вимкнути", callback_data="shutdown")],
        [InlineKeyboardButton("🔁 Рестарт", callback_data="restart")],
        [InlineKeyboardButton("🎮 Steam", callback_data="steam")]
    ])
    return "🖥 CONTROL PANEL", kb


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        return

    text, kb = menu()
    await update.message.reply_text(text, reply_markup=kb)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    # просто підтвердження
    await q.edit_message_text(f"Команда: {q.data}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🟢 BOT RUNNING...")
app.run_polling()
