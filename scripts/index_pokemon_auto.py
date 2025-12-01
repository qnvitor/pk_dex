"""Script automático para indexar Pokémon na base de conhecimento RAG."""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.rag.pokemon_knowledge import PokemonKnowledgeBuilder


# =============================================================================
# INDEX_POKEMON_AUTO - Script de Indexação da Base de Conhecimento RAG
# =============================================================================
# 
#  O QUE FAZ:
#    - Baixa dados de 151 Pokémon da PokéAPI
#    - Gera embeddings semânticos para cada Pokémon
#    - Armazena na base ChromaDB para busca vetorial
#    - Popular vector store ANTES de usar chatbot RAG
#
#  REFERÊNCIAS:
#    - Usa PokemonKnowledgeBuilder de src/rag/pokemon_knowledge.py linha 20
#    - Popula PokemonVectorStore usado por src/rag/rag_chatbot.py linha 54
#    - Dados salvos em: data/chroma_db/


def main():
    """Função principal de indexação automática."""
    print("=" * 60)
    print("INDEXACAO AUTOMATICA DA BASE DE CONHECIMENTO POKEMON")
    print("=" * 60)
    
    # Cria o builder
    builder = PokemonKnowledgeBuilder()
    
    # Indexa 151 Pokémon (primeira geração)
    num_pokemon = 151
    
    print(f"\nBase atual tem {builder.vector_store.count()} Pokemon indexados.")
    print(f"Indexando {num_pokemon} Pokemon da primeira geracao...")
    
    # Executa indexação
    indexed = builder.build_knowledge_base(num_pokemon)
    
    # Mostra estatísticas
    stats = builder.get_stats()
    print("\n" + "=" * 60)
    print("INDEXACAO CONCLUIDA!")
    print("=" * 60)
    print(f"Pokemon indexados: {indexed}")
    print(f"Total na base: {stats['total_pokemon']}")
    print(f"Status: {stats['status']}")
    print("\nAgora voce pode usar o chatbot com RAG!")
    print("=" * 60)


if __name__ == "__main__":
    main()
