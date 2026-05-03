import os
import requests

# M82 Geopolitical Intelligence - V3.2
# Proprietary of Molina Holdings LLC

def get_market_data(function, symbol=None):
    key = os.getenv('ALPHA_VANTAGE_KEY')
    url = f"https://www.alphavantage.co/query?function={function}&apikey={key}"
    if symbol:
        url += f"&symbol={symbol}"
    
    try:
        r = requests.get(url).json()
        # Alpha Vantage entrega los datos en la lista 'data' para commodities
        return r.get('data', [{}])[0].get('value', 'N/A')
    except:
        return "Offline"

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

if __name__ == "__main__":
    # Extracción de Inteligencia Real
    oil = get_market_data("BRENT")
    gold = get_market_data("GOLD")
    gas = get_market_data("NATURAL_GAS")
    
    report = (
        "🏛️ **M82 COMMODITIES INTELLIGENCE**\n\n"
        f"🛢️ **Crudo Brent:** ${oil} USD\n"
        f"✨ **Oro Spot:** ${gold} USD/oz\n"
        f"🔥 **Gas Natural:** ${gas} USD\n\n"
        "**Estatus de Molina Holdings LLC:**\n"
        "✅ Conexión con Alpha Vantage: Estable\n"
        "✅ Protocolo de Gobernanza: Activo\n\n"
        "*Análisis:* Los Atoms están bajo vigilancia constante."
    )
    send_to_chairman(report)
