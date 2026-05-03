import os
import requests
import time

def get_data(symbol, is_index=True):
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    # Usamos GLOBAL_QUOTE para máxima precisión en Equities/ETFs
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}"
    try:
        time.sleep(0.7)
        r = requests.get(url).json()
        quote = r.get('Global Quote', {})
        price = quote.get('05. price', 'N/A')
        change = quote.get('10. change percent', '0%')
        if price != 'N/A':
            return f"${float(price):,.2f} ({change})"
        return "N/A"
    except: return "N/A"

def get_treasury_yield():
    # El bono a 10 años es el benchmark global
    key = os.getenv('ALPHA_VANTAGE_KEY', '').strip()
    url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=10year&apikey={key}"
    try:
        time.sleep(0.7)
        r = requests.get(url).json()
        val = r.get('data', [{}])[0].get('value', 'N/A')
        return f"{val}%" if val != 'N/A' else "N/A"
    except: return "N/A"

def send_intel(msg):
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    # 1. EQUITIES & INDEX ETFs
    spy = get_data("SPY")   # S&P 500
    qqq = get_data("QQQ")   # Nasdaq 100
    dia = get_data("DIA")   # Dow Jones
    
    # 2. BONDS (Renta Fija)
    t10y = get_treasury_yield() # Yield 10 Años
    tlt = get_data("TLT")       # ETF de Bonos +20 años (Sentimiento de tipos)
    
    # 3. SECTORIAL / COMMODITIES
    gold = get_data("GLD")      # ETF Oro
    oil = get_data("USO")       # ETF Petróleo
    
    report = (
        "🏛️ **M82 ASSET MATRIX BRIEFING**\n\n"
        "📈 **Equities & Indices:**\n"
        f"  • SPY: {spy}\n"
        f"  • QQQ: {qqq}\n"
        f"  • DIA: {dia}\n\n"
        "🏦 **Fixed Income (Bonds):**\n"
        f"  • US 10Y Yield: {t10y}\n"
        f"  • TLT (Long Bond): {tlt}\n\n"
        "🛡️ **Strategic ETFs:**\n"
        f"  • GLD (Oro): {gold}\n"
        f"  • USO (Crudo): {oil}\n\n"
        "🐋 *LSEG Order Flow Analysis: Pending Key...*\n"
        "⚡ *Molina Holdings: Multi-Asset Surveillance*"
    )
    send_intel(report)
