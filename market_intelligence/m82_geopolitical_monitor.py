import os
import requests

def force_ping():
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Mensaje de fuerza bruta para romper el silencio
    payload = {
        "chat_id": chat_id,
        "text": "🚨 **M82 SIGNAL RECOVERY**\nConexión establecida con el Chairman.",
        "parse_mode": "Markdown"
    }
    
    r = requests.post(url, json=payload)
    print(f"Resultado: {r.status_code}")
    print(f"Respuesta: {r.text}")

if __name__ == "__main__":
    force_ping()
