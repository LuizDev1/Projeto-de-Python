# Stack Overflow Developer Survey 2023 — Análise Exploratória

Projeto desenvolvido como trabalho final da disciplina de Ciência de Dados, com o objetivo de analisar o perfil e os salários de desenvolvedores de software ao redor do mundo a partir dos dados da pesquisa anual do Stack Overflow.

**Pergunta de negócio:** Quais fatores mais influenciam o salário de desenvolvedores de software ao redor do mundo?

---

## Tecnologias Utilizadas

- Python 3
- Pandas
- NumPy
- Matplotlib
- Streamlit

---

## Estrutura do Projeto

```
Projeto-de-Python/
├── analise.py                    # Limpeza e preparação dos dados
├── app.py                        # Dashboard interativo com Streamlit
├── survey_results_public.csv     # Dataset (Stack Overflow Developer Survey 2023)
└── README.md
```

---

## Como Executar

**1. Instale as dependências:**
```bash
pip install pandas numpy matplotlib streamlit
```

**2. Execute o dashboard:**
```bash
python -m streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## Etapas da Análise

**Preparação dos dados (`analise.py`):**
- Seleção das colunas relevantes
- Remoção de registros sem salário informado
- Filtragem de outliers salariais (entre USD 1.000 e USD 500.000 anuais)
- Conversão da coluna de experiência para tipo numérico
- Criação de novas features: faixa salarial e linguagem principal

**Dashboard (`app.py`):**
- Top 10 países com mais desenvolvedores respondentes
- Distribuição de salários por faixa
- Top 10 linguagens mais utilizadas
- Salário mediano por linguagem principal
- Relação entre anos de experiência e salário
- Distribuição do nível de escolaridade

---

## Dataset

Fonte: [Stack Overflow Developer Survey 2023 — Kaggle](https://www.kaggle.com/datasets/stackoverflow/stack-overflow-2018-developer-survey)

O dataset contém 89.184 respostas de desenvolvedores de todo o mundo, coletadas pela plataforma Stack Overflow. Após o processo de limpeza, foram utilizados 46.831 registros válidos.
