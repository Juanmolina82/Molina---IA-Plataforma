import os
import requests
import time

def get_market_data(function):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function={function}&apikey={key}"
    for _ in range(3):  # Reintento inteligente
        try:
            r = requests.get(url).json()
            val = r.get('data', [{}])[0].get('value', 'N/A')
            if val != 'N/A': return val
            time.sleep(2)
        except:
            continue
    return "Estable"

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    oil = get_market_data("BRENT")
    gold = get_market_data("GOLD")
    
    report = (
        "🏛️ **M82 ASSET MONITOR**\n\n"
        f"🛢️ **Brent Oil:** \${oil} USD\n"
        f"✨ **Gold Spot:** \${gold} USD/oz\n\n"
        "✅ **Molina Holdings LLC:** Vigilancia Activa."
    )
    send_to_chairman(report)
