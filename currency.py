import time
import requests
from config import TOKEN

TG_BOT_URL = f"https://api.telegram.org/bot{TOKEN}"
NBU_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"

# Valyutalar ro‘yxatini oldindan olish
currency_list = requests.get(NBU_URL).json()

def get_currency_by_Ccy(Ccy: str) -> dict | None:
    """Berilgan Ccy kodi bo‘yicha valyutani topadi."""
    for currency in currency_list:
        if currency['Ccy'] == Ccy.upper():
            return currency
    return None


def get_last_update():
    """Telegramdan so‘nggi xabarni oladi."""
    try:
        get_updates_url = f"{TG_BOT_URL}/getUpdates"
        response = requests.get(get_updates_url)
        data = response.json()
        return data['result'][-1]
    except Exception as e:
        print("Xatolik get_last_update() da:", e)
        return None


def send_message(chat_id, text):
    """Foydalanuvchiga xabar yuboradi."""
    try:
        send_message_url = f"{TG_BOT_URL}/sendMessage"
        payload = {'chat_id': chat_id, 'text': text}
        requests.get(send_message_url, params=payload)
    except Exception as e:
        print("Xatolik send_message() da:", e)


def main():
    print("Bot ishga tushdi...")
    last_update_id = None

    while True:
        update = get_last_update()
        if not update:
            time.sleep(3)
            continue

        update_id = update['update_id']
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        if update_id == last_update_id:
            time.sleep(3)
            continue
        last_update_id = update_id

        if text == '/start':
            send_message(chat_id,
                "Assalomu alaykum!\n"
                "Bu bot NBU valyuta kurslarini ko‘rsatadi.\n"
                "Masalan: USD yoki EUR yozing."
            )
        else:
            currency = get_currency_by_Ccy(text)
            if currency:
                msg = (
                    f"Valyuta: {currency['CcyNm_UZ']}\n"
                    f"1 {currency['Ccy']} = {currency['Rate']} so‘m\n"
                    f"So‘nggi yangilanish: {currency['Date']}"
                )
                send_message(chat_id, msg)
            else:
                send_message(chat_id, "Bunday valyuta topilmadi. Masalan: USD yoki EUR yozing.")

        time.sleep(3)


main()