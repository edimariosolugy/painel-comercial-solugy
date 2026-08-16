#!/usr/bin/env python3
"""
Busca métricas do Instagram via API oficial da Meta (Instagram Graph) e grava
data/instagram.js. Suporta DUAS contas: @solugyoficial e @edimariosolugy.
Rodado de hora em hora pelo GitHub Actions.

Variáveis de ambiente (GitHub Secrets):
  IG_TOKEN     - token de longa duração (usuário ou página) com acesso às contas
  IG_USER_ID   - ID da conta Instagram Business principal (@solugyoficial)
  IG_USER_ID2  - (opcional) ID da segunda conta (@edimariosolugy)
  IG_TOKEN2    - (opcional) token específico da segunda conta; se ausente, usa IG_TOKEN

Apenas biblioteca padrão do Python.
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "data" / "instagram.js"
G = "https://graph.facebook.com/v21.0"


def get(caminho, token, **params):
    params["access_token"] = token
    url = f"{G}/{caminho}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


def coleta_conta(ig_id, token):
    """Coleta perfil, alcance 30d, visitas e últimos posts de uma conta."""
    perfil = get(ig_id, token, fields="username,name,followers_count,media_count")
    desde = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())

    alcance = []
    try:
        ins = get(f"{ig_id}/insights", token, metric="reach", period="day", since=desde)
        for v in ins.get("data", [{}])[0].get("values", []):
            alcance.append({"data": v.get("end_time", "")[:10], "valor": v.get("value", 0)})
    except Exception as e:
        print(f"[aviso] {perfil.get('username')}: alcance indisponível: {e}")

    visitas = None
    try:
        ins = get(f"{ig_id}/insights", token, metric="profile_views", period="day", since=desde)
        visitas = sum(v.get("value", 0) for v in ins.get("data", [{}])[0].get("values", []))
    except Exception as e:
        print(f"[aviso] {perfil.get('username')}: profile_views indisponível: {e}")

    posts = []
    try:
        med = get(f"{ig_id}/media", token, fields="caption,media_type,permalink,timestamp,like_count,comments_count", limit=12)
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
        print(f"[aviso] {perfil.get('username')}: posts indisponíveis: {e}")

    return {
        "perfil": {
            "username": perfil.get("username", ""),
            "nome": perfil.get("name", ""),
            "seguidores": perfil.get("followers_count", 0),
            "totalPosts": perfil.get("media_count", 0),
        },
        "alcance30d": alcance,
        "visitasPerfil30d": visitas,
        "posts": posts,
    }


def main():
    token = os.environ["IG_TOKEN"]
    contas_cfg = [(os.environ["IG_USER_ID"], token)]
    if os.environ.get("IG_USER_ID2"):
        contas_cfg.append((os.environ["IG_USER_ID2"], os.environ.get("IG_TOKEN2") or token))

    contas = []
    for ig_id, tk in contas_cfg:
        try:
            c = coleta_conta(ig_id, tk)
            contas.append(c)
            print(f"[ok] @{c['perfil']['username']}: {c['perfil']['seguidores']} seguidores, {len(c['posts'])} posts")
        except Exception as e:
            print(f"[erro] conta {ig_id}: {e}")

    if not contas:
        raise SystemExit("Nenhuma conta coletada — verifique IG_TOKEN/IG_USER_ID.")

    payload = {
        "atualizadoEm": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "contas": contas,
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
    print(f"Gravado {SAIDA} — {len(contas)} conta(s).")


if __name__ == "__main__":
    main()
