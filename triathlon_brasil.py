import feedparser
import requests
import os
import json

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1003899535115"
HIST_FILE = "historicos/triathlon_brasil.json"

FEEDS = [
    "https://cbtri.org.br/feed/"
]

def enviar(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg, "disable_web_page_preview": True}
    )

def rodar_triathlon_brasil():
    os.makedirs("historicos", exist_ok=True)
    hist = set(json.load(open(HIST_FILE))) if os.path.exists(HIST_FILE) else set()

    novas = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            if e.link in hist:
                continue
            novas.append((e.title, e.link))

    if not novas:
        return

    msg = "🇧🇷🏊🚴‍♂️🏃 TRIATHLON – BRASIL\n\n"
    for t, l in novas[:5]:
        msg += f"• {t}\n{l}\n\n"
        hist.add(l)

    enviar(msg)
    json.dump(list(hist), open(HIST_FILE, "w"))
