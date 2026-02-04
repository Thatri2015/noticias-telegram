import os
import json
import requests
import feedparser
from textwrap import wrap

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1003899535115"  # canal Noticias
HIST_FILE = "historico_chapeco.json"

# Feeds Chapecó / Oeste SC
FEEDS = [
    "https://clicrdc.com.br/feed/",
    "https://g1.globo.com/sc/santa-catarina/rss/ultimas.xml"
]

MAX_ITENS_POR_MENSAGEM = 3


def enviar(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)


def carregar_historico():
    if not os.path.exists(HIST_FILE):
        return set()
    with open(HIST_FILE, "r") as f:
        return set(json.load(f))


def salvar_historico(hist):
    with open(HIST_FILE, "w") as f:
        json.dump(list(hist), f)


def limpar_html(texto):
    return texto.replace("<p>", "").replace("</p>", "").strip()


def coletar_noticias():
    historico = carregar_historico()
    novas = []

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            link = entry.get("link")
            if not link or link in historico:
                continue

            titulo = entry.get("title", "").strip()
            resumo = limpar_html(entry.get("summary", ""))[:180]

            texto = f"• {titulo}. {resumo}\n{link}"
            novas.append((texto, link))

    return novas


def enviar_por_blocos(noticias):
    if not noticias:
        return

    blocos = [
        noticias[i:i + MAX_ITENS_POR_MENSAGEM]
        for i in range(0, len(noticias), MAX_ITENS_POR_MENSAGEM)
    ]

    for idx, bloco in enumerate(blocos):
        cabecalho = "🏙️ CHAPECÓ / OESTE DE SC"
        if idx > 0:
            cabecalho += " (continuação)"

        mensagem = cabecalho + "\n\n"
        for texto, _ in bloco:
            mensagem += texto + "\n\n"

        enviar(mensagem)


def main():
    noticias = coletar_noticias()
    if not noticias:
        return  # silêncio se não houver novidade

    historico = carregar_historico()
    for _, link in noticias:
        historico.add(link)

    enviar_por_blocos(noticias)
    salvar_historico(historico)


if __name__ == "__main__":
    main()
