import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from analise import (
    carregar_dados,
    aplicar_filtros,
    salario_por_experiencia,
    salario_por_linguagem,
    salario_por_tipo_dev,
    salario_por_escolaridade_e_experiencia,
    salario_por_pais_e_experiencia,
    salario_por_regime,
    gerar_insight_salario_experiencia,
    gerar_insight_linguagem,
    gerar_insight_tipo_dev,
    gerar_insight_regime,
)

st.set_page_config(page_title="Stack Overflow Developer Survey", layout="wide")

@st.cache_data
def get_data():
    return carregar_dados()

def plot_barh(serie, titulo, xlabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(serie.index.astype(str), serie.values)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    return fig

def plot_line(serie, titulo, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(serie.index.astype(str), serie.values, marker="o")
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    plt.xticks(rotation=15)
    plt.tight_layout()
    return fig

def plot_heatmap(df_tabela, titulo):
    fig, ax = plt.subplots(figsize=(10, 4))
    dados = df_tabela.fillna(0)
    imagem = ax.imshow(dados.values, aspect="auto")
    ax.set_title(titulo)
    ax.set_xticks(range(len(dados.columns)))
    ax.set_yticks(range(len(dados.index)))
    ax.set_xticklabels(dados.columns, rotation=25, ha="right", fontsize=9)
    ax.set_yticklabels(dados.index, fontsize=9)
    for i in range(len(dados.index)):
        for j in range(len(dados.columns)):
            valor = dados.iloc[i, j]
            texto = "" if valor == 0 else f"{valor:,.0f}"
            ax.text(j, i, texto, ha="center", va="center", fontsize=7)
    fig.colorbar(imagem, ax=ax)
    plt.tight_layout()
    return fig

df = get_data()

st.title("Stack Overflow Developer Survey 2023")
st.markdown(
    "Dashboard para responder à pergunta de negócio: "
    "**Quais fatores mais influenciam o salário de desenvolvedores de software ao redor do mundo?**"
)

st.sidebar.header("Filtros da análise")

paises = st.sidebar.multiselect(
    "País",
    sorted(df["PaisTraducao"].dropna().unique())
)
linguagens = st.sidebar.multiselect(
    "Linguagem principal",
    sorted(df["LinguagemPrincipal"].dropna().unique())
)
tipos_dev = st.sidebar.multiselect(
    "Tipo de desenvolvedor",
    sorted(df["TipoDesenvolvedorPrincipal"].dropna().unique())
)
escolaridades = st.sidebar.multiselect(
    "Escolaridade",
    sorted(df["EscolaridadeSimplificada"].dropna().unique())
)
min_anos = int(df["YearsCode"].min())
max_anos = int(df["YearsCode"].max())
faixa_anos = st.sidebar.slider("Anos de experiência", min_anos, max_anos, (min_anos, max_anos))

df_filtrado = aplicar_filtros(df, paises=paises, linguagens=linguagens, tipos_dev=tipos_dev, escolaridades=escolaridades, faixa_anos=faixa_anos)

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Respondentes analisados", f"{len(df_filtrado):,}")
col2.metric("Salário médio", f"US$ {df_filtrado['ConvertedCompYearly'].mean():,.0f}")
col3.metric("Salário mediano", f"US$ {df_filtrado['ConvertedCompYearly'].median():,.0f}")
col4.metric("Países no recorte", df_filtrado["PaisTraducao"].nunique())
st.markdown("---")

st.header("1. Experiência e salário")
serie_exp = salario_por_experiencia(df_filtrado)
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(plot_line(serie_exp, "Salário mediano por faixa de experiência", "Faixa de experiência", "Salário mediano (USD)"))
with col2:
    st.info(gerar_insight_salario_experiencia(df_filtrado))
st.markdown("---")

st.header("2. Linguagem principal e salário")
serie_lang = salario_por_linguagem(df_filtrado)
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(plot_barh(serie_lang, "Salário mediano por linguagem principal", "Salário mediano (USD)"))
with col2:
    st.info(gerar_insight_linguagem(df_filtrado))
st.markdown("---")

st.header("3. Tipo de desenvolvedor e salário")
serie_tipo = salario_por_tipo_dev(df_filtrado)
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(plot_barh(serie_tipo, "Salário mediano por tipo de desenvolvedor", "Salário mediano (USD)"))
with col2:
    st.info(gerar_insight_tipo_dev(df_filtrado))
st.markdown("---")

st.header("4. Regime de trabalho e salário")
serie_regime = salario_por_regime(df_filtrado)
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(plot_barh(serie_regime, "Salário mediano por regime de trabalho", "Salário mediano (USD)"))
with col2:
    st.info(gerar_insight_regime(df_filtrado))
st.markdown("---")

st.header("5. Escolaridade combinada com experiência")
tabela_edu = salario_por_escolaridade_e_experiencia(df_filtrado)
if tabela_edu.empty:
    st.warning("Não há dados suficientes para cruzar escolaridade e experiência.")
else:
    st.pyplot(plot_heatmap(tabela_edu, "Salário mediano por escolaridade e faixa de experiência (USD)"))
    st.info(
        "Essa tabela mostra que a escolaridade não deve ser lida isoladamente. "
        "Dentro do mesmo nível educacional, a experiência ainda gera variações salariais significativas."
    )
st.markdown("---")

st.header("6. País combinado com experiência")
tabela_pais = salario_por_pais_e_experiencia(df_filtrado)
if tabela_pais.empty:
    st.warning("Não há dados suficientes para cruzar país e experiência.")
else:
    st.pyplot(plot_heatmap(tabela_pais, "Salário mediano por país e faixa de experiência (USD)"))
    st.info(
        "O país de atuação influencia fortemente o salário, pois reflete diferenças de mercado, "
        "moeda e custo de vida. Combinado com a experiência, esse cruzamento revela padrões mais precisos."
    )
st.markdown("---")

st.header("Conclusão: principais fatores analisados")
st.markdown(
    """
- **Experiência:** quanto maior a experiência, maior o salário mediano — com variação percentual calculada dinamicamente.
- **Linguagem principal:** tecnologias como Go e Rust tendem a estar associadas a salários mais altos.
- **Tipo de desenvolvedor:** áreas de dados, cloud e SRE lideram em remuneração.
- **Regime de trabalho:** o regime remoto ou híbrido aparece associado a salários medianos mais altos.
- **Escolaridade × experiência:** o nível educacional sozinho não explica o salário; a experiência é determinante dentro de cada faixa.
- **País × experiência:** mercados como Estados Unidos e Suíça lideram em remuneração em todas as faixas de carreira.
    """
)