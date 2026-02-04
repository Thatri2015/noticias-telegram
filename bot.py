import os
import requests
import feedparser

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

feeds = [
    "https://clicrdc.com.br/feed/",
    "https://g1.globo.com/sc/santa-catarina/rss/ultimas.xml"
]

mensagem = "🏙️ TESTE FORÇADO – CHAPECÓ / OESTE DE SC\n\n"

for feed_url in feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:3]:
        titulo = entry.title
        link = entry.link
        resumo = entry.summary[:120].replace("<p>", "").replace("</p>", "")
        mensagem += f"• {titulo}\n{link}\n\n"

enviar(mensagem)
