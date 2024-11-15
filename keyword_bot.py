import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # The URL to use for the webhook

# List of keywords to monitor
KEYWORDS = ["urgent", "mercado livre", "cupom", "promoção"]

# Function to handle incoming messages and check for keywords
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower() if update.message and update.message.text else ""
    for keyword in KEYWORDS:
        if keyword in text:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Keyword Alert: '{keyword}' detected!"
            )
            break

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Keyword monitoring bot is active!")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set up webhook
    application.run_webhook(
        listen="0.0.0.0",               # Bind to all available IP addresses
        port=5000,                      # Use port 5000 (can be adjusted if needed)
        url_path=f"{BOT_TOKEN}",
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )

if __name__ == "__main__":
    main()
