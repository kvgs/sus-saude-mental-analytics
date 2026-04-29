# 🧠 Análise de Saúde Mental no SUS — SP

Projeto de análise de dados em saúde mental no estado de São Paulo, integrando cinco fontes públicas do DATASUS e IBGE. O projeto combina engenharia de dados, análise exploratória, estatística e visualização para gerar insights sobre internações psiquiátricas, atendimentos ambulatoriais, suicídios e infraestrutura de saúde mental.

> **Pipeline de dados:** [sus-data-pipeline](https://github.com/kvgs/sus-data-pipeline) — repositório com a arquitetura AWS + dbt que alimenta este projeto.

## 📊 Fontes de Dados

| Dataset | Descrição | Período | Volume |
|---------|-----------|---------|--------|
| **SIH/DATASUS** | Internações psiquiátricas (ESPEC=05 ou CID F*) | 2018–2025 | ~708k internações |
| **CNES** | Estabelecimentos de saúde mental (CAPS, hospitais) | 2018–2025 | snapshot anual |
| **SIM** | Óbitos por suicídio (CID X60–X84) | 2018–2024 | ~18k óbitos |
| **RAAS** | Atendimentos ambulatoriais nos CAPS | 2018–2025 | ~33M atendimentos |
| **Censo 2022 (IBGE)** | População e domicílios em favelas por município | 2022 | 645 municípios SP |

## 🗂️ Estrutura do Projeto
```
sus-saude-mental-analytics/
├── notebooks/
│   ├── 01_etl.ipynb           — conexão Athena, carregamento e notas metodológicas
│   └── 02_exploratory.ipynb   — análise exploratória completa
├── dashboard/
│   └── app.py                 — dashboard Streamlit (em desenvolvimento)
├── output/                    — gráficos e arquivos gerados
├── athena_client.py           — módulo de conexão com AWS Athena
└── requirements.txt
```
## 🔍 Principais Achados

**Evolução temporal**
- Queda de 28% nas internações em 2020 — serviços fecharam durante a pandemia
- CAPS se recuperaram mais rápido e cresceram 35% acima do nível pré-pandemia
- Suicídios não caíram em 2020 — cresceram durante toda a pandemia até 2022

**Sexo**
- Internações: 61.6% masculino / 38.4% feminino — estável no período
- Suicídios: 78.3% masculino / 21.7% feminino
- Suicídio feminino cresceu 26.8% vs 18.5% masculino (2018→2024)

**Diagnósticos**
- Múltiplas drogas lidera com 103k internações (2018–2025)
- Demência não especificada (F03) tem taxa de óbito de 2% — 7x acima da média
- F29 (Psicose NE) em 4º lugar indica subqualidade no registro diagnóstico

**Suicídios**
- Pico em 2022 (2.923 casos) com queda gradual até 2024 (2.656)
- Enforcamento responde por mais de 50% dos casos em todos os anos
- Crescimento de 32% entre 2018 e 2022

**CAPS e infraestrutura**
- Uso de drogas caiu de 33% para 17.6% dos atendimentos (2018→2025)
- Pessoas em situação de rua: pico de 198k atendimentos em 2024
- Correlação não significativa entre CAPS e taxa de internação por município

**Raça/cor**
- Parda com maior crescimento proporcional: +52% (2018→2025)
- População preta sub-representada nas internações
- Taxa de óbito similar entre raças — perfil diagnóstico diferente explica

**Faixa etária**
- 30-44 anos: faixa com mais internações (244k no período)
- 75+: taxa de óbito 24x maior que 18-29 anos (2.68% vs 0.11%)
- Idosos 60-74 e 75+ com queda consistente — tendência de desinstitucionalização

## 🛠️ Stack Tecnológica

- **Linguagem:** Python (pandas, numpy, matplotlib, seaborn, plotly, scipy)
- **Dados:** AWS Athena via PyAthena
- **Visualização:** Matplotlib, Seaborn, Plotly (interativo)
- **Dashboard:** Streamlit (em desenvolvimento)
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

## 📅 Próximos passos

- [ ] `03_statistical.ipynb` — testes de hipótese e análise estatística
- [ ] `04_equidade.ipynb` — análise de equidade por raça, gênero e faixa etária
- [ ] `05_cruzamentos.ipynb` — cruzamentos entre os datasets
- [ ] `06_geoespacial.ipynb` — mapas com GeoPandas e Folium
- [ ] Dashboard Streamlit completo com todas as análises

## 👩‍💻 Autora

**Kelli Vasconcelos** — [LinkedIn](https://www.linkedin.com/in/kellivgs/) | [GitHub](https://github.com/kvgs)