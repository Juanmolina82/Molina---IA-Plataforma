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
        time.sleep(1.5) # Pausa de seguridad para el Tridente M82
        r = requests.get(url).json()
        if symbol:
            val = r.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate', 'N/A')
            return f"{float(val):,.2f}" if val != 'N/A' else 'N/A'
        data = r.get('data', [{}])
        val = data[0].get('value', 'N/A') if data else 'N/A'
        return val
    except:
        return "N/A"

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Energía y Metales
    oil = get_data("BRENT")
    gas = get_data("NATURAL_GAS")
    gold = get_data("GOLD")
    silver = get_data("SILVER")
    copper = get_data("COPPER")
    
    # Agricultura (Soft Commodities)
    corn = get_data("CORN")
    wheat = get_data("WHEAT")
    
    # Criptoactivos
    btc = get_data(None, "BTC")
    eth = get_data(None, "ETH")
    sol = get_data(None, "SOL")

    report = (
        "🏛️ **M82 FULL ASSET INTELLIGENCE**\n\n"
        "🔥 **Energía:**\n"
        f"  • Petróleo Brent: \${oil} USD\n"
        f"  • Gas Natural: \${gas} USD\n\n"
        "⚒️ **Metales:**\n"
        f"  • Oro Spot: \${gold} USD\n"
        f"  • Plata: \${silver} USD\n"
        f"  • Cobre: \${copper} USD\n\n"
        "🌾 **Agricultura:**\n"
        f"  • Trigo: \${wheat} USD\n"
        f"  • Maíz: \${corn} USD\n\n"
        "₿ **Criptoactivos:**\n"
        f"  • BTC: \${btc}\n"
        f"  • ETH: \${eth}\n"
        f"  • SOL: \${sol}\n\n"
        "✅ **Gobernanza:** Molina Holdings LLC"
    )
    send_intel(report)
