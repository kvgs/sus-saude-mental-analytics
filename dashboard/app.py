import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# configuração da página
st.set_page_config(
    page_title="Saúde Mental no SUS",
    page_icon="🧠",
    layout="wide"
)

# carregar dados
@st.cache_data
def load_data():
    return pd.read_parquet('../data/processed/internacoes_psiquiatricas.parquet')

df = load_data()

# header
st.title("🧠 Internações Psiquiátricas no SUS")
st.markdown("**Estado de São Paulo | 2017–2023**")
st.markdown("---")

# aviso de desenvolvimento
st.warning("""
⚠️ **Dashboard em construção**
Este painel está em desenvolvimento ativo. Próximas versões incluirão:
- Análise estatística interativa (testes de hipótese)
- Mapa de internações por município
- Decomposição de série temporal
- Comparativo com dados populacionais do IBGE
""")

# sidebar — filtros
st.sidebar.header("Filtros")

periodo = st.sidebar.multiselect(
    "Período",
    options=['Pré-pandemia', 'Pandemia', 'Pós-pandemia'],
    default=['Pré-pandemia', 'Pandemia', 'Pós-pandemia']
)

diagnostico = st.sidebar.multiselect(
    "Diagnóstico",
    options=sorted(df['GRUPO_DIAG'].unique()),
    default=sorted(df['GRUPO_DIAG'].unique())
)

sexo = st.sidebar.multiselect(
    "Sexo",
    options=['Masculino', 'Feminino'],
    default=['Masculino', 'Feminino']
)

# aplicar filtros
df_filtrado = df[
    df['PERIODO'].isin(periodo) &
    df['GRUPO_DIAG'].isin(diagnostico) &
    df['SEXO'].isin(sexo)
]

# KPIs
st.subheader("Visão Geral")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Internações", f"{len(df_filtrado):,}")
col2.metric("Média de Dias Internado", f"{df_filtrado['DIAS_PERM'].median():.0f} dias")
col3.metric("Taxa de Óbito", f"{df_filtrado['MORTE'].astype(float).mean():.2%}")
col4.metric("Custo Médio por Internação", f"R$ {df_filtrado['VAL_TOT'].mean():,.2f}")

st.markdown("---")

# gráficos — linha 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Evolução Anual")
    evolucao = df_filtrado.groupby('ANO').size().reset_index(name='total')
    fig = px.line(evolucao, x='ANO', y='total',
                  markers=True, color_discrete_sequence=['steelblue'])
    fig.update_layout(xaxis_title='Ano', yaxis_title='Internações')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Por Diagnóstico")
    diag = df_filtrado.groupby('GRUPO_DIAG').size().reset_index(name='total').sort_values('total')
    fig = px.bar(diag, x='total', y='GRUPO_DIAG',
                 orientation='h', color_discrete_sequence=['steelblue'])
    fig.update_layout(xaxis_title='Total', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# gráficos — linha 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Por Sexo e Diagnóstico")
    sexo_diag = df_filtrado.groupby(['GRUPO_DIAG', 'SEXO']).size().reset_index(name='total')
    fig = px.bar(sexo_diag, x='GRUPO_DIAG', y='total', color='SEXO',
                 barmode='group',
                 color_discrete_map={'Masculino': 'steelblue', 'Feminino': 'coral'})
    fig.update_layout(xaxis_tickangle=45, xaxis_title='', yaxis_title='Internações')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Tempo Médio de Internação")
    tempo = df_filtrado.groupby('GRUPO_DIAG')['DIAS_PERM'].median().reset_index()
    tempo.columns = ['GRUPO_DIAG', 'mediana_dias']
    tempo = tempo.sort_values('mediana_dias')
    fig = px.bar(tempo, x='mediana_dias', y='GRUPO_DIAG',
                 orientation='h', color_discrete_sequence=['coral'])
    fig.update_layout(xaxis_title='Mediana de dias', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# gráfico linha 3 — raça/cor
st.subheader("Por Raça/Cor")
raca = df_filtrado[df_filtrado['RACA_COR'] != 'Ignorado']
raca = raca.groupby('RACA_COR').size().reset_index(name='total').sort_values('total', ascending=False)
fig = px.bar(raca, x='RACA_COR', y='total',
             color_discrete_sequence=['steelblue'])
fig.update_layout(xaxis_title='', yaxis_title='Internações')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Fonte: DATASUS — Sistema de Informações Hospitalares (SIH) | Desenvolvido por Kelli Vasconcelos")