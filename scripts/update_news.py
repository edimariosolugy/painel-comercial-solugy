#!/usr/bin/env python3
"""
Atualiza data/news.js com as últimas notícias de investimento por setor,
via Google News RSS (pt-BR). Executado diariamente pelo GitHub Actions.
Sem dependências externas — usa apenas a biblioteca padrão do Python.
"""
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ_SECTORS = RAIZ / "data" / "sectors.js"
ARQ_NEWS = RAIZ / "data" / "news.js"
MAX_POR_SETOR = 3
UA = "Mozilla/5.0 (compatible; PainelSolugy/1.0)"


def carregar_setores():
    """Extrai slug e newsQuery do sectors.js sem precisar de um parser JS."""
    texto = ARQ_SECTORS.read_text(encoding="utf-8")
    pares = re.findall(r'slug:\s*"([^"]+)".*?newsQuery:\s*"([^"]+)"', texto, re.S)
    return pares


def buscar_rss(query):
    url = ("https://news.google.com/rss/search?q=" +
           urllib.parse.quote(query + " when:7d") +
           "&hl=pt-BR&gl=BR&ceid=BR:pt-419")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse_itens(xml_bytes):
    itens = []
    root = ET.fromstring(xml_bytes)
    for item in root.iter("item"):
        titulo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = item.findtext("pubDate")
        fonte_el = item.find("{https://news.google.com/rss}source")
        if fonte_el is None:
            fonte_el = item.find("source")
        fonte = (fonte_el.text or "").strip() if fonte_el is not None else ""
        # Título do Google News costuma vir como "Manchete - Fonte"
        if fonte and titulo.endswith(" - " + fonte):
            titulo = titulo[: -(len(fonte) + 3)]
        data_iso = None
        if pub:
            try:
                data_iso = parsedate_to_datetime(pub).date().isoformat()
            except Exception:
                pass
        if titulo and link:
            itens.append({"titulo": titulo, "link": link, "fonte": fonte, "data": data_iso})
        if len(itens) >= MAX_POR_SETOR:
            break
    return itens


def main():
    resultado = {}
    erros = []
    for slug, query in carregar_setores():
        try:
            resultado[slug] = parse_itens(buscar_rss(query))
            print(f"[ok] {slug}: {len(resultado[slug])} notícias")
        except Exception as e:
            erros.append(f"{slug}: {e}")
            resultado[slug] = []
            print(f"[erro] {slug}: {e}")

    # Não regrava (nem gera commit/deploy) se as notícias não mudaram
    if ARQ_NEWS.exists():
        try:
            antigo = json.loads(ARQ_NEWS.read_text(encoding="utf-8").split("window.NEWS = ", 1)[1].rstrip().rstrip(";"))
            if antigo.get("itens") == resultado:
                print("Sem mudanças nas notícias — nada a gravar.")
                return
        except Exception:
            pass

    payload = {
        "atualizadoEm": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "itens": resultado,
    }
    ARQ_NEWS.write_text(
        "// Gerado automaticamente por scripts/update_news.py — não editar manualmente.\n"
        "window.NEWS = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"\nGravado {ARQ_NEWS} — {sum(len(v) for v in resultado.values())} notícias, {len(erros)} erros.")


if __name__ == "__main__":
    main()
