from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = 1073348110

LAST_COMMAND = None


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Статус", callback_data="refresh")],
        [InlineKeyboardButton("⛔ Вимкнути", callback_data="shutdown")],
        [InlineKeyboardButton("🔁 Рестарт", callback_data="restart")],
        [InlineKeyboardButton("🎮 Steam", callback_data="steam")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        return

    await update.message.reply_text("🖥 CONTROL PANEL", reply_markup=menu())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LAST_COMMAND

    query = update.callback_query
    await query.answer()

    LAST_COMMAND = query.data

    await query.edit_message_text(f"✅ Команда: {LAST_COMMAND}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🟢 BOT RUNNING...")
app.run_polling()
