import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# تنظیمات لاگ برای خطایابی
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دستورات ربات
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("سلام! لطفاً شماره تلفن خود را وارد کنید.")

async def get_api_id(update: Update, context: CallbackContext) -> None:
    phone_number = update.message.text.strip()
    telegram_app = TelegramApplication(phone_number)

    if telegram_app.send_password():
        await update.message.reply_text("پسورد به شماره شما ارسال شد. لطفاً پسورد را وارد کنید.")

    context.user_data['telegram_app'] = telegram_app

async def get_api_hash(update: Update, context: CallbackContext) -> None:
    cloud_password = update.message.text.strip()
    telegram_app = context.user_data.get('telegram_app')

    if telegram_app and telegram_app.auth_login(cloud_password):
        api_id, api_hash = telegram_app.auth_app()
        await update.message.reply_text(f"API ID: {api_id}\nAPI HASH: {api_hash}")
    else:
        await update.message.reply_text("لطفاً ابتدا شماره تلفن و پسورد را وارد کنید.")

# تابع اصلی برای شروع ربات
async def main():
    bot_token = "8068187481:AAH7YdFS2s0A5NltxtHMG25XSJmzgeeyumQ"

    # ایجاد یک شی از Application
    application = Application.builder().token(bot_token).build()

    # فرمان‌ها را اضافه می‌کنیم
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_api_id", get_api_id))
    application.add_handler(CommandHandler("get_api_hash", get_api_hash))

    # شروع ربات
    logger.info("Bot started.")
    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())  # استفاده از asyncio.run برای اجرای برنامه
    except RuntimeError:  # Catching already running event loop error
        loop = asyncio.get_event_loop()
        loop.create_task(main())  # Use the existing event loop
