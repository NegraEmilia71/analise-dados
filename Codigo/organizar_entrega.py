# ================================================================
# SCRIPT PARA ORGANIZAR A ESTRUTURA DE ENTREGA
# Analista de Inteligência em Pesquisa Sênior – Temple
# ================================================================

import os
import shutil
from pathlib import Path

def main():
    # Diretório atual (raiz do projeto)
    root = Path.cwd()
    
    # Definição das pastas de destino
    codigo_dir = root / "Codigo"
    base_dir = root / "Base"
    relatorio_dir = root / "relatorio_qualitativo"
    imagens_dir = relatorio_dir / "imagens"
    
    # 1. Criar as pastas necessárias
    print("📁 Criando estrutura de pastas...")
    codigo_dir.mkdir(exist_ok=True)
    base_dir.mkdir(exist_ok=True)
    relatorio_dir.mkdir(exist_ok=True)
    imagens_dir.mkdir(exist_ok=True)
    print(f"   ✅ {codigo_dir}/")
    print(f"   ✅ {base_dir}/")
    print(f"   ✅ {relatorio_dir}/")
    print(f"   ✅ {imagens_dir}/")
    
    # 2. Mover arquivos para Codigo/
    arquivos_codigo = [
        "EDA.ipynb",
        "extrar_para_csv.py",
        "gerar_relatorio_insights.py",
        "organizar_entrega.py"  # move a si mesmo após a execução
    ]
    
    for arquivo in arquivos_codigo:
        src = root / arquivo
        dst = codigo_dir / arquivo
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"✅ Movido: {arquivo} -> {dst}")
        else:
            print(f"⚠️ Arquivo não encontrado (ignorado): {arquivo}")
    
    # 3. Mover arquivos para Base/
    arquivos_base = [
        "Base_Survey.csv",
        "Dicionario_Variaveis.csv",
        "entrevistas.csv",
        "mobilizacao.csv",
        "indicadores_sec.csv"  # será renomeado para indicadores.csv
    ]
    
    for arquivo in arquivos_base:
        src = root / arquivo
        if arquivo == "indicadores_sec.csv":
            dst = base_dir / "indicadores.csv"  # Renomeia para indicadores.csv
        else:
            dst = base_dir / arquivo
        
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"✅ Movido: {arquivo} -> {dst}")
        else:
            print(f"⚠️ Arquivo não encontrado (ignorado): {arquivo}")
    
    # 4. Garantir que o relatório qualitativo esteja no lugar certo
    relatorio_md = relatorio_dir / "Relatorio_Insights_Completo.md"
    if not relatorio_md.exists():
        with open(relatorio_md, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Insights\n\n")
            f.write("Relatório gerado automaticamente.\n")
            f.write("Execute o script `gerar_relatorio_insights.py` para gerar o conteúdo completo.\n")
        print(f"📝 Placeholder criado: {relatorio_md}")
    else:
        print(f"✅ Relatório encontrado: {relatorio_md}")
    
    # 5. Verificar se as imagens estão na pasta correta
    imagens_esperadas = [
        "wordcloud_Principal_Preocupacao.png",
        "wordcloud_Prioridade_Investimento.png",
        "wordcloud_Sugestao.png",
        "media_indicadores.png",
        "heatmap_municipios.png",
        "urbano_rural_comparacao.png",
        "perfil_sexo.png",
        "perfil_idade.png"
    ]
    
    imagens_encontradas = 0
    for img in imagens_esperadas:
        if (imagens_dir / img).exists():
            imagens_encontradas += 1
    
    if imagens_encontradas > 0:
        print(f"✅ {imagens_encontradas} imagens encontradas em: {imagens_dir}/")
    else:
        print(f"⚠️ Nenhuma imagem encontrada em {imagens_dir}/")
        print(f"   Execute o script 'gerar_relatorio_insights.py' para gerar as imagens.")
    
    # 6. Criar README.md na raiz (se não existir)
    readme_path = root / "README.md"
    if not readme_path.exists():
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("# Análise de Inteligência em Pesquisa\n\n")
            f.write("## Estrutura do Projeto\n\n")
            f.write("```\n")
            f.write("├── Codigo/\n")
            f.write("│   ├── EDA.ipynb\n")
            f.write("│   ├── extrar_para_csv.py\n")
            f.write("│   ├── gerar_relatorio_insights.py\n")
            f.write("│   └── organizar_entrega.py\n")
            f.write("├── Base/\n")
            f.write("│   ├── Base_Survey.csv\n")
            f.write("│   ├── Dicionario_Variaveis.csv\n")
            f.write("│   ├── entrevistas.csv\n")
            f.write("│   ├── indicadores.csv\n")
            f.write("│   └── mobilizacao.csv\n")
            f.write("├── relatorio_qualitativo/\n")
            f.write("│   ├── imagens/\n")
            f.write("│   │   ├── wordcloud_Principal_Preocupacao.png\n")
            f.write("│   │   ├── wordcloud_Prioridade_Investimento.png\n")
            f.write("│   │   ├── wordcloud_Sugestao.png\n")
            f.write("│   │   ├── media_indicadores.png\n")
            f.write("│   │   ├── heatmap_municipios.png\n")
            f.write("│   │   ├── urbano_rural_comparacao.png\n")
            f.write("│   │   ├── perfil_sexo.png\n")
            f.write("│   │   └── perfil_idade.png\n")
            f.write("│   └── Relatorio_Insights_Completo.md\n")
            f.write("└── README.md\n")
            f.write("```\n\n")
            f.write("## Como executar\n\n")
            f.write("1. Instale as dependências:\n")
            f.write("   ```bash\n")
            f.write("   pip install pandas matplotlib seaborn wordcloud numpy python-docx\n")
            f.write("   ```\n")
            f.write("2. Execute os scripts em ordem:\n")
            f.write("   - `extrar_para_csv.py` (extrai dados dos DOCX para CSV)\n")
            f.write("   - `gerar_relatorio_insights.py` (gera o relatório e gráficos)\n")
            f.write("   - `organizar_entrega.py` (organiza a estrutura final)\n\n")
            f.write("---\n")
            f.write("*Estrutura organizada automaticamente.*\n")
        print(f"📝 README.md criado na raiz: {readme_path}")
    else:
        print(f"✅ README.md já existe na raiz.")
    
    # 7. Resumo final
    print("\n" + "="*60)
    print("✅ ESTRUTURA ORGANIZADA COM SUCESSO!")
    print("="*60)
    print("\n📂 Estrutura final:")
    print(f"   - Códigos: {codigo_dir}/")
    print(f"   - Bases: {base_dir}/")
    print(f"   - Relatório: {relatorio_dir}/")
    print("\n📋 Verifique se todos os arquivos foram movidos corretamente.")
    print("   - Se algum arquivo estiver faltando, verifique se ele estava na pasta raiz antes da execução.")
    print("="*60)

if __name__ == "__main__":
    main()
    