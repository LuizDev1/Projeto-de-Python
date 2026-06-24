import pandas as pd
import numpy as np

COLUNAS_BASE = [
    "Country",
    "YearsCode",
    "ConvertedCompYearly",
    "LanguageHaveWorkedWith",
    "EdLevel",
    "DevType",
    "RemoteWork",
]

TRADUCAO_DEVTYPE = {
    "Developer, full-stack": "Dev Full-stack",
    "Developer, back-end": "Dev Back-end",
    "Developer, front-end": "Dev Front-end",
    "Developer, mobile": "Dev Mobile",
    "Developer, desktop or enterprise applications": "Dev Desktop / Enterprise",
    "Developer, embedded applications or devices": "Dev Embarcado",
    "Developer, game or graphics": "Dev Jogos / Gráficos",
    "Developer, QA or test": "Dev QA / Testes",
    "Data scientist or machine learning specialist": "Cientista de Dados / ML",
    "Data or business analyst": "Analista de Dados / Negócios",
    "Engineer, data": "Engenheiro de Dados",
    "Engineer, site reliability": "Engenheiro SRE",
    "Engineering manager": "Gestor de Engenharia",
    "DevOps specialist": "Especialista DevOps",
    "Cloud infrastructure engineer": "Engenheiro de Cloud",
    "Security professional": "Profissional de Segurança",
    "Database administrator": "Administrador de Banco de Dados",
    "System administrator": "Administrador de Sistemas",
    "Senior Executive (C-Suite, VP, etc.)": "Executivo Sênior (C-Suite, VP)",
    "Product manager": "Gerente de Produto",
    "Project manager": "Gerente de Projetos",
    "Academic researcher": "Pesquisador Acadêmico",
    "Blockchain": "Desenvolvedor Blockchain",
    "Designer": "Designer",
    "Educator": "Educador",
    "Developer Advocate": "Developer Advocate",
    "Developer Experience": "Developer Experience",
    "Hardware Engineer": "Engenheiro de Hardware",
    "Marketing or sales professional": "Profissional de Marketing / Vendas",
    "Research & Development role": "P&D",
    "Scientist": "Cientista",
    "Student": "Estudante",
    "Other (please specify):": "Outro",
}

TRADUCAO_PAISES = {
    "United States of America": "Estados Unidos",
    "Germany": "Alemanha",
    "United Kingdom of Great Britain and Northern Ireland": "Reino Unido",
    "Canada": "Canadá",
    "India": "Índia",
    "France": "França",
    "Netherlands": "Países Baixos",
    "Poland": "Polônia",
    "Brazil": "Brasil",
    "Australia": "Austrália",
    "Sweden": "Suécia",
    "Spain": "Espanha",
    "Italy": "Itália",
    "Russian Federation": "Rússia",
    "Switzerland": "Suíça",
    "Portugal": "Portugal",
    "Austria": "Áustria",
    "Norway": "Noruega",
    "Denmark": "Dinamarca",
    "Finland": "Finlândia",
    "Belgium": "Bélgica",
    "Israel": "Israel",
    "Czech Republic": "República Tcheca",
    "Romania": "Romênia",
    "Ukraine": "Ucrânia",
    "Turkey": "Turquia",
    "Pakistan": "Paquistão",
    "Argentina": "Argentina",
    "Mexico": "México",
    "China": "China",
    "Japan": "Japão",
    "Republic of Korea": "Coreia do Sul",
    "New Zealand": "Nova Zelândia",
    "South Africa": "África do Sul",
    "Nigeria": "Nigéria",
    "Greece": "Grécia",
    "Hungary": "Hungria",
    "Ireland": "Irlanda",
    "Colombia": "Colômbia",
    "Bulgaria": "Bulgária",
    "Iran, Islamic Republic of...": "Irã",
    "Serbia": "Sérvia",
    "Lithuania": "Lituânia",
    "Slovakia": "Eslováquia",
    "Slovenia": "Eslovênia",
    "Croatia": "Croácia",
    "Bangladesh": "Bangladesh",
    "Estonia": "Estônia",
    "Indonesia": "Indonésia",
    "Singapore": "Singapura",
    "Chile": "Chile",
    "Philippines": "Filipinas",
    "Malaysia": "Malásia",
    "Viet Nam": "Vietnã",
    "Georgia": "Geórgia",
    "Thailand": "Tailândia",
    "Latvia": "Letônia",
    "Taiwan": "Taiwan",
    "United Arab Emirates": "Emirados Árabes Unidos",
    "Hong Kong (S.A.R.)": "Hong Kong",
    "Sri Lanka": "Sri Lanka",
    "Uruguay": "Uruguai",
    "Egypt": "Egito",
    "Peru": "Peru",
    "Kenya": "Quênia",
    "Armenia": "Armênia",
    "Costa Rica": "Costa Rica",
    "Nepal": "Nepal",
    "Venezuela, Bolivarian Republic of...": "Venezuela",
    "Ecuador": "Equador",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina",
    "Luxembourg": "Luxemburgo",
    "Cyprus": "Chipre",
    "Belarus": "Bielorrússia",
    "Kazakhstan": "Cazaquistão",
    "Morocco": "Marrocos",
    "Dominican Republic": "República Dominicana",
    "Tunisia": "Tunísia",
    "Guatemala": "Guatemala",
    "Saudi Arabia": "Arábia Saudita",
    "Iceland": "Islândia",
    "The former Yugoslav Republic of Macedonia": "Macedônia do Norte",
    "Malta": "Malta",
    "Montenegro": "Montenegro",
    "Jordan": "Jordânia",
    "Ethiopia": "Etiópia",
    "El Salvador": "El Salvador",
    "Paraguay": "Paraguai",
    "Lebanon": "Líbano",
    "Bolivia": "Bolívia",
    "Ghana": "Gana",
    "Republic of Moldova": "Moldávia",
    "Nicaragua": "Nicarágua",
    "Azerbaijan": "Azerbaijão",
    "Albania": "Albânia",
    "Algeria": "Argélia",
    "Uganda": "Uganda",
    "Nomadic": "Nômade",
    "Cuba": "Cuba",
    "Uzbekistan": "Uzbequistão",
    "Myanmar": "Mianmar",
    "Mauritius": "Maurício",
    "Mongolia": "Mongólia",
    "Kyrgyzstan": "Quirguistão",
    "United Republic of Tanzania": "Tanzânia",
    "Panama": "Panamá",
    "Syrian Arab Republic": "Síria",
    "Honduras": "Honduras",
    "Iraq": "Iraque",
    "Cambodia": "Camboja",
    "Palestine": "Palestina",
    "Kosovo": "Kosovo",
    "Isle of Man": "Ilha de Man",
    "Zimbabwe": "Zimbábue",
    "Zambia": "Zâmbia",
    "Jamaica": "Jamaica",
    "Somalia": "Somália",
    "Maldives": "Maldivas",
    "Trinidad and Tobago": "Trinidad e Tobago",
    "Côte d'Ivoire": "Costa do Marfim",
    "Yemen": "Iêmen",
    "Kuwait": "Kuwait",
    "Cameroon": "Camarões",
    "Benin": "Benim",
    "Andorra": "Andorra",
    "Madagascar": "Madagascar",
    "Rwanda": "Ruanda",
    "Bahrain": "Bahrein",
    "Afghanistan": "Afeganistão",
    "Qatar": "Catar",
    "Oman": "Omã",
    "Senegal": "Senegal",
    "Turkmenistan": "Turcomenistão",
    "Mozambique": "Moçambique",
    "Malawi": "Malaui",
    "Togo": "Togo",
    "Swaziland": "Essuatíni",
    "Djibouti": "Djibuti",
    "Fiji": "Fiji",
    "Barbados": "Barbados",
    "Mali": "Mali",
    "Palau": "Palau",
    "Belize": "Belize",
    "Namibia": "Namíbia",
    "Saint Lucia": "Santa Lúcia",
    "Monaco": "Mônaco",
    "Niger": "Níger",
    "Suriname": "Suriname",
    "Tajikistan": "Tajiquistão",
    "Lao People's Democratic Republic": "Laos",
    "Gabon": "Gabão",
    "Guinea-Bissau": "Guiné-Bissau",
    "Guyana": "Guiana",
    "Botswana": "Botsuana",
    "Mauritania": "Mauritânia",
    "Dominica": "Dominica",
    "Liechtenstein": "Liechtenstein",
    "Saint Kitts and Nevis": "São Cristóvão e Nevis",
    "Brunei Darussalam": "Brunei",
    "Angola": "Angola",
    "Burundi": "Burundi",
    "Cape Verde": "Cabo Verde",
    "Sudan": "Sudão",
    "Guinea": "Guiné",
    "Saint Vincent and the Grenadines": "São Vicente e Granadinas",
    "Burkina Faso": "Burkina Faso",
    "Antigua and Barbuda": "Antígua e Barbuda",
    "Libyan Arab Jamahiriya": "Líbia",
    "Portugal": "Portugal",
    "Israel": "Israel",
    "Argentina": "Argentina",
    "China": "China",
    "Bangladesh": "Bangladesh",
    "Chile": "Chile",
    "Taiwan": "Taiwan",
    "Sri Lanka": "Sri Lanka",
    "South Korea": "Coreia do Sul",
    "Peru": "Peru",
    "Bahamas": "Bahamas",
    "Bhutan": "Butão",
    "Central African Republic": "República Centro-Africana",
    "Congo, Republic of the...": "Congo",
    "Democratic People's Republic of Korea": "Coreia do Norte",
    "Democratic Republic of the Congo": "República Democrática do Congo",
    "Grenada": "Granada",
    "Haiti": "Haiti",
    "Lesotho": "Lesoto",
    "Liberia": "Libéria",
    "Marshall Islands": "Ilhas Marshall",
    "North Korea": "Coreia do Norte",
    "Samoa": "Samoa",
    "San Marino": "San Marino",
    "Sierra Leone": "Serra Leoa",
    "Timor-Leste": "Timor-Leste",
}

TRADUCAO_REGIME = {
    "Remote": "Remoto",
    "Hybrid (some remote, some in-person)": "Híbrido",
    "In-person": "Presencial",
}


def simplificar_escolaridade(valor):
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


def carregar_dados(caminho_csv="survey_results_public.csv"):
    df_original = pd.read_csv(caminho_csv)
    colunas = [c for c in COLUNAS_BASE if c in df_original.columns]
    df = df_original[colunas].copy()

    df = df.dropna(subset=["ConvertedCompYearly"])
    df = df[(df["ConvertedCompYearly"] >= 1000) & (df["ConvertedCompYearly"] <= 500000)]

    df["YearsCode"] = pd.to_numeric(df["YearsCode"], errors="coerce")
    df = df.dropna(subset=["YearsCode"])
    df["YearsCode"] = df["YearsCode"].astype(int)

    df["FaixaExperiencia"] = df["YearsCode"].apply(criar_faixa_experiencia)

    bins = [0, 30000, 70000, 120000, 500000]
    labels = ["Baixo", "Médio", "Alto", "Muito alto"]
    df["FaixaSalarial"] = pd.cut(df["ConvertedCompYearly"], bins=bins, labels=labels, include_lowest=True)

    df["LinguagemPrincipal"] = df["LanguageHaveWorkedWith"].fillna("Não informado").str.split(";").str[0]

    df["TipoDesenvolvedorPrincipal"] = (
        df["DevType"].fillna("Não informado").str.split(";").str[0].map(lambda x: TRADUCAO_DEVTYPE.get(x, x))
    )

    df["EscolaridadeSimplificada"] = df["EdLevel"].apply(simplificar_escolaridade)

    df["PaisTraducao"] = df["Country"].map(lambda x: TRADUCAO_PAISES.get(x, x))

    df["Regime"] = df["RemoteWork"].map(TRADUCAO_REGIME)

    df = df.drop_duplicates()
    return df


def aplicar_filtros(df, paises=None, linguagens=None, tipos_dev=None, escolaridades=None, faixa_anos=None):
    df_filtrado = df.copy()
    if paises:
        df_filtrado = df_filtrado[df_filtrado["PaisTraducao"].isin(paises)]
    if linguagens:
        df_filtrado = df_filtrado[df_filtrado["LinguagemPrincipal"].isin(linguagens)]
    if tipos_dev:
        df_filtrado = df_filtrado[df_filtrado["TipoDesenvolvedorPrincipal"].isin(tipos_dev)]
    if escolaridades:
        df_filtrado = df_filtrado[df_filtrado["EscolaridadeSimplificada"].isin(escolaridades)]
    if faixa_anos:
        minimo, maximo = faixa_anos
        df_filtrado = df_filtrado[(df_filtrado["YearsCode"] >= minimo) & (df_filtrado["YearsCode"] <= maximo)]
    return df_filtrado


def salario_por_experiencia(df):
    ordem = ["0 a 2 anos", "3 a 5 anos", "6 a 10 anos", "11 a 20 anos", "Mais de 20 anos"]
    return df.groupby("FaixaExperiencia", observed=False)["ConvertedCompYearly"].median().reindex(ordem).dropna()


def salario_por_linguagem(df, top_n=10):
    top = df["LinguagemPrincipal"].value_counts().head(top_n).index
    return df[df["LinguagemPrincipal"].isin(top)].groupby("LinguagemPrincipal")["ConvertedCompYearly"].median().sort_values()


def salario_por_tipo_dev(df, top_n=10):
    top = df["TipoDesenvolvedorPrincipal"].value_counts().head(top_n).index
    return df[df["TipoDesenvolvedorPrincipal"].isin(top)].groupby("TipoDesenvolvedorPrincipal")["ConvertedCompYearly"].median().sort_values()


def salario_por_escolaridade_e_experiencia(df):
    resultado = pd.pivot_table(
        df, values="ConvertedCompYearly",
        index="EscolaridadeSimplificada", columns="FaixaExperiencia",
        aggfunc="median", observed=False,
    )
    ordem = ["0 a 2 anos", "3 a 5 anos", "6 a 10 anos", "11 a 20 anos", "Mais de 20 anos"]
    return resultado.reindex(columns=[c for c in ordem if c in resultado.columns]).dropna(how="all")


def salario_por_pais_e_experiencia(df, top_n=8):
    top = df["PaisTraducao"].value_counts().head(top_n).index
    resultado = pd.pivot_table(
        df[df["PaisTraducao"].isin(top)], values="ConvertedCompYearly",
        index="PaisTraducao", columns="FaixaExperiencia",
        aggfunc="median", observed=False,
    )
    ordem = ["0 a 2 anos", "3 a 5 anos", "6 a 10 anos", "11 a 20 anos", "Mais de 20 anos"]
    return resultado.reindex(columns=[c for c in ordem if c in resultado.columns]).dropna(how="all")


def salario_por_regime(df):
    return df.groupby("Regime")["ConvertedCompYearly"].median().sort_values()


def gerar_insight_salario_experiencia(df):
    serie = salario_por_experiencia(df)
    if len(serie) < 2:
        return "Não há dados suficientes para comparar salário por experiência."
    maior = serie.idxmax()
    menor = serie.idxmin()
    variacao = ((serie.max() - serie.min()) / serie.min()) * 100
    return (
        f"A faixa com maior salário mediano é **{maior}** e a menor é **{menor}**. "
        f"A diferença entre elas é de **{variacao:.0f}%**, o que indica que a experiência "
        "tem impacto relevante na remuneração."
    )


def gerar_insight_linguagem(df):
    serie = salario_por_linguagem(df)
    if serie.empty:
        return "Não há dados suficientes para comparar salários por linguagem."
    maior = serie.idxmax()
    menor = serie.idxmin()
    return (
        f"**{maior}** lidera com o maior salário mediano no recorte atual, "
        f"enquanto **{menor}** aparece na posição mais baixa entre as linguagens mais usadas. "
        "Isso sugere que a escolha tecnológica pode influenciar diretamente na remuneração."
    )


def gerar_insight_tipo_dev(df):
    serie = salario_por_tipo_dev(df)
    if serie.empty:
        return "Não há dados suficientes para comparar salários por tipo de desenvolvedor."
    maior = serie.idxmax()
    valor = serie.max()
    return (
        f"**{maior}** aparece com o maior salário mediano neste recorte, "
        f"aproximadamente **US$ {valor:,.0f}** ao ano. "
        "Áreas como dados, cloud e engenharia de confiabilidade tendem a ter remuneração superior."
    )


def gerar_insight_regime(df):
    serie = salario_por_regime(df)
    if serie.empty:
        return "Não há dados suficientes para comparar salários por regime de trabalho."
    maior = serie.idxmax()
    menor = serie.idxmin()
    variacao = ((serie.max() - serie.min()) / serie.min()) * 100
    return (
        f"O regime **{maior}** está associado ao maior salário mediano, "
        f"enquanto **{menor}** aparece com o menor. "
        f"A diferença entre os regimes é de **{variacao:.0f}%** no recorte atual."
    )