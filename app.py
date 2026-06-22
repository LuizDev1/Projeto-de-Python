import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from analise import carregar_dados

st.set_page_config(page_title='Stack Overflow Developer Survey', layout='wide')

@st.cache_data
def get_data():
    return carregar_dados()

df = get_data()

traducao_paises = {
    'United States of America': 'Estados Unidos',
    'Germany': 'Alemanha',
    'United Kingdom of Great Britain and Northern Ireland': 'Reino Unido',
    'Canada': 'Canadá',
    'India': 'Índia',
    'France': 'França',
    'Netherlands': 'Países Baixos',
    'Poland': 'Polônia',
    'Brazil': 'Brasil',
    'Australia': 'Austrália',
}

traducao_edlevel = {
    'Bachelor\u2019s degree (B.A., B.S., B.Eng., etc.)': 'Bacharelado',
    'Master\u2019s degree (M.A., M.S., M.Eng., MBA, etc.)': 'Mestrado',
    'Some college/university study without earning a degree': 'Cursando / Sem diploma',
    'Professional degree (JD, MD, Ph.D, Ed.D, etc.)': 'Pós-graduação / Doutorado',
    'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 'Ensino Médio',
    'Associate degree (A.A., A.S., etc.)': 'Tecnólogo / Associado',
    'Something else': 'Outro',
    'Primary/elementary school': 'Ensino Fundamental',
}

st.title('Stack Overflow Developer Survey 2023')
st.markdown('Análise exploratória sobre salários e perfil de desenvolvedores ao redor do mundo.')

st.markdown('---')
col1, col2, col3 = st.columns(3)
col1.metric('Total de Respondentes', f'{len(df):,}')
col2.metric('Salário Médio (USD)', f'${df["ConvertedCompYearly"].mean():,.0f}')
col3.metric('Países Representados', df['Country'].nunique())
st.markdown('---')

st.subheader('Top 10 Países com Mais Desenvolvedores')
top_paises = df['Country'].value_counts().head(10)
top_paises.index = [traducao_paises.get(p, p) for p in top_paises.index]
fig1, ax1 = plt.subplots(figsize=(7, 3))
ax1.barh(top_paises.index[::-1], top_paises.values[::-1], color='steelblue')
ax1.set_xlabel('Número de Respondentes')
ax1.set_ylabel('País')
plt.tight_layout()
st.pyplot(fig1)

st.markdown('---')

st.subheader('Distribuição de Salários por Faixa')
faixa_ordem = ['Baixo', 'Médio', 'Alto', 'Muito Alto']
faixa_counts = df['FaixaSalarial'].value_counts().reindex(faixa_ordem)
fig2, ax2 = plt.subplots(figsize=(6, 3))
ax2.bar(faixa_counts.index, faixa_counts.values, color=['#4CAF50', '#2196F3', '#FF9800', '#F44336'])
ax2.set_xlabel('Faixa Salarial')
ax2.set_ylabel('Número de Desenvolvedores')
plt.tight_layout()
st.pyplot(fig2)

st.markdown('---')

st.subheader('Top 10 Linguagens Mais Utilizadas')
top_linguagens = df['LinguagemPrincipal'].value_counts().head(10)
fig3, ax3 = plt.subplots(figsize=(7, 3))
ax3.barh(top_linguagens.index[::-1], top_linguagens.values[::-1], color='mediumseagreen')
ax3.set_xlabel('Número de Desenvolvedores')
ax3.set_ylabel('Linguagem')
plt.tight_layout()
st.pyplot(fig3)

st.markdown('---')

st.subheader('Salário Mediano por Linguagem Principal (Top 10)')
top_langs = df['LinguagemPrincipal'].value_counts().head(10).index
salario_lang = df[df['LinguagemPrincipal'].isin(top_langs)].groupby('LinguagemPrincipal')['ConvertedCompYearly'].median().sort_values()
fig4, ax4 = plt.subplots(figsize=(7, 3))
ax4.barh(salario_lang.index, salario_lang.values, color='coral')
ax4.set_xlabel('Salário Mediano (USD)')
ax4.set_ylabel('Linguagem')
plt.tight_layout()
st.pyplot(fig4)

st.markdown('---')

st.subheader('Experiência vs. Salário')
anos_sal = df.groupby('YearsCode')['ConvertedCompYearly'].median().reset_index()
fig5, ax5 = plt.subplots(figsize=(7, 3))
ax5.plot(anos_sal['YearsCode'], anos_sal['ConvertedCompYearly'], marker='o', color='steelblue')
ax5.set_xlabel('Anos de Experiência')
ax5.set_ylabel('Salário Mediano (USD)')
plt.tight_layout()
st.pyplot(fig5)

st.markdown('---')

st.subheader('Nível de Escolaridade dos Desenvolvedores')
edlevel_counts = df['EdLevel'].value_counts()
edlevel_labels = [traducao_edlevel.get(l, l) for l in edlevel_counts.index]
cores = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f']
fig6, ax6 = plt.subplots(figsize=(5, 4))
wedges, _, autotexts = ax6.pie(
    edlevel_counts.values,
    autopct='%1.1f%%',
    startangle=140,
    pctdistance=0.78,
    colors=cores,
)
for at in autotexts:
    at.set_fontsize(6)
ax6.legend(
    wedges,
    edlevel_labels,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.02),
    ncol=2,
    fontsize=6,
)
plt.tight_layout()
st.pyplot(fig6)