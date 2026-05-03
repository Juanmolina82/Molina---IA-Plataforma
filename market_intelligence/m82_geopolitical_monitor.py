import os
import requests
import time
import yfinance as yf
from pyfinviz.news import News

def get_realtime_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Obtenemos el precio actual y el cierre anterior para el %
        data = ticker.fast_info
        last_price = data['last_price']
        prev_close = data['previous_close']
        change = ((last_price - prev_close) / prev_close) * 100
        return f"${last_price:,.2f} ({change:+.2f}%)"
    except:
        return "N/A"

def get_treasury_yield():
    # El rendimiento del bono a 10 años también está en yfinance como '^TNX'
    try:
        tnx = yf.Ticker("^TNX")
        yield_val = tnx.fast_info['last_price']
        return f"{yield_val:.2f}%"
    except:
        return "N/A"

def get_finviz_intel():
    try:
        news_client = News()
        headlines = news_client.news_df.head(5)['Headline'].tolist()
        keywords = ["CRASH", "BREAKING", "EMERGENCY", "HALT"]
        alerts = [f"🚨 **{h}**" for h in headlines if any(w in h.upper() for w in keywords)]
        news = [f"• {h}" for h in headlines if not any(w in h.upper() for w in keywords)]
        return alerts, news[:5]
    except:
        return [], ["⚠️ Finviz: Standby."]

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Extracción masiva sin bloqueos (yfinance)
    spy = get_realtime_data("SPY")
    qqq = get_realtime_data("QQQ")
    dia = get_realtime_data("DIA")
    tlt = get_realtime_data("TLT")
    gold = get_realtime_data("GLD")
    oil = get_realtime_data("USO")
    t10y = get_treasury_yield()
    
    alerts, news = get_finviz_intel()
    alert_block = "\n".join(alerts) + "\n\n" if alerts else ""
    
    report = (
        f"{'🔴 **M82 EMERGENCY ALERT**' if alerts else '🏛️ **M82 ASSET MATRIX**'}\n\n"
        f"{alert_block}"
        "📈 **Equities & Indices:**\n"
        f"  • SPY: {spy} | QQQ: {qqq} | DIA: {dia}\n\n"
        "🏦 **Fixed Income:**\n"
        f"  • US 10Y Yield: {t10y} | TLT: {tlt}\n\n"
        "🛡️ **Strategic ETFs:**\n"
        f"  • Gold: {gold} | Crude: {oil}\n\n"
        "📰 **Finviz Feed:**\n"
        f"{'| '.join(news[:3])}\n\n"
        "⚡ *Molina Holdings: yFinance Hybrid Active*"
    )
    send_intel(report)
