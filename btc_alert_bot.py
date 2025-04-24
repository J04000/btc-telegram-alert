import asyncio
import requests
from telegram import Bot

TOKEN = "7757204285:AAH1cKohAVRBcIHEEV7h7bCLnefn5hNyk44"
CHAT_ID = "7743912374"
CHECK_INTERVAL = 300  # 5 minutos
THRESHOLD = 1200

bot = Bot(token=TOKEN)

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")
    data = response.json()
    return data["bitcoin"]["usd"]

def get_price_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1&interval=hourly"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")
    data = response.json()
    return [p[1] for p in data["prices"]]

def analyze_trend():
    prices = get_price_history()
    if len(prices) < 5:
        return "Dados insuficientes para análise."
    media = sum(prices[-5:]) / 5
    atual = prices[-1]
    if atual > media:
        return "Tendência de ALTA - possível momento de compra."
    elif atual < media:
        return "Tendência de BAIXA - possível recuada no preço."
    return "Sem tendência clara."

async def send_alert(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def monitor():
    last_price = get_btc_price()
    trend = analyze_trend()  # Obter a tendência inicial
    await send_alert(f"Monitoramento iniciado: ${last_price:.2f}\n{trend}")
    
    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        try:
            current_price = get_btc_price()
            trend = analyze_trend()  # Atualizar a tendência antes de enviar a alerta
            diff = current_price - last_price
            if abs(diff) >= THRESHOLD:
                direction = "subiu" if diff > 0 else "caiu"
                await send_alert(
                    f"O Bitcoin {direction} ${abs(diff):.2f} e está em ${current_price:.2f}\n{trend}"
                )
                last_price = current_price
        except Exception as e:
            await send_alert(f"Erro: {e}")

if __name__ == "__main__":
    asyncio.run(monitor())
