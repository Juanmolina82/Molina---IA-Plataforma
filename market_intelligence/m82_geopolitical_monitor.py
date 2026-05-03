import os
import requests
import time

def get_market_data(function, symbol=None):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    # Diferenciamos entre Commodities y Cripto
    if symbol:
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey={key}"
    else:
        url = f"https://www.alphavantage.co/query?function={function}&apikey={key}"
    
    try:
        time.sleep(1) # Pausa técnica para evitar saturar la API
        r = requests.get(url).json()
        if symbol:
            return r.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate', 'N/A')[:9]
        return r.get('data', [{}])[0].get('value', 'N/A')
    except:
        return "N/A"

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Commodities
    oil = get_market_data("BRENT")
    gold = get_market_data("GOLD")
    
    # Criptoactivos
    btc = get_market_data(None, "BTC")
    eth = get_market_data(None, "ETH")
    sol = get_market_data(None, "SOL")
    
    report = (
        "🏛️ **M82 GLOBAL ASSET MONITOR**\n\n"
        "📈 **Commodities:**\n"
        f"🛢️ Brent: \${oil} USD\n"
        f"✨ Oro: \${gold} USD/oz\n\n"
        "₿ **Digital Assets:**\n"
        f"🟠 Bitcoin: \${btc} USD\n"
        f"🔹 Ethereum: \${eth} USD\n"
        f"🟣 Solana: \${sol} USD\n\n"
        "✅ **Molina Holdings LLC:** Vigilancia Total Activa."
    )
    send_to_chairman(report)
