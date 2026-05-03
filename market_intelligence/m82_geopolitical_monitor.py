import os
import requests

# M82 Intelligence & Equities Engine - V3.2
# Proprietary of Molina Holdings LLC

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id, 
            "text": f"🏛️ **M82 COMMAND CENTER**\n\n{message}", 
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

def monitor_full_spectrum():
    # Datos de Inteligencia (Simulados para validación de estructura)
    oil_price = 121
    # Portafolio M82 (Ejemplo: Energía y Tecnología)
    equities_performance = "+2.45%" 
    
    report = (
        "📊 **M82 EQUITIES REPORT**\n\n"
        "• **Atoms (Crudo):** $121/bbl ⚠️\n"
        "• **Portafolio M82:** {perf}\n"
        "• **Estado:** Blindaje Patrimonial Activo\n\n"
        "Chairman, el alza en el petróleo está siendo compensada por las posiciones en el sector energético de **Molina Holdings LLC**."
    ).format(perf=equities_performance)
    
    send_to_chairman(report)

if __name__ == "__main__":
    monitor_full_spectrum()
