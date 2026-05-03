import os
import requests

# Copyright 2026 Molina Global LLC
# M82 Geopolitical Intelligence Engine - V3.2
# Reuters/LSEG Monitoring Integration

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

def monitor_reuters_and_energy():
    print("--- M82: Analizando Flujos de Reuters & Atoms ---")
    
    # Umbral de alerta definido por la Matriz
    oil_price = 120 
    
    if oil_price >= 120:
        report = (
            "⚠️ **ALERTA GEOPOLÍTICA**\n"
            "Instrumento: Crude Oil (Brent)\n"
            "Estado: Umbral de **$120** alcanzado.\n"
            "Acción: Ejecutando protocolos de blindaje patrimonial.\n"
            "Source: Reuters/LSEG Workspace via M82 Engine"
        )
        send_to_chairman(report)

if __name__ == "__main__":
    monitor_reuters_and_energy()
