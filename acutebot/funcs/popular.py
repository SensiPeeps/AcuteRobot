from telegram.ext import CommandHandler
from acutebot import dp

def popular(update, context):
    context.bot.sendMessage(update.effective_chat.id, "This feature is currently in devlopment...")

dp.add_handler(CommandHandler("popular", popular))
