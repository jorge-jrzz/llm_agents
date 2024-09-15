from datetime import datetime
import telebot
import os
from src import YouTube, Video


API_TOKEN = '7457112221:AAFF_tTrlpRE-XzKOr6FYW_00DCt8GKctsY'

bot = telebot.TeleBot(API_TOKEN)

yt = YouTube()
vi = Video()
summarize_yt_video = False
summarize_video = False


def download_video(message: telebot.types.Message, dst_path: str) -> None:
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(dst_path, 'wb') as new_file:
        new_file.write(downloaded_file)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hola, soy un bot para probrar los desarrollos de ajgentes de IA. 🫦")

@bot.message_handler(commands=['youtube'])
def command_youtube_video(message):
    global summarize_yt_video
    bot.reply_to(message, "Dame el link 🔗 de un video de YouTube y te daré el resumen.")
    summarize_yt_video = True


@bot.message_handler(commands=['video'])
def command_file_video(message):
    global summarize_video
    bot.reply_to(message, "Dame el archivo 🎞️ de video y te daré el resumen.")
    summarize_video = True

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global summarize_yt_video
    if summarize_yt_video:
        if message.text.startswith("https://youtu.be/") or message.text.startswith("https://www.youtube.com/"):
            bot.reply_to(message, "Procesando video de YouTube...")
            try:
                summary = yt.generate_summary(message.text)
                bot.reply_to(message, "Resumen del video de YouTube.\n" + summary)
            except Exception:
                bot.reply_to(message, "Error al procesar el video de YouTube.")
        else:
            bot.reply_to(message, "No es un link de YouTube.")
        summarize_yt_video = False
    else:
        bot.reply_to(message, message.text)

# Handles all sent documents and audio files
@bot.message_handler(content_types='video') # list relevant content types
def summarize_file_video(message):
    global summarize_video
    if summarize_video:
        bot.reply_to(message, "Procesando video...")
        try:
            date = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
            video_path = f"./videos/{date}-{message.video.file_name}"
            download_video(message, video_path)
            summary = vi.generate_sumary(video_path, f"./audios/{date}-{message.video.file_name}.mp3")
            bot.reply_to(message, "Resumen del video.\n" + summary)
        except Exception:
            bot.reply_to(message, "Error al procesar el video.")
        summarize_video = False
    else:
        bot.reply_to(message, "No esperaba un archivo de video.")


bot.infinity_polling()
