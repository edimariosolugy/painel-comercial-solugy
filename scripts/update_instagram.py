#!/usr/bin/env python3
"""
Busca métricas do Instagram @solugyoficial via API oficial da Meta (Instagram
Graph) e grava data/instagram.js. Rodado de hora em hora pelo GitHub Actions.

Variáveis de ambiente (GitHub Secrets):
  IG_TOKEN   - token de página de longa duração (ver GUIA-PUBLICACAO.md, etapa 5)
  IG_USER_ID - ID da conta Instagram Business (@solugyoficial)

Apenas biblioteca padrão do Python.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "data" / "instagram.js"
G = "https://graph.facebook.com/v21.0"


def get(caminho, **params):
    params["access_token"] = os.environ["IG_TOKEN"]
    url = f"{G}/{caminho}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


def main():
    ig = os.environ["IG_USER_ID"]

    # Perfil
    perfil = get(ig, fields="username,name,followers_count,media_count")

    # Alcance diário (últimos 30 dias) — tolerante a mudanças de API
    alcance = []
    try:
        desde = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())
        ins = get(f"{ig}/insights", metric="reach", period="day", since=desde)
        for v in ins.get("data", [{}])[0].get("values", []):
            alcance.append({"data": v.get("end_time", "")[:10], "valor": v.get("value", 0)})
    except Exception as e:
        print(f"[aviso] alcance indisponível: {e}")

    # Visitas ao perfil (nem toda conta expõe; tolerante)
    visitas30d = None
    try:
        ins = get(f"{ig}/insights", metric="profile_views", period="day", since=desde)
        visitas30d = sum(v.get("value", 0) for v in ins.get("data", [{}])[0].get("values", []))
    except Exception as e:
        print(f"[aviso] profile_views indisponível: {e}")

    # Últimos 12 posts
    posts = []
    try:
        med = get(f"{ig}/media", fields="caption,media_type,permalink,timestamp,like_count,comments_count", limit=12)
        for m in med.get("data", []):
            posts.append({
                "legenda": (m.get("caption") or "")[:120],
                "tipo": m.get("media_type", ""),
                "link": m.get("permalink", ""),
                "data": (m.get("timestamp") or "")[:10],
                "likes": m.get("like_count", 0),
                "comentarios": m.get("comments_count", 0),
            })
    except Exception as e:
        print(f"[aviso] posts indisponíveis: {e}")

    payload = {
        "atualizadoEm": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "perfil": {
            "username": perfil.get("username", "solugyoficial"),
            "nome": perfil.get("name", ""),
            "seguidores": perfil.get("followers_count", 0),
            "totalPosts": perfil.get("media_count", 0),
        },
        "alcance30d": alcance,
        "visitasPerfil30d": visitas30d,
        "posts": posts,
    }

    # Não regrava se nada mudou (evita commit/deploy inútil)
    if SAIDA.exists():
        try:
            antigo = json.loads(SAIDA.read_text(encoding="utf-8").split("window.INSTA = ", 1)[1].rstrip().rstrip(";"))
            antigo.pop("atualizadoEm", None)
            novo = dict(payload); novo.pop("atualizadoEm", None)
            if antigo == novo:
                print("Sem mudanças no Instagram — nada a gravar.")
                return
        except Exception:
            pass

    SAIDA.write_text(
        "// Gerado por scripts/update_instagram.py — não editar manualmente.\n"
        "window.INSTA = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"OK: @{payload['perfil']['username']} · {payload['perfil']['seguidores']} seguidores · {len(posts)} posts -> {SAIDA}")


if __name__ == "__main__":
    main()
