import pandas as pd
import numpy as np

def carregar_dados():
    df = pd.read_csv('survey_results_public.csv')

    colunas = [
        'Country',
        'YearsCode',
        'ConvertedCompYearly',
        'LanguageHaveWorkedWith',
        'EdLevel',
        'DevType',
    ]
    df = df[colunas]

    df = df.dropna(subset=['ConvertedCompYearly'])
    df = df[(df['ConvertedCompYearly'] >= 1000) & (df['ConvertedCompYearly'] <= 500000)]

    df['YearsCode'] = pd.to_numeric(df['YearsCode'], errors='coerce')
    df = df.dropna(subset=['YearsCode'])
    df['YearsCode'] = df['YearsCode'].astype(int)

    bins = [0, 30000, 70000, 120000, 500000]
    labels = ['Baixo', 'Médio', 'Alto', 'Muito Alto']
    df['FaixaSalarial'] = pd.cut(df['ConvertedCompYearly'], bins=bins, labels=labels)

    df['LinguagemPrincipal'] = df['LanguageHaveWorkedWith'].str.split(';').str[0]

    df = df.drop_duplicates()

    return df
