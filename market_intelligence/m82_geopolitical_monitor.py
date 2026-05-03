import os
import requests
import time
from datetime import datetime

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

def get_sector_performance():
    # Identifica el sector líder del día
    sectors = {"XLK": "Tecnología", "XLE": "Energía", "XLF": "Finanzas", "XLV": "Salud", "XLY": "Consumo"}
    leader = "N/A"
    max_gain = -99.0
    for sym, name in sectors.items():
        data = get_data(sym)
        if "(" in data:
            pct = float(data.split("(")[1].replace("%)", "").replace("%", ""))
            if pct > max_gain:
                max_gain = pct
                leader = f"{name} ({pct}%)"
    return leader

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    now = datetime.now().hour
    
    # Core Data
    spy, qqq = get_data("SPY"), get_data("QQQ")
    t10y_url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=10year&apikey={os.getenv('ALPHA_VANTAGE_KEY')}"
    t10y = requests.get(t10y_url).json().get('data', [{}])[0].get('value', 'N/A')

    # Especial de Cierre (4 PM NY -> Aprox 20:00/21:00 UTC)
    sector_info = ""
    if 20 <= now <= 22:
        leader = get_sector_performance()
        sector_info = f"\n🏆 **Sector Ganador del Día:** {leader}\n"

    report = (
        "🏛️ **M82 ASSET MATRIX**\n\n"
        f"📈 **Indices:** SPY {spy} | QQQ {qqq}\n"
        f"🏦 **Rates:** US 10Y Yield: {t10y}%\n"
        f"{sector_info}\n"
        "🐋 *LSEG Order Flow: Monitor activo.*\n"
        "⚡ *Molina Holdings: Full Cycle Control*"
    )
    send_intel(report)
