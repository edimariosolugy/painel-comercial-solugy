# Guia de Publicação — Painel Comercial Solugy

Passo a passo para publicar pelo seu PC, igual ao painel já existente do grupo: repositório privado no GitHub + Static Web App no Azure com login Microsoft automático e atualização de hora em hora.

Tempo estimado: 30–40 min (etapas 1 a 3). A etapa 4 (sincronização automática da planilha) depende de um registro no Entra ID — se você não for admin do Microsoft 365 da Solugy, peça ao TI com o texto pronto abaixo.

---

## Etapa 1 — Publicar no GitHub pelo seu PC

1. Instale o **Git**: https://git-scm.com/download/win (Avançar em tudo).
2. Crie o repositório: em https://github.com/new → nome `painel-comercial-solugy` → **Private** ✅ → *Create repository* (sem README).
3. Extraia o ZIP do painel numa pasta (ex.: `C:\Projetos\painel-comercial-solugy`).
4. Abra o **Prompt de Comando** nessa pasta (na barra de endereço do Explorer, digite `cmd` e Enter) e rode:

```bash
git init
git add .
git commit -m "Painel Comercial Solugy"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/painel-comercial-solugy.git
git push -u origin main
```

> Na primeira vez o Git abre o navegador para você logar no GitHub. Troque `SEU-USUARIO` pelo seu usuário.

---

## Etapa 2 — Criar o Static Web App no Azure

1. Acesse https://portal.azure.com → **Criar um recurso** → procure **Static Web App** → *Criar*.
2. Preencha:
   - **Assinatura/Grupo de recursos**: os mesmos usados pelo painel do grupo (ou crie `rg-paineis-solugy`).
   - **Nome**: `painel-comercial-solugy`
   - **Plano**: Free
   - **Região**: Brazil South (ou a mesma do painel existente)
   - **Origem**: GitHub → autorize → escolha seu usuário, o repo `painel-comercial-solugy` e a branch `main`.
   - **Build**: Predefinição **Custom** · App location: `/` · Api location: *(vazio)* · Output location: *(vazio)*.
3. *Revisar + criar* → *Criar*. O Azure grava sozinho o secret `AZURE_STATIC_WEB_APPS_API_TOKEN` no repo e dispara o primeiro deploy (acompanhe na aba **Actions** do GitHub, ~2 min).

> O Azure vai criar um workflow próprio de deploy no repo. Pode deixar — ele convive com o `azure-static-web-apps.yml` incluído; se preferir, apague um dos dois.

4. A URL do painel aparece na página do recurso (algo como `https://nice-sky-0a1b2c3.azurestaticapps.net`).

### Login automático com o usuário do Windows

Já está configurado no `staticwebapp.config.json`: ao abrir a URL, o Azure redireciona para o login Microsoft. Quem já estiver logado no Windows/Edge com a conta corporativa entra direto e vê **"Bem-vindo, {nome} 👋"**.

Para **restringir ao time** (recomendado): no recurso do Azure → **Role management** → *Invite user* → e-mail de cada pessoa → role `authenticated`. 

---

## Etapa 3 — Ativar o robô de notícias

Aba **Actions** do GitHub → workflow **"Atualizar notícias (de hora em hora)"** → *Run workflow* (primeira carga manual). Depois disso ele roda sozinho **de hora em hora, das 06h às 20h (Brasília), seg–sáb**, e só comita/republica quando há notícia nova.

> Quer 24/7? Edite `.github/workflows/update-news.yml` e troque o cron por `"0 * * * *"`. Atenção: repositório privado tem 2.000 min/mês grátis de Actions — o padrão comercial (06–20h) consome ~40% disso; 24/7 pode estourar o limite.

---

## Etapa 4 — Sincronização automática da planilha do funil (de hora em hora)

Faz o painel ler sozinho a **"Gestão e Controle de Orçamentos.xlsm"** direto do OneDrive/SharePoint da Solugy. Precisa de um registro de aplicativo no Entra ID (uma vez só, feito por um admin do Microsoft 365).

**Texto pronto para enviar ao TI:**

> Preciso de um App Registration no Entra ID para leitura de arquivos via Microsoft Graph (client credentials), para automação de um painel interno:
> 1. Entra ID → App registrations → New registration → nome `painel-comercial-sync`.
> 2. API permissions → Microsoft Graph → **Application permissions** → `Files.Read.All` (e `Sites.Read.All` se o arquivo estiver em site SharePoint) → **Grant admin consent**.
> 3. Certificates & secrets → New client secret (24 meses) → me enviar: **Tenant ID**, **Client ID** e o **valor do secret**.

Com os três valores em mãos, no GitHub: repo → **Settings → Secrets and variables → Actions → New repository secret**, crie:

| Secret | Valor |
|---|---|
| `GRAPH_TENANT_ID` | Tenant ID enviado pelo TI |
| `GRAPH_CLIENT_ID` | Client ID |
| `GRAPH_CLIENT_SECRET` | valor do secret |
| `SP_USER_UPN` | `edimario.lima@solugy.com.br` (dono do OneDrive onde a planilha está) |
| `SP_FILE_PATH` | `2026/02 - Comercial/Funil de Vendas/Gestão e Controle de Orçamentos.xlsm` |

> Se a pasta "MySolugy - Documentos" for uma biblioteca de **site SharePoint** (não OneDrive pessoal), use o secret `SP_SITE` no lugar de `SP_USER_UPN`, com o valor `solugy.sharepoint.com:/sites/MySolugy` (confirme o endereço abrindo a pasta no navegador).

Teste: aba **Actions** → **"Sincronizar funil com a planilha (de hora em hora)"** → *Run workflow*. Se aparecer verde e o painel atualizar, pronto: qualquer mudança que o time salvar na planilha aparece no painel em até 1 hora, sem ninguém rodar nada.

*Enquanto os secrets não existirem, esse workflow apenas se pula com um aviso — o resto do painel funciona normalmente, e você pode atualizar o funil manualmente com `python scripts/extract_funil.py "caminho da planilha"` + push.*

---

## Etapa 5 — Aba Instagram (@solugyoficial) de hora em hora

Conecta a aba Instagram à API oficial da Meta. Pré-requisito: o **@solugyoficial** deve ser conta **profissional** (Business/Criador) **vinculada a uma Página do Facebook** da Solugy (configura-se no app do Instagram → Configurações → Central de contas).

1. Acesse https://developers.facebook.com (logado com a conta que administra a Página) → **My Apps → Create App** → tipo **Business** → nome `painel-solugy-instagram`.
2. Abra **Tools → Graph API Explorer** (https://developers.facebook.com/tools/explorer):
   - Em *Meta App*, selecione o app criado.
   - Em *Permissions*, adicione: `instagram_basic`, `instagram_manage_insights`, `pages_show_list`, `pages_read_engagement` → **Generate Access Token** (autorize com sua conta).
3. Ainda no Explorer, descubra os IDs (rode cada consulta na barra de endereço do Explorer):
   - `me/accounts` → copie o **id** da Página Solugy e o **access_token** dela (este é o token de página, de longa duração).
   - `{id-da-pagina}?fields=instagram_business_account` → o **id** retornado é o **IG_USER_ID**.
4. No GitHub: repo → **Settings → Secrets and variables → Actions**, crie:

| Secret | Valor |
|---|---|
| `IG_TOKEN` | o access_token **da Página** (passo 3) |
| `IG_USER_ID` | o id do instagram_business_account |

5. Teste: aba **Actions** → **"Atualizar Instagram (de hora em hora)"** → *Run workflow*. Ficando verde, a aba Instagram do painel mostra seguidores, alcance diário (30 dias), visitas ao perfil e o ranking de engajamento dos últimos posts — atualizando a cada hora (06:30–20:30, seg–sáb).

> Dica: para o token de página não expirar, gere-o a partir de um token de usuário de longa duração (Explorer → ⓘ do token → *Open in Access Token Tool* → *Extend Access Token*, e refaça o passo `me/accounts`). Enquanto os secrets não existirem, o workflow se pula com aviso e a aba mostra as instruções.

### Segunda conta: @edimariosolugy

A aba suporta duas contas com um seletor. Para adicionar o @edimariosolugy:

1. Vincule o @edimariosolugy a uma Página do Facebook (pode criar uma página própria, ex. "Edimário Solugy" — mesma Central de Contas do celular). A conta precisa ser profissional.
2. Repita o passo 3 da Etapa 5: `me/accounts` → localize essa página → `{id-da-pagina}?fields=instagram_business_account` → copie o `id`.
3. Crie o secret **`IG_USER_ID2`** com esse id. Se a página for administrada por outra conta/token, crie também **`IG_TOKEN2`**; senão, o `IG_TOKEN` principal é reaproveitado (basta o mesmo perfil pessoal administrar as duas páginas).
4. Rode o workflow do Instagram — o seletor @solugyoficial / @edimariosolugy aparece sozinho na aba.

---

## Resumo do funcionamento automático

| O quê | Frequência | Como |
|---|---|---|
| Notícias dos 20 setores | de hora em hora (06–20h BRT, seg–sáb) | GitHub Actions + Google News |
| Funil + indicadores mensais | de hora em hora (06:15–20:15) | GitHub Actions + Microsoft Graph (planilha no OneDrive) |
| Publicação no Azure | a cada mudança | Deploy automático no push |
| Indicadores de mercado (sectors.js) | manual | editar e dar push |

## Problemas comuns

- **Workflow vermelho na sincronização**: confira se o TI deu *Grant admin consent* e se `SP_FILE_PATH` está exatamente igual ao caminho no OneDrive (com acentos e espaços).
- **Painel pede login em loop**: limpe cookies do domínio ou verifique o Role management.
- **"Bem-vindo" sem nome**: só acontece se abrir o `index.html` localmente (sem Azure) — na URL publicada o nome vem do login.
- **Estourou os minutos do Actions**: reduza a janela dos crons (ex.: a cada 2h: `0 9-23/2 * * 1-6`).
