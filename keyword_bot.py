import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Load your bot token from the .env file
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Define your list of keywords to monitor
KEYWORDS = ["urgent", "meeting", "error", "alert"]

# Function to handle messages and check for keywords
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower() if update.message and update.message.text else ""
    for keyword in KEYWORDS:
        if keyword in text:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Keyword Alert: '{keyword}' detected!"
            )
            break

# Start command to check if the bot is working
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Keyword monitoring bot is active!")

def main():
    # Initialize the bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
