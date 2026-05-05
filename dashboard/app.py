import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import os
import sys

# Funciona tanto localmente quanto no Streamlit Cloud
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from athena_client import query

st.set_page_config(
    page_title="Saúde Mental no SUS — SP",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Source+Sans+3:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }

.hero { padding: 3rem 0 2rem 0; border-bottom: 1px solid #e8e4df; margin-bottom: 2.5rem; }
.hero-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #c0392b; font-weight: 500; margin-bottom: 0.8rem; }
.hero-title { font-family: 'Source Serif 4', serif; font-size: 2.8rem; font-weight: 300; color: #1a1a1a; line-height: 1.2; margin-bottom: 1rem; }
.hero-deck { font-size: 1rem; font-weight: 300; color: #555; line-height: 1.7; max-width: 780px; margin-bottom: 1rem; }
.hero-byline { font-size: 0.78rem; color: #999; letter-spacing: 0.05em; }

.section-divider { border: none; border-top: 1px solid #e8e4df; margin: 2.5rem 0; }

.chapter-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.15em; color: #c0392b; font-weight: 500; margin-bottom: 0.5rem; }
.chapter-title { font-family: 'Source Serif 4', serif; font-size: 1.7rem; font-weight: 300; color: #1a1a1a; margin-bottom: 0.8rem; line-height: 1.3; }
.chapter-intro { font-size: 1rem; color: #444; line-height: 1.8; max-width: 720px; margin-bottom: 1.5rem; font-weight: 300; }

.stat-callout { border-left: 3px solid #c0392b; padding: 1.2rem 1.5rem; margin: 1rem 0; background: #faf9f7; }
.stat-number { font-family: 'Source Serif 4', serif; font-size: 2.4rem; font-weight: 300; color: #c0392b; line-height: 1; margin-bottom: 0.3rem; }
.stat-label { font-size: 0.85rem; color: #666; line-height: 1.5; }

.note-box { background: #f5f3ef; border-top: 2px solid #1a1a1a; padding: 1.2rem 1.5rem; margin: 1.5rem 0; }
.note-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em; color: #888; margin-bottom: 0.5rem; }
.note-text { font-size: 0.92rem; color: #333; line-height: 1.75; }

.chart-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; margin-bottom: 0.3rem; }
.chart-title { font-family: 'Source Serif 4', serif; font-size: 1.05rem; font-weight: 300; color: #1a1a1a; margin-bottom: 0.8rem; line-height: 1.4; }
.source-note { font-size: 0.72rem; color: #aaa; margin-top: 0.3rem; font-style: italic; }

.methodology { background: #faf9f7; border: 1px solid #e8e4df; padding: 1.2rem 1.5rem; margin-top: 2rem; }
.methodology p { font-size: 0.8rem; color: #777; line-height: 1.7; margin: 0; }
</style>
""", unsafe_allow_html=True)


# ── CARGA DE DADOS ────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def carregar_dados():

    df_ano = query("""
        SELECT ano,
               COUNT(*) AS internacoes,
               SUM(obito) AS obitos,
               APPROX_PERCENTILE(CAST(dias_internacao AS double), 0.5) AS mediana_dias,
               SUM(CASE WHEN sexo = '1' THEN 1 ELSE 0 END) AS masculino,
               SUM(CASE WHEN sexo = '3' THEN 1 ELSE 0 END) AS feminino,
               SUM(CASE WHEN raca_cor = '01' THEN 1 ELSE 0 END) AS branca,
               SUM(CASE WHEN raca_cor = '03' THEN 1 ELSE 0 END) AS parda,
               SUM(CASE WHEN raca_cor = '02' THEN 1 ELSE 0 END) AS preta
        FROM sus_pipeline.sih_internacoes_psiquiatria
        WHERE ano NOT IN ('2026')
          AND dias_internacao > 0 AND dias_internacao < 365
          AND obito IN (0,1)
        GROUP BY ano ORDER BY ano
    """)
    df_ano['ano'] = df_ano['ano'].astype(int)
    for c in ['internacoes','obitos','mediana_dias','masculino','feminino',
              'branca','parda','preta']:
        df_ano[c] = pd.to_numeric(df_ano[c], errors='coerce')

    df_sim = query("""
        SELECT ano,
               SUM(CASE WHEN sexo='1' THEN 1 ELSE 0 END) AS masculino,
               SUM(CASE WHEN sexo='2' THEN 1 ELSE 0 END) AS feminino,
               COUNT(*) AS total
        FROM sus_pipeline.sim_suicidios
        WHERE sexo IN ('1','2')
        GROUP BY ano ORDER BY ano
    """)
    df_sim['ano'] = df_sim['ano'].astype(int)
    for c in ['masculino','feminino','total']:
        df_sim[c] = pd.to_numeric(df_sim[c], errors='coerce')

    df_caps = query("""
        SELECT ano,
               SUM(qtd_atendimentos) AS total,
               SUM(CASE WHEN sexo='M' THEN qtd_atendimentos ELSE 0 END) AS masculino,
               SUM(CASE WHEN sexo='F' THEN qtd_atendimentos ELSE 0 END) AS feminino
        FROM sus_pipeline.raas_atendimentos
        WHERE ano NOT IN ('2017','2026')
        GROUP BY ano ORDER BY ano
    """)
    df_caps['ano'] = df_caps['ano'].astype(int)
    for c in ['total','masculino','feminino']:
        df_caps[c] = pd.to_numeric(df_caps[c], errors='coerce')

    df_pop = query("""
        SELECT ano, SUM(populacao) AS populacao
        FROM sus_pipeline.ibge_populacao
        WHERE ano BETWEEN '2015' AND '2025'
        GROUP BY ano ORDER BY ano
    """)
    df_pop['ano']       = df_pop['ano'].astype(int)
    df_pop['populacao'] = pd.to_numeric(df_pop['populacao'], errors='coerce')

    df_sinan = query("""
        SELECT sexo,
               SUBSTR(TRIM(cid_circunstancia), 1, 3) AS cid3,
               COUNT(*) AS n
        FROM sus_pipeline.sinan_violencia_silver
        WHERE tentativa_suicidio = 1
          AND ano NOT IN ('2026')
          AND sexo IN ('M','F')
        GROUP BY sexo, SUBSTR(TRIM(cid_circunstancia), 1, 3)
    """)
    df_sinan['n'] = pd.to_numeric(df_sinan['n'], errors='coerce')

    return df_ano, df_sim, df_caps, df_pop, df_sinan


with st.spinner("Carregando dados..."):
    df_ano, df_sim, df_caps, df_pop, df_sinan = carregar_dados()

# Merge população
pop_map          = df_pop.set_index('ano')['populacao'].to_dict()
df_ano['pop']    = df_ano['ano'].map(pop_map)
df_ano['taxa']   = df_ano['internacoes'] / df_ano['pop'] * 100_000
df_sim['pop']    = df_sim['ano'].map(pop_map)
df_sim['taxa']   = df_sim['total'] / df_sim['pop'] * 100_000

# Métodos SINAN
METODO_MAP = {
    'X60':'Medicamentos','X61':'Medicamentos','X62':'Medicamentos',
    'X63':'Outras substâncias','X64':'Outras substâncias',
    'X65':'Outras substâncias','X66':'Outras substâncias',
    'X67':'Outras substâncias','X68':'Outras substâncias',
    'X69':'Outras substâncias','X70':'Enforcamento',
    'X71':'Afogamento','X72':'Arma de fogo',
    'X73':'Arma de fogo','X74':'Arma de fogo',
    'X78':'Objeto cortante','X79':'Objeto contundente',
    'X80':'Salto/precipitação','X81':'Outros',
    'X82':'Outros','X83':'Outros','X84':'Outros',
}
df_sinan['metodo'] = df_sinan['cid3'].map(METODO_MAP).fillna('Outros')

ANOS     = df_ano['ano'].tolist()
ANOS_SIM = df_sim['ano'].tolist()
ANOS_CAP = df_caps['ano'].tolist()

BG   = 'rgba(0,0,0,0)'
GRID = '#f0ede8'
FONT = dict(family='Source Sans 3', color='#333', size=12)
MAR  = dict(l=0, r=0, t=10, b=0)

def base(fig, h=300, **kw):
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=FONT, margin=MAR, height=h, **kw
    )
    fig.update_xaxes(gridcolor=GRID, showline=False,
                     tickfont=dict(size=11, color='#888'))
    fig.update_yaxes(gridcolor=GRID, showline=False,
                     tickfont=dict(size=11, color='#888'))
    return fig


# ── HERO ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-label">Dados públicos · Estado de São Paulo · 2015–2025</div>
  <div class="hero-title">Internações psiquiátricas, suicídio<br>e atenção ambulatorial no SUS/SP</div>
  <div class="hero-deck">
    Uma análise de {df_ano['internacoes'].sum():,.0f} internações psiquiátricas,
    {df_sim['total'].sum():,.0f} óbitos por suicídio e
    {df_caps['total'].sum()/1e6:.1f} milhões de atendimentos nos CAPS
    registrados entre 2015 e 2025 no estado de São Paulo.
  </div>
  <div class="hero-byline">Fontes: SIH · SIM · RAAS · SINAN / DATASUS · IBGE &nbsp;·&nbsp; Kelli Vasconcelos, 2025</div>
</div>
""", unsafe_allow_html=True)

# ── CALLOUTS ──────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
var_suc = (df_sim[df_sim['ano']==df_sim['ano'].max()]['total'].values[0] /
           df_sim[df_sim['ano']==df_sim['ano'].min()]['total'].values[0] - 1) * 100

callouts = [
    (f"{df_ano['internacoes'].sum():,.0f}",
     f"internações psiquiátricas\n{ANOS[0]}–{ANOS[-1]}"),
    (f"{df_sim['total'].sum():,.0f}",
     f"óbitos por suicídio\n{ANOS_SIM[0]}–{ANOS_SIM[-1]}"),
    (f"{df_caps['total'].sum()/1e6:.1f}M",
     f"atendimentos nos CAPS\n{ANOS_CAP[0]}–{ANOS_CAP[-1]}"),
    (f"{var_suc:+.1f}%",
     f"variação nos óbitos por suicídio\n{ANOS_SIM[0]}–{ANOS_SIM[-1]}"),
]
for col, (num, lbl) in zip([c1,c2,c3,c4], callouts):
    with col:
        st.markdown(f"""
        <div class="stat-callout">
          <div class="stat-number">{num}</div>
          <div class="stat-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ── SEÇÃO 1 — TENDÊNCIA TEMPORAL ──────────────────────────────────────
st.markdown("""
<div class="chapter-label">Seção 1</div>
<div class="chapter-title">Internações ao longo do tempo</div>
<div class="chapter-intro">
As internações psiquiátricas em SP caíram de forma consistente entre 2015 e 2019.
Em março de 2020, houve uma queda abrupta adicional — o sistema de saúde fechou
ou reduziu serviços no início da pandemia. A partir de 2022, as internações voltaram
a crescer, mas ainda estão abaixo do nível de 2015. As internações também estão
ficando mais curtas: a mediana de dias caiu de 28 para 13 em dez anos, sem
nenhuma reversão.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="chart-label">Internações por 100 mil habitantes por ano</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Queda antes da pandemia, colapso em 2020 e recuperação parcial a partir de 2022</div>', unsafe_allow_html=True)

    cores = ['#c0392b' if a in [2020,2021] else '#2c3e50' for a in ANOS]
    fig = go.Figure()
    fig.add_bar(x=ANOS, y=df_ano['taxa'], marker_color=cores, opacity=0.85,
                hovertemplate='<b>%{x}</b><br>%{y:.1f} internações/100k<extra></extra>')
    fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                  opacity=0.06, layer='below', line_width=0)
    fig.add_annotation(x=2020.5, y=df_ano['taxa'].max()*0.55,
                       text="Pandemia", showarrow=False,
                       font=dict(size=10, color='#c0392b'))
    fig.add_annotation(x=2022, y=df_ano['taxa'].max()*0.72,
                       text="Revisão<br>Censo 2022", showarrow=True,
                       ax=30, ay=-30,
                       arrowhead=2, arrowcolor='#aaa',
                       font=dict(size=9, color='#aaa'))
    base(fig, 320, yaxis=dict(title='Internações / 100k hab.'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Fonte: SIH/DATASUS + IBGE. Barras vermelhas = 2020 e 2021.
    A queda aparente em 2022 reflete uma revisão da estimativa populacional
    feita pelo IBGE após o Censo 2022 — não uma queda real nas internações.
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-label">Mediana de dias de internação por ano</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Em 2015 a internação típica durava 28 dias. Em 2025, 13 dias.</div>', unsafe_allow_html=True)

    fig2 = go.Figure()
    fig2.add_scatter(x=ANOS, y=df_ano['mediana_dias'],
                     mode='lines+markers',
                     line=dict(color='#2c3e50', width=2.5),
                     marker=dict(size=7, color='#2c3e50'),
                     fill='tozeroy', fillcolor='rgba(44,62,80,0.07)',
                     hovertemplate='<b>%{x}</b><br>%{y:.0f} dias<extra></extra>')
    fig2.add_annotation(x=ANOS[0], y=df_ano['mediana_dias'].iloc[0],
                        text=f"{df_ano['mediana_dias'].iloc[0]:.0f}d",
                        xanchor='left', showarrow=False,
                        font=dict(size=10, color='#888'))
    fig2.add_annotation(x=ANOS[-1], y=df_ano['mediana_dias'].iloc[-1],
                        text=f"{df_ano['mediana_dias'].iloc[-1]:.0f}d",
                        xanchor='right', showarrow=False,
                        font=dict(size=10, color='#c0392b'))
    base(fig2, 320, yaxis=dict(title='Dias (mediana)', range=[0, 35]))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    A queda é contínua e sem exceções em todos os 11 anos analisados.
    Internações mais curtas podem refletir avanços na política de saúde mental
    — que desde 2001 prioriza o cuidado na comunidade em vez da internação prolongada —
    mas também podem indicar alta antes do momento ideal por falta de leitos ou recursos.
    Os dados não permitem distinguir as duas situações.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
  <div class="note-label">O que a análise estatística mostra</div>
  <div class="note-text">
    Usando um modelo de série temporal com 132 meses de dados (2015–2025),
    estimamos que a pandemia causou uma queda adicional de 21,5% nas internações
    em março de 2020 — além da tendência de queda que já existia antes.
    Após 2022, o sistema reverteu para crescimento de 4,1% ao ano.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ── SEÇÃO 2 — ANÁLISE POR SEXO ────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Seção 2</div>
<div class="chapter-title">Diferenças entre homens e mulheres</div>
<div class="chapter-intro">
Homens são a maioria das internações psiquiátricas — 62% do total.
Mas o tipo de transtorno que leva homens e mulheres ao hospital é muito diferente.
Homens internam principalmente por dependência de álcool e drogas.
Mulheres internam principalmente por transtornos de humor, como depressão grave
e transtorno bipolar.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-label">Proporção de mulheres nas internações por ano</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">A participação feminina cresceu lentamente, mas de forma consistente</div>', unsafe_allow_html=True)

    df_ano['pct_fem']  = df_ano['feminino']  / df_ano['internacoes'] * 100
    df_ano['pct_masc'] = df_ano['masculino'] / df_ano['internacoes'] * 100

    fig3 = go.Figure()
    fig3.add_scatter(x=ANOS, y=df_ano['pct_fem'], name='Mulheres',
                     mode='lines+markers',
                     line=dict(color='#c0392b', width=2.5),
                     marker=dict(size=7),
                     hovertemplate='%{x}: %{y:.1f}% mulheres<extra></extra>')
    fig3.add_scatter(x=ANOS, y=df_ano['pct_masc'], name='Homens',
                     mode='lines+markers',
                     line=dict(color='#2c3e50', width=2.5),
                     marker=dict(size=7),
                     hovertemplate='%{x}: %{y:.1f}% homens<extra></extra>')
    fig3.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                   opacity=0.06, layer='below', line_width=0)
    base(fig3, 300,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)),
         yaxis=dict(ticksuffix='%', range=[0, 100]))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    A proporção de mulheres passou de 37,1% (2015) para 38,4% (2025).
    A tendência de crescimento é estatisticamente significativa (p &lt; 0,001).
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-label">Diagnósticos — diferença entre mulheres e homens</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Quanto cada diagnóstico é mais ou menos comum em mulheres do que em homens</div>', unsafe_allow_html=True)

    diags = ['Bipolar — mania grave','Borderline','Psicose NE',
             'Depressão grave','Demência','Dependência cocaína',
             'Dependência álcool','Múltiplas drogas']
    difs  = [10.8, 4.6, 4.4, 3.6, 1.9, -0.9, -12.2, -12.7]
    cores_d = ['#c0392b' if v > 0 else '#2c3e50' for v in difs]

    fig4 = go.Figure()
    fig4.add_bar(x=difs, y=diags, orientation='h',
                 marker_color=cores_d, opacity=0.85,
                 hovertemplate='%{y}: %{x:+.1f} pontos percentuais<extra></extra>')
    fig4.add_vline(x=0, line_color='#ccc', line_width=1)
    base(fig4, 300,
         xaxis=dict(title='Diferença em pontos percentuais\n(vermelho = mais comum em mulheres | azul = mais comum em homens)'))
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Mulheres têm 6,5 vezes mais chance de internação por transtorno borderline
    do que homens. Homens têm 4,5 vezes mais chance de internação por
    dependência de álcool do que mulheres.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
  <div class="note-label">O que a análise estatística mostra</div>
  <div class="note-text">
    As diferenças entre homens e mulheres nos diagnósticos são grandes e
    estatisticamente robustas.
    Transtornos por uso de álcool e drogas somam 42% das internações masculinas.
    Transtornos de humor somam uma parcela muito maior das internações femininas.
    Mesmo quando comparamos pacientes com o mesmo diagnóstico, mesma idade e
    mesmo ano de internação, mulheres recebem alta em média 8,5% mais rápido
    que homens, diferença que não é explicada pelo tipo de transtorno.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ── SEÇÃO 3 — ANÁLISE RACIAL ───────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Seção 3</div>
<div class="chapter-title">Raça e internações psiquiátricas</div>
<div class="chapter-intro">
Em 2015, 65% dos internados eram brancos e 24% pardos. Em 2025, brancos são 55%
e pardos são 36%. Quando calculamos a taxa por habitante de cada
grupo racial, todos os grupos internaram menos em 2023 do que em 2015.
A análise estatística separa os dois efeitos e confirma: a mudança na composição
racial das internações é explicada pela queda nas taxas, não por mudança
demográfica da população.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="chart-label">Proporção de cada grupo racial nas internações</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">A queda nas internações foi muito maior entre brancos do que entre pardos</div>', unsafe_allow_html=True)

    total_r        = df_ano['branca'] + df_ano['parda'] + df_ano['preta']
    df_ano['p_br'] = df_ano['branca'] / total_r * 100
    df_ano['p_pa'] = df_ano['parda']  / total_r * 100
    df_ano['p_pr'] = df_ano['preta']  / total_r * 100

    fig5 = go.Figure()
    fig5.add_scatter(x=ANOS, y=df_ano['p_br'], name='Branca',
                     mode='lines+markers',
                     line=dict(color='#2c3e50', width=2.5), marker=dict(size=6),
                     hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
    fig5.add_scatter(x=ANOS, y=df_ano['p_pa'], name='Parda',
                     mode='lines+markers',
                     line=dict(color='#BA7517', width=2.5), marker=dict(size=6),
                     hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
    fig5.add_scatter(x=ANOS, y=df_ano['p_pr'], name='Preta',
                     mode='lines+markers',
                     line=dict(color='#444441', width=1.5, dash='dot'),
                     marker=dict(size=5),
                     hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
    fig5.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                   opacity=0.06, layer='below', line_width=0)
    base(fig5, 300,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)),
         yaxis=dict(ticksuffix='%', range=[0, 80]))
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Proporção de cada grupo no total de internações por ano.
    Exclui os 10,1% de registros sem raça informada.
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-label">Taxa de internação por 100 mil habitantes — por grupo racial</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Todos os grupos internaram menos — a queda foi maior entre brancos e pretos</div>', unsafe_allow_html=True)

    # Calcular taxas por grupo usando PNADC como denominador
    # Proporções raciais da PNADC (valores do notebook)
    prop_raca_pnadc = {
        2015: {'Branca': 0.641, 'Parda': 0.301, 'Preta': 0.058},
        2016: {'Branca': 0.635, 'Parda': 0.305, 'Preta': 0.060},
        2017: {'Branca': 0.628, 'Parda': 0.310, 'Preta': 0.062},
        2018: {'Branca': 0.621, 'Parda': 0.315, 'Preta': 0.064},
        2019: {'Branca': 0.614, 'Parda': 0.320, 'Preta': 0.066},
        2020: {'Branca': 0.607, 'Parda': 0.325, 'Preta': 0.068},
        2021: {'Branca': 0.600, 'Parda': 0.329, 'Preta': 0.071},
        2022: {'Branca': 0.595, 'Parda': 0.323, 'Preta': 0.083},
        2023: {'Branca': 0.581, 'Parda': 0.328, 'Preta': 0.091},
    }

    anos_raca, taxa_br, taxa_pa, taxa_pr = [], [], [], []
    for _, row in df_ano.iterrows():
        ano = int(row['ano'])
        if ano not in prop_raca_pnadc:
            continue
        pop = pop_map.get(ano)
        if not pop:
            continue
        props = prop_raca_pnadc[ano]
        anos_raca.append(ano)
        taxa_br.append(row['branca'] / (pop * props['Branca']) * 100_000)
        taxa_pa.append(row['parda']  / (pop * props['Parda'])  * 100_000)
        taxa_pr.append(row['preta']  / (pop * props['Preta'])  * 100_000)

    fig5b = go.Figure()
    fig5b.add_scatter(x=anos_raca, y=taxa_br, name='Branca',
                      mode='lines+markers',
                      line=dict(color='#2c3e50', width=2.5), marker=dict(size=6),
                      hovertemplate='%{x}: %{y:.0f}/100k<extra></extra>')
    fig5b.add_scatter(x=anos_raca, y=taxa_pa, name='Parda',
                      mode='lines+markers',
                      line=dict(color='#BA7517', width=2.5), marker=dict(size=6),
                      hovertemplate='%{x}: %{y:.0f}/100k<extra></extra>')
    fig5b.add_scatter(x=anos_raca, y=taxa_pr, name='Preta',
                      mode='lines+markers',
                      line=dict(color='#444441', width=1.5, dash='dot'),
                      marker=dict(size=5),
                      hovertemplate='%{x}: %{y:.0f}/100k<extra></extra>')
    fig5b.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                    opacity=0.06, layer='below', line_width=0)
    base(fig5b, 300,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)),
         yaxis=dict(title='Internações / 100k hab.'))
    st.plotly_chart(fig5b, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Taxa calculada com denominador da PNADC (composição racial da população
    por ano, com peso amostral). Disponível para 2015–2023.
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-label">Por que a proporção parda cresceu? Decomposição de Kitagawa</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Quase toda a variação vem de mudança nas taxas — não na composição da população</div>', unsafe_allow_html=True)

    componentes = ['Mudança<br>nas taxas', 'Mudança na<br>composição', 'Total']
    valores     = [-65.4, 3.0, -62.4]
    cores_k     = ['#2c3e50', '#BA7517', '#444441']

    fig6 = go.Figure()
    fig6.add_bar(x=componentes, y=valores, marker_color=cores_k, opacity=0.85,
                 text=[f'{v:+.1f}' for v in valores],
                 textposition='outside',
                 hovertemplate='%{x}: %{y:+.1f} internações/100k<extra></extra>')
    fig6.add_hline(y=0, line_color='#ccc', line_width=1)
    base(fig6, 300,
         yaxis=dict(title='Internações / 100k hab.'))
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    A decomposição de Kitagawa separa dois efeitos: mudança na taxa de internação
    dentro de cada grupo (efeito de taxa) e mudança na composição racial
    da população (efeito demográfico). 104,8% da variação vem das taxas.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
  <div class="note-label">O que a análise estatística mostra</div>
  <div class="note-text">
    Em 2015, pessoas pretas internavam 456 por 100 mil habitantes —
    75% mais do que pessoas brancas (260/100k). Em 2023, as taxas convergiram:
    210/100k para pretos e 187/100k para brancos. Os três gráficos contam
    a mesma história de ângulos diferentes: a proporção parda cresceu (gráfico 1)
    porque a taxa branca caiu mais (gráfico 2), e essa mudança é explicada
    pelas taxas — não pela demografia (gráfico 3). O que causou a queda
    maior entre brancos não pode ser determinado com dados administrativos.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── SEÇÃO 4 — SUICÍDIOS ────────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Seção 5</div>
<div class="chapter-title">Óbitos por suicídio</div>
<div class="chapter-intro">
Os óbitos por suicídio cresceram 20% entre 2018 e 2024 no estado de SP.
O pico foi em 2022 — dois anos após o início da pandemia, não durante ela.
Homens morrem por suicídio 3,6 vezes mais do que mulheres, padrão que
se manteve estável ao longo de todo o período.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-label">Total de óbitos por suicídio e taxa por 100 mil habitantes</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Crescimento consistente com pico em 2022 e queda parcial depois</div>', unsafe_allow_html=True)

    fig9 = make_subplots(specs=[[{"secondary_y": True}]])
    fig9.add_bar(x=ANOS_SIM, y=df_sim['total'],
                 name='Total de óbitos', marker_color='#2c3e50', opacity=0.7,
                 hovertemplate='%{x}: %{y:,.0f} óbitos<extra></extra>',
                 secondary_y=False)
    fig9.add_scatter(x=ANOS_SIM, y=df_sim['taxa'],
                     name='Taxa por 100k', mode='lines+markers',
                     line=dict(color='#c0392b', width=2.5),
                     marker=dict(size=7),
                     hovertemplate='%{x}: %{y:.2f} por 100k hab.<extra></extra>',
                     secondary_y=True)
    for x, y in zip(ANOS_SIM, df_sim['taxa']):
        fig9.add_annotation(x=x, y=y, text=f'{y:.2f}',
                            yref='y2', showarrow=False,
                            yshift=12, font=dict(size=9, color='#c0392b'))
    base(fig9, 320,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)))
    fig9.update_yaxes(title='Total de óbitos', tickformat=',.0f',
                      gridcolor=GRID, secondary_y=False)
    fig9.update_yaxes(title='Por 100k hab.', tickformat='.2f',
                      gridcolor='rgba(0,0,0,0)', secondary_y=True)
    st.plotly_chart(fig9, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Fonte: SIM/DATASUS. CID X60–X84 (lesão autoprovocada intencional).
    Barras = total de óbitos. Linha vermelha = taxa por 100 mil habitantes.
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-label">Óbitos por sexo e razão entre homens e mulheres</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Homens morrem por suicídio 3,6 vezes mais do que mulheres</div>', unsafe_allow_html=True)

    fig10 = make_subplots(specs=[[{"secondary_y": True}]])
    fig10.add_bar(x=ANOS_SIM, y=df_sim['masculino'],
                  name='Homens', marker_color='#2c3e50', opacity=0.85,
                  hovertemplate='%{x} homens: %{y:,.0f}<extra></extra>',
                  secondary_y=False)
    fig10.add_bar(x=ANOS_SIM, y=df_sim['feminino'],
                  name='Mulheres', marker_color='#c0392b', opacity=0.85,
                  hovertemplate='%{x} mulheres: %{y:,.0f}<extra></extra>',
                  secondary_y=False)
    razao = df_sim['masculino'] / df_sim['feminino']
    fig10.add_scatter(x=ANOS_SIM, y=razao,
                      name='Razão H/M', mode='lines+markers',
                      line=dict(color='#BA7517', width=2, dash='dot'),
                      marker=dict(size=6),
                      hovertemplate='%{x}: %{y:.1f}x mais homens<extra></extra>',
                      secondary_y=True)
    base(fig10, 320, barmode='group',
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)))
    fig10.update_yaxes(title='Óbitos', tickformat=',.0f',
                       gridcolor=GRID, secondary_y=False)
    fig10.update_yaxes(title='Razão H/M', tickformat='.1f',
                       gridcolor='rgba(0,0,0,0)', secondary_y=True)
    st.plotly_chart(fig10, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Homens: crescimento de +18,5% entre 2018 e 2024.
    Mulheres: crescimento de +26,8% no mesmo período.
    A linha amarela mostra a razão entre os dois grupos (eixo direito).
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
  <div class="note-label">O que a análise estatística mostra</div>
  <div class="note-text">
    O pico de suicídios em 2022 — e não em 2020 — é um padrão documentado
    em outras crises: os efeitos do isolamento, do luto e da perda de emprego
    se manifestam nos anos seguintes ao pico da crise, não imediatamente.
    O crescimento feminino proporcionalmente maior (+26,8% vs +18,5%) reduziu
    levemente a diferença entre os sexos — a razão caiu de 3,8x em 2018 para
    3,5x em 2024. As internações psiquiátricas caíram no mesmo período em que
    os suicídios cresceram. Os dois fenômenos capturam situações diferentes
    e não devem ser comparados diretamente.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ── SEÇÃO 5 — TENTATIVAS ──────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Seção 6</div>
<div class="chapter-title">Tentativas de suicídio</div>
<div class="chapter-intro">
165.543 tentativas de suicídio foram registradas no SINAN entre 2015 e 2025 —
apenas os casos que geraram atendimento em algum serviço de saúde.
Mulheres representam 69% das tentativas, mas apenas 22% dos óbitos.
Homens representam 31% das tentativas e 78% dos óbitos.
A diferença no método utilizado explica grande parte dessa inversão.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-label">Quem tenta e quem morre — comparação entre os dois sistemas</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Mulheres tentam mais; homens morrem mais</div>', unsafe_allow_html=True)

    grupos_s  = ['Mulheres', 'Homens']
    pct_tent  = [69.0, 31.0]
    pct_obit  = [21.7, 78.3]
    x_pos     = np.arange(len(grupos_s))

    fig11 = go.Figure()
    fig11.add_bar(x=list(x_pos - 0.2), y=pct_tent,
                  name='Tentativas (SINAN)',
                  marker_color='#c0392b', opacity=0.85, width=0.35,
                  text=[f'{v:.0f}%' for v in pct_tent],
                  textposition='outside',
                  hovertemplate='%{text} das tentativas<extra></extra>')
    fig11.add_bar(x=list(x_pos + 0.2), y=pct_obit,
                  name='Óbitos (SIM)',
                  marker_color='#2c3e50', opacity=0.85, width=0.35,
                  text=[f'{v:.0f}%' for v in pct_obit],
                  textposition='outside',
                  hovertemplate='%{text} dos óbitos<extra></extra>')
    base(fig11, 300,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)),
         xaxis=dict(tickvals=list(x_pos), ticktext=grupos_s),
         yaxis=dict(ticksuffix='%', range=[0, 95]))
    st.plotly_chart(fig11, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    SINAN = notificações de lesão autoprovocada com atendimento registrado.
    SIM = óbitos com CID X60–X84. Os dois sistemas capturam populações diferentes.
    46% das tentativas registradas não eram o primeiro episódio da pessoa.
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-label">Método utilizado — diferença entre mulheres e homens</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Homens usam métodos mais letais com mais frequência</div>', unsafe_allow_html=True)

    met_pivot = (df_sinan.groupby(['sexo', 'metodo'])['n']
                 .sum().unstack(fill_value=0))

    if 'M' in met_pivot.index and 'F' in met_pivot.index:
        tot_m    = met_pivot.loc['M'].sum()
        tot_f    = met_pivot.loc['F'].sum()
        prop_m   = met_pivot.loc['M'] / tot_m * 100
        prop_f   = met_pivot.loc['F'] / tot_f * 100
        diff_met = (prop_f - prop_m).sort_values()
        metodos_plot = diff_met.index.tolist()
        difs_plot    = diff_met.values.tolist()
    else:
        metodos_plot = ['Medicamentos','Outras substâncias','Objeto cortante',
                        'Outros','Salto/precipitação','Enforcamento','Arma de fogo']
        difs_plot    = [10.0, 3.0, -0.2, -2.3, -2.8, -7.1, -0.6]

    cores_m = ['#c0392b' if v > 0 else '#2c3e50' for v in difs_plot]
    fig12 = go.Figure()
    fig12.add_bar(x=difs_plot, y=metodos_plot,
                  orientation='h', marker_color=cores_m, opacity=0.85,
                  hovertemplate='%{y}: %{x:+.1f} pontos percentuais<extra></extra>')
    fig12.add_vline(x=0, line_color='#ccc', line_width=1)
    base(fig12, 300,
         xaxis=dict(title='Diferença em pontos percentuais\n(vermelho = mais comum em mulheres | azul = mais comum em homens)'))
    st.plotly_chart(fig12, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Mulheres usam medicamentos com 10 pontos percentuais a mais do que homens —
    método que permite intervenção antes do óbito.
    Homens usam enforcamento com 7 pontos percentuais a mais — método de
    alta letalidade com menor janela de resgate.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
  <div class="note-label">O que a análise estatística mostra</div>
  <div class="note-text">
    A diferença entre tentar e morrer por suicídio tem uma explicação direta
    nos dados: o método. Mulheres usam principalmente medicamentos e substâncias —
    métodos que dão tempo para resgate e atendimento. Homens usam com mais
    frequência métodos que não deixam essa janela. Isso não significa que
    a tentativa feminina é menos séria — significa que o sistema de saúde
    tem mais oportunidade de intervir. Quase metade das tentativas registradas
    (46%) não era o primeiro episódio: a pessoa já havia tentado antes e
    continuava sem acompanhamento adequado.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ── SEÇÃO 6 — CAPS ────────────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Seção 7</div>
<div class="chapter-title">Atendimentos nos CAPS</div>
<div class="chapter-intro">
Os Centros de Atenção Psicossocial (CAPS) são o principal serviço de saúde
mental fora dos hospitais no SUS. Os atendimentos cresceram 56% entre 2018 e 2025.
Em 2020, os CAPS reduziram sua atividade durante a pandemia — e voltaram a crescer
de forma acelerada a partir de 2022.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-label">Atendimentos nos CAPS por ano</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Crescimento de 56% entre 2018 e 2025, com queda em 2020</div>', unsafe_allow_html=True)

    cores_c = ['#c0392b' if a in [2020, 2021] else '#2c3e50' for a in ANOS_CAP]
    fig13 = go.Figure()
    fig13.add_bar(x=ANOS_CAP,
                  y=df_caps['total'] / 1e6,
                  marker_color=cores_c, opacity=0.85,
                  text=[f'{v/1e6:.2f}M' for v in df_caps['total']],
                  textposition='outside',
                  hovertemplate='<b>%{x}</b><br>%{y:.2f} milhões de atendimentos<extra></extra>')
    fig13.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                    opacity=0.06, layer='below', line_width=0)
    base(fig13, 320,
         yaxis=dict(title='Milhões de atendimentos', range=[0, 1.7]))
    st.plotly_chart(fig13, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Fonte: RAAS/DATASUS. Barras vermelhas = 2020 e 2021.
    Atendimentos não equivalem a pacientes únicos —
    uma mesma pessoa pode gerar vários registros por ano.
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-label">Variação acumulada desde 2018 — CAPS vs internações</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">CAPS cresceram 56%; internações estão 3% abaixo do nível de 2018</div>', unsafe_allow_html=True)

    anos_comuns  = sorted(set(ANOS) & set(ANOS_CAP))
    int_comuns   = df_ano[df_ano['ano'].isin(anos_comuns)]['internacoes'].values
    cap_comuns   = df_caps[df_caps['ano'].isin(anos_comuns)]['total'].values
    base_int     = int_comuns[0]
    base_cap     = cap_comuns[0]
    var_int      = [(v / base_int - 1) * 100 for v in int_comuns]
    var_cap      = [(v / base_cap - 1) * 100 for v in cap_comuns]

    fig14 = go.Figure()
    fig14.add_scatter(x=anos_comuns, y=var_int,
                      name='Internações',
                      mode='lines+markers',
                      line=dict(color='#2c3e50', width=2.5),
                      marker=dict(size=7),
                      hovertemplate='%{x}: %{y:+.1f}% vs 2018<extra></extra>')
    fig14.add_scatter(x=anos_comuns, y=var_cap,
                      name='CAPS',
                      mode='lines+markers',
                      line=dict(color='#0F6E56', width=2.5),
                      marker=dict(size=7),
                      hovertemplate='%{x}: %{y:+.1f}% vs 2018<extra></extra>')
    fig14.add_hline(y=0, line_color='#ccc', line_width=1,
                    line_dash='dash', annotation_text='Nível de 2018',
                    annotation_position='right')
    fig14.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                    opacity=0.06, layer='below', line_width=0)
    base(fig14, 320,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)),
         yaxis=dict(title='Variação acumulada (%)', ticksuffix='%'))
    st.plotly_chart(fig14, use_container_width=True)
    st.markdown("""
    <div class="source-note">
    Variação percentual acumulada em relação a 2018.
    Os dois serviços sofreram queda em 2020, mas os CAPS se recuperaram
    muito mais rápido e cresceram bem acima do nível pré-pandemia.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
  <div class="note-label">O que a análise estatística mostra</div>
  <div class="note-text">
    Os CAPS cresceram de forma consistente e significativa ao longo do período
    (r = +0,976, p &lt; 0,001). A variação acumulada desde 2018 deixa clara
    a divergência de trajetórias: os CAPS estão 56% acima do nível de 2018,
    enquanto as internações estão praticamente no mesmo patamar.
    Em nível municipal, municípios com mais CAPS por habitante não apresentaram
    taxas de internação menores — o que indica que os dois serviços atendem
    estágios diferentes de gravidade e não são substitutos diretos um do outro.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ── METODOLOGIA ────────────────────────────────────────────────────────
st.markdown("""
<div class="methodology">
  <p><strong>Fontes de dados:</strong>
  SIH (internações), SIM (óbitos), RAAS (CAPS) e SINAN (tentativas) via DATASUS;
  Estimativas populacionais anuais e Censo 2022 do IBGE;
  PNADC trimestre 1 para composição racial da população.
  Pipeline de dados: AWS S3 + Athena + dbt.
  Análise estatística: Python (scipy, statsmodels, lifelines).
  </p>
  <p style="margin-top:0.6rem"><strong>Principais métodos:</strong>
  Série temporal interrompida com Poisson robusto (ITS, n=132 meses);
  Regressão logística para risco de óbito (AUC = 0,841);
  Modelo de Cox multivariado para tempo até alta (C-index = 0,640);
  Decomposição de Kitagawa para separar efeito demográfico de efeito de taxa;
  Correção de Benjamini-Hochberg aplicada a 77 testes — nenhum resultado
  significativo foi invalidado.
  </p>
  <p style="margin-top:0.6rem"><strong>Limitações principais:</strong>
  Internação reflete acesso ao sistema e política pública — não prevalência de transtornos.
  10,1% dos registros do SIH sem raça informada, excluídos das análises raciais.
  SINAN registra apenas tentativas com atendimento — subnotificação estrutural.
  Quebra na série populacional em 2022 por revisão do Censo.
  Suicídios sujeitos a subregistro estimado em 10–30%.
  </p>
  <p style="margin-top:0.6rem">
  Código disponível em
  <a href="https://github.com/kvgs/sus-saude-mental-analytics" target="_blank">
  github.com/kvgs/sus-saude-mental-analytics</a>.
  </p>
</div>
""", unsafe_allow_html=True)