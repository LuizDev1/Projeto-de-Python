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
    salario_por_satisfacao,
    satisfacao_por_experiencia,
    gerar_insight_salario_experiencia,
    gerar_insight_linguagem,
    gerar_insight_tipo_dev,
)


st.set_page_config(
    page_title="Stack Overflow Developer Survey",
    layout="wide"
)


@st.cache_data
def get_data():
    return carregar_dados()


def formatar_dolar(valor):
    return f"US$ {valor:,.0f}"


def plot_barh(serie, titulo, xlabel):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.barh(serie.index.astype(str), serie.values)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    return fig


def plot_line(serie, titulo, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(serie.index.astype(str), serie.values, marker="o")
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    plt.xticks(rotation=20)
    plt.tight_layout()
    return fig


def plot_tabela_como_heatmap(df_tabela, titulo):
    fig, ax = plt.subplots(figsize=(10, 4))

    dados = df_tabela.fillna(0)

    imagem = ax.imshow(dados.values, aspect="auto")
    ax.set_title(titulo)
    ax.set_xticks(range(len(dados.columns)))
    ax.set_yticks(range(len(dados.index)))
    ax.set_xticklabels(dados.columns, rotation=30, ha="right")
    ax.set_yticklabels(dados.index)

    for i in range(len(dados.index)):
        for j in range(len(dados.columns)):
            valor = dados.iloc[i, j]
            texto = "" if valor == 0 else f"{valor:,.0f}"
            ax.text(j, i, texto, ha="center", va="center", fontsize=8)

    fig.colorbar(imagem, ax=ax)
    plt.tight_layout()

    return fig


df = get_data()

st.title("Stack Overflow Developer Survey")
st.markdown(
    """
    Dashboard para responder à pergunta de negócio:

    **Quais fatores mais influenciam a satisfação e o salário de desenvolvedores de software ao redor do mundo?**

    A análise considera salário anual convertido para dólar, experiência, país, linguagem principal,
    tipo de desenvolvedor, escolaridade e satisfação quando essa coluna estiver disponível no CSV.
    """
)

st.sidebar.header("Filtros da análise")

paises = st.sidebar.multiselect(
    "País",
    sorted(df["Country"].dropna().unique())
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

faixa_anos = st.sidebar.slider(
    "Anos de experiência",
    min_value=min_anos,
    max_value=max_anos,
    value=(min_anos, max_anos)
)

df_filtrado = aplicar_filtros(
    df,
    paises=paises,
    linguagens=linguagens,
    tipos_dev=tipos_dev,
    escolaridades=escolaridades,
    faixa_anos=faixa_anos,
)

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Respondentes analisados", f"{len(df_filtrado):,}")
col2.metric("Salário médio", formatar_dolar(df_filtrado["ConvertedCompYearly"].mean()))
col3.metric("Salário mediano", formatar_dolar(df_filtrado["ConvertedCompYearly"].median()))
col4.metric("Países no recorte", df_filtrado["Country"].nunique())

st.markdown("---")

st.header("1. Relação entre experiência e salário")

serie_exp = salario_por_experiencia(df_filtrado)

col_grafico, col_texto = st.columns([2, 1])

with col_grafico:
    st.pyplot(
        plot_line(
            serie_exp,
            "Salário mediano por faixa de experiência",
            "Faixa de experiência",
            "Salário mediano anual em USD"
        )
    )

with col_texto:
    st.info(gerar_insight_salario_experiencia(df_filtrado))
    st.markdown(
        """
        Essa análise é mais profunda do que apenas contar respondentes, pois compara
        diretamente uma variável explicativa, **experiência**, com a variável de resultado,
        **salário**.
        """
    )

st.markdown("---")

st.header("2. Linguagem principal e salário")

serie_lang = salario_por_linguagem(df_filtrado)

col_grafico, col_texto = st.columns([2, 1])

with col_grafico:
    st.pyplot(
        plot_barh(
            serie_lang,
            "Salário mediano por linguagem principal",
            "Salário mediano anual em USD"
        )
    )

with col_texto:
    st.info(gerar_insight_linguagem(df_filtrado))
    st.markdown(
        """
        Aqui o objetivo não é apenas mostrar as linguagens mais usadas, mas observar
        quais aparecem associadas a maiores salários medianos no recorte selecionado.
        """
    )

st.markdown("---")

st.header("3. Tipo de desenvolvedor e salário")

serie_tipo = salario_por_tipo_dev(df_filtrado)

col_grafico, col_texto = st.columns([2, 1])

with col_grafico:
    st.pyplot(
        plot_barh(
            serie_tipo,
            "Salário mediano por tipo de desenvolvedor",
            "Salário mediano anual em USD"
        )
    )

with col_texto:
    st.info(gerar_insight_tipo_dev(df_filtrado))
    st.markdown(
        """
        Essa comparação ajuda a identificar se a área de atuação, como backend,
        frontend, mobile, dados ou gestão, tem relação com diferenças salariais.
        """
    )

st.markdown("---")

st.header("4. Escolaridade combinada com experiência")

tabela_edu_exp = salario_por_escolaridade_e_experiencia(df_filtrado)

if tabela_edu_exp.empty:
    st.warning("Não há dados suficientes para cruzar escolaridade e experiência.")
else:
    st.pyplot(
        plot_tabela_como_heatmap(
            tabela_edu_exp,
            "Salário mediano por escolaridade e faixa de experiência"
        )
    )

    st.info(
        "Essa tabela evita uma conclusão superficial. Ela mostra que a escolaridade deve ser interpretada junto com a experiência, "
        "pois o salário pode variar bastante dentro do mesmo nível educacional."
    )

st.markdown("---")

st.header("5. País combinado com experiência")

tabela_pais_exp = salario_por_pais_e_experiencia(df_filtrado)

if tabela_pais_exp.empty:
    st.warning("Não há dados suficientes para cruzar país e experiência.")
else:
    st.pyplot(
        plot_tabela_como_heatmap(
            tabela_pais_exp,
            "Salário mediano por país e faixa de experiência"
        )
    )

    st.info(
        "O país é um fator importante porque salários convertidos para dólar variam muito conforme mercado local, moeda, custo de vida "
        "e concentração de empresas internacionais."
    )

st.markdown("---")

st.header("6. Satisfação e salário")

serie_sat = salario_por_satisfacao(df_filtrado)

if serie_sat.empty:
    st.warning(
        "Não foi encontrada uma coluna de satisfação adequada no CSV ou não há dados suficientes para essa análise."
    )
else:
    col_grafico, col_texto = st.columns([2, 1])

    with col_grafico:
        st.pyplot(
            plot_barh(
                serie_sat,
                "Salário mediano por nível de satisfação",
                "Salário mediano anual em USD"
            )
        )

    with col_texto:
        st.info(
            "Essa análise verifica se níveis diferentes de satisfação aparecem associados a salários medianos diferentes."
        )

    tabela_sat_exp = satisfacao_por_experiencia(df_filtrado)

    if not tabela_sat_exp.empty:
        st.subheader("Distribuição percentual de satisfação por experiência")
        st.dataframe(tabela_sat_exp.round(1))

        st.info(
            "Essa tabela ajuda a observar se a satisfação muda conforme a experiência, sem olhar apenas para o salário."
        )

st.markdown("---")

st.header("Os principais fatores analisados:")

st.markdown(
    """
    - **Experiência:** permite observar evolução salarial por tempo de carreira.
    - **País:** ajuda a explicar diferenças salariais entre mercados.
    - **Linguagem principal:** mostra tecnologias associadas a maiores salários medianos.
    - **Tipo de desenvolvedor:** compara diferentes áreas de atuação.
    - **Escolaridade:** é interpretada junto com experiência para evitar conclusões simples demais.
    - **Satisfação:** quando disponível no dataset, é comparada com salário e experiência.
    """
)
