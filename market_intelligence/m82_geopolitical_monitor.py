import os
import requests
import time
from pyfinviz.news import News

def get_finviz_intel():
    try:
        # Extraemos las noticias globales (Market News)
        news_client = News()
        # Tomamos los primeros 5 titulares del DataFrame de noticias
        headlines = news_client.news_df.head(5)['Headline'].tolist()
        formatted_news = "\n".join([f"• {h}" for h in headlines])
        return formatted_news
    except Exception as e:
        return "⚠️ Finviz News: Temporalmente indisponible."

def get_data(symbol):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}"
    try:
        time.sleep(0.7)
        r = requests.get(url).json()
        quote = r.get('Global Quote', {})
        price = quote.get('05. price', 'N/A')
        change = quote.get('10. change percent', '0%')
        return f"${float(price):,.2f} ({change})" if price != 'N/A' else "N/A"
    except: return "N/A"

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Datos Core
    spy = get_data("SPY")
    
    # Inteligencia de Finviz
    finviz_news = get_finviz_intel()
    
    report = (
        "🏛️ **M82 FINVIZ INTELLIGENCE**\n\n"
        f"📈 **Market Status:** SPY {spy}\n\n"
        "📰 **Finviz Global Headlines:**\n"
        f"{finviz_news}\n\n"
        "🐋 *LSEG Order Flow: Monitor activo.*\n"
        "⚡ *Molina Holdings: Full System Integrated*"
    )
    send_intel(report)
