#!/usr/bin/env python3
"""
Baixa a planilha "Gestão e Controle de Orçamentos.xlsm" direto do
SharePoint/OneDrive da Solugy via Microsoft Graph (sem interação).
Usado pelo workflow sync-funil.yml para atualizar o painel de hora em hora.

Variáveis de ambiente necessárias (GitHub Secrets):
  GRAPH_TENANT_ID    - ID do tenant Entra ID da Solugy
  GRAPH_CLIENT_ID    - ID do app registrado no Entra ID
  GRAPH_CLIENT_SECRET- segredo do app
  SP_FILE_PATH       - caminho do arquivo na biblioteca, ex.:
                       2026/02 - Comercial/Funil de Vendas/Gestão e Controle de Orçamentos.xlsm
E UMA das duas origens:
  SP_SITE            - site SharePoint, ex.: solugy.sharepoint.com:/sites/MySolugy
  SP_USER_UPN        - ou o e-mail do dono do OneDrive, ex.: edimario.lima@solugy.com.br

Apenas biblioteca padrão do Python.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

GRAPH = "https://graph.microsoft.com/v1.0"


def req(url, data=None, token=None):
    headers = {}
    if token:
        headers["Authorization"] = "Bearer " + token
    r = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(r, timeout=60) as resp:
        return resp.read()


def main():
    tenant = os.environ["GRAPH_TENANT_ID"]
    client = os.environ["GRAPH_CLIENT_ID"]
    secret = os.environ["GRAPH_CLIENT_SECRET"]
    fpath = os.environ["SP_FILE_PATH"]
    destino = sys.argv[1] if len(sys.argv) > 1 else "planilha.xlsm"

    # 1) token (client credentials)
    corpo = urllib.parse.urlencode({
        "client_id": client, "client_secret": secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }).encode()
    tok = json.loads(req(f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token", data=corpo))["access_token"]

    # 2) resolve a raiz do drive (site SharePoint ou OneDrive do usuário)
    fpath_enc = urllib.parse.quote(fpath)
    if os.environ.get("SP_SITE"):
        site = json.loads(req(f"{GRAPH}/sites/{os.environ['SP_SITE']}", token=tok))
        url = f"{GRAPH}/sites/{site['id']}/drive/root:/{fpath_enc}:/content"
    elif os.environ.get("SP_USER_UPN"):
        upn = urllib.parse.quote(os.environ["SP_USER_UPN"])
        url = f"{GRAPH}/users/{upn}/drive/root:/{fpath_enc}:/content"
    else:
        sys.exit("Defina SP_SITE ou SP_USER_UPN.")

    # 3) baixa o arquivo
    conteudo = req(url, token=tok)
    with open(destino, "wb") as f:
        f.write(conteudo)
    print(f"OK: {len(conteudo)/1024:.0f} KB baixados -> {destino}")


if __name__ == "__main__":
    main()
