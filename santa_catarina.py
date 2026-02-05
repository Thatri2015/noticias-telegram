import os
import json
import requests
import feedparser

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1003899535115"
HIST_FILE = "historicos/santa_catarina.json"

FEEDS = [
    "https://g1.globo.com/sc/santa-catarina/rss/ultimas.xml",
    "https://ndmais.com.br/feed/"
]

MAX_ITENS = 3


def enviar(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg,
            "disable_web_page_preview": True
        }
    )


def carregar_hist():
    if not os.path.exists(HIST_FILE):
        return set()
    with open(HIST_FILE, "r") as f:
        return set(json.load(f))


def salvar_hist(hist):
    os.makedirs("historicos", exist_ok=True)
    with open(HIST_FILE, "w") as f:
        json.dump(list(hist), f)


def rodar_santa_catarina():
    historico = carregar_hist()
    novas = []

    for url in FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            link = e.get("link")
            if not link or link in historico:
                continue

            titulo = e.get("title", "")
            resumo = e.get("summary", "").replace("<p>", "").replace("</p>", "")[:160]

            novas.append((f"• {titulo}. {resumo}\n{link}", link))

    if not novas:
        return

    blocos = [novas[i:i+MAX_ITENS] for i in range(0, len(novas), MAX_ITENS)]

    for i, bloco in enumerate(blocos):
        cab = "🌎 SANTA CATARINA"
        if i > 0:
            cab += " (continuação)"

        msg = cab + "\n\n" + "\n\n".join(n[0] for n in bloco)
        enviar(msg)

    for _, l in novas:
        historico.add(l)

    salvar_hist(historico)
