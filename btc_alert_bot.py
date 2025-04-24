def get_price_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1&interval=hourly"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro na API de histórico: {response.status_code} - {response.text}")
    data = response.json()
    if "prices" not in data or not data["prices"]:
        raise Exception(f"Resposta inesperada da API de histórico: {data}")
    prices = [p[1] for p in data["prices"]]
    return prices
