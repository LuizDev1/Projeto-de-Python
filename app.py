import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from analise import carregar_dados

st.set_page_config(page_title='Stack Overflow Developer Survey', layout='wide')

@st.cache_data
def get_data():
    return carregar_dados()

df = get_data()

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
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.barh(top_paises.index[::-1], top_paises.values[::-1], color='steelblue')
ax1.set_xlabel('Número de Respondentes')
ax1.set_ylabel('País')
plt.tight_layout()
st.pyplot(fig1)

st.markdown('---')

st.subheader('Distribuição de Salários por Faixa')
faixa_ordem = ['Baixo', 'Médio', 'Alto', 'Muito Alto']
faixa_counts = df['FaixaSalarial'].value_counts().reindex(faixa_ordem)
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(faixa_counts.index, faixa_counts.values, color=['#4CAF50', '#2196F3', '#FF9800', '#F44336'])
ax2.set_xlabel('Faixa Salarial')
ax2.set_ylabel('Número de Desenvolvedores')
plt.tight_layout()
st.pyplot(fig2)

st.markdown('---')

st.subheader('Top 10 Linguagens Mais Utilizadas')
top_linguagens = df['LinguagemPrincipal'].value_counts().head(10)
fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.barh(top_linguagens.index[::-1], top_linguagens.values[::-1], color='mediumseagreen')
ax3.set_xlabel('Número de Desenvolvedores')
ax3.set_ylabel('Linguagem')
plt.tight_layout()
st.pyplot(fig3)

st.markdown('---')

st.subheader('Salário Médio por Linguagem Principal (Top 10)')
top_langs = df['LinguagemPrincipal'].value_counts().head(10).index
salario_lang = df[df['LinguagemPrincipal'].isin(top_langs)].groupby('LinguagemPrincipal')['ConvertedCompYearly'].median().sort_values()
fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.barh(salario_lang.index, salario_lang.values, color='coral')
ax4.set_xlabel('Salário Mediano (USD)')
ax4.set_ylabel('Linguagem')
plt.tight_layout()
st.pyplot(fig4)

st.markdown('---')

st.subheader('Experiência vs. Salário')
fig5, ax5 = plt.subplots(figsize=(10, 4))
anos_sal = df.groupby('YearsCode')['ConvertedCompYearly'].median().reset_index()
ax5.plot(anos_sal['YearsCode'], anos_sal['ConvertedCompYearly'], marker='o', color='steelblue')
ax5.set_xlabel('Anos de Experiência')
ax5.set_ylabel('Salário Mediano (USD)')
plt.tight_layout()
st.pyplot(fig5)

st.markdown('---')

st.subheader('Nível de Escolaridade dos Desenvolvedores')
edlevel_counts = df['EdLevel'].value_counts()
edlevel_labels = [label[:30] + '...' if len(label) > 30 else label for label in edlevel_counts.index]
fig6, ax6 = plt.subplots(figsize=(6, 6))
ax6.pie(edlevel_counts.values, labels=edlevel_labels, autopct='%1.1f%%', startangle=140)
plt.tight_layout()
st.pyplot(fig6)
