import json
import requests
from lxml import html
from fake_useragent import FakeUserAgent
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

fake_useragent = FakeUserAgent()

# کلاسی که تلگرام رو مدیریت می‌کنه
class TelegramApplication:
    def __init__(self, phone_number: str, app_title: str = "", app_shortname: str = "", app_url: str = "", app_platform: str = "desktop", app_desc: str = "", random_hash: str = None, stel_token: str = None, useragent: str = fake_useragent.random) -> None:
        self.phone_number = phone_number
        self.app_title = app_title
        self.app_shortname = app_shortname
        self.app_url = app_url
        self.app_platform = app_platform
        self.app_desc = app_desc
        self.random_hash = random_hash
        self.stel_token = stel_token
        self.useragent = useragent

    def send_password(self) -> bool:
        try:
            response = requests.post(
                url="https://my.telegram.org/auth/send_password",
                data="phone={0}".format(self.phone_number),
                headers={
                    "Origin": "https://my.telegram.org",
                    "User-Agent": self.useragent,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "application/json"
                })
            
            get_json = json.loads(response.content)
            self.random_hash = get_json["random_hash"]
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def auth_login(self, cloud_password: str) -> bool:
        try:
            responses = requests.post(
                url="https://my.telegram.org/auth/login",
                data="phone={0}&random_hash={1}&password={2}".format(self.phone_number, self.random_hash, cloud_password),
                headers={
                    "Origin": "https://my.telegram.org",
                    "User-Agent": self.useragent,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "application/json"
                }
            )
            self.stel_token = responses.cookies['stel_token']
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def auth_app(self) -> tuple:
        try:
            resp = requests.get(
                url="https://my.telegram.org/apps",
                headers={
                    "Cookie": "stel_token={0}".format(self.stel_token),
                    "User-Agent": self.useragent,
                }
            )
            tree = html.fromstring(resp.content)
            api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
            return api[0], api[1]
        except Exception as e:
            print(f"Error: {e}")
            return False


# تعریف فرمان های ربات تلگرام
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("سلام! لطفاً شماره تلفن خود را وارد کنید.")

def get_api_id(update: Update, context: CallbackContext) -> None:
    try:
        # شماره تلفن از پیام دریافتی
        phone_number = update.message.text.strip()

        # ساخت یک شی از کلاس TelegramApplication
        telegram_app = TelegramApplication(phone_number)

        if telegram_app.send_password():
            update.message.reply_text("پسورد به شماره شما ارسال شد. لطفاً پسورد را وارد کنید.")

        context.user_data['telegram_app'] = telegram_app
    except Exception as e:
        update.message.reply_text(f"خطا: {e}")

def get_api_hash(update: Update, context: CallbackContext) -> None:
    try:
        cloud_password = update.message.text.strip()
        telegram_app = context.user_data.get('telegram_app')

        if telegram_app and telegram_app.auth_login(cloud_password):
            api_id, api_hash = telegram_app.auth_app()
            update.message.reply_text(f"API ID: {api_id}\nAPI HASH: {api_hash}")
        else:
            update.message.reply_text("لطفاً ابتدا شماره تلفن و پسورد را وارد کنید.")
    except Exception as e:
        update.message.reply_text(f"خطا: {e}")

def main():
    # توکن ربات تلگرام خود را وارد کنید
    bot_token = "8068187481:AAH7YdFS2s0A5NltxtHMG25XSJmzgeeyumQ"

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    # فرمان ها
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("get_api_id", get_api_id))
    dispatcher.add_handler(CommandHandler("get_api_hash", get_api_hash))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
