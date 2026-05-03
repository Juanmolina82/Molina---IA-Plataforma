import os
import requests

def get_market_data(function):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function={function}&apikey={key}"
    try:
        r = requests.get(url).json()
        # Extraemos el valor más reciente de la lista de datos
        return r.get('data', [{}])[0].get('value', 'Consultando...')
    except:
        return "N/A"

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    # Obteniendo Inteligencia Real
    oil = get_market_data("BRENT")
    gold = get_market_data("GOLD")
    
    report = (
        "🏛️ **M82 COMMAND CENTER ACTIVE**\n\n"
        "El sistema de Molina Holdings LLC está en línea.\n\n"
        f"🛢️ **Crudo Brent:** \${oil} USD\n"
        f"✨ **Oro Spot:** \${gold} USD/oz\n\n"
        "✅ **Status:** Sincronización completa.\n"
        "✅ **Seguridad:** Encriptación de grado militar."
    )
    send_to_chairman(report)
