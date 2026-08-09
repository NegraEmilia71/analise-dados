# 📊 Análise de Inteligência em Pesquisa – Diagnóstico Socioambiental

Este projeto foi desenvolvido como parte do **teste técnico para a posição de Analista de Inteligência em Pesquisa Sênior**. O objetivo é consolidar, analisar e extrair insights a partir de diferentes fontes de dados de uma pesquisa socioambiental, gerando um relatório executivo e um dashboard para apresentação ao cliente.

---

## 📂 Estrutura do Projeto

```
├── Codigo/
│   ├── EDA.ipynb                            # Notebook com análise exploratória completa
│   ├── extrar_para_csv.py                   # Extrai dados de .docx para .csv
│   ├── gerar_relatorio_insights.py          # Gera relatório com gráficos e insights
│   └── organizar_entrega.py                 # Organiza a estrutura final de entrega
│
├── Base/
│   ├── Base_Survey.csv                      # Dados brutos do survey (6.000+ respondentes)
│   ├── Dicionario_Variaveis.csv             # Dicionário com descrição de todas as variáveis
│   ├── entrevistas.csv                      # Dados estruturados das 6 entrevistas em profundidade
│   ├── indicadores.csv                      # Indicadores secundários por município
│   └── mobilizacao.csv                      # Registros de mobilização social (6 eventos)
│
├── relatorio_qualitativo/
│   ├── imagens/
│   │   ├── wordcloud_Principal_Preocupacao.png
│   │   ├── wordcloud_Prioridade_Investimento.png
│   │   ├── wordcloud_Sugestao.png
│   │   ├── media_indicadores.png
│   │   ├── heatmap_municipios.png
│   │   ├── urbano_rural_comparacao.png
│   │   ├── perfil_sexo.png
│   │   └── perfil_idade.png
│   └── Relatorio_Insights_Completo.md       # Relatório executivo com recomendações
│
└── README.md                                # Instruções e documentação do projeto
```

---

## 🎯 Objetivos do Projeto

- **Integrar** dados quantitativos (survey) e qualitativos (entrevistas, mobilização, indicadores secundários).
- **Identificar** padrões, percepções e principais preocupações da população nos 8 municípios.
- **Gerar** recomendações objetivas e acionáveis para o cliente, com base em evidências.
- **Automatizar** o pipeline de extração, tratamento, análise e geração de relatório.

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta / Biblioteca | Finalidade |
| :--- | :--- |
| **Python 3.13** | Linguagem principal do pipeline |
| **Pandas** | Manipulação e análise de dados |
| **Matplotlib / Seaborn** | Geração de gráficos e visualizações |
| **WordCloud** | Nuvens de palavras para campos abertos |
| **python-docx** | Extração de texto de arquivos `.docx` |
| **Jupyter Notebook** | Ambiente para análise exploratória (EDA) |

---

## 📥 Como Executar o Pipeline

### 1. Clone o repositório

```bash
git clone https://github.com/NegraEmilia71/analise-dados.git
cd analise-dados
```

### 2. Instale as dependências

```bash
pip install pandas matplotlib seaborn wordcloud numpy python-docx
```

### 3. Execute os scripts em ordem

| Script | Descrição |
| :--- | :--- |
| `extrar_para_csv.py` | Extrai os dados dos arquivos `.docx` e gera os CSVs estruturados (`entrevistas.csv`, `mobilizacao.csv`, `indicadores.csv`). |
| `gerar_relatorio_insights.py` | Lê a `Base_Survey.csv`, o `Dicionario_Variaveis.csv` e os CSVs gerados, produzindo gráficos e o relatório completo. |
| `organizar_entrega.py` | Organiza automaticamente a estrutura final de pastas para entrega. |

---

## 📊 Principais Insights do Relatório

A análise integrada das fontes de dados revelou:

- **Qualidade de Vida (QV):** Média de **2.85** (escala 1–5), com variações significativas entre áreas urbanas e rurais.
- **Temas emergentes:** Água, emprego e participação comunitária são as principais preocupações, especialmente em comunidades rurais (Santa Aurora, Serra Azul).
- **Confiança institucional:** Confiança na empresa (**2.91**) é ligeiramente superior à confiança no poder público (**2.72**), indicando oportunidade de fortalecer o diálogo.
- **Mobilização social:** 4 dos 6 registros são positivos, destacando o aumento da receptividade após ações da equipe.

**Recomendações estratégicas incluídas no relatório:**
1. Priorizar ações de abastecimento de água em comunidades rurais.
2. Investir em programas de qualificação profissional e geração de renda.
3. Manter a mobilização contínua para consolidar a confiança.
4. Criar canais permanentes de escuta ativa com lideranças locais.

---

## 📈 Visualizações Geradas

As visualizações estão disponíveis em `relatorio_qualitativo/imagens/`:

- **Nuvens de palavras:** `Principal_Preocupacao`, `Prioridade_Investimento`, `Sugestao`.
- **Gráficos:** Média dos indicadores, mapa de calor por município, comparação urbano/rural, distribuição por sexo e faixa etária.

---

## 📄 Relatório Final

O relatório consolidado está disponível em:
```
relatorio_qualitativo/Relatorio_Insights_Completo.md
```

Ele contém:
- Resumo executivo com os principais números.
- Perfil demográfico dos respondentes.
- Análise qualitativa dos campos abertos.
- Indicadores numéricos por município e área.
- Recomendações estratégicas para o cliente.

---

## 🔄 Melhorias Futuras

- **Pipeline automatizado em produção:** Integrar com ferramentas como Airflow para execução diária.
- **Dashboard interativo:** Expandir o Power BI para permitir filtros dinâmicos por município, área e tema.
- **Análise de sentimento:** Aprimorar a classificação de sentimentos com modelos de NLP (ex: BERT).

---

## 👩‍💻 Autor

**Joyce**  
Candidata à vaga de **Analista de Inteligência em Pesquisa Sênior**  
[LinkedIn](https://www.linkedin.com/in/joyce-emília-datascientist) | [GitHub](https://github.com/NegraEmilia71)

---

## 📌 Observações

- Os dados utilizados são **anônimos** e fazem parte de um projeto de diagnóstico socioambiental.
- O pipeline foi desenvolvido para ser **reprodutível** e **escalável** para futuras rodadas de coleta.

---

*Estrutura organizada e relatório gerado automaticamente.* 🚀
