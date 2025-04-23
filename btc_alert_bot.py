import requests
import time
import telegram

TOKEN = "7757204285:AAH1cKohAVRBcIHEEV7h7bCLnefn5hNyk44"
CHAT_ID = "7743912374"
CHECK_INTERVAL = 180  # 3 minutos em segundos
THRESHOLD = 1200  # Alerta a cada variação de $1200

bot = telegram.Bot(token=TOKEN)

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data["bitcoin"]["usd"]

def send_alert(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    last_price = get_btc_price()
    send_alert(f"Monitoramento iniciado. Preço atual do BTC: ${last_price}")

    while True:
        time.sleep(CHECK_INTERVAL)
        try:
            current_price = get_btc_price()
            diff = abs(current_price - last_price)

            if diff >= THRESHOLD:
                direction = "subiu" if current_price > last_price else "caiu"
                send_alert(f"O Bitcoin {direction} ${diff:.2f} e está em ${current_price:.2f}")
                last_price = current_price
        except Exception as e:
            send_alert("Erro ao verificar o preço do Bitcoin.")

if __name__ == "__main__":
    main()
