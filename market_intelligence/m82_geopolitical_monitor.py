import os
import requests

# M82 Intelligence Engine - V3.2
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
    else:
        print("Error: Credenciales no encontradas en el entorno.")

if __name__ == "__main__":
    # Mensaje de éxito de la infraestructura
    report = (
        "✅ **SISTEMA ONLINE - FASE V3.2**\n\n"
        "Chairman **M82**, la conexión ha sido establecida.\n\n"
        "• **Entidad:** Molina Holdings LLC\n"
        "• **Gobernanza:** Activa\n"
        "• **Seguridad:** Secrets Encriptados\n"
        "• **Monitor:** Atoms & Reuters Ready"
    )
    send_to_chairman(report)
