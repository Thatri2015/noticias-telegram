import os
import requests
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1003899535115"  # canal Noticias

def enviar(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    hoje = datetime.now().strftime("%d/%m/%Y")
    mensagem = f"🗞️ Bot de notícias ativo ✅\nData: {hoje}"
    enviar(mensagem)
