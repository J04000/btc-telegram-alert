import requests
import time
import logging
from telegram import Bot

# Configurações do bot
TOKEN = "7757204285:AAH1cKohAVRBcIHEEV7h7bCLnefn5hNyk44"
CHAT_ID = "7743912374"  # Você precisa substituir isso pelo seu ID real
INTERVAL = 180  # 3 minutos
THRESHOLD = 1200  # 1200 USDT

bot = Bot(token=TOKEN)
last_price = None

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    return float(response.json()["price"])

def send_alert(current_price, diff):
    direction = "subiu" if diff > 0 else "caiu"
    bot.send_message(chat_id=CHAT_ID, text=f"O Bitcoin {direction} ${abs(diff):.2f} e está valendo agora ${current_price:.2f}")

def main():
    global last_price
    while True:
        try:
            price = get_btc_price()
            if last_price is None:
                last_price = price
            elif abs(price - last_price) >= THRESHOLD:
                send_alert(price, price - last_price)
                last_price = price
        except Exception as e:
            logging.error(f"Erro: {e}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
