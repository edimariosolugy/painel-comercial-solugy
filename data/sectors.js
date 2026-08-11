// ============================================================
// PAINEL SETORIAL SOLUGY — Dados dos 20 setores-alvo
// Edite este arquivo para atualizar indicadores e destaques.
// Última revisão: agosto/2026
// ============================================================
window.SECTORS = [
  {
    id: 1, nome: "Agronegócio", slug: "agronegocio",
    crescimento: "+7% em contratações de crédito (jul/25–fev/26)",
    investimento: "R$ 605,2 bi — Plano Safra 2025/26 (recorde)",
    valorBi: 605.2, moeda: "R$",
    destaques: ["R$ 516,2 bi agricultura empresarial + R$ 89 bi agricultura familiar", "R$ 101,5 bi destinados a investimentos", "Plano Safra 2026/27 já anunciado: R$ 525,1 bi"],
    tendencias: ["Etanol de milho", "Agricultura de precisão", "Irrigação e armazenagem"],
    newsQuery: "investimento agronegócio Brasil"
  },
  {
    id: 2, nome: "Alimentos e Bebidas", slug: "alimentos-bebidas",
    crescimento: "+8% no faturamento (R$ 1,39 tri em 2025 — 10,9% do PIB)",
    investimento: "R$ 120 bi até 2026 (ABIA) — 97% já executado",
    valorBi: 120, moeda: "R$",
    destaques: ["R$ 75 bi em expansão e modernização de plantas", "R$ 45 bi em pesquisa e desenvolvimento", "Emprego no setor cresce 2,4% (2,1 mi trabalhadores)"],
    tendencias: ["Alimentos saudáveis/proteína", "Automação de plantas", "Exportação em alta"],
    newsQuery: "investimento indústria alimentos bebidas Brasil"
  },
  {
    id: 3, nome: "Automotivo e Autopeças", slug: "automotivo",
    crescimento: "Produção +3,7% em 2026 (2,74 mi un.); vendas +12,1%",
    investimento: "R$ 140 bi anunciados pelas montadoras",
    valorBi: 140, moeda: "R$",
    destaques: ["Eletrificados: +60,8% e 11,2% de participação", "Move Brasil: R$ 10 bi em crédito para renovação de frota", "Mercado deve superar 3 mi de veículos vendidos (maior desde 2014)"],
    tendencias: ["Eletrificação/híbridos", "Nearshoring de autopeças", "Pressão de importados"],
    newsQuery: "investimento montadoras autopeças Brasil"
  },
  {
    id: 4, nome: "Bioenergia e Sucroenergético", slug: "bioenergia",
    crescimento: "Etanol de milho +15,5% (9,5 bi litros)",
    investimento: "R$ 106,7 bi previstos 2026–2035 (EPE)",
    valorBi: 106.7, moeda: "R$",
    destaques: ["Produção de 36 bi de litros de etanol na safra 25/26", "Exportações de açúcar e etanol: US$ 14,3 bi", "Proposta de gasolina E32 e autossuficiência"],
    tendencias: ["Etanol de milho", "Biometano/biogás", "SAF (combustível de aviação)"],
    newsQuery: "investimento usina etanol bioenergia Brasil"
  },
  {
    id: 5, nome: "Cimento e Materiais de Construção", slug: "cimento",
    crescimento: "Consumo de cimento +3,7% (66,9 Mt em 2025)",
    investimento: "R$ 27,5 bi da indústria de cimento (2023–2027)",
    valorBi: 27.5, moeda: "R$",
    destaques: ["Construção civil projeta +2% em 2026 (3º ano de alta)", "Impulso: MCMV, orçamento recorde FGTS e queda de juros", "Faturamento do cimento: ~R$ 27 bi/ano"],
    tendencias: ["Habitação popular", "Cimento verde/CCUS", "Industrialização da construção"],
    newsQuery: "investimento cimento materiais construção Brasil"
  },
  {
    id: 6, nome: "Comércio e Distribuição", slug: "comercio",
    crescimento: "Varejo em expansão moderada com juros em queda",
    investimento: "Investimentos em CDs, logística e digitalização",
    valorBi: null, moeda: "R$",
    destaques: ["Consolidação de atacarejo e farma", "Expansão de centros de distribuição automatizados", "Integração omnichannel e last-mile"],
    tendencias: ["Atacarejo", "E-commerce/quick commerce", "Automação de CDs"],
    newsQuery: "investimento varejo centro de distribuição Brasil"
  },
  {
    id: 7, nome: "Energia — Geração e Transmissão", slug: "energia-gt",
    crescimento: "Ciclo 2023–26: R$ 67,8 bi contratados, 19 mil km de linhas",
    investimento: "R$ 25+ bi em leilões de transmissão em 2026",
    valorBi: 25, moeda: "R$",
    destaques: ["Leilão mar/26: R$ 5,7 bi e 888 km em 12 estados", "2º leilão 2026: R$ 20+ bi e 3.500 km em estudo", "Foco em escoamento de renováveis"],
    tendencias: ["Expansão de transmissão", "Baterias/armazenamento", "Data centers como carga"],
    newsQuery: "leilão transmissão energia investimento Brasil"
  },
  {
    id: 8, nome: "Energia Solar e Renováveis", slug: "solar",
    crescimento: "+10,6 GW previstos em 2026",
    investimento: "R$ 300+ bi acumulados em solar no Brasil",
    valorBi: 300, moeda: "R$",
    destaques: ["Solar já superou R$ 300 bi em investimentos acumulados", "Desafio: curtailment e fluxo reverso na GD", "Híbridas solar+eólica+baterias ganham espaço"],
    tendencias: ["Armazenamento (BESS)", "Hidrogênio verde", "PPAs corporativos"],
    newsQuery: "investimento energia solar renovável Brasil"
  },
  {
    id: 9, nome: "Engenharia, EPC e Construção", slug: "epc",
    crescimento: "Infraestrutura: R$ 280 bi investidos em 2025 (+3%)",
    investimento: "Novo PAC: R$ 944,8 bi executados (ciclo 2023–26)",
    valorBi: 280, moeda: "R$",
    destaques: ["46,3% do investimento em infra de 2025 foi privado", "Novo PAC com 89,5% dos recursos executados", "Pacto Brasil: meta de infra a 4% do PIB até 2030"],
    tendencias: ["Concessões e PPPs", "Ferrovias e portos", "Transição para capital privado"],
    newsQuery: "investimento obras infraestrutura EPC Brasil"
  },
  {
    id: 10, nome: "Farmacêutico e Saúde", slug: "farma",
    crescimento: "+10,6% projetado para a indústria farmacêutica em 2026",
    investimento: "Mercado de ~R$ 257 bi em movimentação",
    valorBi: 257, moeda: "R$",
    destaques: ["Genéricos: 40%+ do mercado; economia de R$ 14,6 bi no 1T26", "Canetas emagrecedoras (GLP-1) puxam o crescimento", "Dermocosméticos e POC em expansão"],
    tendencias: ["GLP-1/emagrecedores", "Genéricos e biossimilares", "Dermocosméticos"],
    newsQuery: "investimento indústria farmacêutica saúde Brasil"
  },
  {
    id: 11, nome: "Fertilizantes e Agroquímicos", slug: "fertilizantes",
    crescimento: "Demanda recorde puxada pela safra",
    investimento: "Plano Nacional de Fertilizantes 2050 em execução",
    valorBi: null, moeda: "R$",
    destaques: ["Meta PNF: reduzir dependência de importação (~85%) para 45% até 2050", "Retomada de unidades de nitrogenados", "Novos projetos de fosfato e potássio"],
    tendencias: ["Bioinsumos", "Fertilizantes especiais", "Nacionalização da produção"],
    newsQuery: "investimento fertilizantes agroquímicos Brasil"
  },
  {
    id: 12, nome: "Indústria Geral", slug: "industria-geral",
    crescimento: "Recuperação gradual da atividade industrial",
    investimento: "Nova Indústria Brasil: financiamento bilionário até 2026",
    valorBi: null, moeda: "R$",
    destaques: ["Depreciação acelerada incentiva renovação de máquinas", "Reindustrialização e adensamento de cadeias", "Eficiência energética como prioridade"],
    tendencias: ["Indústria 4.0", "Eficiência energética", "Descarbonização"],
    newsQuery: "investimento indústria fábrica Brasil"
  },
  {
    id: 13, nome: "Logística e Distribuição", slug: "logistica",
    crescimento: "Modernização acelerada de portos, ferrovias e rodovias",
    investimento: "R$ 47 bi em portos até 2026 (Novo PAC)",
    valorBi: 47, moeda: "R$",
    destaques: ["R$ 42,5 bi privados + R$ 4,7 bi públicos em portos", "Novas concessões rodoviárias e ferroviárias", "CDs automatizados e malha multimodal"],
    tendencias: ["Multimodalidade", "Automação logística", "Concessões privadas"],
    newsQuery: "investimento logística portos ferrovia Brasil"
  },
  {
    id: 14, nome: "Máquinas e Equipamentos Industriais", slug: "maquinas",
    crescimento: "Retomada com depreciação acelerada e queda de juros",
    investimento: "Setor de ~9.000 empresas (ABIMAQ)",
    valorBi: null, moeda: "R$",
    destaques: ["Demanda por PMOC e equipamentos de processo", "Renovação de parque fabril incentivada", "Exportações buscando novos mercados"],
    tendencias: ["Automação/robótica", "Retrofit de máquinas", "Serviços e locação"],
    newsQuery: "investimento máquinas equipamentos industriais Brasil"
  },
  {
    id: 15, nome: "Mineração", slug: "mineracao",
    crescimento: "Faturamento R$ 77,9 bi no 1T26 (+6% a/a)",
    investimento: "US$ 76,9 bi previstos 2026–2030 (IBRAM, +12,5%)",
    valorBi: 415, moeda: "US$ 76,9 bi",
    destaques: ["US$ 21,3 bi para minerais críticos (lítio, cobre, níquel, terras raras, grafita, manganês)", "Minério de ferro segue concentrando aportes — pequenas usinas em expansão", "Ouro e transição energética atraem novos projetos"],
    tendencias: ["Minerais críticos", "Transição energética", "Descarbonização de minas"],
    newsQuery: "investimento mineração minerais críticos Brasil"
  },
  {
    id: 16, nome: "Papel e Celulose", slug: "papel-celulose",
    crescimento: "Produção de celulose +6,9% (29,4 Mt — recorde)",
    investimento: "R$ 105 bi até 2028",
    valorBi: 105, moeda: "R$",
    destaques: ["Arauco R$ 25 bi, CMPC R$ 25 bi, Suzano R$ 22,2 bi, Bracell R$ 5 bi", "Exportações recorde: 20,7 Mt (+11,6%)", "36 mil empregos na construção dos projetos"],
    tendencias: ["Novas plantas de celulose", "Embalagens sustentáveis", "Bioprodutos"],
    newsQuery: "investimento papel celulose fábrica Brasil"
  },
  {
    id: 17, nome: "Química e Gases Industriais", slug: "quimica",
    crescimento: "+22,8% no 1T26 — sinais de revitalização",
    investimento: "Presiq: potencial de +R$ 112 bi ao PIB (2027–31)",
    valorBi: null, moeda: "R$",
    destaques: ["Governo triplica incentivo fiscal ao setor químico", "Braskem, Innova, OCQ e Unipar com projetos em implantação", "Mercado livre de gás reduz custo de matéria-prima"],
    tendencias: ["Presiq/REIQ", "Gás natural competitivo", "Química verde"],
    newsQuery: "investimento indústria química gases industriais Brasil"
  },
  {
    id: 18, nome: "Saneamento", slug: "saneamento",
    crescimento: "Investimento anual +51% após o Marco Legal",
    investimento: "R$ 58,4 bi em leilões e PPPs — 625 municípios",
    valorBi: 58.4, moeda: "R$",
    destaques: ["Portfólio atende 18+ mi de pessoas; 4 grandes PPPs em 2026 (R$ 20,3 bi, 477 municípios)", "UTRs (tratamento de resíduos), abastecimento de água e esgotamento", "2020–24: R$ 112,6 bi investidos; meta de universalização até 2033"],
    tendencias: ["PPPs municipais", "UTR / resíduos", "Universalização água e esgoto"],
    newsQuery: "investimento saneamento leilão concessão Brasil"
  },
  {
    id: 19, nome: "Siderurgia e Metalurgia", slug: "siderurgia",
    crescimento: "Margens em recuperação gradual",
    investimento: "Expansões e modernização em curso",
    valorBi: null, moeda: "R$",
    destaques: ["Pressão de aço importado mantém defesa comercial em pauta", "Gerdau e Usiminas com melhora de margens", "Aço verde e fornos elétricos em avaliação"],
    tendencias: ["Defesa comercial", "Aço verde/H2", "Reciclagem de sucata"],
    newsQuery: "investimento siderurgia metalurgia aço Brasil"
  },
  {
    id: 20, nome: "Odontologia", slug: "odontologia",
    crescimento: "+13% a.a. projetado até 2030",
    investimento: "Mercado de ~R$ 38 bi/ano",
    valorBi: 38, moeda: "R$",
    destaques: ["Faturamento de clínicas: US$ 4,6 bi → US$ 6,9 bi até 2030", "Brasil lidera potencial tecnológico na América Latina", "Consolidação de redes e digitalização"],
    tendencias: ["CAD/CAM e impressão 3D", "Scanners intraorais", "Estética e alinhadores"],
    newsQuery: "investimento mercado odontológico equipamentos Brasil"
  }
];
window.SECTORS_META = {
  atualizadoEm: "2026-08-10",
  notaCambio: "Valores em US$ convertidos a R$ 5,40 apenas para o ranking comparativo."
};
