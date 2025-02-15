import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("سلام! لطفاً شماره تلفن خود را وارد کنید.")

async def get_api_id(update: Update, context: CallbackContext) -> None:
    # شماره تلفن از پیام دریافتی
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

async def main():
    bot_token = "8068187481:AAH7YdFS2s0A5NltxtHMG25XSJmzgeeyumQ"

    # به جای Updater از Application استفاده می‌کنیم
    application = Application.builder().token(bot_token).build()

    # فرمان ها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_api_id", get_api_id))
    application.add_handler(CommandHandler("get_api_hash", get_api_hash))

    # شروع ربات
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
