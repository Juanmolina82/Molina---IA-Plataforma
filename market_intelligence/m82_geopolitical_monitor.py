import os
import requests

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id, 
            "text": f"🏛️ **M82 COMMODITIES WATCH**\n\n{message}", 
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

def monitor_commodities():
    # Matriz de Commodities M82 - Valores de referencia para validación
    data = {
        "Crudo Brent": {"price": 121, "status": "⚠️ CRÍTICO"},
        "Oro (Spot)": {"price": 2450, "status": "✅ COBERTURA"},
        "Cobre": {"price": 4.50, "status": "📈 DEMANDA ALTA"}
    }
    
    report = "Reporte de Situación de Materias Primas:\n\n"
    for item, info in data.items():
        report += f"• **{item}:** ${info['price']} | {info['status']}\n"
    
    report += "\n**Análisis:** La exposición de Molina Holdings LLC en Oro está mitigando la volatilidad energética."
    
    send_to_chairman(report)

if __name__ == "__main__":
    monitor_commodities()
