import os
import requests
import time

def get_data(function, symbol=None):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    if symbol:
        # Usamos GLOBAL_QUOTE para acciones/ETFs de índices
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}"
    else:
        url = f"https://www.alphavantage.co/query?function={function}&apikey={key}"
    
    try:
        time.sleep(0.7) # Velocidad máxima optimizada
        r = requests.get(url).json()
        if symbol:
            val = r.get('Global Quote', {}).get('05. price', 'N/A')
            return f"{float(val):,.2f}" if val != 'N/A' else 'N/A'
        data = r.get('data', [{}])
        return data[0].get('value', 'N/A') if data else 'N/A'
    except:
        return "N/A"

def get_crypto(symbol):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey={key}"
    try:
        time.sleep(0.7)
        r = requests.get(url).json()
        val = r.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate', 'N/A')
        return f"{float(val):,.0f}" if val != 'N/A' else 'N/A'
    except:
        return "N/A"

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # Índices (vía ETFs principales)
    spy = get_data(None, "SPY")
    qqq = get_data(None, "QQQ")
    
    # Commodities & Futuros
    oil = get_data("BRENT")
    gold = get_data("GOLD")
    gas = get_data("NATURAL_GAS")
    
    # Cripto
    btc = get_crypto("BTC")
    eth = get_crypto("ETH")

    report = (
        "🏛️ **M82 COMMANDER BRIEFING**\n\n"
        "📊 **Índices de Mercado:**\n"
        f"  • S&P 500 (SPY): \${spy}\n"
        f"  • Nasdaq (QQQ): \${qqq}\n\n"
        "🛢️ **Commodities & Futures:**\n"
        f"  • Oil Brent: \${oil} | Gas: \${gas}\n"
        f"  • Oro Spot: \${gold} USD\n\n"
        "₿ **Digital Assets:**\n"
        f"  • BTC: \${btc} | ETH: \${eth}\n\n"
        "⚡ *Molina Holdings: Full System Sync*"
    )
    send_intel(report)
