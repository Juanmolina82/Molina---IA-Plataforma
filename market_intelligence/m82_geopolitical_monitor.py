import os
import requests
import time

def get_order_flow_logic(symbol):
    # Una vez vinculado LSEG, aquí procesaremos el 'Real-time Order Flow'
    # Por ahora, mantenemos el placeholder de inteligencia
    return "ANALIZANDO FLUJO LSEG..."

def get_data(symbol):
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
    # Activos Clave para Order Flow
    spy_price = get_data("SPY")
    qqq_price = get_data("QQQ")
    
    # Sección de Order Flow (Placeholder hasta AppKey)
    flow_spy = "Institutional Accumulation: HIGH (LSEG Data Pending)"
    flow_qqq = "Retail Sentiment: BEARISH (LSEG Data Pending)"

    report = (
        "🏛️ **M82 ORDER FLOW INTELLIGENCE**\n\n"
        "📊 **Snapshot de Mercado:**\n"
        f"  • S&P 500: \${spy_price}\n"
        f"  • Nasdaq: \${qqq_price}\n\n"
        "🐋 **Institutional Flow (LSEG Analysis):**\n"
        f"  • SPY Flow: {flow_spy}\n"
        f"  • QQQ Flow: {flow_qqq}\n\n"
        "⚠️ **Insight:** Seguimiento de flujos de órdenes institucionales activos. Esperando vinculación LSEG Workspace para precisión 1:1.\n\n"
        "⚡ *Molina Holdings: Transparency Era*"
    )
    send_intel(report)
