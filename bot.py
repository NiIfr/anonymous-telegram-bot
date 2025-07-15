from telegram.ext import Updater, MessageHandler, Filters
import os, re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

def escape_markdown(text):
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)

def handle_all_messages(update, context):
    message = update.message
    user = message.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name or "ناشناس"

    if message.text and message.text.strip() == '/start':
        message.reply_text("سلام! خوش اومدی. هر سوال، پیام یا عکس داری اینجا بفرست.")
        return

    sent_msg = None

    if message.text:
        sent_msg = context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"پیام ناشناس شما 💌 :\n\n{message.text}")
        message.reply_text("✅ پیامت دریافت شد @niloofarvafaei")

    elif message.photo:
        file_id = message.photo[-1].file_id
        caption = escape_markdown(message.caption) if message.caption else None
        sent_msg = context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=file_id, caption=caption, parse_mode="MarkdownV2")
        message.reply_text("✅ عکست دریافت شد @niloofarvafaei")

    elif message.voice:
        file_id = message.voice.file_id
        caption = escape_markdown(message.caption) if message.caption else None
        sent_msg = context.bot.send_voice(chat_id=ADMIN_CHAT_ID, voice=file_id, caption=caption, parse_mode="MarkdownV2")
        message.reply_text("✅ ویس دریافت شد @niloofarvafaei")

    elif message.video:
        file_id = message.video.file_id
        caption = escape_markdown(message.caption) if message.caption else None
        sent_msg = context.bot.send_video(chat_id=ADMIN_CHAT_ID, video=file_id, caption=caption, parse_mode="MarkdownV2")
        message.reply_text("✅ ویدیو دریافت شد @niloofarvafaei")

    else:
        message.reply_text("❌ این نوع پیام پشتیبانی نمی‌شود.")
        return

    user_info = f"👤 مشخصات فرستنده:\n"
    user_info += f"▪️ نام: {escape_markdown(first_name)}\n"
    user_info += f"▪️ آیدی عددی: `{user_id}`\n"

    if username:
        user_info += f"▪️ یوزرنیم: @{escape_markdown(username)}\n"
        user_info += f"📬 [باز کردن چت](https://t.me/{escape_markdown(username)})"
    else:
        user_info += "⚠️ کاربر یوزرنیم ندارد."

    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=user_info,
        parse_mode="MarkdownV2",
        reply_to_message_id=sent_msg.message_id if sent_msg else None
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all, handle_all_messages))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
