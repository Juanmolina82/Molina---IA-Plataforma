import os
import requests

def send_to_chairman(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ ERROR TELEGRAM: {response.status_code} - {response.text}")
    else:
        print("✅ MENSAJE ENVIADO CON ÉXITO")

if __name__ == "__main__":
    send_to_chairman("🏛️ **M82 PROTOCOLO DE EMERGENCIA**\nChairman, si lee esto, la conexión es total.")
