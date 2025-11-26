"""Script para indexar Pokémon na base de conhecimento RAG."""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.rag.pokemon_knowledge import PokemonKnowledgeBuilder


def main():
    """Função principal de indexação."""
    print("=" * 60)
    print("INDEXAÇÃO DA BASE DE CONHECIMENTO POKÉMON")
    print("=" * 60)
    
    # Cria o builder
    builder = PokemonKnowledgeBuilder()
    
    # Pergunta quantos Pokémon indexar
    print("\nQuantos Pokémon deseja indexar?")
    print("  1. 151 (Primeira geração - Recomendado)")
    print("  2. 251 (Até segunda geração)")
    print("  3. Personalizado")
    
    choice = input("\nEscolha (1-3): ").strip()
    
    if choice == "1":
        num_pokemon = 151
    elif choice == "2":
        num_pokemon = 251
    elif choice == "3":
        try:
            num_pokemon = int(input("Digite o número de Pokémon: "))
        except ValueError:
            print("Número inválido! Usando 151 por padrão.")
            num_pokemon = 151
    else:
        print("Opção inválida! Usando 151 por padrão.")
        num_pokemon = 151
    
    # Pergunta se deve limpar base existente
    print(f"\nBase atual tem {builder.vector_store.count()} Pokémon indexados.")
    rebuild = input("Deseja limpar e reconstruir a base? (s/N): ").strip().lower()
    
    if rebuild == 's':
        print("\nReconstruindo base de conhecimento...")
        indexed = builder.rebuild_knowledge_base(num_pokemon)
    else:
        print("\nAdicionando a base existente...")
        indexed = builder.build_knowledge_base(num_pokemon)
    
    # Mostra estatísticas
    stats = builder.get_stats()
    print("\n" + "=" * 60)
    print("INDEXAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"Pokemon indexados: {indexed}")
    print(f"Total na base: {stats['total_pokemon']}")
    print(f"Status: {stats['status']}")
    print("\nAgora voce pode usar o chatbot com RAG!")
    print("=" * 60)


if __name__ == "__main__":
    main()
