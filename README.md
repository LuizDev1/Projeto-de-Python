# 📊 Análise do Perfil e Salário de Desenvolvedores
### Stack Overflow Developer Survey 2023

Projeto desenvolvido para a disciplina **Novas Tecnologias**, utilizando Python para realizar uma análise exploratória de dados do **Stack Overflow Developer Survey 2023**, buscando responder à seguinte pergunta de negócio:

> **Quais fatores mais influenciam o salário de desenvolvedores de software ao redor do mundo?**

---

# 📌 Objetivo

O objetivo deste projeto é identificar quais fatores apresentam maior relação com a remuneração de desenvolvedores de software, utilizando dados reais da pesquisa anual realizada pelo Stack Overflow.

Durante o projeto são realizadas etapas de:

- Limpeza dos dados;
- Tratamento de valores ausentes;
- Remoção de outliers;
- Criação de novas variáveis;
- Análise exploratória;
- Construção de um dashboard interativo utilizando Streamlit.

---

# 📂 Dataset

**Fonte:**

Stack Overflow Developer Survey 2023

https://survey.stackoverflow.co/2023/

Disponível também no Kaggle.

O conjunto de dados possui aproximadamente:

- 89 mil respondentes
- mais de 80 variáveis

Após o tratamento foram utilizados aproximadamente **46 mil registros válidos**.

---

# 🛠 Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit

---

# 📈 Tratamento dos Dados

Durante o pré-processamento foram realizadas as seguintes etapas:

- Seleção apenas das colunas relevantes para a pergunta de negócio;
- Remoção de salários ausentes;
- Remoção de salários inferiores a US$ 1.000 e superiores a US$ 500.000;
- Conversão da coluna de anos de experiência para formato numérico;
- Criação da variável **Faixa de Experiência**;
- Criação da variável **Faixa Salarial**;
- Extração da linguagem principal de programação;
- Extração do tipo principal de desenvolvedor;
- Tradução de países para português;
- Tradução dos regimes de trabalho;
- Simplificação dos níveis de escolaridade;
- Remoção de registros duplicados.

---

# 🎛 Dashboard

O projeto disponibiliza um dashboard interativo desenvolvido em Streamlit.

É possível aplicar filtros por:

- 🌍 País
- 💻 Linguagem principal
- 👨‍💻 Tipo de desenvolvedor
- 🎓 Escolaridade
- 📅 Anos de experiência

Todos os gráficos são atualizados automaticamente conforme os filtros selecionados.

---

# 📊 Análises realizadas

O dashboard apresenta seis análises principais.

## 1️⃣ Experiência × Salário

Mostra a evolução do salário mediano conforme aumenta a experiência profissional.

---

## 2️⃣ Linguagem Principal × Salário

Compara a remuneração mediana entre as linguagens mais utilizadas.

---

## 3️⃣ Tipo de Desenvolvedor × Salário

Analisa quais áreas da computação apresentam maior remuneração.

Exemplos:

- Back-end
- Full-stack
- Cientista de Dados
- Cloud
- DevOps
- SRE

---

## 4️⃣ Regime de Trabalho × Salário

Compara os salários entre profissionais:

- Remotos
- Híbridos
- Presenciais

---

## 5️⃣ Escolaridade × Experiência

Heatmap mostrando como experiência e formação acadêmica influenciam conjuntamente o salário.

---

## 6️⃣ País × Experiência

Heatmap comparando diferentes países em todas as faixas de experiência.

---

# 💡 Insights automáticos

Além dos gráficos, o sistema gera interpretações automaticamente para cada análise.

Os insights são calculados dinamicamente conforme os filtros selecionados pelo usuário.

---

# 🚀 Como executar

## 1. Clone o repositório

```bash
git clone https://github.com/LuizDev1/Projeto-de-Python.git
```

---

## 2. Entre na pasta

```bash
cd Projeto-de-Python
```

---

## 3. Crie um ambiente virtual (opcional)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 5. Execute o projeto

```bash
streamlit run app.py
```

---

# 📁 Estrutura do Projeto

```
Projeto-de-Python/
│
├── app.py                      # Dashboard Streamlit
├── analise.py                  # Tratamento e análise dos dados
├── survey_results_public.csv   # Dataset
├── requirements.txt
├── README.md
└── Relatório.pdf
```

---

# 📌 Principais Resultados

A análise mostrou que:

- A experiência possui forte relação com o salário;
- O país de atuação exerce grande influência na remuneração;
- Áreas como Dados, Cloud e SRE apresentam salários mais elevados;
- O regime remoto está associado a maiores salários em muitos cenários;
- A experiência tende a ter maior impacto na remuneração do que apenas o nível de escolaridade.

---

# 👨‍💻 Autor

**Luiz Fernando Gomes**

Projeto desenvolvido para a disciplina de **Novas Tecnologias** da Universidade Católica de Brasília (UCB).
