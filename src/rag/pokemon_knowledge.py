"""Construtor de base de conhecimento de Pokémon."""

from src.api.pokeapi_client import PokeAPIClient
from src.rag.vector_store import PokemonVectorStore
from tqdm import tqdm
from typing import Optional
import time


class PokemonKnowledgeBuilder:
    """Constrói e gerencia a base de conhecimento de Pokémon."""
    
    def __init__(self):
        """Inicializa o construtor de conhecimento."""
        self.api_client = PokeAPIClient()
        self.vector_store = PokemonVectorStore()
    
    def build_knowledge_base(
        self,
        num_pokemon: int = 151,
        start_id: int = 1,
        batch_size: int = 10
    ) -> int:
        """
        Constrói base de conhecimento indexando Pokémon.
        
        Args:
            num_pokemon: Número de Pokémon a indexar
            start_id: ID inicial
            batch_size: Tamanho do batch para processamento
            
        Returns:
            Número de Pokémon indexados com sucesso
        """
        print(f"\n[KNOWLEDGE] Iniciando indexação de {num_pokemon} Pokémon...")
        print(f"[KNOWLEDGE] IDs: {start_id} a {start_id + num_pokemon - 1}")
        
        indexed_count = 0
        batch = []
        
        for pokemon_id in tqdm(
            range(start_id, start_id + num_pokemon),
            desc="Indexando Pokémon"
        ):
            try:
                # Busca dados do Pokémon
                pokemon_data = self.api_client.get_pokemon_by_id(pokemon_id)
                
                if pokemon_data:
                    batch.append(pokemon_data)
                    
                    # Processa batch quando atingir o tamanho
                    if len(batch) >= batch_size:
                        count = self.vector_store.add_pokemon_batch(batch)
                        indexed_count += count
                        batch = []
                    
                    # Pequeno delay para não sobrecarregar a API
                    time.sleep(0.1)
                else:
                    print(f"\n[AVISO] Não foi possível obter dados do Pokémon #{pokemon_id}")
                    
            except Exception as e:
                print(f"\n[ERRO] Erro ao processar Pokémon #{pokemon_id}: {e}")
                continue
        
        # Processa batch restante
        if batch:
            count = self.vector_store.add_pokemon_batch(batch)
            indexed_count += count
        
        print(f"\n[KNOWLEDGE] Indexacao concluida!")
        print(f"[KNOWLEDGE] Total indexado: {indexed_count}/{num_pokemon}")
        print(f"[KNOWLEDGE] Documentos no vector store: {self.vector_store.count()}")
        
        return indexed_count
    
    def update_pokemon(self, pokemon_id: int) -> bool:
        """
        Atualiza dados de um Pokémon específico.
        
        Args:
            pokemon_id: ID do Pokémon
            
        Returns:
            True se atualizado com sucesso
        """
        print(f"[KNOWLEDGE] Atualizando Pokémon #{pokemon_id}...")
        
        pokemon_data = self.api_client.get_pokemon_by_id(pokemon_id)
        
        if pokemon_data:
            success = self.vector_store.add_pokemon(pokemon_data)
            if success:
                print(f"[KNOWLEDGE] Pokemon #{pokemon_id} atualizado!")
            return success
        else:
            print(f"[KNOWLEDGE] Nao foi possivel obter dados do Pokemon #{pokemon_id}")
            return False
    
    def rebuild_knowledge_base(self, num_pokemon: int = 151) -> int:
        """
        Reconstrói completamente a base de conhecimento.
        
        Args:
            num_pokemon: Número de Pokémon a indexar
            
        Returns:
            Número de Pokémon indexados
        """
        print("[KNOWLEDGE] Limpando base de conhecimento existente...")
        self.vector_store.clear()
        
        return self.build_knowledge_base(num_pokemon)
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas da base de conhecimento.
        
        Returns:
            Dicionário com estatísticas
        """
        count = self.vector_store.count()
        
        return {
            "total_pokemon": count,
            "status": "ready" if count > 0 else "empty"
        }
    
    def search_pokemon(self, query: str, n_results: int = 3) -> dict:
        """
        Busca Pokémon por similaridade semântica.
        
        Args:
            query: Texto de busca
            n_results: Número de resultados
            
        Returns:
            Resultados da busca
        """
        return self.vector_store.search(query, n_results)
