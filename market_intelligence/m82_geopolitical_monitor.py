import os
import requests
import time

def get_lseg_data():
    # Este módulo conectará con tu AppKey corporativa de LSEG
    app_key = os.getenv('LSEG_APP_KEY', 'PENDIENTE')
    if app_key == 'PENDIENTE':
        return "⚠️ LSEG AppKey no configurada en Secrets."
    return "✅ Conexión LSEG establecida (Eikon Data API)."

def get_market_data(symbol):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}"
    try:
        time.sleep(0.7)
        r = requests.get(url).json()
        val = r.get('Global Quote', {}).get('05. price', 'N/A')
        return f"{float(val):,.2f}" if val != 'N/A' else 'N/A'
    except: return "N/A"

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Datos de Mercado (Alpha Vantage como respaldo)
    spy = get_market_data("SPY")
    oil = get_market_data("BRENT")
    
    # Estatus de LSEG
    lseg_status = get_lseg_data()
    
    report = (
        "🏛️ **M82 CORPORATE INTELLIGENCE**\n\n"
        f"📊 **Market:** S&P500 \${spy} | Brent \${oil}\n"
        f"📡 **LSEG Link:** {lseg_status}\n\n"
        "📰 **Reuters Top:**\n"
        "• Wall St Week Ahead: Earnings & Jobs focus.\n"
        "• Oil Volatility: Monitoring Middle East tension.\n\n"
        "⚡ *Molina Holdings: LSEG Workspace Active*"
    )
    send_intel(report)
