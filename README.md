# 🧠 Análise de Internações Psiquiátricas no SUS
**Estado de São Paulo | 2017–2023**

## Motivação
A saúde mental é uma das áreas mais negligenciadas da saúde pública brasileira.
Este projeto analisa 546.737 internações psiquiátricas no SUS paulista entre 2017 e 2023,
período que inclui a pandemia de COVID-19 e seus impactos no acesso ao cuidado em saúde mental.

## Fonte dos Dados
DATASUS — Sistema de Informações Hospitalares (SIH)
Grupo RD (AIH Reduzida) — Estado de São Paulo

## Tecnologias
- **Python:** pandas, scipy, statsmodels, matplotlib, seaborn, plotly
- **ETL:** PySUS, PyArrow
- **Visualização:** Streamlit
- **Versionamento:** Git/GitHub

## Principais Achados

### 📉 Impacto da Pandemia
- Queda de 19% nas internações mensais durante a pandemia (7.124 → 5.774/mês)
- Redução estatisticamente significativa (p < 0,001, Cohen's d = 1,11)
- Em 2023 o volume ainda não retornou ao nível pré-pandemia

### 🔍 Perfil dos Diagnósticos
- Transtornos por uso de substâncias: diagnóstico mais frequente (33% do total)
- Psicoses (esquizofrenia): segundo mais frequente, com maior tempo de internação
- Transtornos de humor: queda menor durante a pandemia — casos graves continuaram sendo atendidos
- Transtornos por uso de substâncias: único grupo que superou o nível pré-pandemia no pós-pandemia

### 👥 Perfil por Sexo
- Homens representam 61% das internações
- Transtornos por uso de substâncias: 4x mais internações masculinas
- Transtornos de humor: 2x mais internações femininas

### 📅 Sazonalidade
- Picos em Janeiro e Agosto — útil para planejamento de capacidade hospitalar
- Padrão sazonal consistente ao longo de todos os anos analisados

### 📊 Inferência Bayesiana
- Transtornos orgânicos: taxa de óbito aumentou após pandemia (1,20% → 1,57%)
- Maioria dos diagnósticos manteve taxa de óbito estável

## Como Reproduzir
```bash
git clone https://github.com/kvgs/sus-saude-mental-analytics
cd sus-saude-mental-analytics
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Rodando o Dashboard
```bash
cd dashboard
streamlit run app.py
```

## Status
- [x] ETL — coleta e limpeza dos dados
- [x] Análise exploratória
- [x] Testes de hipótese e poder estatístico
- [x] Série temporal e sazonalidade
- [x] Teste A/B simulado
- [x] Inferência bayesiana
- [x] Dashboard Streamlit
- [ ] Mapa por município
- [ ] Comparativo com dados populacionais IBGE