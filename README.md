# Análise de Saúde Mental no SUS — SP

Projeto de análise de dados em saúde mental no estado de São Paulo, integrando nove fontes públicas do DATASUS, IBGE, SINAN e PNADC. Combina engenharia de dados, estatística epidemiológica e visualização para analisar internações psiquiátricas, atendimentos ambulatoriais, suicídios, tentativas de suicídio e desigualdades raciais e de gênero no sistema de saúde mental paulista.

> **Pipeline de dados:** [sus-data-pipeline](https://github.com/kvgs/sus-data-pipeline) — repositório com a arquitetura AWS S3 + Athena + dbt que alimenta este projeto.

## Fontes de Dados

| Dataset | Descrição | Período | Volume |
|---------|-----------|---------|--------|
| **SIH/DATASUS** | Internações psiquiátricas (ESPEC=05 ou CID F*) | 2015–2025 | ~1,05M internações |
| **SIM/DATASUS** | Óbitos por suicídio (CID X60–X84) | 2018–2024 | ~18k óbitos |
| **RAAS/DATASUS** | Atendimentos ambulatoriais nos CAPS | 2018–2025 | ~9M atendimentos |
| **SINAN/DATASUS** | Notificações de violência e lesão autoprovocada | 2015–2025 | ~1,18M notificações |
| **CNES/DATASUS** | Estabelecimentos de saúde mental | 2018–2025 | snapshot anual |
| **Estimativas Pop. IBGE** | População estimada por município por ano | 2015–2025 | 645 municípios × 11 anos |
| **Censo 2022 (IBGE)** | Domicílios em favelas e demografia por município | 2022 | 645 municípios SP |
| **Censo 2022 Demográfico** | População por município, idade, sexo e raça | 2022 | 270k registros |
| **PNADC (IBGE)** | Microdados de renda e emprego SP, com peso amostral | 2015–2023 | 358k registros |

## Estrutura do Projeto
```
sus-saude-mental-analytics/
├── notebooks/
│   ├── 01_etl_exploratory.ipynb   — inventário, validação e análise exploratória
│   └── 02_statistical.ipynb       — análise estatística completa (v3)
├── dashboard/
│   └── app.py                     — dashboard Streamlit com dados ao vivo via Athena
├── output/                        — gráficos PNG, mapas HTML e tabela suplementar FDR
├── athena_client.py               — módulo de conexão com AWS Athena
└── requirements.txt
```
## Análises — notebook 02_statistical.ipynb (v3)

O notebook segue o padrão de publicação acadêmica: cada análise tem célula markdown com contexto metodológico, código e insight interpretativo. Correção FDR de Benjamini-Hochberg aplicada globalmente a 77 testes — nenhum resultado significativo foi invalidado.

| Célula | Análise | Método principal |
|--------|---------|-----------------|
| 2 | Perfil descritivo da amostra (Tabela 1) | Mediana + IQR |
| 3 | Tendência temporal das internações | Regressão de Poisson + teste de overdispersion |
| 4 | Efeito da pandemia | Série Temporal Interrompida (ITS) com erros robustos HC3 |
| 5 | Diferenças por sexo | Z-test de proporções + OR por diagnóstico |
| 6 | Composição racial | Spearman + decomposição de Kitagawa (PNADC como denominador) |
| 7 | Tempo até a alta | Kaplan-Meier + Cox multivariado |
| 8 | Risco de óbito intra-hospitalar | Regressão logística (AUC = 0,841) |
| 9 | Equidade diagnóstica: raça × CID | χ² + V de Cramér + resíduos padronizados |
| 10 | Equidade diagnóstica: sexo × CID | χ² + V de Cramér + OR por diagnóstico |
| 11 | Tentativas de suicídio e métodos | SINAN vs SIM + χ² por sexo e método |
| 12 | Óbitos por suicídio | Tendência temporal por sexo e raça |
| 13 | Atendimentos nos CAPS | Tendência + proporção por sexo |
| 14 | Análise municipal | Correlação ecológica + mapas Folium |
| 15 | Correção FDR | Benjamini-Hochberg (77 testes) |

## Principais Achados

**Tendência temporal (2015–2025)**
- Queda de 0,80%/mês nas internações antes da pandemia (ITS, p = 0,005)
- Pandemia causou queda adicional imediata de 21,5% em março/2020 (IRR = 0,785)
- A partir de 2022, crescimento de 4,1%/ano — recuperação além da tendência pré-pandemia
- Mediana de dias de internação caiu de 28 para 13 dias em dez anos (r = −0,991, p < 0,001)
- Suicídios cresceram 20,3% entre 2018 e 2024, com pico em 2022
- CAPS cresceram 56,3% entre 2018 e 2025 (r = +0,976, p < 0,001)

**Sexo**
- Homens representam 62% das internações; proporção feminina cresceu de 37,1% para 38,4% (r = +0,873, p < 0,001)
- Transtornos por substâncias dominam internações masculinas (41,9% do total masculino)
- Transtornos de humor dominam internações femininas (bipolar mania grave: OR = 3,96; borderline: OR = 6,50)
- Após controle multivariado, mulheres têm alta 8,5% mais rápida que homens (HR = 1,085, p < 0,001)
- Mulheres representam 69% das tentativas de suicídio e 21,7% dos óbitos — paradoxo explicado pelo método

**Raça**
- Decomposição de Kitagawa: 104,8% da variação na taxa de internação explicada pelo efeito de taxa — não demográfico
- Taxa preta convergiu com taxa branca: 456/100k (2015) → 210/100k (2023); branca: 260 → 187/100k
- Após controle multivariado, pardos têm alta 12% mais rápida que brancos (HR = 1,120, p < 0,001)
- Pardos com excesso de Psicose NE (resíduo = +37,5) e déficit de esquizofrenia residual (−44,3) — padrão consistente com acesso tardio ao sistema

**Risco de óbito intra-hospitalar**
- Taxa de 0,27% (2.870 óbitos em 1.049.790 internações)
- Idosos ≥ 60 anos têm risco 10× maior que adultos de 30–44 anos (OR = 10,072)
- Cada dia adicional de internação reduz o risco em 9,3% — óbitos ocorrem no início da internação
- Risco caiu 3% ao ano entre 2015 e 2025 (OR = 0,970, p < 0,001)
- AUC = 0,841

**Municípios**
- % domicílios em favelas × taxa de suicídio: r = −0,241, p < 0,001 — único par significativo após correção de Bonferroni local
- Densidade de CAPS não se correlaciona com taxa de internação em nível municipal (r = 0,041, ns)

## Stack Tecnológica

- **Linguagem:** Python 3.12
- **Dados:** AWS Athena via PyAthena
- **Análise estatística:** scipy, statsmodels, lifelines
- **Visualização:** matplotlib, seaborn, plotly, folium
- **Dashboard:** Streamlit com conexão ao vivo via Athena
- **Versionamento:** Git/GitHub

## Como Reproduzir

### Pré-requisitos
- Python 3.12+
- AWS CLI configurado com acesso ao Athena
- Pipeline [sus-data-pipeline](https://github.com/kvgs/sus-data-pipeline) configurado

### Instalação

```bash
git clone https://github.com/kvgs/sus-saude-mental-analytics
cd sus-saude-mental-analytics
pip install -r requirements.txt
```

### Executar notebooks

```bash
jupyter notebook notebooks/
```

### Executar dashboard

```bash
cd dashboard
streamlit run app.py
```

## Autora

**Kelli Vasconcelos** — [LinkedIn](https://www.linkedin.com/in/kellivgs/) | [GitHub](https://github.com/kvgs)