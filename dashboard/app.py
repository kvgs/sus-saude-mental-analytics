import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Saúde Mental no SUS — SP",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    font-weight: 400;
    color: #0a0a0a;
    margin-bottom: 0.2rem;
    line-height: 1.2;
}

.subtitle {
    font-size: 1rem;
    color: #6b6b6b;
    margin-bottom: 2rem;
    font-weight: 300;
}

.metric-card {
    background: #f8f7f4;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    border-left: 4px solid;
}

.metric-label {
    font-size: 0.75rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.metric-delta {
    font-size: 0.8rem;
    font-weight: 400;
}

.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    font-weight: 400;
    color: #0a0a0a;
    margin-bottom: 0.3rem;
}

.insight-box {
    background: #f0f4ff;
    border-left: 3px solid #185FA5;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #444;
    line-height: 1.6;
    margin-top: 0.5rem;
}

.tab-header {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #888;
    margin-bottom: 1rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 20px;
    border: 1px solid #e0e0e0;
    padding: 6px 16px;
    background: transparent;
    color: #666;
    font-size: 0.85rem;
}

.stTabs [aria-selected="true"] {
    background: #185FA5 !important;
    border-color: #185FA5 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

CORES = {
    'azul': '#185FA5',
    'coral': '#D85A30',
    'verde': '#1D9E75',
    'amber': '#BA7517',
    'roxo': '#534AB7',
    'vermelho': '#E24B4A',
    'cinza': '#888780',
}

ANOS = list(range(2015, 2026))
INTERNACOES = [138012, 119164, 104277, 96993, 98165, 70223, 77536, 82387, 90414, 93185, 98765]
MEDIA_DIAS = [21.6, 21.2, 20.1, 19.0, 18.8, 17.7, 17.8, 16.8, 16.7, 15.8, 15.3]
TAXA_OBITO = [0.26, 0.30, 0.32, 0.26, 0.27, 0.27, 0.34, 0.30, 0.31, 0.28, 0.23]
INT_MASC = [86624, 74649, 65196, 60814, 60520, 43913, 48246, 50613, 55389, 56831, 60569]
INT_FEM = [51388, 44515, 39081, 36179, 37645, 26310, 29290, 31774, 35025, 36354, 38196]

ANOS_SUC = list(range(2018, 2025))
SUICIDIOS = [2207, 2378, 2359, 2645, 2923, 2787, 2656]
SUC_MASC = [1742, 1876, 1857, 2076, 2295, 2175, 2081]
SUC_FEM = [465, 502, 502, 569, 628, 612, 575]
SUC_ENFORC = [1305, 1415, 1410, 1555, 1709, 1637, 1562]
SUC_ARMA = [287, 311, 308, 349, 388, 371, 352]
SUC_ENVEN = [278, 296, 293, 325, 362, 348, 329]
SUC_SALTO = [180, 195, 194, 224, 249, 242, 228]

ANOS_CAPS = list(range(2018, 2026))
CAPS_TOTAL = [4100000, 4400000, 3100000, 3400000, 3700000, 4500000, 5000000, 5500000]
CAPS_MASC = [2603000, 2794000, 1968000, 2159800, 2349000, 2655000, 2950000, 3245000]
CAPS_FEM = [1497000, 1606000, 1132000, 1240200, 1351000, 1845000, 2050000, 2255000]
CAPS_DROGAS_PCT = [33.0, 33.5, 33.0, 31.1, 27.5, 26.8, 25.8, 17.6]
CAPS_RUA = [164000, 178000, 140000, 144000, 135000, 168000, 198000, 130000]

ANOS_VIOL = list(range(2015, 2026))
VIOLENCIA = [46639, 58220, 75735, 52421, 95942, 158660, 99036, 114177, 153199, 153648, 173406]
TENT_SUIC = [2500, 3100, 5500, 5700, 13300, 20200, 14000, 18000, 25700, 27800, 29700]
VIT_FEM = [33300, 41800, 55800, 37800, 69100, 112300, 70400, 81200, 107400, 107700, 119900]
VIT_MASC = [13300, 16400, 19900, 14600, 26800, 46300, 28600, 32900, 45700, 45900, 53500]

RACAS_ANOS = list(range(2015, 2026))
PCT_BRANCA = [65.2, 65.5, 63.7, 62.1, 60.3, 60.1, 59.3, 59.1, 56.0, 55.0, 54.4]
PCT_PARDA = [24.0, 23.7, 25.2, 27.2, 29.0, 29.1, 30.0, 30.2, 33.6, 35.6, 35.7]
PCT_PRETA = [10.8, 10.8, 11.1, 10.7, 10.7, 10.8, 10.7, 10.7, 10.4, 9.4, 9.9]

ANOS_RENDA = list(range(2015, 2024))
RENDA_BRANCA = [2544, 2677, 2858, 3080, 3199, 3402, 3469, 3446, 3900]
RENDA_PARDA = [1468, 1557, 1618, 1746, 1813, 1932, 1981, 2140, 2396]
RENDA_PRETA = [1641, 1558, 1702, 1746, 1813, 2050, 1981, 2306, 2396]

DIAG_LABELS = ['Esquizofrenia paranoide', 'Múltiplas drogas', 'Dependência álcool',
               'Psicose NE', 'Bipolar mania grave', 'Esquizofrenia residual',
               'Dep. cocaína', 'Depressão grave']
DIAG_TOTAL = [149000, 134000, 79000, 68000, 49000, 43000, 25000, 19000]
DIAG_DIAS = [22.0, 16.5, 18.1, 13.5, 15.9, 28.9, 15.9, 11.0]
DIAG_TAXA_OBITO = [0.143, 0.016, 0.156, 0.141, 0.104, 0.429, 0.021, 0.047]

DIAG_DIFF_SEXO_LABELS = ['Bipolar mania', 'TPB', 'Psicose NE', 'Depressão grave',
                          'Esq. paranoide', 'Esq. residual', 'Dep. cocaína',
                          'Dep. álcool', 'Múltiplas drogas']
DIAG_DIFF_SEXO = [11.3, 4.8, 4.7, 3.9, 1.1, 0.0, -0.8, -12.3, -12.7]

DIAG_DIFF_RACA_LABELS = ['Psicose NE', 'Múltiplas drogas', 'Bipolar mania',
                          'Depressão grave', 'Dep. cocaína', 'Dep. álcool',
                          'Esq. paranoide', 'Esq. residual']
DIAG_DIFF_RACA = [4.6, 3.1, 2.1, -0.2, -0.3, -1.5, -3.3, -4.5]

TEMPLATE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#444'),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(gridcolor='#f0f0f0', showline=False, tickfont=dict(size=11)),
    yaxis=dict(gridcolor='#f0f0f0', showline=False, tickfont=dict(size=11)),
)


def apply_template(fig):
    fig.update_layout(**TEMPLATE)
    return fig


st.markdown('<div class="main-title">Saúde mental no SUS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estado de São Paulo · 2015–2025 · 9 fontes públicas · SIH · SIM · RAAS · SINAN · PNADC</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""<div class="metric-card" style="border-color:#185FA5">
        <div class="metric-label">Internações (2025)</div>
        <div class="metric-value" style="color:#185FA5">98,8k</div>
        <div class="metric-delta" style="color:#1D9E75">-28,4% vs 2015</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="metric-card" style="border-color:#E24B4A">
        <div class="metric-label">Suicídios (2024)</div>
        <div class="metric-value" style="color:#E24B4A">2.656</div>
        <div class="metric-delta" style="color:#E24B4A">+20,3% vs 2018</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="metric-card" style="border-color:#1D9E75">
        <div class="metric-label">Atendimentos CAPS (2025)</div>
        <div class="metric-value" style="color:#1D9E75">5,5M</div>
        <div class="metric-delta" style="color:#1D9E75">+34,7% vs 2018</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class="metric-card" style="border-color:#BA7517">
        <div class="metric-label">Média dias internação</div>
        <div class="metric-value" style="color:#BA7517">15,3d</div>
        <div class="metric-delta" style="color:#1D9E75">-29% vs 2015</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Evolução temporal",
    "Por sexo",
    "Por raça/cor",
    "Diagnósticos",
    "Renda e desigualdade"
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Internações psiquiátricas por ano</div>', unsafe_allow_html=True)
        df = pd.DataFrame({'Ano': ANOS, 'Internações': INTERNACOES})
        cores_bar = ['#E24B4A' if a in [2020, 2021] else '#185FA5' for a in ANOS]
        fig = go.Figure()
        fig.add_bar(x=df['Ano'], y=df['Internações'],
                    marker_color=cores_bar,
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        z = np.polyfit(ANOS, INTERNACOES, 1)
        fig.add_scatter(x=ANOS, y=np.poly1d(z)(ANOS),
                        mode='lines', line=dict(dash='dash', color='#888', width=1.5),
                        name='Tendência', hoverinfo='skip')
        fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#E24B4A', opacity=0.08,
                      layer='below', line_width=0)
        fig.update_layout(**TEMPLATE, height=280, showlegend=False,
                          yaxis=dict(gridcolor='#f0f0f0', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Tendência secular:</b> -3.319 internações/ano (r=-0.99, p&lt;0.001). Pandemia causou queda adicional de 26.466 internações em 2020–2021 (DiD, p=0.019).</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Suicídios e atendimentos CAPS</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_bar(x=ANOS_SUC, y=SUICIDIOS, name='Suicídios',
                    marker_color='#E24B4A', opacity=0.85,
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>',
                    secondary_y=False)
        fig.add_scatter(x=ANOS_CAPS, y=[v/1e6 for v in CAPS_TOTAL],
                        name='CAPS (M)', mode='lines+markers',
                        line=dict(color='#1D9E75', width=2.5),
                        marker=dict(size=6),
                        hovertemplate='%{x}: %{y:.1f}M<extra></extra>',
                        secondary_y=True)
        fig.update_layout(**TEMPLATE, height=280,
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)))
        fig.update_yaxes(title_text='Suicídios', secondary_y=False,
                         gridcolor='#f0f0f0', tickformat=',.0f')
        fig.update_yaxes(title_text='CAPS (M)', secondary_y=True,
                         gridcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Divergência pandemia:</b> CAPS caíram em 2020, suicídios continuaram subindo. Em 2022, pico de 2.923 óbitos.</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Desinstitucionalização — média de dias</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_scatter(x=ANOS, y=MEDIA_DIAS, mode='lines+markers',
                        line=dict(color='#534AB7', width=2.5),
                        marker=dict(size=7, color='#534AB7'),
                        fill='tozeroy', fillcolor='rgba(83,74,183,0.08)',
                        hovertemplate='%{x}: %{y:.1f} dias<extra></extra>')
        fig.update_layout(**TEMPLATE, height=220,
                          yaxis=dict(gridcolor='#f0f0f0', range=[13, 23]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>r=-0.991, p&lt;0.001.</b> Queda de 0,65 dias/ano há 11 anos — Lei 10.216/2001 (Reforma Psiquiátrica) produzindo efeito mensurável.</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-title">Violência SINAN — notificações</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_bar(x=ANOS_VIOL, y=VIOLENCIA, name='Total violência',
                    marker_color='#BA7517', opacity=0.7,
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        fig.add_scatter(x=ANOS_VIOL, y=TENT_SUIC, name='Tentativas suicídio',
                        mode='lines+markers',
                        line=dict(color='#E24B4A', width=2),
                        marker=dict(size=6),
                        hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        fig.update_layout(**TEMPLATE, height=220,
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Atenção:</b> crescimento reflete expansão do registro, não só aumento real. Tentativas de suicídio crescem de 2,5k (2015) para 29,7k (2025).</div>', unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Proporção por sexo nas internações</div>', unsafe_allow_html=True)
        pct_fem = [f/(f+m)*100 for f, m in zip(INT_FEM, INT_MASC)]
        pct_masc = [100-p for p in pct_fem]
        fig = go.Figure()
        fig.add_scatter(x=ANOS, y=pct_masc, name='Masculino',
                        mode='lines+markers', fill='tozeroy',
                        line=dict(color='#185FA5', width=2),
                        fillcolor='rgba(24,95,165,0.15)',
                        hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
        fig.add_scatter(x=ANOS, y=pct_fem, name='Feminino',
                        mode='lines+markers', fill='tozeroy',
                        line=dict(color='#D85A30', width=2),
                        fillcolor='rgba(216,90,48,0.15)',
                        hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
        fig.update_layout(**TEMPLATE, height=280,
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', range=[0, 100], ticksuffix='%'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Proporção feminina cresce:</b> r=0.873, p&lt;0.001. De 37,2% (2015) para 38,6% (2025). Gap de gênero está diminuindo.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Diagnósticos por sexo — diferença (pp)</div>', unsafe_allow_html=True)
        cores_sexo = ['#D85A30' if v > 0 else '#185FA5' for v in DIAG_DIFF_SEXO]
        fig = go.Figure()
        fig.add_bar(x=DIAG_DIFF_SEXO, y=DIAG_DIFF_SEXO_LABELS,
                    orientation='h', marker_color=cores_sexo,
                    hovertemplate='%{y}: %{x:+.1f}pp<extra></extra>')
        fig.add_vline(x=0, line_color='#ccc', line_width=1)
        fig.update_layout(**TEMPLATE, height=280,
                          xaxis=dict(gridcolor='#f0f0f0', ticksuffix='pp'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>χ²=68.603, p&lt;0.001.</b> Laranja = mais feminino. Azul = mais masculino. Múltiplas drogas + álcool = 42,7% das internações masculinas.</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Razão masculino/feminino por sistema</div>', unsafe_allow_html=True)
        sistemas = ['CAPS', 'Internações', 'Suicídios']
        razoes = [1.48, 1.62, 3.60]
        fig = go.Figure()
        fig.add_bar(x=sistemas, y=razoes,
                    marker_color=['#1D9E75', '#185FA5', '#E24B4A'],
                    text=[f'{r:.2f}x' for r in razoes],
                    textposition='outside',
                    hovertemplate='%{x}: %{y:.2f}x<extra></extra>')
        fig.add_hline(y=1, line_dash='dash', line_color='#ccc')
        fig.update_layout(**TEMPLATE, height=220,
                          yaxis=dict(gridcolor='#f0f0f0', range=[0, 4.5]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Suicídio tem maior gap</b> (3,60x). Homens chegam em crise mais tarde e mais grave.</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-title">Suicídios por sexo (2018–2024)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_bar(x=ANOS_SUC, y=SUC_MASC, name='Masculino',
                    marker_color='#185FA5', opacity=0.85,
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        fig.add_bar(x=ANOS_SUC, y=SUC_FEM, name='Feminino',
                    marker_color='#D85A30', opacity=0.85,
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        fig.update_layout(**TEMPLATE, height=220, barmode='group',
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Ambos crescem, mas masculino mais acelerado. Em 2022, pico de 2.295 (M) e 628 (F).</div>', unsafe_allow_html=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Proporção por raça/cor nas internações</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_scatter(x=RACAS_ANOS, y=PCT_BRANCA, name='Branca',
                        mode='lines+markers', line=dict(color='#185FA5', width=2.5),
                        marker=dict(size=6),
                        hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
        fig.add_scatter(x=RACAS_ANOS, y=PCT_PARDA, name='Parda',
                        mode='lines+markers', line=dict(color='#BA7517', width=2.5),
                        marker=dict(size=6),
                        hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
        fig.add_scatter(x=RACAS_ANOS, y=PCT_PRETA, name='Preta',
                        mode='lines+markers', line=dict(color='#2C2C2A', width=2),
                        marker=dict(size=6),
                        hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
        fig.update_layout(**TEMPLATE, height=280,
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', ticksuffix='%'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>χ²=6.903, p&lt;0.001.</b> Parda: +11,7pp em 11 anos. Branca: -10,8pp. Maior mudança na composição racial das internações psiquiátricas.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Diagnósticos por raça — diferença Parda−Branca (pp)</div>', unsafe_allow_html=True)
        cores_raca = ['#E24B4A' if v > 0 else '#1D9E75' for v in DIAG_DIFF_RACA]
        fig = go.Figure()
        fig.add_bar(x=DIAG_DIFF_RACA, y=DIAG_DIFF_RACA_LABELS,
                    orientation='h', marker_color=cores_raca,
                    hovertemplate='%{y}: %{x:+.1f}pp<extra></extra>')
        fig.add_vline(x=0, line_color='#ccc', line_width=1)
        fig.update_layout(**TEMPLATE, height=280,
                          xaxis=dict(gridcolor='#f0f0f0', ticksuffix='pp'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Vermelho = parda mais frequente.</b> Pardos internam mais por Psicose NE (+4,6pp) — possível acesso tardio e diagnóstico impreciso.</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Vítimas de violência por sexo</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_bar(x=ANOS_VIOL, y=VIT_FEM, name='Feminino',
                    marker_color='#D85A30', opacity=0.85,
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        fig.add_bar(x=ANOS_VIOL, y=VIT_MASC, name='Masculino',
                    marker_color='#185FA5', opacity=0.85,
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        fig.update_layout(**TEMPLATE, height=220, barmode='group',
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">70,6% das vítimas são femininas. Pico em 2020 — pandemia e isolamento intensificaram violência doméstica.</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-title">Taxa de óbito por raça e diagnóstico (%)</div>', unsafe_allow_html=True)
        diags = ['Esq. residual', 'Dep. álcool', 'Psicose NE', 'Esq. paranoide', 'Bipolar', 'Dep. grave']
        branca = [0.429, 0.156, 0.141, 0.143, 0.104, 0.047]
        parda = [0.396, 0.100, 0.148, 0.130, 0.116, 0.132]
        preta = [0.321, 0.144, 0.068, 0.112, 0.137, 0.000]
        x = np.arange(len(diags))
        fig = go.Figure()
        fig.add_bar(name='Branca', x=diags, y=branca, marker_color='#185FA5', opacity=0.85)
        fig.add_bar(name='Parda', x=diags, y=parda, marker_color='#BA7517', opacity=0.85)
        fig.add_bar(name='Preta', x=diags, y=preta, marker_color='#2C2C2A', opacity=0.85)
        fig.update_layout(**TEMPLATE, height=220, barmode='group',
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', ticksuffix='%'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Depressão grave parda: taxa de óbito 2,8x maior que branca. Inequidade racial no desfecho clínico.</div>', unsafe_allow_html=True)

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Top 8 diagnósticos — total de internações</div>', unsafe_allow_html=True)
        idx_ord = np.argsort(DIAG_TOTAL)
        fig = go.Figure()
        fig.add_bar(x=[DIAG_TOTAL[i] for i in idx_ord],
                    y=[DIAG_LABELS[i] for i in idx_ord],
                    orientation='h', marker_color='#185FA5',
                    hovertemplate='%{y}: %{x:,.0f}<extra></extra>')
        fig.update_layout(**TEMPLATE, height=300,
                          xaxis=dict(gridcolor='#f0f0f0', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Esquizofrenia paranoide lidera com 149k internações. Múltiplas drogas em 2º com 134k — transtornos por substâncias dominam o perfil masculino.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Mediana de dias de internação por diagnóstico</div>', unsafe_allow_html=True)
        idx_dias = np.argsort(DIAG_DIAS)
        cores_dias = ['#E24B4A' if DIAG_DIAS[i] > 20 else '#185FA5' for i in idx_dias]
        fig = go.Figure()
        fig.add_bar(x=[DIAG_DIAS[i] for i in idx_dias],
                    y=[DIAG_LABELS[i] for i in idx_dias],
                    orientation='h', marker_color=cores_dias,
                    hovertemplate='%{y}: %{x:.1f} dias<extra></extra>')
        fig.update_layout(**TEMPLATE, height=300,
                          xaxis=dict(gridcolor='#f0f0f0', ticksuffix=' d'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>H=90.668, p&lt;0.001.</b> Esquizofrenia residual: 28,9d. Depressão grave: 11d. Crônicos ficam 2,6x mais que agudos.</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Taxa de óbito por diagnóstico (%)</div>', unsafe_allow_html=True)
        idx_ob = np.argsort(DIAG_TAXA_OBITO)
        cores_ob = ['#E24B4A' if DIAG_TAXA_OBITO[i] > 0.3 else '#185FA5' for i in idx_ob]
        fig = go.Figure()
        fig.add_bar(x=[DIAG_TAXA_OBITO[i] for i in idx_ob],
                    y=[DIAG_LABELS[i] for i in idx_ob],
                    orientation='h', marker_color=cores_ob,
                    hovertemplate='%{y}: %{x:.3f}%<extra></extra>')
        media_ob = np.mean(DIAG_TAXA_OBITO)
        fig.add_vline(x=media_ob, line_dash='dash', line_color='#888',
                      annotation_text=f'Média: {media_ob:.3f}%',
                      annotation_position='top right')
        fig.update_layout(**TEMPLATE, height=220,
                          xaxis=dict(gridcolor='#f0f0f0', ticksuffix='%'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Esquizofrenia residual: 0,429% — mais letal. Múltiplas drogas: 0,016% — baixa letalidade mas altíssimo volume.</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-title">Suicídios por método (2018–2024)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_bar(x=ANOS_SUC, y=SUC_ENFORC, name='Enforcamento',
                    marker_color='#185FA5', opacity=0.85)
        fig.add_bar(x=ANOS_SUC, y=SUC_ARMA, name='Arma de fogo',
                    marker_color='#E24B4A', opacity=0.85)
        fig.add_bar(x=ANOS_SUC, y=SUC_ENVEN, name='Envenenamento',
                    marker_color='#1D9E75', opacity=0.85)
        fig.add_bar(x=ANOS_SUC, y=SUC_SALTO, name='Salto',
                    marker_color='#BA7517', opacity=0.85)
        fig.update_layout(**TEMPLATE, height=220, barmode='stack',
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=10)),
                          yaxis=dict(gridcolor='#f0f0f0', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Enforcamento responde por ~60% dos casos em todos os anos. Crescimento consistente em todos os métodos de 2020 a 2022.</div>', unsafe_allow_html=True)

with tab5:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Renda média por raça/cor — SP (PNADC 2015–2023)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_scatter(x=ANOS_RENDA, y=RENDA_BRANCA, name='Branca',
                        mode='lines+markers', line=dict(color='#185FA5', width=2.5),
                        marker=dict(size=6),
                        hovertemplate='%{x}: R$%{y:,.0f}<extra></extra>')
        fig.add_scatter(x=ANOS_RENDA, y=RENDA_PARDA, name='Parda',
                        mode='lines+markers', line=dict(color='#BA7517', width=2.5),
                        marker=dict(size=6),
                        hovertemplate='%{x}: R$%{y:,.0f}<extra></extra>')
        fig.add_scatter(x=ANOS_RENDA, y=RENDA_PRETA, name='Preta',
                        mode='lines+markers', line=dict(color='#2C2C2A', width=2),
                        marker=dict(size=6),
                        hovertemplate='%{x}: R$%{y:,.0f}<extra></extra>')
        fig.update_layout(**TEMPLATE, height=280,
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', tickprefix='R$', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Em 2023: Branca R$3.900 vs Parda R$2.400 vs Preta R$2.600. Gap racial persistente ao longo de toda a série.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Renda por raça e sexo — SP 2023</div>', unsafe_allow_html=True)
        racas_2023 = ['Branca', 'Preta', 'Parda']
        masc_2023 = [4402, 2849, 2669]
        fem_2023 = [3300, 2355, 2040]
        fig = go.Figure()
        fig.add_bar(name='Masculino', x=racas_2023, y=masc_2023,
                    marker_color='#185FA5', opacity=0.85,
                    text=[f'R${v:,.0f}' for v in masc_2023],
                    textposition='outside',
                    hovertemplate='%{x} Masc: R$%{y:,.0f}<extra></extra>')
        fig.add_bar(name='Feminino', x=racas_2023, y=fem_2023,
                    marker_color='#D85A30', opacity=0.85,
                    text=[f'R${v:,.0f}' for v in fem_2023],
                    textposition='outside',
                    hovertemplate='%{x} Fem: R$%{y:,.0f}<extra></extra>')
        fig.update_layout(**TEMPLATE, height=280, barmode='group',
                          legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11)),
                          yaxis=dict(gridcolor='#f0f0f0', range=[0, 5200],
                                     tickprefix='R$', tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Pior combinação:</b> mulher parda — R$2.040/mês. <b>Melhor:</b> homem branco — R$4.402. Gap de 2,16x pela intersecção de raça e gênero.</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">% atendimentos CAPS por uso de drogas</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_scatter(x=ANOS_CAPS, y=CAPS_DROGAS_PCT,
                        mode='lines+markers',
                        line=dict(color='#BA7517', width=2.5),
                        marker=dict(size=7),
                        fill='tozeroy', fillcolor='rgba(186,117,23,0.1)',
                        hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
        fig.update_layout(**TEMPLATE, height=220,
                          yaxis=dict(gridcolor='#f0f0f0', ticksuffix='%', range=[0, 40]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Queda de 33% (2018) para 17,6% (2025) — mudança no perfil dos usuários dos CAPS ou melhora nos serviços especializados em dependência.</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-title">Pessoas em situação de rua nos CAPS</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_bar(x=ANOS_CAPS, y=CAPS_RUA,
                    marker_color='#993C1D', opacity=0.85,
                    text=[f'{v//1000}k' for v in CAPS_RUA],
                    textposition='outside',
                    hovertemplate='%{x}: %{y:,.0f}<extra></extra>')
        fig.update_layout(**TEMPLATE, height=220,
                          yaxis=dict(gridcolor='#f0f0f0', range=[0, 230000],
                                     tickformat=',.0f'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Pico de 198k atendimentos em 2024. Queda em 2025 pode refletir mudança de política ou subnotificação.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""<div style="font-size:11px; color:#aaa; border-top:0.5px solid #eee; padding-top:12px;">
Fontes: SIH/DATASUS · SIM · RAAS · SINAN · PNADC · Censo 2022 · Estimativas IBGE &nbsp;|&nbsp;
Pipeline: <a href="https://github.com/kvgs/sus-data-pipeline" target="_blank">sus-data-pipeline</a> &nbsp;|&nbsp;
Análise: <a href="https://github.com/kvgs/sus-saude-mental-analytics" target="_blank">sus-saude-mental-analytics</a> &nbsp;|&nbsp;
Kelli Vasconcelos · 2025
</div>""", unsafe_allow_html=True)