import requests
import time
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread

TOKEN = "7757204285:AAH1cKohAVRBcIHEEV7h7bCLnefn5hNyk44"
CHAT_ID = "7743912374"
bot = Bot(token=TOKEN)

CHECK_INTERVAL = 180  # 3 minutos
THRESHOLD = 1200

logging.basicConfig(level=logging.INFO)

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    try:
        data = response.json()
        price = data.get("bitcoin", {}).get("usd")
        if price is None:
            raise ValueError("Preço do Bitcoin não encontrado.")
        return price
    except Exception as e:
        print("Erro ao obter o preço do BTC:", e)
        raise

def get_price_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1&interval=hourly"
    response = requests.get(url)
    data = response.json()
    return [p[1] for p in data["prices"]]

def analyze_trend():
    prices = get_price_history()
    if len(prices) < 5:
        return "Dados insuficientes para análise."
    current_price = prices[-1]
    moving_average = sum(prices[-5:]) / 5
    if current_price > moving_average:
        return f"Tendência de ALTA — Preço atual: ${current_price:.2f}"
    elif current_price < moving_average:
        return f"Tendência de BAIXA — Preço atual: ${current_price:.2f}"
    else:
        return f"Sem tendência clara — Preço atual: ${current_price:.2f}"

async def analise_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Comando /analise recebido")
    trend = analyze_trend()
    await update.message.reply_text(trend)

def monitor():
    try:
        last_price = get_btc_price()
        bot.send_message(chat_id=CHAT_ID, text=f"Monitoramento iniciado. BTC: ${last_price:.2f}")
    except Exception as e:
        logging.error(f"Erro inicial: {e}")
        return

    while True:
        time.sleep(CHECK_INTERVAL)
        try:
            current_price = get_btc_price()
            diff = abs(current_price - last_price)
            if diff >= THRESHOLD:
                direction = "subiu" if current_price > last_price else "caiu"
                trend = analyze_trend()
                bot.send_message(chat_id=CHAT_ID,
                                 text=f"O Bitcoin {direction} ${diff:.2f} e está em ${current_price:.2f}\n{trend}")
                last_price = current_price
        except Exception as e:
            logging.error(f"Erro no loop: {e}")
            bot.send_message(chat_id=CHAT_ID, text="Erro ao verificar o preço do BTC.")

if __name__ == "__main__":
    Thread(target=monitor).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("analise", analise_handler))
    app.run_polling()
