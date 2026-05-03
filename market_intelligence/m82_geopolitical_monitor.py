import os
import requests
import time

def get_data(function, symbol=None):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    if symbol:
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey={key}"
    else:
        url = f"https://www.alphavantage.co/query?function={function}&apikey={key}"
    
    try:
        # Reducción de latencia al mínimo seguro (0.8s)
        time.sleep(0.8) 
        r = requests.get(url).json()
        if symbol:
            val = r.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate', 'N/A')
            return f"{float(val):,.0f}" if val != 'N/A' else 'N/A'
        data = r.get('data', [{}])
        return data[0].get('value', 'N/A') if data else 'N/A'
    except:
        return "N/A"

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Commodities
    oil, gas = get_data("BRENT"), get_data("NATURAL_GAS")
    gold, silver = get_data("GOLD"), get_data("SILVER")
    copper = get_data("COPPER")
    
    # Cripto (Redondeado para lectura rápida)
    btc, eth, sol = get_data(None, "BTC"), get_data(None, "ETH"), get_data(None, "SOL")

    report = (
        "🏛️ **M82 RAPID INTEL**\n\n"
        f"🛢️ **Brent:** \${oil} | **Gas:** \${gas}\n"
        f"✨ **Oro:** \${gold} | **Plata:** \${silver}\n"
        f"⚒️ **Cobre:** \${copper}\n\n"
        f"🟠 **BTC:** \${btc}\n"
        f"🔹 **ETH:** \${eth}\n"
        f"🟣 **SOL:** \${sol}\n\n"
        "⚡ *Molina Holdings: High-Speed Mode*"
    )
    send_intel(report)
