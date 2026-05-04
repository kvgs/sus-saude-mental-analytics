# 🧠 Análise de Saúde Mental no SUS — SP

Projeto de análise de dados em saúde mental no estado de São Paulo, integrando nove fontes públicas do DATASUS, IBGE, SINAN e PNADC. Combina engenharia de dados, análise exploratória, estatística, equidade e visualização geoespacial para gerar insights sobre internações psiquiátricas, atendimentos ambulatoriais, suicídios, violência e desigualdades raciais e de gênero no sistema de saúde mental paulista.

> **Pipeline de dados:** [sus-data-pipeline](https://github.com/kvgs/sus-data-pipeline) — repositório com a arquitetura AWS S3 + Athena + dbt que alimenta este projeto.

## 📊 Fontes de Dados

| Dataset | Descrição | Período | Volume |
|---------|-----------|---------|--------|
| **SIH/DATASUS** | Internações psiquiátricas (ESPEC=05 ou CID F*) | 2015–2025 | ~1.1M internações |
| **CNES** | Estabelecimentos de saúde mental (CAPS, hospitais) | 2018–2025 | snapshot anual |
| **SIM** | Óbitos por suicídio (CID X60–X84) | 2018–2024 | ~18k óbitos |
| **RAAS** | Atendimentos ambulatoriais nos CAPS | 2018–2025 | ~33M atendimentos |
| **Censo 2022 (IBGE)** | População, favelas e demografia por município | 2022 | 645 municípios SP |
| **Estimativas Pop. IBGE** | População estimada por município por ano | 2015–2025 | 5.160 registros |
| **SINAN Violência** | Notificações de violência doméstica e autoprovocada | 2015–2025 | ~1.18M notificações |
| **PNADC (Base dos Dados)** | Microdados de renda, emprego e escolaridade SP | 2015–2023 | 358k registros |
| **Censo 2022 Demográfico** | População por município, idade, sexo e raça | 2022 | 270k registros |

## 🗂️ Estrutura do Projeto
```
sus-saude-mental-analytics/
├── notebooks/
│   ├── 01_etl_exploratory.ipynb  — inventário, validação e análise exploratória
│   └── 02_statistical.ipynb      — testes estatísticos, equidade, cruzamentos e mapas
├── output/                        — gráficos PNG e mapas HTML interativos
├── athena_client.py               — módulo de conexão com AWS Athena
└── requirements.txt
```
## 🔍 Principais Achados

**Evolução temporal (2015–2025)**
- Tendência secular de queda de 3.319 internações/ano — já existia antes da pandemia
- Pandemia causou queda adicional de 26.466 internações/ano (DiD, p=0.019)
- ~53.000 internações não realizadas em 2020-2021
- Desinstitucionalização confirmada: -0.65 dias de internação/ano (r=-0.991, p<0.001)
- CAPS cresceram 34.7% (2018–2025) — único sistema que superou o nível pré-pandemia
- Suicídios cresceram 20.3% (2018–2024) com pico em 2022

**Sexo**
- Proporção feminina nas internações cresce consistentemente (r=0.873, p<0.001)
- Gap no suicídio: 3.60x mais masculino (p<0.001)
- Mulheres: bipolar mania grave (+11.3pp) e transt. personalidade borderline (+4.8pp)
- Homens: múltiplas drogas (+12.7pp) e dependência álcool (+12.3pp)

**Raça/cor**
- Distribuição racial mudou significativamente (χ²=6903, p<0.001)
- Parda: 24% (2015) → 35.7% (2025) — crescimento de 11.7pp em 11 anos
- Branca: 65.2% (2015) → 54.4% (2025) — queda de 10.8pp
- Pardos com mais Psicose NE (+4.6pp) — possível acesso tardio e diagnóstico impreciso
- Depressão grave: taxa de óbito parda 2.8x maior que branca

**Diagnósticos**
- Esquizofrenia paranoide lidera: 150k+ internações (2015–2025)
- Dias de internação diferem significativamente por diagnóstico (H=90668, p<0.001)
- Esquizofrenia residual: 31 dias mediana | Depressão grave: 7 dias
- Demência NE: taxa de óbito 1.75% — mais letal

**Desigualdade de renda (PNADC)**
- Branca R$3.9k vs Parda R$2.4k vs Preta R$2.6k (2023)
- Gap de gênero: masculino ~33% acima do feminino em todas as raças
- Pior combinação: mulher parda — R$2.040/mês

**Municípios**
- % Favelas x Taxa suicídio: r=-0.181, p=0.004 — paradoxo da integração social
- Interior do estado com taxas de suicídio mais altas que a capital
- CAPS concentrados na RMSP — lacuna de cobertura no interior

## 📈 Outputs

**Gráficos (PNG):**
- Evolução temporal dos quatro sistemas (2015–2025)
- Análise por sexo com tendências
- Top 15 diagnósticos e taxa de óbito
- Análise de suicídios por método e sexo
- Atendimentos CAPS por tipo
- Violência SINAN por tipo e sexo
- Desigualdade de renda PNADC por raça e sexo
- Análise por raça/cor e faixa etária
- Equidade racial e por sexo nos diagnósticos
- DiD — efeito da pandemia
- Sazonalidade mensal
- Cruzamentos entre datasets

**Mapas interativos (HTML):**
- Taxa de internação psiquiátrica por município
- Taxa de suicídio por município
- Cobertura de CAPS por município
- CAPS x Taxa de internação (scatter interativo)
- Correlações por município

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.12 (pandas, numpy, matplotlib, seaborn, plotly, scipy, statsmodels, folium)
- **Dados:** AWS Athena via PyAthena
- **Estatística:** scipy, statsmodels (Mann-Whitney, Kruskal-Wallis, qui-quadrado, regressão OLS, DiD)
- **Geoespacial:** Folium + GeoJSON IBGE
- **Versionamento:** Git/GitHub

## 🚀 Como Reproduzir

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

## 👩‍💻 Autora

**Kelli Vasconcelos** — [LinkedIn](https://www.linkedin.com/in/kellivgs/) | [GitHub](https://github.com/kvgs)