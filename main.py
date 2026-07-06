import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("TOKEN")

def download(url):
    ydl_opts = {'outtmpl': 'video.%(ext)s', 'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for f in os.listdir():
        if f.startswith("video"):
            return f

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Video link gönder.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("İndiriliyor...")

    try:
        file = download(url)
        await update.message.reply_video(video=open(file, "rb"))
        os.remove(file)
    except Exception as e:
        await update.message.reply_text(str(e))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
