# Painel Comercial Solugy

Painel para o time comercial em 4 abas: **Setores & Investimentos** (20 setores-alvo), **Indicadores Mensais** (orçado, MC, taxa de aprovação, origem), **Notícias do Dia** (atualização automática) e **Funil de Prospecção** (200 empresas priorizadas). Hospedado no **Azure Static Web Apps** com deploy automático via **GitHub Actions**.

> ⚠️ **O repositório deve ser PRIVADO** — o painel contém dados comerciais internos (funil, MC e orçamentos).

## Login automático com a conta Microsoft/Windows

O `staticwebapp.config.json` já exige autenticação: ao abrir o site, o Azure redireciona para o login Microsoft (Entra ID). Se a pessoa já estiver logada no Windows/Edge com a conta corporativa, o login é silencioso e o painel abre direto com **"Bem-vindo, {nome} 👋"** — mesmo padrão do DashboardExec do grupo.

- Funciona no plano **Free** com o provedor Entra ID embutido (`/.auth/login/aad`).
- Para restringir a entrada só ao time (e não a qualquer conta Microsoft), use o **Role management** do recurso no portal (convide os e-mails do time) ou o plano Standard com registro do app no Entra ID do tenant Solugy.
- O primeiro nome fica memorizado no navegador (localStorage) para aparecer instantaneamente nas próximas visitas.

## Estrutura

| Arquivo | Função |
|---|---|
| `index.html` | O painel (HTML único, sem build) |
| `data/sectors.js` | Indicadores dos 20 setores — **edite aqui** para atualizar números |
| `data/news.js` | Notícias por setor — gerado automaticamente, não editar |
| `data/funil.js` | Funil e indicadores mensais — gerado da planilha, não editar |
| `data/logo.js` | Logo oficial Solugy (mesmo do DashboardExec do grupo) |
| `scripts/update_news.py` | Robô que busca notícias no Google News (pt-BR) |
| `scripts/extract_funil.py` | Extrai funil + indicadores da planilha de orçamentos |
| `scripts/sync_sharepoint.py` | Baixa a planilha do OneDrive/SharePoint via Microsoft Graph |
| `.github/workflows/update-news.yml` | Notícias de hora em hora (06–20h BRT, seg–sáb) |
| `.github/workflows/sync-funil.yml` | Sincroniza a planilha de hora em hora (precisa dos secrets Graph) |
| `.github/workflows/azure-static-web-apps.yml` | Publica no Azure a cada push na `main` |

> 📘 **Publicação passo a passo: veja o [GUIA-PUBLICACAO.md](GUIA-PUBLICACAO.md).**

## Sincronizar com a planilha do funil

Sempre que atualizar **"Gestão e Controle de Orçamentos.xlsm"** (abas Prospecção, Lançamentos, Fechamentos, Segmentos, Origem):

```bash
pip install openpyxl
python scripts/extract_funil.py "C:/caminho/para/Gestão e Controle de Orçamentos.xlsm"
git add data/funil.js && git commit -m "atualiza funil" && git push
```

O site republica sozinho. Os segmentos padronizados da aba Prospecção casam automaticamente com os 20 setores do painel.

## Como publicar (uma vez só)

1. **GitHub** — crie um repositório (ex.: `painel-setores-solugy`) e envie estes arquivos:
   ```bash
   git init && git add . && git commit -m "Painel setorial Solugy"
   git branch -M main
   git remote add origin https://github.com/SUA-ORG/painel-setores-solugy.git
   git push -u origin main
   ```
2. **Azure** — no portal ([portal.azure.com](https://portal.azure.com)), crie um recurso **Static Web App** (plano Free):
   - Origem: GitHub → selecione o repositório e a branch `main`.
   - Presets de build: **Custom** · App location: `/` · Output location: *(vazio)*.
   - O Azure cria o secret `AZURE_STATIC_WEB_APPS_API_TOKEN` no repo automaticamente. Se criar manualmente, copie o *deployment token* do recurso e cadastre em *Settings → Secrets and variables → Actions*.
3. **Notícias** — vá na aba **Actions** do GitHub e rode manualmente o workflow "Atualizar notícias diariamente" (botão *Run workflow*) para popular as primeiras notícias. Depois disso, roda sozinho todo dia às 06:00.

## Manutenção

- **Atualizar indicadores**: edite `data/sectors.js` e faça push — o site republica sozinho.
- **Setores-foco** (borda vermelha): lista `SETORES_FOCO` no `index.html` (hoje: 10-Farmacêutico, 15-Mineração, 18-Saneamento).
- **Cores da marca**: variáveis CSS no topo do `index.html` (`--azul`, `--vermelho`, `--verde`).
- **Termos de busca das notícias**: campo `newsQuery` de cada setor em `data/sectors.js`.

## Fontes dos indicadores (ago/2026)

MAPA (Plano Safra), ABIA, Anfavea, EPE, SNIC/CBIC, MME (leilões de transmissão), ABSOLAR, Casa Civil (Novo PAC), PróGenéricos/Sindusfarma, IBRAM, Ibá, Abiquim, ANA/Marco Legal do Saneamento, IPEA.
