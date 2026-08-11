from __future__ import annotations

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import numpy as np
import re

# Configuração da página
st.set_page_config(
    page_title="Dashboard dos Resultados encontrados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# 1. CARREGAMENTO DOS DADOS
# ================================================================

def normalizar_colunas_indicadores(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza nomes de colunas de indicadores vindos de CSV e DOCX."""
    if df is None or df.empty:
        return df

    renomeacoes = {
        'Jovens 18–29 (%)': 'Jovens de 18 a 29 anos (%)',
        'Jovens 18-29 (%)': 'Jovens de 18 a 29 anos (%)'
    }

    colunas_para_renomear = {
        antiga: nova for antiga, nova in renomeacoes.items() if antiga in df.columns
    }
    if colunas_para_renomear:
        df = df.rename(columns=colunas_para_renomear)

    return df

def criar_faixa_etaria(df: pd.DataFrame) -> pd.DataFrame:
    """Cria a coluna Faixa_Etaria a partir da coluna Idade se não existir."""
    df = df.copy()
    if 'Faixa_Etaria' not in df.columns and 'Idade' in df.columns:
        bins = [0, 17, 29, 44, 59, 150]
        labels = ['Menor de 18 anos', 'De 18 a 29 anos', 'De 30 a 44 anos', 'De 45 a 59 anos', 'Acima de 60 anos']
        df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=bins, labels=labels, right=False)
    return df

@st.cache_data
def carregar_dados():
    """Carrega os dados do survey e indicadores."""
    caminhos_esperados = [
        "Base/Base_Survey.csv",
        "Base/entrevistas.csv",
        "Base/mobilizacao.csv",
        "Base/indicadores.csv",
    ]

    caminhos_ausentes = [caminho for caminho in caminhos_esperados if not os.path.exists(caminho)]
    if caminhos_ausentes:
        st.warning(
            "Arquivos CSV não encontrados: " + ", ".join(caminhos_ausentes)
            + ". Usando dados de exemplo."
        )
        return carregar_dados_exemplo()

    try:
        df_survey = pd.read_csv("Base/Base_Survey.csv", encoding='utf-8-sig')
        df_survey = criar_faixa_etaria(df_survey)
        df_entrevistas = pd.read_csv("Base/entrevistas.csv", encoding='utf-8-sig')
        df_mobilizacao = pd.read_csv("Base/mobilizacao.csv", encoding='utf-8-sig')
        df_indicadores = pd.read_csv("Base/indicadores.csv", encoding='utf-8-sig')
        df_indicadores = normalizar_colunas_indicadores(df_indicadores)
        return df_survey, df_entrevistas, df_mobilizacao, df_indicadores
    except FileNotFoundError:
        st.warning("Arquivo CSV desapareceu durante a leitura. Usando dados de exemplo.")
        return carregar_dados_exemplo()

@st.cache_data
def carregar_dados_exemplo():
    """Dados de exemplo para demonstração"""
    np.random.seed(42)
    municipios = ['Rio Claro', 'Pedra Branca', 'Boa Esperança', 'Lagoa Nova', 
                  'Santa Aurora', 'São Miguel do Norte', 'Vale Verde', 'Serra Azul']
    areas = ['Urbana', 'Rural']
    generos = ['Masculino', 'Feminino']
    faixas = ['De 18 a 29 anos', 'De 30 a 44 anos', 'De 45 a 59 anos', 'Acima de 60 anos']
    escolaridades = ['Fundamental', 'Médio', 'Superior']
    ocupacoes = ['Formal', 'Autônomo', 'Agricultura', 'Desempregado', 'Aposentado']
    
    df = pd.DataFrame({
        'ID': range(1, 601),
        'Municipio': np.random.choice(municipios, 600),
        'Area': np.random.choice(areas, 600, p=[0.6, 0.4]),
        'Sexo': np.random.choice(generos, 600, p=[0.51, 0.49]),
        'Idade': np.random.randint(18, 80, 600),
        'Faixa_Etaria': np.random.choice(faixas, 600, p=[0.2, 0.26, 0.22, 0.32]),
        'Escolaridade': np.random.choice(escolaridades, 600, p=[0.31, 0.33, 0.36]),
        'Ocupacao': np.random.choice(ocupacoes, 600, p=[0.19, 0.21, 0.20, 0.21, 0.19]),
        'Renda': np.random.normal(2500, 800, 600).clip(500, 6000).astype(int),
        'QV': np.random.normal(3.6, 0.6, 600).clip(1, 5),
        'Saude': np.random.normal(3.4, 0.7, 600).clip(1, 5),
        'Educacao': np.random.normal(3.2, 0.7, 600).clip(1, 5),
        'Transporte': np.random.normal(3.0, 0.8, 600).clip(1, 5),
        'Seguranca': np.random.normal(3.1, 0.7, 600).clip(1, 5),
        'Meio_Ambiente': np.random.normal(3.3, 0.7, 600).clip(1, 5),
        'Agua': np.random.normal(2.8, 0.9, 600).clip(1, 5),
        'Geracao_Renda': np.random.normal(3.0, 0.8, 600).clip(1, 5),
        'Confianca_Empresa': np.random.normal(3.57, 0.7, 600).clip(1, 5),
        'Confianca_PoderPublico': np.random.normal(3.46, 0.7, 600).clip(1, 5),
        'Principal_Preocupacao': np.random.choice(
            ['Água', 'Saúde', 'Emprego', 'Segurança', 'Educação', 'Infraestrutura', 'Transporte', 'Meio Ambiente'],
            600, p=[0.25, 0.15, 0.12, 0.10, 0.10, 0.10, 0.09, 0.09]
        )
    })
    
    # Entrevistas
    entrevistas = pd.DataFrame({
        'id': range(1, 7),
        'perfil': ['Jovem, 23 anos', 'Agricultora, 41 anos', 'Comerciante, 56 anos',
                   'Liderança comunitária, 48 anos', 'Professora, 38 anos', 'Moradora, 67 anos'],
        'municipio': ['Rio Claro', 'Santa Aurora', 'Vale Verde', 'Serra Azul', 'Boa Esperança', 'Lagoa Nova'],
        'zona': ['urbana', 'rural', 'urbana', 'rural', 'urbana', 'rural'],
        'trecho': [
            'Hoje a maior dificuldade é conseguir trabalho.',
            'Quando alguém adoece precisamos ir até a sede do município.',
            'Percebo que a empresa conversa mais com a comunidade.',
            'A maior reclamação da comunidade continua sendo a água.',
            'Muitos alunos abandonam os estudos porque precisam trabalhar cedo.',
            'Depois que participei da reunião, passei a entender melhor o projeto.'
        ]
    })
    
    # Mobilização
    mobilizacao = pd.DataFrame({
        'id': range(1, 7),
        'municipio': ['Rio Claro', 'Santa Aurora', 'Vale Verde', 'Serra Azul', 'Boa Esperança', 'Lagoa Nova'],
        'data': ['14/04/2026', '17/04/2026', '22/04/2026', '24/04/2026', '28/04/2026', '02/05/2026'],
        'resumo': [
            'Boa adesão à oficina na escola municipal (35 participantes)',
            'Baixa participação devido à interrupção do abastecimento de água',
            'Moradores passaram a incentivar vizinhos a responder ao survey',
            'Resistência inicial em comunidade rural',
            'Jovens demonstraram interesse em cursos profissionalizantes',
            'Aumento da receptividade após reuniões comunitárias'
        ],
        'sentimento': ['positivo', 'negativo', 'positivo', 'negativo', 'positivo', 'positivo']
    })
    
    # Indicadores
    indicadores = pd.DataFrame({
        'Municipio': municipios,
        '% Populacao Rural': [25, 70, 30, 70, 20, 60, 35, 75],
        'Cobertura APS (%)': [78, 45, 82, 38, 85, 50, 80, 42],
        'Desocupacao (%)': [12, 18, 10, 22, 8, 16, 11, 20],
        'Jovens de 18 a 29 anos (%)': [15, 20, 18, 25, 22, 30, 17, 28],
        'Domicilios com agua encanada (%)': [85, 40, 90, 35, 92, 45, 88, 38],
        'Observacao': ['', '', '', '', '', '', '', '']
    })
    
    return df, entrevistas, mobilizacao, indicadores

# ================================================================
# 2. FUNÇÕES AUXILIARES
# ================================================================

def criar_wordcloud(textos, titulo):
    """Cria uma nuvem de palavras a partir de uma lista de textos"""
    if not textos:
        return None
    
    stopwords = {'a', 'o', 'e', 'que', 'de', 'da', 'do', 'para', 'com', 'um', 'uma',
                 'mais', 'muito', 'se', 'por', 'em', 'no', 'na', 'os', 'as', 'é',
                 'são', 'está', 'já', 'quando', 'como', 'mas', 'porque', 'ainda',
                 'vai', 'ser', 'ter', 'pode', 'tem', 'sua', 'seu', 'deles', 'delas',
                 'sobre', 'ou', 'pelo', 'pela', 'dos', 'das', 'nao', 'sim', 'tambem'}
    
    texto_limpo = ' '.join(str(t).lower() for t in textos if pd.notna(t))
    palavras = re.findall(r'[a-záéíóúãõç]+', texto_limpo)
    palavras_filtradas = [p for p in palavras if len(p) > 3 and p not in stopwords]
    
    if not palavras_filtradas:
        return None
    
    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          max_words=50, colormap='viridis').generate(' '.join(palavras_filtradas))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title(titulo, fontsize=14)
    ax.axis('off')
    return fig

def criar_grafico_indicadores(df):
    """Cria gráfico de barras com médias dos indicadores"""
    indicadores_cols = ['QV', 'Saude', 'Educacao', 'Transporte', 'Seguranca', 
                        'Meio_Ambiente', 'Agua', 'Geracao_Renda', 'Confianca_Empresa']
    existentes = [col for col in indicadores_cols if col in df.columns]
    
    if not existentes:
        return None
    
    medias = df[existentes].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cores = sns.color_palette("viridis", n_colors=len(medias))
    medias.plot(kind='bar', color=cores, ax=ax)
    ax.set_title('Média dos Indicadores de Qualidade de Vida e Percepção', fontsize=14)
    ax.set_xlabel('Indicador')
    ax.set_ylabel('Média (1-5)')
    ax.set_ylim(0, 5)
    ax.axhline(y=3, color='red', linestyle='--', alpha=0.5, label='Referência (3)')
    ax.legend()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    return fig

def criar_heatmap_municipios(df):
    """Cria mapa de calor de indicadores por município"""
    indicadores_cols = ['QV', 'Saude', 'Educacao', 'Transporte', 'Seguranca', 'Agua']
    existentes = [col for col in indicadores_cols if col in df.columns]
    
    if not existentes or 'Municipio' not in df.columns:
        return None
    
    heatmap_data = df.groupby('Municipio')[existentes].mean()
    
    if heatmap_data.empty:
        return None
    
    if len(heatmap_data) < 2:
        return None
    
    if heatmap_data.isna().all().all():
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn', center=3, fmt='.2f', ax=ax)
    ax.set_title('Mapa de Calor - Indicadores por Município', fontsize=14)
    plt.tight_layout()
    return fig

# ================================================================
# 3. INTERFACE DO DASHBOARD
# ================================================================

st.title("📊 Dashboard dos Resultados Encontrados")
st.markdown("### Diagnóstico Socioambiental")
st.markdown("---")

# Carregar dados
df_survey, df_entrevistas, df_mobilizacao, df_indicadores = carregar_dados()

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")

municipios = ['Todos'] + sorted(df_survey['Municipio'].unique().tolist())
municipio_selecionado = st.sidebar.selectbox("Município", municipios)

area_selecionada = st.sidebar.selectbox("Área", ['Todas', 'Urbana', 'Rural'])

genero_selecionado = st.sidebar.selectbox("Gênero", ['Todos', 'Masculino', 'Feminino'])

# Aplicar filtros
df_filtrado = df_survey.copy()

if municipio_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Municipio'] == municipio_selecionado]

if area_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Area'] == area_selecionada]

if genero_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Sexo'] == genero_selecionado]

# ========== VERIFICAÇÃO DE DADOS ==========
if df_filtrado.empty:
    st.sidebar.markdown("---")
    st.sidebar.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros para visualizar os dados.")
    st.stop()
# ==========================================

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total de respondentes:** {len(df_filtrado)}")
st.sidebar.markdown(f"**Municípios:** {df_filtrado['Municipio'].nunique()}")

# ================================================================
# 4. MÉTRICAS PRINCIPAIS (Cards)
# ================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total de Respondentes",
        value=f"{len(df_filtrado):,}",
        delta="6.000 esperado" if len(df_filtrado) < 6000 else "Meta atingida!"
    )

with col2:
    qv_mean = df_filtrado['QV'].mean() if 'QV' in df_filtrado.columns else 3.59
    st.metric(
        label="Qualidade de Vida (QV)",
        value=f"{qv_mean:.2f}",
        delta="Escala 1-5"
    )

with col3:
    conf_empresa = df_filtrado['Confianca_Empresa'].mean() if 'Confianca_Empresa' in df_filtrado.columns else 3.57
    st.metric(
        label="Confiança na Empresa",
        value=f"{conf_empresa:.2f}",
        delta="Escala 1-5"
    )

with col4:
    conf_publico = df_filtrado['Confianca_PoderPublico'].mean() if 'Confianca_PoderPublico' in df_filtrado.columns else 3.46
    st.metric(
        label="Confiança no Poder Público",
        value=f"{conf_publico:.2f}",
        delta="Escala 1-5"
    )

st.markdown("---")

# ================================================================
# 5. GRÁFICOS PRINCIPAIS
# ================================================================

# Row 1: Distribuição demográfica
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Distribuição por Sexo")
    
    sexo_counts = df_filtrado['Sexo'].dropna().value_counts()
    
    if sexo_counts.empty:
        st.warning("⚠️ Nenhum dado de gênero disponível para os filtros selecionados.")
    elif len(sexo_counts) >= 2:
        fig_sexo, ax = plt.subplots(figsize=(6, 6))
        sexo_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#2E86AB', '#F18F01'], ax=ax)
        ax.set_ylabel('')
        ax.set_title('')
        plt.tight_layout()
        st.pyplot(fig_sexo)
    else:
        genero_unico = sexo_counts.index[0]
        st.info(f"ℹ️ Todos os respondentes filtrados são do gênero **{genero_unico}**.")
        
        fig, ax = plt.subplots(figsize=(4, 3))
        valor = int(sexo_counts.iloc[0])
        ax.bar([genero_unico], [valor], color='#2E86AB')
        ax.set_title('Distribuição por Sexo', fontsize=12)
        ax.set_ylabel('Quantidade')
        ax.set_xlabel('Gênero')
        ax.text(0, valor + 0.5, str(valor), ha='center', va='bottom', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)

with col2:
    st.subheader("📊 Distribuição por Faixa Etária")
    
    if 'Faixa_Etaria' in df_filtrado.columns:
        # Remover nulos e contar
        faixa_counts = df_filtrado['Faixa_Etaria'].dropna().value_counts()
        
        if faixa_counts.empty:
            st.warning("⚠️ Nenhum dado de faixa etária disponível para os filtros selecionados.")
        else:
            # Ordem cronológica
            ordem_faixas = ['18-29', '30-44', '45-59', '60+']
            
            # Verificar se os valores existem e reindexar
            faixa_counts = faixa_counts.reindex([f for f in ordem_faixas if f in faixa_counts.index])
            
            if faixa_counts.empty:
                st.warning("⚠️ Nenhum dado válido de faixa etária disponível.")
            else:
                fig_idade, ax = plt.subplots(figsize=(6, 4))
                
                cores_padrao = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
                num_barras = len(faixa_counts)
                cores_usar = cores_padrao[:num_barras] if num_barras > 0 else ['#2E86AB']
                
                faixa_counts.plot(kind='bar', color=cores_usar, ax=ax)
                ax.set_xlabel('Faixa Etária')
                ax.set_ylabel('Nº de Respondentes')
                ax.set_title('')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                
                for i, v in enumerate(faixa_counts):
                    ax.text(i, v + 0.5, str(int(v)), ha='center', va='bottom', fontsize=10)
                
                plt.tight_layout()
                st.pyplot(fig_idade)
    else:
        st.warning("⚠️ Coluna 'Faixa_Etaria' não encontrada nos dados.")

st.markdown("---")

# Row 2: Indicadores principais
st.subheader("📈 Indicadores de Qualidade de Vida e Percepção")

col1, col2 = st.columns(2)

with col1:
    fig_indicadores = criar_grafico_indicadores(df_filtrado)
    if fig_indicadores:
        st.pyplot(fig_indicadores)
    else:
        st.info("ℹ️ Dados insuficientes para gerar o gráfico de indicadores. Tente ajustar os filtros.")

with col2:
    fig_heatmap = criar_heatmap_municipios(df_filtrado)
    if fig_heatmap:
        st.pyplot(fig_heatmap)
    else:
        st.info("ℹ️ Dados insuficientes para gerar o mapa de calor. Selecione mais municípios ou ajuste os filtros.")

st.markdown("---")

# Row 3: Preocupações e Sugestões
st.subheader("💬 Principais Preocupações")

if 'Principal_Preocupacao' in df_filtrado.columns:
    preocupacoes = df_filtrado['Principal_Preocupacao'].value_counts().reset_index()
    preocupacoes.columns = ['Preocupação', 'Frequência']
    
    fig = px.bar(
        preocupacoes,
        x='Preocupação',
        y='Frequência',
        color='Frequência',
        color_continuous_scale='Viridis',
        title='Preocupações da População',
        labels={'Preocupação': 'Tema', 'Frequência': 'Nº de Menções'}
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 4: Análise por Município
st.subheader("📍 Análise por Município")

col1, col2 = st.columns(2)

with col1:
    municipio_counts = df_filtrado['Municipio'].value_counts().reset_index()
    municipio_counts.columns = ['Municipio', 'Respondentes']
    
    fig = px.bar(
        municipio_counts,
        x='Municipio',
        y='Respondentes',
        color='Respondentes',
        color_continuous_scale='Blues',
        title='Distribuição de Respondentes por Município'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if 'QV' in df_filtrado.columns:
        qv_por_municipio = df_filtrado.groupby('Municipio')['QV'].mean().reset_index()
        qv_por_municipio.columns = ['Municipio', 'QV_Média']
        qv_por_municipio = qv_por_municipio.sort_values('QV_Média', ascending=False)
        
        fig = px.bar(
            qv_por_municipio,
            x='Municipio',
            y='QV_Média',
            color='QV_Média',
            color_continuous_scale='RdYlGn',
            range_color=[2.5, 4.5],
            title='Qualidade de Vida por Município',
            labels={'QV_Média': 'QV Média (1-5)'}
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 5: Entrevistas e Mobilização
st.subheader("📝 Análise Qualitativa")

tab1, tab2 = st.tabs(["📌 Entrevistas", "📢 Mobilização"])

with tab1:
    if not df_entrevistas.empty:
        st.markdown("**Trechos selecionados de entrevistas em profundidade:**")
        for _, row in df_entrevistas.iterrows():
            with st.expander(f"🎤 {row['perfil']} – {row['municipio']} ({row['zona']})"):
                st.markdown(f"> {row['trecho']}")
    else:
        st.info("Nenhum dado de entrevista disponível.")

with tab2:
    if not df_mobilizacao.empty:
        st.markdown("**Registros de mobilização social:**")
        for _, row in df_mobilizacao.iterrows():
            icon = "✅" if row['sentimento'] == 'positivo' else "⚠️"
            with st.expander(f"{icon} {row['data']} – {row['municipio']}"):
                st.markdown(f"**Resumo:** {row['resumo']}")
                st.markdown(f"**Sentimento:** `{row['sentimento']}`")
    else:
        st.info("Nenhum dado de mobilização disponível.")

st.markdown("---")

# Row 6: Indicadores Secundários
st.subheader("📊 Indicadores Secundários por Município")

if df_indicadores.empty or df_indicadores.isna().all().all():
    st.warning("⚠️ Nenhum dado de indicadores secundários encontrado no arquivo CSV.")
    st.info("📌 Usando dados de exemplo para demonstração:")
        
    dados_exemplo = pd.DataFrame({
        'Municipio': ['Rio Claro', 'Santa Aurora', 'Vale Verde', 'Serra Azul', 'Boa Esperança', 'Lagoa Nova', 'São Miguel do Norte', 'Pedra Branca'],
        '% Populacao Rural': [28, 54, 39, 61, 31, 47, 36, 43],
        'Cobertura APS (%)': [86, 68, 82, 64, 84, 71, 79, 73],
        'Desocupacao (%)': [10.8, 9.2, 8.7, 8.4, 12.1, 7.9, 11.3, 9.5],
        'Jovens de 18 a 29 anos (%)': [24, 19, 22, 18, 27, 20, 23, 21],
        'Domicilios com agua encanada (%)': [91, 63, 88, 58, 90, 75, 81, 66],
        'Observacao': [
            'Maior dinamismo econômico da região.',
            'Cobertura de água abaixo da média regional.',
            'Indicadores próximos da média regional.',
            'Maior vulnerabilidade em abastecimento de água.',
            'Maior proporção de jovens da região.',
            'Acesso à saúde limitado na zona rural.',
            'Mercado de trabalho em recuperação.',
            'Déficit de abastecimento em comunidades rurais.'
        ]
    })
    df_indicadores = dados_exemplo
    st.dataframe(
        df_indicadores,
        use_container_width=True,
        hide_index=True
    )
    st.caption("ℹ️ Estes são dados ilustrativos. Substitua pelo arquivo 'Base/indicadores.csv' com os dados reais.")

else:
    colunas_esperadas = [
        'Municipio',
        '% Populacao Rural',
        'Cobertura APS (%)',
        'Desocupacao (%)',
        'Jovens de 18 a 29 anos (%)',
        'Domicilios com agua encanada (%)',
        'Observacao'
    ]

    df_indicadores = normalizar_colunas_indicadores(df_indicadores)
    colunas_existentes = [col for col in colunas_esperadas if col in df_indicadores.columns]

    if not colunas_existentes:
        st.error("❌ O arquivo 'indicadores.csv' não possui as colunas esperadas.")
        st.code("Colunas esperadas: " + ", ".join(colunas_esperadas))
    else:
        df_tabela = df_indicadores.reindex(columns=colunas_esperadas)
        df_tabela = df_tabela.dropna(axis=1, how='all')

        colunas_numericas = [
            '% Populacao Rural',
            'Cobertura APS (%)',
            'Desocupacao (%)',
            'Jovens de 18 a 29 anos (%)',
            'Domicilios com agua encanada (%)'
        ]
        for coluna in colunas_numericas:
            if coluna in df_tabela.columns:
                df_tabela[coluna] = pd.to_numeric(df_tabela[coluna], errors='coerce')

        if df_tabela.empty:
            st.warning("⚠️ A tabela de indicadores secundários está vazia após a validação das colunas.")
        else:
            st.dataframe(
                df_tabela,
                use_container_width=True,
                hide_index=True
            )

# Após a tabela de indicadores
with st.expander("📘 O que significa a Cobertura APS? Clique aqui para saber mais"):
    st.markdown("""
    A **Cobertura APS (%)** indica a proporção da população de um município que é atendida pela **Atenção Primária à Saúde (APS)**.

    ### 🩺 Atenção Primária à Saúde do Sistema Único de Saúde (SUS)
    A APS é o primeiro contato do cidadão com o sistema de saúde. Ela é oferecida por equipes multiprofissionais nas **Unidades Básicas de Saúde (UBS)** ou Posto de Saúde e, principalmente, por meio das **Equipes de Saúde da Família (ESF)**.

    ### 📊 Por que esse indicador é importante?
    | Benefício | Descrição |
    | :--- | :--- |
    | ✅ **Prevenção de doenças** | Ações de promoção da saúde, vacinação e educação em saúde. |
    | ✅ **Diagnóstico precoce** | Identificação de problemas de saúde antes que se agravem. |
    | ✅ **Redução de internações** | Evita hospitalizações por condições que poderiam ser tratadas na atenção básica. |

    ### 🌎 Panorama no Brasil
    - Em 2023, **mais de 73% dos municípios brasileiros** já apresentavam cobertura superior a 90%.
    - **53% dos municípios** já atingiram **100% de cobertura populacional**.

    📎 *Fonte: Ministério da Saúde*
    """)

st.markdown("---")

# Footer
st.markdown(
    """
    <div style="text-align: center; color: #888; padding: 20px;">
        <p>
        Dashboard gerado automaticamente por <strong>Python + Streamlit</strong><br>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)