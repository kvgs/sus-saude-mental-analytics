import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Saúde Mental no SUS — SP",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Source+Sans+3:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

.hero {
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #e8e4df;
    margin-bottom: 2.5rem;
}

.hero-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #c0392b;
    font-weight: 500;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-family: 'Source Serif 4', serif;
    font-size: 2.8rem;
    font-weight: 300;
    color: #1a1a1a;
    line-height: 1.2;
    margin-bottom: 1rem;
}

.hero-deck {
    font-family: 'Source Serif 4', serif;
    font-size: 1.15rem;
    font-weight: 300;
    font-style: italic;
    color: #555;
    line-height: 1.7;
    max-width: 780px;
    margin-bottom: 1rem;
}

.hero-byline {
    font-size: 0.78rem;
    color: #999;
    letter-spacing: 0.05em;
}

.section-divider {
    border: none;
    border-top: 1px solid #e8e4df;
    margin: 2.5rem 0;
}

.chapter-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #c0392b;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.chapter-title {
    font-family: 'Source Serif 4', serif;
    font-size: 1.7rem;
    font-weight: 300;
    color: #1a1a1a;
    margin-bottom: 0.8rem;
    line-height: 1.3;
}

.chapter-intro {
    font-size: 1rem;
    color: #444;
    line-height: 1.8;
    max-width: 720px;
    margin-bottom: 1.5rem;
    font-weight: 300;
}

.stat-callout {
    border-left: 3px solid #c0392b;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    background: #faf9f7;
}

.stat-number {
    font-family: 'Source Serif 4', serif;
    font-size: 2.4rem;
    font-weight: 300;
    color: #c0392b;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.stat-label {
    font-size: 0.85rem;
    color: #666;
    line-height: 1.5;
}

.annotation {
    font-size: 0.82rem;
    color: #777;
    font-style: italic;
    line-height: 1.6;
    margin-top: 0.5rem;
}

.reflection {
    background: #f5f3ef;
    border-top: 2px solid #1a1a1a;
    padding: 1.5rem 1.8rem;
    margin: 1.5rem 0;
}

.reflection-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #888;
    margin-bottom: 0.6rem;
}

.reflection-text {
    font-family: 'Source Serif 4', serif;
    font-size: 1rem;
    font-weight: 300;
    color: #333;
    line-height: 1.8;
}

.chart-title {
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #888;
    margin-bottom: 0.3rem;
}

.chart-subtitle {
    font-family: 'Source Serif 4', serif;
    font-size: 1.05rem;
    font-weight: 300;
    color: #1a1a1a;
    margin-bottom: 0.8rem;
    line-height: 1.4;
}

.source-note {
    font-size: 0.72rem;
    color: #aaa;
    margin-top: 0.3rem;
    font-style: italic;
}

.methodology {
    background: #faf9f7;
    border: 1px solid #e8e4df;
    padding: 1.2rem 1.5rem;
    margin-top: 2rem;
}

.methodology p {
    font-size: 0.8rem;
    color: #777;
    line-height: 1.7;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

ANOS = list(range(2015, 2026))
INT  = [138012,119164,104277,96993,98165,70223,77536,82387,90414,93185,98765]
DIAS = [21.6,21.2,20.1,19.0,18.8,17.7,17.8,16.8,16.7,15.8,15.3]
INT_M = [86624,74649,65196,60814,60520,43913,48246,50613,55389,56831,60569]
INT_F = [51388,44515,39081,36179,37645,26310,29290,31774,35025,36354,38196]

ANOS_S = list(range(2018, 2025))
SUC   = [2207,2378,2359,2645,2923,2787,2656]
SUC_M = [1742,1876,1857,2076,2295,2175,2081]
SUC_F = [465,502,502,569,628,612,575]

ANOS_C = list(range(2018, 2026))
CAPS  = [4100000,4400000,3100000,3400000,3700000,4500000,5000000,5500000]

PCT_BRANCA = [65.2,65.5,63.7,62.1,60.3,60.1,59.3,59.1,56.0,55.0,54.4]
PCT_PARDA  = [24.0,23.7,25.2,27.2,29.0,29.1,30.0,30.2,33.6,35.6,35.7]
PCT_PRETA  = [10.8,10.8,11.1,10.7,10.7,10.8,10.7,10.7,10.4,9.4,9.9]

BG   = 'rgba(0,0,0,0)'
GRID = '#f0ede8'
FONT = dict(family='Source Sans 3', color='#333', size=12)
MAR  = dict(l=0, r=0, t=10, b=0)

def base(fig, h=300, **kw):
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=FONT, margin=MAR, height=h,
        **kw
    )
    fig.update_xaxes(gridcolor=GRID, showline=False,
                     tickfont=dict(size=11, color='#888'))
    fig.update_yaxes(gridcolor=GRID, showline=False,
                     tickfont=dict(size=11, color='#888'))
    return fig

# ── HERO ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-label">Relatório de dados · Estado de São Paulo · 2015–2025</div>
  <div class="hero-title">O colapso silencioso da<br>saúde mental no SUS</div>
  <div class="hero-deck">Em dez anos, mais de um milhão de internações psiquiátricas, 17 mil
  vidas perdidas para o suicídio e 33 milhões de atendimentos ambulatoriais revelam um sistema
  sob pressão crescente — agravado pela pandemia, marcado por profundas desigualdades.</div>
  <div class="hero-byline">Fontes: SIH · SIM · RAAS/DATASUS · IBGE &nbsp;·&nbsp; Análise: Kelli Vasconcelos, 2025</div>
</div>
""", unsafe_allow_html=True)

# ── NÚMEROS INICIAIS ───────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
callouts = [
    ("1.069.121", "internações psiquiátricas\nentre 2015 e 2025"),
    ("17.955",    "vidas perdidas para\no suicídio entre 2018 e 2024"),
    ("33,7 milhões", "atendimentos nos CAPS\nentre 2018 e 2025"),
    ("+20,3%",   "crescimento nos suicídios\nde 2018 a 2024"),
]
for col, (num, lbl) in zip([c1,c2,c3,c4], callouts):
    with col:
        st.markdown(f"""
        <div class="stat-callout">
          <div class="stat-number">{num}</div>
          <div class="stat-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── CAPÍTULO 1 ─────────────────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Capítulo 1</div>
<div class="chapter-title">Uma queda que começou antes da pandemia</div>
<div class="chapter-intro">
As internações psiquiátricas em São Paulo caem há mais de uma década.
Em 2015, eram 138 mil por ano. Em 2025, chegaram a 99 mil — uma redução de 28%.
Mas essa queda não é apenas um problema: parte dela reflete um avanço deliberado
de política pública, a Reforma Psiquiátrica brasileira, que desde 2001 substitui
progressivamente o modelo de internações longas pelo cuidado comunitário.
O problema é quando a queda é forçada — como aconteceu em 2020.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="chart-title">Internações psiquiátricas por ano</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">A pandemia acelerou uma queda que já existia — mas de forma abrupta</div>', unsafe_allow_html=True)

    cores = ['#c0392b' if a in [2020,2021] else '#2c3e50' for a in ANOS]
    fig = go.Figure()
    fig.add_bar(x=ANOS, y=INT, marker_color=cores, opacity=0.85,
                hovertemplate='<b>%{x}</b><br>%{y:,.0f} internações<extra></extra>')
    z = np.polyfit(ANOS[:5], INT[:5], 1)
    anos_ext = list(range(2015, 2026))
    fig.add_scatter(x=anos_ext, y=np.poly1d(z)(anos_ext), mode='lines',
                    line=dict(dash='dot', color='#95a5a6', width=1.5),
                    name='Tendência pré-pandemia', hoverinfo='skip')
    fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                  opacity=0.06, layer='below', line_width=0)
    fig.add_annotation(x=2020.5, y=max(INT)*0.95, text="Pandemia",
                       showarrow=False, font=dict(size=10, color='#c0392b'))
    base(fig, 320, showlegend=True,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)),
         yaxis=dict(tickformat=',.0f', title='Internações'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="source-note">Fonte: SIH/DATASUS. Barras vermelhas = anos de pandemia. Linha pontilhada = projeção da tendência pré-pandemia.</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-title">Média de dias internado</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">A internação está ficando cada vez mais curta</div>', unsafe_allow_html=True)

    fig2 = go.Figure()
    fig2.add_scatter(x=ANOS, y=DIAS, mode='lines+markers',
                     line=dict(color='#2c3e50', width=2.5),
                     marker=dict(size=7, color='#2c3e50'),
                     fill='tozeroy', fillcolor='rgba(44,62,80,0.07)',
                     hovertemplate='<b>%{x}</b><br>%{y:.1f} dias<extra></extra>')
    fig2.add_annotation(x=2015, y=21.6, text="21,6 dias",
                        xanchor='left', showarrow=False,
                        font=dict(size=10, color='#888'))
    fig2.add_annotation(x=2025, y=15.3, text="15,3 dias",
                        xanchor='right', showarrow=False,
                        font=dict(size=10, color='#c0392b'))
    base(fig2, 320, yaxis=dict(range=[12,24], title='Dias'))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="source-note">Queda de 0,65 dias/ano. Correlação r=−0,991, p&lt;0,001. A mais forte encontrada neste estudo.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="reflection">
  <div class="reflection-label">Reflexão</div>
  <div class="reflection-text">
  A redução de 21,6 para 15,3 dias de internação em dez anos é um dos dados mais reveladores
  deste estudo. Ela confirma estatisticamente o avanço da Reforma Psiquiátrica — mas levanta
  uma questão incômoda: internações mais curtas significam cuidado melhor, ou simplesmente
  alta mais rápida por falta de leitos e recursos? Os dados não respondem sozinhos.
  Para a sociedade civil, a pergunta importa: o que acontece com essas pessoas após a alta precoce?
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── CAPÍTULO 2 ─────────────────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Capítulo 2</div>
<div class="chapter-title">Suicídio: a crise que a pandemia não criou, mas agravou</div>
<div class="chapter-intro">
Os suicídios em São Paulo cresceram de 2.207 em 2018 para 2.923 em 2022 — um aumento de
32% em quatro anos. O pico coincidiu com o segundo ano da pandemia, mas a tendência de alta
já existia antes. Após 2022, os números recuaram levemente, mas permanecem muito acima
do patamar pré-pandemia. São Paulo registrou, em média, 7,3 mortes por suicídio por dia
entre 2018 e 2024.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 3])

with col1:
    st.markdown('<div class="chart-title">Total de óbitos por suicídio</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Crescimento consistente com pico em 2022</div>', unsafe_allow_html=True)

    cores_s = ['#c0392b' if a >= 2020 else '#2c3e50' for a in ANOS_S]
    fig3 = go.Figure()
    fig3.add_bar(x=ANOS_S, y=SUC, marker_color=cores_s, opacity=0.85,
                 text=SUC, textposition='outside', textfont=dict(size=10),
                 hovertemplate='<b>%{x}</b><br>%{y:,.0f} óbitos<extra></extra>')
    base(fig3, 320, yaxis=dict(range=[0, 3400], tickformat=',.0f'))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="source-note">Fonte: SIM/DATASUS. CID X60–X84.</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-title">Suicídios por sexo</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Homens morrem 3,6 vezes mais — e o gap está aumentando</div>', unsafe_allow_html=True)

    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_bar(x=ANOS_S, y=SUC_M, name='Masculino', marker_color='#2c3e50',
                 opacity=0.85, hovertemplate='%{x} M: %{y:,.0f}<extra></extra>',
                 secondary_y=False)
    fig4.add_bar(x=ANOS_S, y=SUC_F, name='Feminino', marker_color='#e67e22',
                 opacity=0.85, hovertemplate='%{x} F: %{y:,.0f}<extra></extra>',
                 secondary_y=False)
    ratio = [m/f for m,f in zip(SUC_M, SUC_F)]
    fig4.add_scatter(x=ANOS_S, y=ratio, name='Razão M/F', mode='lines+markers',
                     line=dict(color='#c0392b', width=2, dash='dot'),
                     marker=dict(size=6),
                     hovertemplate='%{x}: razão %{y:.2f}x<extra></extra>',
                     secondary_y=True)
    base(fig4, 320, barmode='group',
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)))
    fig4.update_yaxes(gridcolor=GRID, tickformat=',.0f', title='Óbitos', secondary_y=False)
    fig4.update_yaxes(gridcolor='rgba(0,0,0,0)', tickformat='.1f',
                      title='Razão M/F', secondary_y=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('<div class="source-note">Linha vermelha pontilhada = razão masculino/feminino (eixo direito). Razão cresce de 3,7x para 3,6x no período.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="reflection">
  <div class="reflection-label">Reflexão</div>
  <div class="reflection-text">
  Homens morrem por suicídio 3,6 vezes mais que mulheres — mas são menos da metade dos
  atendimentos nos CAPS. Esse paradoxo aponta para uma barreira cultural profunda:
  homens pedem menos ajuda, chegam ao serviço de saúde mais tarde, e quando chegam,
  frequentemente já em crise. Políticas de saúde mental que não considerem esse padrão
  de comportamento masculino diante do sofrimento tendem a chegar tarde demais.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── CAPÍTULO 3 ─────────────────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Capítulo 3</div>
<div class="chapter-title">Os CAPS crescem — mas a pandemia deixou marcas</div>
<div class="chapter-intro">
Os Centros de Atenção Psicossocial são a principal aposta da Reforma Psiquiátrica para
substituir o modelo hospitalocêntrico. Entre 2018 e 2025, os atendimentos cresceram 34,7%,
de 4,1 para 5,5 milhões por ano. Mas em 2020, os CAPS fecharam ou reduziram drasticamente
seus serviços — exatamente quando a demanda por saúde mental explodiu.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-title">Atendimentos nos CAPS por ano</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Recuperação pós-pandemia supera nível anterior</div>', unsafe_allow_html=True)

    cores_c = ['#c0392b' if a in [2020,2021] else '#2c3e50' for a in ANOS_C]
    fig5 = go.Figure()
    fig5.add_bar(x=ANOS_C, y=[v/1e6 for v in CAPS], marker_color=cores_c, opacity=0.85,
                 text=[f'{v/1e6:.1f}M' for v in CAPS], textposition='outside',
                 textfont=dict(size=10),
                 hovertemplate='<b>%{x}</b><br>%{y:.2f}M atendimentos<extra></extra>')
    fig5.add_vrect(x0=2019.5, x1=2021.5, fillcolor='#c0392b',
                   opacity=0.06, layer='below', line_width=0)
    base(fig5, 300, yaxis=dict(range=[0, 6.5], title='Milhões de atendimentos'))
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('<div class="source-note">Fonte: RAAS/DATASUS. Barras vermelhas = anos de pandemia.</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-title">Internações x CAPS — dois sistemas, trajetórias opostas</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Enquanto internações caem, CAPS crescem</div>', unsafe_allow_html=True)

    anos_comum = list(range(2018, 2026))
    int_comum = [96993,98165,70223,77536,82387,90414,93185,98765]

    fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    fig6.add_scatter(x=anos_comum, y=[v/1000 for v in int_comum],
                     name='Internações (mil)', mode='lines+markers',
                     line=dict(color='#2c3e50', width=2.5),
                     marker=dict(size=7),
                     hovertemplate='%{x}: %{y:.0f}k internações<extra></extra>',
                     secondary_y=False)
    fig6.add_scatter(x=ANOS_C, y=[v/1e6 for v in CAPS],
                     name='CAPS (milhões)', mode='lines+markers',
                     line=dict(color='#27ae60', width=2.5),
                     marker=dict(size=7),
                     hovertemplate='%{x}: %{y:.1f}M atendimentos<extra></extra>',
                     secondary_y=True)
    base(fig6, 300,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)))
    fig6.update_yaxes(gridcolor=GRID, title='Internações (mil)', secondary_y=False)
    fig6.update_yaxes(gridcolor='rgba(0,0,0,0)', title='CAPS (milhões)', secondary_y=True)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('<div class="source-note">Azul escuro = internações. Verde = atendimentos CAPS. As trajetórias opostas sugerem substituição do modelo.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="reflection">
  <div class="reflection-label">Reflexão</div>
  <div class="reflection-text">
  O crescimento dos CAPS é uma boa notícia — mas esconde uma pergunta difícil.
  Em 2020, enquanto os atendimentos ambulatoriais caíam de 4,4 para 3,1 milhões,
  os suicídios continuavam subindo. Isso sugere que os CAPS, na pandemia, não
  conseguiram ser a rede de proteção que deveriam ser. Para gestores e formuladores
  de políticas, a pergunta urgente é: como garantir que o modelo comunitário funcione
  exatamente quando a sociedade mais precisa dele — em crises?
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── CAPÍTULO 4 ─────────────────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Capítulo 4</div>
<div class="chapter-title">Quem adoece? A desigualdade nos dados</div>
<div class="chapter-intro">
Os dados de internações psiquiátricas revelam uma transformação silenciosa na composição
racial dos pacientes. Em 2015, 65% dos internados eram brancos e 24% pardos. Em 2025,
essa proporção inverteu: brancos representam 54% e pardos, 36%. Essa mudança não é neutra
— ela reflete desigualdades sociais profundas e levanta questões sobre acesso diferencial
ao sistema de saúde.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-title">Composição racial das internações (2015–2025)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">A proporção parda cresce 11,7 pontos percentuais em dez anos</div>', unsafe_allow_html=True)

    fig7 = go.Figure()
    fig7.add_scatter(x=ANOS, y=PCT_BRANCA, name='Branca', mode='lines+markers',
                     line=dict(color='#2c3e50', width=2.5), marker=dict(size=6),
                     hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
    fig7.add_scatter(x=ANOS, y=PCT_PARDA, name='Parda', mode='lines+markers',
                     line=dict(color='#e67e22', width=2.5), marker=dict(size=6),
                     hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
    fig7.add_scatter(x=ANOS, y=PCT_PRETA, name='Preta', mode='lines+markers',
                     line=dict(color='#7f8c8d', width=1.5, dash='dot'),
                     marker=dict(size=5),
                     hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
    fig7.add_annotation(x=2025, y=54.4, text="54,4%",
                        xanchor='right', showarrow=False,
                        font=dict(size=10, color='#2c3e50'))
    fig7.add_annotation(x=2025, y=35.7, text="35,7%",
                        xanchor='right', showarrow=False,
                        font=dict(size=10, color='#e67e22'))
    base(fig7, 320,
         legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=10)),
         yaxis=dict(ticksuffix='%', range=[0,80]))
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('<div class="source-note">χ²=6.903, p&lt;0,001. A mudança é estatisticamente significativa.</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-title">Diferença no perfil diagnóstico por raça</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Pardos internam mais por condições associadas a acesso tardio</div>', unsafe_allow_html=True)

    diag_l = ['Psicose NE','Múlt. drogas','Bipolar mania','Dep. grave',
              'Dep. cocaína','Dep. álcool','Esq. paranoide','Esq. residual']
    diag_v = [4.6, 3.1, 2.1, -0.2, -0.3, -1.5, -3.3, -4.5]
    cores_d = ['#c0392b' if v > 0 else '#2c3e50' for v in diag_v]

    fig8 = go.Figure()
    fig8.add_bar(x=diag_v, y=diag_l, orientation='h', marker_color=cores_d,
                 opacity=0.85, hovertemplate='%{y}: %{x:+.1f}pp<extra></extra>')
    fig8.add_vline(x=0, line_color='#ccc', line_width=1)
    fig8.add_annotation(x=4.6, y='Psicose NE',
                        text="+4,6pp", xanchor='left', showarrow=False,
                        font=dict(size=10, color='#c0392b'))
    base(fig8, 320, xaxis=dict(ticksuffix='pp', title='Diferença parda − branca (pp)'))
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown('<div class="source-note">Vermelho = diagnóstico mais frequente em pardos vs brancos. Psicose NE pode indicar diagnóstico impreciso por acesso tardio.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="reflection">
  <div class="reflection-label">Reflexão</div>
  <div class="reflection-text">
  O crescimento da proporção parda nas internações psiquiátricas pode ser lido de duas
  formas opostas: como expansão do acesso — mais pessoas pardas chegando ao sistema —
  ou como piora das condições de vida — mais adoecimento psíquico em uma população
  historicamente mais vulnerável. O perfil diagnóstico sugere a segunda hipótese:
  pardos internam mais por "Psicose não especificada" — um diagnóstico vago que frequentemente
  indica chegada tardia ao sistema, sem histórico de acompanhamento. Não é possível
  distinguir acesso de adoecimento com estes dados, mas a pergunta precisa ser feita.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── CONCLUSÃO ──────────────────────────────────────────────────────────
st.markdown("""
<div class="chapter-label">Conclusão</div>
<div class="chapter-title">O que os dados nos dizem — e o que silenciam</div>
<div class="chapter-intro">
Este relatório analisou mais de dez anos de dados públicos sobre saúde mental no SUS em
São Paulo. Os números revelam avanços reais — a desinstitucionalização avança, os CAPS
crescem, as internações longas diminuem. Mas revelam também crises que os dados sozinhos
não conseguem nomear: o sofrimento que não chegou ao sistema, as vidas perdidas antes
de qualquer atendimento, as famílias que não aparecem em nenhuma planilha.
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
conclusoes = [
    ("A reforma funciona,\nmas lentamente",
     "A queda de 0,65 dias de internação por ano durante 11 anos consecutivos "
     "é a evidência mais robusta deste estudo. A política pública está produzindo efeito mensurável."),
    ("A pandemia deixou\ncicatrizes permanentes",
     "53 mil internações não realizadas em 2020–2021. Suicídios que continuaram subindo "
     "enquanto os serviços fechavam. A recuperação é parcial — o nível pré-pandemia "
     "ainda não foi totalmente retomado."),
    ("Desigualdade é um\nfator de risco invisível",
     "A composição racial das internações mudou 11 pontos percentuais em dez anos. "
     "Mulheres pardas ganham R$2.040/mês — o piso de vulnerabilidade socioeconômica "
     "que os dados de saúde mental refletem, mas raramente nomeiam."),
]
for col, (titulo, texto) in zip([c1,c2,c3], conclusoes):
    with col:
        st.markdown(f"""
        <div class="reflection" style="height:100%">
          <div class="reflection-label">Achado</div>
          <div class="reflection-text" style="font-weight:400;margin-bottom:0.8rem">{titulo}</div>
          <div style="font-size:0.85rem;color:#555;line-height:1.7">{texto}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="methodology">
  <p><strong>Metodologia e fontes:</strong>
  Os dados foram obtidos via DATASUS (SIH, SIM, RAAS) e IBGE (PNADC, Censo 2022, Estimativas Populacionais)
  e SINAN, processados através de um pipeline de engenharia de dados com AWS S3, Athena e dbt.
  Análise estatística com Python (scipy, statsmodels). Período: 2015–2025 para internações e violência;
  2018–2024 para suicídios; 2018–2025 para CAPS. São Paulo exclui 2026 por dados incompletos.
  Código e metodologia completos disponíveis em
  <a href="https://github.com/kvgs/sus-saude-mental-analytics" target="_blank">github.com/kvgs/sus-saude-mental-analytics</a>.
  </p>
</div>
""", unsafe_allow_html=True)