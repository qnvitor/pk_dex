"""Vector store para armazenamento e busca de embeddings de Pokémon."""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import json
import os
from src.config import CHROMA_DB_PATH


class PokemonVectorStore:
    """Vector store para conhecimento de Pokémon usando ChromaDB."""
    
    def __init__(self, persist_directory: str = CHROMA_DB_PATH):
        """
        Inicializa o vector store.
        
        Args:
            persist_directory: Diretório para persistência do banco
        """
        self.persist_directory = persist_directory
        
        # Cria diretório se não existir
        os.makedirs(persist_directory, exist_ok=True)
        
        print(f"[VECTOR STORE] Inicializando ChromaDB em {persist_directory}...")
        
        try:
            # Inicializa ChromaDB com persistência
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Cria ou carrega coleção
            self.collection = self.client.get_or_create_collection(
                name="pokemon_knowledge",
                metadata={"description": "Pokémon knowledge base for RAG"}
            )
            
            print(f"[VECTOR STORE] ChromaDB inicializado. Documentos: {self.collection.count()}")
        except Exception as e:
            print(f"[ERRO VECTOR STORE] Erro ao inicializar: {e}")
            raise
    
    def add_pokemon(self, pokemon_data: Dict[str, Any]) -> bool:
        """
        Adiciona Pokémon ao vector store.
        
        Args:
            pokemon_data: Dados do Pokémon da PokéAPI
            
        Returns:
            True se adicionado com sucesso, False caso contrário
        """
        try:
            pokemon_id = pokemon_data.get('id')
            pokemon_name = pokemon_data.get('name', '').lower()
            
            # Cria texto descritivo para embedding
            text = self._create_pokemon_text(pokemon_data)
            
            # Prepara metadata
            metadata = self._create_metadata(pokemon_data)
            
            # Adiciona ao vector store
            self.collection.upsert(
                documents=[text],
                metadatas=[metadata],
                ids=[f"pokemon_{pokemon_id}"]
            )
            
            return True
        except Exception as e:
            print(f"[ERRO VECTOR STORE] Erro ao adicionar Pokémon {pokemon_data.get('name')}: {e}")
            return False
    
    def add_pokemon_batch(self, pokemon_list: List[Dict[str, Any]]) -> int:
        """
        Adiciona múltiplos Pokémon de uma vez.
        
        Args:
            pokemon_list: Lista de dados de Pokémon
            
        Returns:
            Número de Pokémon adicionados com sucesso
        """
        documents = []
        metadatas = []
        ids = []
        
        for pokemon_data in pokemon_list:
            try:
                pokemon_id = pokemon_data.get('id')
                text = self._create_pokemon_text(pokemon_data)
                metadata = self._create_metadata(pokemon_data)
                
                documents.append(text)
                metadatas.append(metadata)
                ids.append(f"pokemon_{pokemon_id}")
            except Exception as e:
                print(f"[ERRO VECTOR STORE] Erro ao processar {pokemon_data.get('name')}: {e}")
                continue
        
        if documents:
            try:
                self.collection.upsert(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                return len(documents)
            except Exception as e:
                print(f"[ERRO VECTOR STORE] Erro no batch insert: {e}")
                return 0
        
        return 0
    
    def search(
        self,
        query: str,
        n_results: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Busca Pokémon similares à query.
        
        Args:
            query: Texto de busca
            n_results: Número de resultados a retornar
            filter_metadata: Filtros opcionais (ex: {"type": "fire"})
            
        Returns:
            Dicionário com resultados da busca
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filter_metadata
            )
            
            return results
        except Exception as e:
            print(f"[ERRO VECTOR STORE] Erro na busca: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def get_by_id(self, pokemon_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca Pokémon por ID.
        
        Args:
            pokemon_id: ID do Pokémon
            
        Returns:
            Dados do Pokémon ou None
        """
        try:
            result = self.collection.get(
                ids=[f"pokemon_{pokemon_id}"],
                include=["documents", "metadatas"]
            )
            
            if result['ids']:
                return {
                    'document': result['documents'][0],
                    'metadata': result['metadatas'][0]
                }
            return None
        except Exception as e:
            print(f"[ERRO VECTOR STORE] Erro ao buscar ID {pokemon_id}: {e}")
            return None
    
    def count(self) -> int:
        """
        Retorna número de Pokémon no vector store.
        
        Returns:
            Contagem de documentos
        """
        try:
            return self.collection.count()
        except Exception:
            return 0
    
    def clear(self):
        """Remove todos os dados do vector store."""
        try:
            self.client.delete_collection("pokemon_knowledge")
            self.collection = self.client.create_collection(
                name="pokemon_knowledge",
                metadata={"description": "Pokémon knowledge base for RAG"}
            )
            print("[VECTOR STORE] Vector store limpo com sucesso!")
        except Exception as e:
            print(f"[ERRO VECTOR STORE] Erro ao limpar: {e}")
    
    def _create_pokemon_text(self, pokemon_data: Dict[str, Any]) -> str:
        """
        Cria texto descritivo do Pokémon para embedding.
        
        Args:
            pokemon_data: Dados do Pokémon
            
        Returns:
            Texto formatado
        """
        pokemon_id = pokemon_data.get('id', 0)
        name = pokemon_data.get('name', '').title()
        
        # Tipos
        types = [t['type']['name'].title() for t in pokemon_data.get('types', [])]
        types_str = ', '.join(types)
        
        # Habilidades
        abilities = [a['ability']['name'].replace('-', ' ').title() 
                    for a in pokemon_data.get('abilities', [])]
        abilities_str = ', '.join(abilities)
        
        # Dimensões
        height = pokemon_data.get('height', 0) / 10  # decímetros para metros
        weight = pokemon_data.get('weight', 0) / 10  # hectogramas para kg
        
        # Stats
        stats_dict = {}
        for stat in pokemon_data.get('stats', []):
            stat_name = stat['stat']['name']
            stat_value = stat['base_stat']
            stats_dict[stat_name] = stat_value
        
        # Monta texto descritivo
        text = f"""Pokémon #{pokemon_id:03d}: {name}

Tipo(s): {types_str}
Habilidades: {abilities_str}
Altura: {height:.1f}m
Peso: {weight:.1f}kg

Estatísticas Base:
- HP: {stats_dict.get('hp', 0)}
- Ataque: {stats_dict.get('attack', 0)}
- Defesa: {stats_dict.get('defense', 0)}
- Ataque Especial: {stats_dict.get('special-attack', 0)}
- Defesa Especial: {stats_dict.get('special-defense', 0)}
- Velocidade: {stats_dict.get('speed', 0)}
Total: {sum(stats_dict.values())}"""
        
        return text.strip()
    
    def _create_metadata(self, pokemon_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria metadata para filtragem.
        
        Args:
            pokemon_data: Dados do Pokémon
            
        Returns:
            Dicionário de metadata
        """
        types = [t['type']['name'] for t in pokemon_data.get('types', [])]
        
        return {
            "id": pokemon_data.get('id', 0),
            "name": pokemon_data.get('name', '').lower(),
            "types": json.dumps(types),  # ChromaDB não suporta listas, usa JSON
            "generation": 1 if pokemon_data.get('id', 0) <= 151 else 2  # Simplificado
        }
