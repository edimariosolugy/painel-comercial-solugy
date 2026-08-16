#!/usr/bin/env python3
"""
Busca métricas completas do Instagram via API oficial da Meta (Instagram Graph)
e grava data/instagram.js. Coleta por conta:
  - perfil (seguidores, posts)
  - alcance diário 30d + novos seguidores por dia
  - totais 30d: contas engajadas, interações, curtidas, comentários,
    salvamentos, compartilhamentos, views, cliques no link do perfil
  - horários em que os seguidores estão online (mapa de calor, hora de Brasília)
  - demografia dos seguidores (cidades, idade, gênero)
  - insights por post (alcance, views, salvos, compartilhamentos)

Secrets: IG_TOKEN, IG_USER_ID e opcionais IG_USER_ID2/IG_TOKEN2.
Apenas biblioteca padrão do Python. Todas as métricas são tolerantes a falha —
o que a Meta não liberar para a conta vem como nulo e o painel se adapta.
"""
import json
import os
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "data" / "instagram.js"
G = "https://graph.facebook.com/v21.0"
FUSO_BRT = -3  # deslocamento simples UTC -> Brasília


def get(caminho, token, **params):
    params["access_token"] = token
    url = f"{G}/{caminho}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


def serie_diaria(ig, token, metrica, desde):
    """Métricas com série diária simples (reach, follower_count...)."""
    ins = get(f"{ig}/insights", token, metric=metrica, period="day", since=desde)
    return [{"data": v.get("end_time", "")[:10], "valor": v.get("value", 0) or 0}
            for v in ins.get("data", [{}])[0].get("values", [])]


def total_30d(ig, token, metrica, desde, ate):
    """Métricas agregadas (metric_type=total_value)."""
    ins = get(f"{ig}/insights", token, metric=metrica, period="day",
              metric_type="total_value", since=desde, until=ate)
    return ins.get("data", [{}])[0].get("total_value", {}).get("value")


def demografia(ig, token, breakdown, topo=8):
    ins = get(f"{ig}/insights", token, metric="follower_demographics",
              period="lifetime", metric_type="total_value", breakdown=breakdown)
    res = (ins.get("data", [{}])[0].get("total_value", {})
           .get("breakdowns", [{}])[0].get("results", []))
    itens = [{"nome": ", ".join(r.get("dimension_values", ["?"])), "valor": r.get("value", 0)} for r in res]
    itens.sort(key=lambda x: -x["valor"])
    return itens[:topo]


def heatmap_online(ig, token):
    """Média de seguidores online por (dia da semana, hora) em BRT."""
    ins = get(f"{ig}/insights", token, metric="online_followers", period="lifetime")
    soma = defaultdict(float); cont = defaultdict(int)
    for v in ins.get("data", [{}])[0].get("values", []):
        fim = v.get("end_time", "")
        try:
            dia_utc = datetime.fromisoformat(fim.replace("+0000", "+00:00"))
        except ValueError:
            continue
        for hora_str, qtd in (v.get("value") or {}).items():
            h_utc = int(hora_str)
            dt_brt = dia_utc.replace(hour=h_utc) + timedelta(hours=FUSO_BRT)
            chave = (dt_brt.weekday(), dt_brt.hour)  # 0=segunda
            soma[chave] += qtd or 0; cont[chave] += 1
    return [{"d": d, "h": h, "n": round(soma[(d, h)] / max(cont[(d, h)], 1))}
            for (d, h) in sorted(soma.keys())]


def insights_post(media_id, tipo, token):
    """Métricas por post; conjuntos variam por tipo — tudo tolerante."""
    out = {}
    for metricas in ("reach,saved,shares,views", "reach,saved", "reach"):
        try:
            ins = get(f"{media_id}/insights", token, metric=metricas)
            for d in ins.get("data", []):
                out[d.get("name")] = (d.get("values") or [{}])[0].get("value", 0)
            break
        except Exception:
            continue
    if tipo == "VIDEO":
        try:
            ins = get(f"{media_id}/insights", token, metric="ig_reels_avg_watch_time")
            out["watch_ms"] = (ins.get("data", [{}])[0].get("values") or [{}])[0].get("value")
        except Exception:
            pass
    return out


def coleta_conta(ig, token):
    agora = datetime.now(timezone.utc)
    desde = int((agora - timedelta(days=30)).timestamp())
    ate = int(agora.timestamp())

    perfil = get(ig, token, fields="username,name,followers_count,media_count")
    conta = {
        "perfil": {
            "username": perfil.get("username", ""),
            "nome": perfil.get("name", ""),
            "seguidores": perfil.get("followers_count", 0),
            "totalPosts": perfil.get("media_count", 0),
        },
        "alcance30d": [], "seguidores30d": [], "visitasPerfil30d": None,
        "metricas30d": {}, "online": [], "demografia": None, "posts": [],
    }

    def tenta(rotulo, fn):
        try:
            return fn()
        except Exception as e:
            print(f"[aviso] @{conta['perfil']['username']} {rotulo}: {e}")
            return None

    conta["alcance30d"] = tenta("alcance", lambda: serie_diaria(ig, token, "reach", desde)) or []
    conta["seguidores30d"] = tenta("novos seguidores", lambda: serie_diaria(ig, token, "follower_count", desde)) or []

    visitas = tenta("visitas", lambda: total_30d(ig, token, "profile_views", desde, ate))
    conta["visitasPerfil30d"] = visitas

    METRICAS = {"contasEngajadas": "accounts_engaged", "interacoes": "total_interactions",
                "curtidas": "likes", "comentarios": "comments", "salvos": "saves",
                "compartilhamentos": "shares", "views": "views", "cliquesLink": "profile_links_taps"}
    for chave, met in METRICAS.items():
        conta["metricas30d"][chave] = tenta(met, lambda m=met: total_30d(ig, token, m, desde, ate))

    conta["online"] = tenta("online_followers", lambda: heatmap_online(ig, token)) or []

    demo = {}
    for chave, br in (("cidades", "city"), ("idades", "age"), ("genero", "gender")):
        d = tenta(f"demografia {br}", lambda b=br: demografia(ig, token, b))
        if d:
            demo[chave] = d
    conta["demografia"] = demo or None

    med = tenta("posts", lambda: get(f"{ig}/media", token,
                fields="id,caption,media_type,permalink,timestamp,like_count,comments_count", limit=12))
    for m in (med or {}).get("data", []):
        extra = insights_post(m.get("id"), m.get("media_type", ""), token)
        conta["posts"].append({
            "legenda": (m.get("caption") or "")[:120],
            "tipo": m.get("media_type", ""),
            "link": m.get("permalink", ""),
            "data": (m.get("timestamp") or "")[:10],
            "likes": m.get("like_count", 0),
            "comentarios": m.get("comments_count", 0),
            "alcance": extra.get("reach"),
            "views": extra.get("views"),
            "salvos": extra.get("saved"),
            "compart": extra.get("shares"),
            "watchMs": extra.get("watch_ms"),
        })
    return conta


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
            print(f"[ok] @{c['perfil']['username']}: {c['perfil']['seguidores']} seguidores, "
                  f"{len(c['posts'])} posts, {len(c['online'])} células de heatmap")
        except Exception as e:
            print(f"[erro] conta {ig_id}: {e}")

    if not contas:
        raise SystemExit("Nenhuma conta coletada — verifique IG_TOKEN/IG_USER_ID.")

    payload = {"atualizadoEm": datetime.now(timezone.utc).isoformat(timespec="seconds"), "contas": contas}

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
