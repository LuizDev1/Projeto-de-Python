import pandas as pd
import numpy as np


COLUNAS_BASE = [
    "Country",
    "YearsCode",
    "ConvertedCompYearly",
    "LanguageHaveWorkedWith",
    "EdLevel",
    "DevType",
]

COLUNAS_SATISFACAO_POSSIVEIS = [
    "JobSat",
    "SOComm",
    "SOPartFreq",
]


def converter_anos_experiencia(valor):
    """Converte a coluna YearsCode para número."""
    if pd.isna(valor):
        return np.nan

    valor = str(valor).strip()

    if valor == "Less than 1 year":
        return 0
    if valor == "More than 50 years":
        return 51

    return pd.to_numeric(valor, errors="coerce")


def simplificar_escolaridade(valor):
    """Agrupa os níveis de escolaridade em categorias mais simples."""
    if pd.isna(valor):
        return "Não informado"

    valor = str(valor)

    if "Bachelor" in valor:
        return "Bacharelado"
    if "Master" in valor:
        return "Mestrado"
    if "Professional degree" in valor or "Ph.D" in valor or "doctoral" in valor:
        return "Pós-graduação / Doutorado"
    if "Some college" in valor:
        return "Superior incompleto"
    if "Associate degree" in valor:
        return "Tecnólogo / Associado"
    if "Secondary school" in valor:
        return "Ensino médio"
    if "Primary/elementary" in valor:
        return "Ensino fundamental"

    return "Outro"


def criar_faixa_experiencia(anos):
    """Cria faixas interpretáveis de experiência."""
    if pd.isna(anos):
        return np.nan
    if anos <= 2:
        return "0 a 2 anos"
    if anos <= 5:
        return "3 a 5 anos"
    if anos <= 10:
        return "6 a 10 anos"
    if anos <= 20:
        return "11 a 20 anos"
    return "Mais de 20 anos"


def simplificar_satisfacao(valor):
    """Agrupa respostas de satisfação quando a coluna existir no dataset."""
    if pd.isna(valor):
        return "Não informado"

    valor = str(valor).strip()

    mapa = {
        "Very satisfied": "Muito satisfeito",
        "Slightly satisfied": "Satisfeito",
        "Neither satisfied nor dissatisfied": "Neutro",
        "Slightly dissatisfied": "Insatisfeito",
        "Very dissatisfied": "Muito insatisfeito",
    }

    return mapa.get(valor, valor)


def obter_coluna_satisfacao(df):
    """Retorna a primeira coluna relacionada a satisfação disponível no CSV."""
    for coluna in COLUNAS_SATISFACAO_POSSIVEIS:
        if coluna in df.columns:
            return coluna
    return None


def carregar_dados(caminho_csv="survey_results_public.csv"):
    
    df_original = pd.read_csv(caminho_csv)

    coluna_satisfacao = obter_coluna_satisfacao(df_original)

    colunas = [coluna for coluna in COLUNAS_BASE if coluna in df_original.columns]
    if coluna_satisfacao and coluna_satisfacao not in colunas:
        colunas.append(coluna_satisfacao)

    df = df_original[colunas].copy()

    # Limpeza do salário
    df = df.dropna(subset=["ConvertedCompYearly"])
    df = df[
        (df["ConvertedCompYearly"] >= 1000)
        & (df["ConvertedCompYearly"] <= 500000)
    ]

    # Limpeza da experiência
    df["YearsCode"] = df["YearsCode"].apply(converter_anos_experiencia)
    df = df.dropna(subset=["YearsCode"])
    df["YearsCode"] = df["YearsCode"].astype(int)

    # Colunas derivadas
    df["FaixaExperiencia"] = df["YearsCode"].apply(criar_faixa_experiencia)

    bins_salario = [0, 30000, 70000, 120000, 500000]
    labels_salario = ["Baixo", "Médio", "Alto", "Muito alto"]
    df["FaixaSalarial"] = pd.cut(
        df["ConvertedCompYearly"],
        bins=bins_salario,
        labels=labels_salario,
        include_lowest=True,
    )

    df["LinguagemPrincipal"] = (
        df["LanguageHaveWorkedWith"]
        .fillna("Não informado")
        .str.split(";")
        .str[0]
    )

    df["TipoDesenvolvedorPrincipal"] = (
        df["DevType"]
        .fillna("Não informado")
        .str.split(";")
        .str[0]
    )

    df["EscolaridadeSimplificada"] = df["EdLevel"].apply(simplificar_escolaridade)

    if coluna_satisfacao:
        df["Satisfacao"] = df[coluna_satisfacao].apply(simplificar_satisfacao)
    else:
        df["Satisfacao"] = "Coluna não encontrada"

    df = df.drop_duplicates()

    return df


def aplicar_filtros(df, paises=None, linguagens=None, tipos_dev=None, escolaridades=None, faixa_anos=None):
    """Aplica filtros selecionados no dashboard."""
    df_filtrado = df.copy()

    if paises:
        df_filtrado = df_filtrado[df_filtrado["Country"].isin(paises)]

    if linguagens:
        df_filtrado = df_filtrado[df_filtrado["LinguagemPrincipal"].isin(linguagens)]

    if tipos_dev:
        df_filtrado = df_filtrado[df_filtrado["TipoDesenvolvedorPrincipal"].isin(tipos_dev)]

    if escolaridades:
        df_filtrado = df_filtrado[df_filtrado["EscolaridadeSimplificada"].isin(escolaridades)]

    if faixa_anos:
        minimo, maximo = faixa_anos
        df_filtrado = df_filtrado[
            (df_filtrado["YearsCode"] >= minimo)
            & (df_filtrado["YearsCode"] <= maximo)
        ]

    return df_filtrado


def salario_por_experiencia(df):
    ordem = ["0 a 2 anos", "3 a 5 anos", "6 a 10 anos", "11 a 20 anos", "Mais de 20 anos"]

    resultado = (
        df.groupby("FaixaExperiencia", observed=False)["ConvertedCompYearly"]
        .median()
        .reindex(ordem)
        .dropna()
    )

    return resultado


def salario_por_linguagem(df, top_n=10):
    linguagens_top = df["LinguagemPrincipal"].value_counts().head(top_n).index

    resultado = (
        df[df["LinguagemPrincipal"].isin(linguagens_top)]
        .groupby("LinguagemPrincipal")["ConvertedCompYearly"]
        .median()
        .sort_values()
    )

    return resultado


def salario_por_tipo_dev(df, top_n=10):
    tipos_top = df["TipoDesenvolvedorPrincipal"].value_counts().head(top_n).index

    resultado = (
        df[df["TipoDesenvolvedorPrincipal"].isin(tipos_top)]
        .groupby("TipoDesenvolvedorPrincipal")["ConvertedCompYearly"]
        .median()
        .sort_values()
    )

    return resultado


def salario_por_escolaridade_e_experiencia(df):
    resultado = pd.pivot_table(
        df,
        values="ConvertedCompYearly",
        index="EscolaridadeSimplificada",
        columns="FaixaExperiencia",
        aggfunc="median",
        observed=False,
    )

    ordem_colunas = ["0 a 2 anos", "3 a 5 anos", "6 a 10 anos", "11 a 20 anos", "Mais de 20 anos"]
    resultado = resultado.reindex(columns=[col for col in ordem_colunas if col in resultado.columns])

    return resultado.dropna(how="all")


def salario_por_pais_e_experiencia(df, top_n=8):
    paises_top = df["Country"].value_counts().head(top_n).index

    resultado = pd.pivot_table(
        df[df["Country"].isin(paises_top)],
        values="ConvertedCompYearly",
        index="Country",
        columns="FaixaExperiencia",
        aggfunc="median",
        observed=False,
    )

    ordem_colunas = ["0 a 2 anos", "3 a 5 anos", "6 a 10 anos", "11 a 20 anos", "Mais de 20 anos"]
    resultado = resultado.reindex(columns=[col for col in ordem_colunas if col in resultado.columns])

    return resultado.dropna(how="all")


def salario_por_satisfacao(df):
    if "Satisfacao" not in df.columns or df["Satisfacao"].nunique() <= 1:
        return pd.Series(dtype=float)

    resultado = (
        df[df["Satisfacao"] != "Não informado"]
        .groupby("Satisfacao")["ConvertedCompYearly"]
        .median()
        .sort_values()
    )

    return resultado


def satisfacao_por_experiencia(df):
    if "Satisfacao" not in df.columns or df["Satisfacao"].nunique() <= 1:
        return pd.DataFrame()

    dados = df[
        (df["Satisfacao"] != "Não informado")
        & (df["Satisfacao"] != "Coluna não encontrada")
    ]

    if dados.empty:
        return pd.DataFrame()

    resultado = pd.crosstab(
        dados["FaixaExperiencia"],
        dados["Satisfacao"],
        normalize="index",
    ) * 100

    ordem = ["0 a 2 anos", "3 a 5 anos", "6 a 10 anos", "11 a 20 anos", "Mais de 20 anos"]
    resultado = resultado.reindex([item for item in ordem if item in resultado.index])

    return resultado


def gerar_insight_salario_experiencia(df):
    serie = salario_por_experiencia(df)

    if len(serie) < 2:
        return "Não há dados suficientes para comparar salário por experiência."

    maior = serie.idxmax()
    menor = serie.idxmin()

    return (
        f"A faixa com maior salário mediano é **{maior}**, enquanto a menor é **{menor}**. "
        "Isso indica que a experiência é um fator relevante para o salário, mas deve ser comparada "
        "também com país, escolaridade e tipo de desenvolvedor."
    )


def gerar_insight_linguagem(df):
    serie = salario_por_linguagem(df)

    if serie.empty:
        return "Não há dados suficientes para comparar salários por linguagem."

    maior = serie.idxmax()
    valor = serie.max()

    return (
        f"Entre as linguagens principais mais frequentes, **{maior}** aparece com o maior salário mediano "
        f"no recorte filtrado, cerca de **US$ {valor:,.0f}** ao ano."
    )


def gerar_insight_tipo_dev(df):
    serie = salario_por_tipo_dev(df)

    if serie.empty:
        return "Não há dados suficientes para comparar salários por tipo de desenvolvedor."

    maior = serie.idxmax()
    valor = serie.max()

    return (
        f"O tipo de desenvolvedor com maior salário mediano neste recorte é **{maior}**, "
        f"com aproximadamente **US$ {valor:,.0f}** ao ano."
    )
