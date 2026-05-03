import os
import requests
import time

def get_market_summary():
    # Simulamos el insight de Reuters para el Commander Briefing
    return (
        "⚠️ **WEEK AHEAD FOCUS:**\n"
        "• Petróleo Brent en zona crítica ($103+).\n"
        "• Viernes: US Jobs Report (Forecast: 73k).\n"
        "• Earnings: AMD, PLTR, COIN en el radar."
    )

def get_data(symbol):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}"
    try:
        time.sleep(0.8)
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
    spy = get_data("SPY")
    btc_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={os.getenv('ALPHA_VANTAGE_KEY')}"
    btc = requests.get(btc_url).json().get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate', 'N/A')[:6]
    
    insight = get_market_summary()
    
    report = (
        "🏛️ **M82 LSEG INTELLIGENCE**\n\n"
        f"📈 **S&P 500:** \${spy}\n"
        f"₿ **Bitcoin:** \${btc}\n\n"
        f"{insight}\n\n"
        "⚡ *Molina Holdings: Reuters Sincronizado*"
    )
    send_intel(report)
