import io
import logging
import os
from pytubefix import YouTube
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
# IMPORTANT: Replace with your actual bot token from @BotFather
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Enable logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user_name = update.effective_user.first_name
    await update.message.reply_html(
        f"👋 Hi {user_name}!\n\n"
        f"Send me any YouTube link, and I'll send back the audio. No files are saved on the server!"
    )


async def process_youtube_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Downloads audio from a YouTube link into memory and sends it to the user."""
    url = update.message.text
    chat_id = update.effective_chat.id

    if "youtube.com/" not in url and "youtu.be/" not in url:
        await update.message.reply_text("That doesn't look like a YouTube link. Please try again!")
        return

    processing_message = await context.bot.send_message(
        chat_id=chat_id,
        text="🔗 Got it! Processing your link..."
    )

    try:
        yt = YouTube(url, use_po_token=True)
        # OR, as the error suggests, use the 'po' token, though use_oauth is often the standard fix:
        # yt = YouTube(url, use_po_token=True)
        
        # --- Download Audio Into Memory ---
        audio_stream = yt.streams.get_audio_only()
        if not audio_stream:
            await context.bot.edit_message_text(
                "❌ Sorry, I couldn't find an audio stream for this video.",
                chat_id=chat_id,
                message_id=processing_message.message_id
            )
            return

        await context.bot.edit_message_text(
            text=f"📥 **Downloading:**\n_{yt.title}_",
            chat_id=chat_id,
            message_id=processing_message.message_id,
            parse_mode='Markdown'
        )

        # Create an in-memory buffer (a virtual file in RAM)
        buffer = io.BytesIO()
        audio_stream.stream_to_buffer(buffer)
        # Reset the buffer's position to the beginning for reading
        buffer.seek(0)

        # --- Send Audio to Telegram ---
        await context.bot.edit_message_text(
            text="⬆️ Uploading to Telegram...",
            chat_id=chat_id,
            message_id=processing_message.message_id
        )

        await context.bot.send_audio(
            chat_id=chat_id,
            audio=buffer, # Pass the in-memory buffer directly
            title=yt.title,
            filename=f"{yt.title}.mp3", # Set the filename for the user
            performer=yt.author,
            duration=yt.length,
            thumbnail=yt.thumbnail_url
        )
        
        await context.bot.delete_message(chat_id=chat_id, message_id=processing_message.message_id)

    except Exception as e:
        print(f"Error processing {url}: {e}")
        await context.bot.edit_message_text(
            text=f"{e}",
            chat_id=chat_id,
            message_id=processing_message.message_id,
            parse_mode='Markdown'
        )


def main() -> None:
    """Starts the bot."""
    print("Bot is starting...")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_youtube_link))

    print("Bot is running. Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == '__main__':
    main()