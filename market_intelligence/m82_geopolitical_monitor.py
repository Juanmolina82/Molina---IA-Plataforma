import os
import requests
import time
import xml.etree.ElementTree as ET

def get_data(function, symbol=None):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function={'GLOBAL_QUOTE' if symbol else function}&{f'symbol={symbol}' if symbol else ''}&apikey={key}"
    try:
        time.sleep(0.7)
        r = requests.get(url).json()
        if symbol:
            val = r.get('Global Quote', {}).get('05. price', 'N/A')
            return f"{float(val):,.2f}" if val != 'N/A' else 'N/A'
        data = r.get('data', [{}])
        return data[0].get('value', 'N/A') if data else 'N/A'
    except: return "N/A"

def get_crypto(symbol):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey={key}"
    try:
        time.sleep(0.7)
        r = requests.get(url).json()
        val = r.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate', 'N/A')
        return f"{float(val):,.0f}" if val != 'N/A' else 'N/A'
    except: return "N/A"

def get_reuters_news():
    try:
        # Feed de noticias globales de Reuters
        r = requests.get("https://www.reutersagency.com/feed/?best-topics=political-geopolitics&post_type=best")
        root = ET.fromstring(r.content)
        news = ""
        for item in root.findall('./channel/item')[:3]: # Los 3 titulares más recientes
            title = item.find('title').text
            news += f"• {title}\n"
        return news if news else "Sin noticias recientes."
    except: return "Servicio de noticias temporalmente offline."

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Datos de Mercado
    spy, qqq = get_data(None, "SPY"), get_data(None, "QQQ")
    oil, gold = get_data("BRENT"), get_data("GOLD")
    btc = get_crypto("BTC")
    
    # Noticias Reuters
    news = get_reuters_news()

    report = (
        "🏛️ **M82 COMMANDER BRIEFING & REUTERS**\n\n"
        "📊 **Mercados:**\n"
        f"  • S&P500: \${spy} | Nasdaq: \${qqq}\n"
        f"  • Brent: \${oil} | Oro: \${gold}\n"
        f"  • BTC: \${btc} USD\n\n"
        "📰 **Reuters Geopolitics:**\n"
        f"{news}\n"
        "⚡ *Molina Holdings: Global Intelligence*"
    )
    send_intel(report)
