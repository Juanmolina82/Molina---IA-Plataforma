import os
import requests
import time
from pyfinviz.news import News

def get_finviz_intel():
    try:
        news_client = News()
        headlines = news_client.news_df.head(8)['Headline'].tolist()
        
        # Filtro de Alerta Roja
        keywords = ["CRASH", "BREAKING", "EMERGENCY", "HALT", "COLLAPSE", "FED ALERT"]
        alerts = []
        clean_news = []
        
        for h in headlines:
            if any(word in h.upper() for word in keywords):
                alerts.append(f"🚨 **{h}**")
            else:
                clean_news.append(f"• {h}")
        
        return alerts, clean_news[:5]
    except:
        return [], ["⚠️ Finviz: Servicio offline."]

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
    spy = get_data("SPY")
    alerts, news = get_finviz_intel()
    
    # Construcción del reporte con jerarquía de importancia
    alert_block = "\n".join(alerts) + "\n\n" if alerts else ""
    news_block = "\n".join(news)
    
    header = "🔴 **M82 EMERGENCY BROADCAST**\n\n" if alerts else "🏛️ **M82 FINVIZ INTELLIGENCE**\n\n"
    
    report = (
        f"{header}"
        f"{alert_block}"
        f"📈 **Market Status:** SPY {spy}\n\n"
        "📰 **Global Headlines:**\n"
        f"{news_block}\n\n"
        "⚡ *Molina Holdings: Black Swan Protocol Active*"
    )
    send_intel(report)
