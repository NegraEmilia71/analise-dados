# Análise de Inteligência em Pesquisa

## Estrutura do Projeto

```
analise-dados/
├── dashboard.py              # Dashboard/ painel
├── requirements.txt
├── Codigo/
│   ├── EDA.ipynb
│   └── organizar_entrega.py
├── Base/
│   ├── Base_Survey.csv
│   ├── Dicionario_Variaveis.csv
│   ├── entrevistas.csv
│   ├── indicadores.csv
│   └── mobilizacao.csv
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
│   └── Relatorio_Insights_Completo.md
└── README.md
```

## Como executar

1. Instale as dependências:
   ```bash
   pip install pandas matplotlib seaborn wordcloud numpy python-docx
   ```
2. Execute os scripts em ordem:
   - `extrar_para_csv.py` (extrai dados dos DOCX para CSV)
   - `gerar_relatorio_insights.py` (gera o relatório e gráficos)
   - `organizar_entrega.py` (organiza a estrutura final)

---
*Estrutura organizada automaticamente.*
