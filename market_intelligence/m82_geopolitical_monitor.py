import os
import requests

def get_market_data(function):
    key = os.getenv('ALPHA_VANTAGE_KEY')
    url = f"https://www.alphavantage.co/query?function={function}&apikey={key}"
    try:
        r = requests.get(url).json()
        return r.get('data', [{}])[0].get('value', 'N/A')
    except:
        return "N/A"

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

if __name__ == "__main__":
    oil = get_market_data("BRENT")
    gold = get_market_data("GOLD")
    
    report = (
        "🏛️ **M82 TEST: OPERACIÓN COMMODITIES**\n\n"
        f"🛢️ **Brent:** ${oil} USD\n"
        f"✨ **Oro:** ${gold} USD/oz\n\n"
        "✅ **Status:** Prueba de integridad completada.\n"
        "Gobernanza: **Molina Holdings LLC**"
    )
    send_to_chairman(report)
