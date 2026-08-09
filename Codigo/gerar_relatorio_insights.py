# ================================================================
# SCRIPT PARA GERAR RELATÓRIO DE INSIGHTS (QUALITATIVO + QUANTITATIVO)
# Analista de Inteligência em Pesquisa Sênior – Temple
# ================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
from wordcloud import WordCloud
import re
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ================================================================
# 1. CONFIGURAÇÃO
# ================================================================

BASE_SURVEY = "Base_Survey.csv"
DICIONARIO = "Dicionario_Variaveis.csv"

OUTPUT_DIR = "relatorio_qualitativo"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "imagens")
os.makedirs(IMAGES_DIR, exist_ok=True)

# ================================================================
# 2. CARREGAMENTO E LIMPEZA
# ================================================================

def carregar_dados():
    """Carrega e valida os CSVs."""
    if not os.path.exists(BASE_SURVEY):
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {BASE_SURVEY}")
    if not os.path.exists(DICIONARIO):
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {DICIONARIO}")
    
    df_survey = pd.read_csv(BASE_SURVEY, encoding='utf-8-sig')
    df_dicio = pd.read_csv(DICIONARIO, encoding='utf-8-sig')
    
    print(f"✅ Survey: {len(df_survey)} registros, {len(df_survey.columns)} colunas")
    print(f"✅ Dicionário: {len(df_dicio)} variáveis")
    
    return df_survey, df_dicio

def limpar_dados(df):
    """Limpeza e preparação dos dados."""
    df_clean = df.copy()
    
    # Converter colunas numéricas
    colunas_numericas = ['Idade', 'QV', 'Saude', 'Educacao', 'Transporte', 
                         'Seguranca', 'Meio_Ambiente', 'Agua', 'Geracao_Renda',
                         'Confianca_Empresa', 'Confianca_PoderPublico', 
                         'Pertencimento', 'Conhecimento_Projeto', 'Transparencia', 
                         'Participacao_Social']
    for col in colunas_numericas:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Padronizar municípios
    if 'Municipio' in df_clean.columns:
        df_clean['Municipio'] = df_clean['Municipio'].str.strip().str.title()
    
    # Padronizar áreas
    if 'Area' in df_clean.columns:
        df_clean['Area'] = df_clean['Area'].str.strip().str.lower()
    
    return df_clean

# ================================================================
# 3. ANÁLISE DE CAMPOS ABERTOS 
# ================================================================

def extrair_palavras_chave(texto, stopwords=None):
    """Extrai palavras-chave de um texto, removendo stopwords."""
    if pd.isna(texto):
        return []
    if stopwords is None:
        stopwords = {'a', 'o', 'e', 'que', 'de', 'da', 'do', 'para', 'com', 'um', 'uma',
                     'mais', 'muito', 'se', 'por', 'em', 'no', 'na', 'os', 'as', 'é',
                     'são', 'está', 'já', 'quando', 'como', 'mas', 'porque', 'ainda',
                     'vai', 'ser', 'ter', 'pode', 'tem', 'sua', 'seu', 'deles', 'delas',
                     'sobre', 'ou', 'pelo', 'pela', 'dos', 'das', 'nao', 'sim', 'tambem',
                     'sobre', 'entre', 'sem', 'com', 'ate', 'apos', 'durante'}
    
    texto_limpo = re.sub(r'[^\w\s]', '', str(texto).lower())
    palavras = texto_limpo.split()
    return [p for p in palavras if len(p) > 3 and p not in stopwords]

def analisar_campos_abertos(df):
    """Analisa os campos abertos: Principal_Preocupacao, Prioridade_Investimento, Sugestao."""
    print("\n🔍 ANALISANDO CAMPOS ABERTOS...")
    
    campos_abertos = ['Principal_Preocupacao', 'Prioridade_Investimento', 'Sugestao']
    resultados = {}
    
    for campo in campos_abertos:
        if campo not in df.columns:
            continue
        
        print(f"\n📝 {campo}:")
        
        # Frequência de respostas
        nao_responderam = df[campo].isna().sum()
        responderam = df[campo].notna().sum()
        print(f"   Responderam: {responderam} | Não responderam: {nao_responderam}")
        
        # Extrair palavras-chave
        todas_palavras = []
        for texto in df[campo].dropna():
            todas_palavras.extend(extrair_palavras_chave(texto))
        
        top_palavras = Counter(todas_palavras).most_common(15)
        print(f"   Top palavras: {top_palavras[:5]}")
        
        resultados[campo] = {
            'responderam': responderam,
            'nao_responderam': nao_responderam,
            'top_palavras': top_palavras,
            'todas_palavras': todas_palavras
        }
        
        # Nuvem de palavras
        if todas_palavras:
            wordcloud = WordCloud(width=800, height=400, background_color='white',
                                  max_words=50, colormap='viridis').generate(' '.join(todas_palavras))
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.title(f'Nuvem de Palavras - {campo}', fontsize=14)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(os.path.join(IMAGES_DIR, f'wordcloud_{campo}.png'), dpi=300)
            plt.close()
    
    return resultados

def analisar_por_municipio(df):
    """Analisa percepções por município."""
    print("\n📍 ANÁLISE POR MUNICÍPIO...")
    
    if 'Municipio' not in df.columns:
        return {}
    
    resultados = {}
    
    for municipio in df['Municipio'].unique():
        df_mun = df[df['Municipio'] == municipio]
        
        # Principais preocupações
        preocupacoes = []
        for texto in df_mun['Principal_Preocupacao'].dropna():
            preocupacoes.extend(extrair_palavras_chave(texto))
        top_preocupacoes = Counter(preocupacoes).most_common(5)
        
        # Média dos indicadores
        indicadores = ['QV', 'Saude', 'Educacao', 'Transporte', 'Seguranca', 
                       'Meio_Ambiente', 'Agua', 'Geracao_Renda', 'Confianca_Empresa']
        medias = {}
        for ind in indicadores:
            if ind in df_mun.columns:
                medias[ind] = df_mun[ind].mean()
        
        resultados[municipio] = {
            'total_respondentes': len(df_mun),
            'top_preocupacoes': top_preocupacoes,
            'medias_indicadores': medias
        }
        
        print(f"   {municipio}: {len(df_mun)} respondentes")
    
    return resultados

# ================================================================
# 4. ANÁLISE QUANTITATIVA 
# ================================================================

def analisar_indicadores(df):
    """Análise descritiva dos indicadores numéricos."""
    print("\n📊 ANALISANDO INDICADORES NUMÉRICOS...")
    
    indicadores = ['QV', 'Saude', 'Educacao', 'Transporte', 'Seguranca', 
                   'Meio_Ambiente', 'Agua', 'Geracao_Renda', 'Confianca_Empresa',
                   'Confianca_PoderPublico', 'Pertencimento', 'Conhecimento_Projeto',
                   'Transparencia', 'Participacao_Social']
    
    # Filtrar colunas existentes
    indicadores_existentes = [col for col in indicadores if col in df.columns]
    
    if not indicadores_existentes:
        print("   ⚠️ Nenhum indicador numérico encontrado.")
        return {}
    
    # Estatísticas descritivas
    stats = df[indicadores_existentes].describe()
    print(stats)
    
    # Médias por área
    if 'Area' in df.columns:
        medias_area = df.groupby('Area')[indicadores_existentes].mean()
        print("\n   Médias por área:")
        print(medias_area)
    
    # Médias por município
    if 'Municipio' in df.columns:
        medias_municipio = df.groupby('Municipio')[indicadores_existentes].mean()
        print("\n   Médias por município (top 3):")
        print(medias_municipio.head(3))
    
    return {
        'stats': stats,
        'medias_area': medias_area if 'Area' in df.columns else None,
        'medias_municipio': medias_municipio if 'Municipio' in df.columns else None
    }

def gerar_graficos_quantitativos(df):
    """Gera gráficos para indicadores numéricos."""
    print("\n📈 GERANDO GRÁFICOS QUANTITATIVOS...")
    
    indicadores = ['QV', 'Saude', 'Educacao', 'Transporte', 'Seguranca', 
                   'Meio_Ambiente', 'Agua', 'Geracao_Renda', 'Confianca_Empresa']
    indicadores_existentes = [col for col in indicadores if col in df.columns]
    
    if not indicadores_existentes:
        return
    
    # 1. Perfil médio dos indicadores
    plt.figure(figsize=(12, 6))
    medias = df[indicadores_existentes].mean().sort_values(ascending=False)
    cores = plt.cm.viridis(np.linspace(0.2, 0.8, len(medias)))
    medias.plot(kind='bar', color=cores)
    plt.title('Média dos Indicadores de Qualidade de Vida e Percepção', fontsize=14)
    plt.xlabel('Indicador')
    plt.ylabel('Média (1-5)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'media_indicadores.png'), dpi=300)
    plt.close()
    
    # 2. Distribuição por município (mapa de calor)
    if 'Municipio' in df.columns:
        plt.figure(figsize=(14, 8))
        heatmap_data = df.groupby('Municipio')[indicadores_existentes].mean()
        sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn', center=3, fmt='.2f')
        plt.title('Mapa de Calor - Indicadores por Município', fontsize=14)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, 'heatmap_municipios.png'), dpi=300)
        plt.close()
    
    # 3. Comparação urbano vs rural
    if 'Area' in df.columns:
        plt.figure(figsize=(12, 6))
        area_means = df.groupby('Area')[indicadores_existentes].mean().T
        area_means.plot(kind='bar')
        plt.title('Comparação Urbano vs Rural', fontsize=14)
        plt.xlabel('Indicador')
        plt.ylabel('Média')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Área')
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, 'urbano_rural_comparacao.png'), dpi=300)
        plt.close()

# ================================================================
# 5. ANÁLISE DE PERFIL DEMOGRÁFICO
# ================================================================

def analisar_perfil(df):
    """Análise do perfil demográfico dos respondentes."""
    print("\n👤 ANALISANDO PERFIL DEMOGRÁFICO...")
    
    perfil = {}
    
    # Sexo
    if 'Sexo' in df.columns:
        perfil['sexo'] = df['Sexo'].value_counts()
        print(f"   Sexo: {perfil['sexo'].to_dict()}")
    
    # Faixa etária
    if 'Faixa_Etaria' in df.columns:
        perfil['faixa_etaria'] = df['Faixa_Etaria'].value_counts()
        print(f"   Faixa etária: {perfil['faixa_etaria'].to_dict()}")
    
    # Escolaridade
    if 'Escolaridade' in df.columns:
        perfil['escolaridade'] = df['Escolaridade'].value_counts()
        print(f"   Escolaridade: {perfil['escolaridade'].to_dict()}")
    
    # Ocupação
    if 'Ocupacao' in df.columns:
        perfil['ocupacao'] = df['Ocupacao'].value_counts()
        print(f"   Ocupação: {perfil['ocupacao'].to_dict()}")
    
    # Renda
    if 'Renda' in df.columns:
        perfil['renda_media'] = df['Renda'].mean()
        perfil['renda_mediana'] = df['Renda'].median()
        print(f"   Renda média: R$ {perfil['renda_media']:.2f}")
        print(f"   Renda mediana: R$ {perfil['renda_mediana']:.2f}")
    
    return perfil

def gerar_graficos_perfil(df):
    """Gera gráficos do perfil demográfico."""
    print("\n📊 GERANDO GRÁFICOS DE PERFIL...")
    
    # 1. Distribuição por sexo
    if 'Sexo' in df.columns:
        # Mapear valores: M -> Masculino, F -> Feminino
        sexo_map = {'M': 'Masculino', 'F': 'Feminino'}
        sexo_series = df['Sexo'].dropna().map(sexo_map).dropna()
        
        if not sexo_series.empty:
            plt.figure(figsize=(6, 6))
            sexo_series.value_counts().plot(
                kind='pie', 
                autopct='%1.1f%%', 
                colors=['#2E86AB', '#F18F01']
            )
            plt.title('Distribuição por Sexo', fontsize=14)
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig(os.path.join(IMAGES_DIR, 'perfil_sexo.png'), dpi=300)
            plt.close()
    
    # 2. Distribuição por faixa etária
    if 'Faixa_Etaria' in df.columns:
        plt.figure(figsize=(10, 5))
        df['Faixa_Etaria'].value_counts().sort_index().plot(kind='bar', color="#9228A7")
        plt.title('Distribuição por Faixa Etária', fontsize=14)
        plt.xlabel('Faixa Etária')
        plt.ylabel('Nº de Respondentes')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, 'perfil_idade.png'), dpi=300)
        plt.close()

# ================================================================
# 6. GERAÇÃO DO RELATÓRIO EM MARKDOWN
# ================================================================

def gerar_relatorio_markdown(df, perfil, analise_texto, analise_indicadores, analise_municipio):
    """Gera o relatório completo em Markdown."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    relatorio_path = os.path.join(OUTPUT_DIR, 'Relatorio_Insights_Completo.md')
    
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write("# Relatório de Insights – Diagnóstico Socioambiental\n\n")
        f.write(f"**Data de geração:** {timestamp}\n\n")
        f.write("**Cargo:** Analista de Inteligência em Pesquisa Sênior\n\n")
        f.write("**Responsável:** [Joyce Emília O. Mota]\n\n")
        f.write("---\n\n")
        
        # 1. Resumo Executivo
        f.write("## 1. Resumo Executivo\n\n")
        f.write(f"O survey contou com **{len(df)} respondentes** distribuídos por **{df['Municipio'].nunique()} municípios**. ")
        f.write("Os dados revelam percepções importantes sobre Qualidade de Vida (QV), confiança em instituições e prioridades da população.\n\n")
        f.write("**Principais destaques:**\n")
        # Verifica e escreve QV média
        if 'QV' in df.columns and df['QV'].notna().any():
            qv_mean = df['QV'].mean()
            f.write(f"- A Qualidade de vida média (QV) é **{qv_mean:.2f}** (escala 1-5).\n")
        else:
            f.write("- A Qualidade de vida média (QV) não pôde ser calculada (dados insuficientes).\n")

        # Confiança na empresa
        if 'Confianca_Empresa' in df.columns and df['Confianca_Empresa'].notna().any():
            ce_mean = df['Confianca_Empresa'].mean()
            f.write(f"- Confiança na empresa: **{ce_mean:.2f}**\n")
        else:
            f.write("- Confiança na empresa: dados insuficientes.\n")

        # Confiança no poder público
        if 'Confianca_PoderPublico' in df.columns and df['Confianca_PoderPublico'].notna().any():
            cpp_mean = df['Confianca_PoderPublico'].mean()
            f.write(f"- Confiança no poder público: **{cpp_mean:.2f}**\n")
        else:
            f.write("- Confiança no poder público: dados insuficientes.\n")

        f.write("\n---\n\n")
        
        # 2. Perfil dos Respondentes
        f.write("## 2. Perfil dos Respondentes\n\n")
        f.write("### 2.1. Distribuição Demográfica\n\n")
        if 'sexo' in perfil:
            f.write(f"- **Sexo:** {perfil['sexo'].to_dict()}\n")
        if 'faixa_etaria' in perfil:
            f.write(f"- **Faixa etária:** {perfil['faixa_etaria'].to_dict()}\n")
        if 'escolaridade' in perfil:
            f.write(f"- **Escolaridade:** {perfil['escolaridade'].to_dict()}\n")
        if 'ocupacao' in perfil:
            f.write(f"- **Ocupação:** {perfil['ocupacao'].to_dict()}\n")
        if 'renda_media' in perfil:
            f.write(f"- **Renda média:** R$ {perfil['renda_media']:.2f}\n")
        f.write("\n![Distribuição por Sexo](imagens/perfil_sexo.png)\n")
        f.write("\n![Distribuição por Idade](imagens/perfil_idade.png)\n\n")
        f.write("---\n\n")
        
        # 3. Análise dos Campos Abertos
        f.write("## 3. Análise Qualitativa \n\n")
        
        for campo, dados in analise_texto.items():
            f.write(f"### 3.{list(analise_texto.keys()).index(campo)+1}. {campo}\n\n")
            f.write(f"- **Responderam:** {dados['responderam']} | **Não responderam:** {dados['nao_responderam']}\n")
            f.write(f"- **Principais palavras-chave:** ")
            f.write(", ".join([f"{p[0]} ({p[1]})" for p in dados['top_palavras'][:5]]))
            f.write("\n\n")
            f.write(f"![Nuvem de Palavras - {campo}](imagens/wordcloud_{campo}.png)\n\n")
        f.write("---\n\n")
        
        # 4. Indicadores Numéricos
        f.write("## 4. Indicadores de Qualidade de Vida e Percepção\n\n")
        f.write("### 4.1. Médias Gerais\n\n")
        f.write("![Média dos Indicadores](imagens/media_indicadores.png)\n\n")
        
        f.write("### 4.2. Por Município (Mapa de Calor)\n\n")
        f.write("![Mapa de Calor por Município](imagens/heatmap_municipios.png)\n\n")
        
        f.write("### 4.3. Comparação Região Urbana vs Rural\n\n")
        f.write("![Comparação Urbano vs Rural](imagens/urbano_rural_comparacao.png)\n\n")
        f.write("---\n\n")
        
        # 5. Percepções por Município
        f.write("## 5. Percepções por Município\n\n")
        for municipio, dados in analise_municipio.items():
            f.write(f"### 5.{list(analise_municipio.keys()).index(municipio)+1}. {municipio}\n\n")
            f.write(f"- **Total de respondentes:** {dados['total_respondentes']}\n")
            f.write(f"- **Principais preocupações:** ")
            f.write(", ".join([f"{p[0]} ({p[1]})" for p in dados['top_preocupacoes'][:3]]) if dados['top_preocupacoes'] else "Nenhuma mencionada")
            f.write("\n")
            if dados['medias_indicadores']:
                f.write(f"- **QV média:** {dados['medias_indicadores'].get('QV', 'N/A'):.2f}\n")
            f.write("\n")
        f.write("---\n\n")
        
        # 6. Recomendações
        f.write("## 6. Recomendações Estratégicas\n\n")
        f.write("1. **Fortalecer a confiança institucional:** A confiança na empresa e no poder público é um ponto crítico. Recomenda-se ampliar canais de diálogo e transparência.\n")
        f.write("2. **Priorizar ações em áreas rurais:** Os indicadores de água, saúde e infraestrutura são menores nas áreas rurais. Investimentos específicos são urgentes.\n")
        f.write("3. **Focar em geração de renda e educação:** Os campos abertos indicam que essas são as principais preocupações. Programas de qualificação e emprego devem ser priorizados.\n")
        f.write("4. **Manter escuta ativa:** As sugestões qualitativas revelam oportunidades de melhoria que devem ser incorporadas ao planejamento.\n\n")
        
        f.write("---\n\n")
        f.write(f"*Relatório gerado automaticamente em {timestamp}.*\n")
    
    print(f"📄 Relatório gerado: {relatorio_path}")
    return relatorio_path

# ================================================================
# 7. EXECUÇÃO PRINCIPAL
# ================================================================

def main():
    print("="*70)
    print("GERAÇÃO DE RELATÓRIO DE INSIGHTS (QUALITATIVO + QUANTITATIVO)")
    print("="*70)
    
    try:
        df_survey, df_dicio = carregar_dados()
        df_clean = limpar_dados(df_survey)
        
        print(f"\n📊 Dados carregados: {len(df_clean)} respondentes")
        print(f"   Colunas: {len(df_clean.columns)}")
        
        # Análises
        perfil = analisar_perfil(df_clean)
        gerar_graficos_perfil(df_clean)
        
        analise_texto = analisar_campos_abertos(df_clean)
        analise_indicadores = analisar_indicadores(df_clean)
        analise_municipio = analisar_por_municipio(df_clean)
        
        gerar_graficos_quantitativos(df_clean)
        
        # Relatório
        gerar_relatorio_markdown(df_clean, perfil, analise_texto, analise_indicadores, analise_municipio)
        
        print("\n" + "="*70)
        print("✅ RELATÓRIO GERADO COM SUCESSO!")
        print(f"📂 Pasta: {OUTPUT_DIR}/")
        print("="*70)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    