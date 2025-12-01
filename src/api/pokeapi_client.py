"""Cliente para PokéAPI com cache em SQLite."""

import requests
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from src.database.db_manager import DatabaseManager

# Carrega .env - ignora se houver problema de encoding
try:
    load_dotenv()
except Exception:
    pass

POKEAPI_BASE_URL = os.getenv('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2')


# =============================================================================
# POKEAPICLIENT - Cliente HTTP com Cache Inteligente (Cache-Aside Pattern)
# =============================================================================
# 
#  O QUE FAZ:
#    - Wrapper da PokéAPI com sistema de cache SQLite local
#    - Implementa padrão Cache-Aside com TTL (Time-To-Live)
#    - Reduz latência e uso de rede com cache automático
#
#  REFERÊNCIAS:
#    - Usado por: todas as páginas (Buscar, Reconhecimento, Chatbot)
#    - Usa DatabaseManager de src/database/db_manager.py linha 26
#    - Cache salvo em: data/pokemon_db.sqlite

class PokeAPIClient:
    """Cliente para PokéAPI com sistema de cache."""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """Inicializa o cliente da PokéAPI."""
        self.base_url = POKEAPI_BASE_URL
        # Tenta criar db_manager, mas não trava se falhar
        try:
            self.db_manager = db_manager or DatabaseManager()
        except Exception as e:
            print(f"[AVISO API] Erro ao inicializar DatabaseManager: {e}")
            self.db_manager = None
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str) -> Optional[Dict[Any, Any]]:
        """
        Faz requisição para a PokéAPI.
        
        Args:
            endpoint: Endpoint da API (ex: 'pokemon/1')
            
        Returns:
            Dados da resposta ou None em caso de erro
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            # Timeout reduzido para evitar travamentos
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout na requisição para {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: {e}")
            return None
    
    def get_pokemon_by_id(self, pokemon_id: int) -> Optional[Dict[Any, Any]]:
        """
        Busca Pokémon por ID.
        
        Args:
            pokemon_id: ID numérico do Pokémon
            
        Returns:
            Dados do Pokémon ou None
        """
        # ---------------------------------------------------------------------------
        # CACHE-ASIDE PATTERN - Fluxo de Leitura
        # ---------------------------------------------------------------------------
        # 1. Verifica cache primeiro (fast path)
        # 2. Se encontrar e não expirou (TTL), retorna imediatamente
        # 3. Se não encontrar, busca na API (slow path)
        # 4. Salva resultado no cache para próximas consultas
        # 
        # Performance:
        # - Cache hit: ~5ms (SQLite local)
        # - Cache miss: ~500ms (requisição HTTP + rede)
        # ---------------------------------------------------------------------------
        
        # Verifica cache primeiro (se disponível)
        if self.db_manager:
            try:
                cached = self.db_manager.get_cached(str(pokemon_id))
                if cached:
                    return cached  # Cache hit - retorna imediatamente!
            except Exception as e:
                print(f"[AVISO API] Erro ao buscar cache: {e}")
        
        # Busca na API (cache miss)
        data = self._make_request(f'pokemon/{pokemon_id}')
        
        if data and self.db_manager:
            try:
                # Salva no cache (se disponível)
                self.db_manager.save_cache(data)
            except Exception as e:
                print(f"[AVISO API] Erro ao salvar cache: {e}")
        
        return data
    
    def get_pokemon_by_name(self, name: str) -> Optional[Dict[Any, Any]]:
        """
        Busca Pokémon por nome.
        
        Args:
            name: Nome do Pokémon
        
        Returns:
            Dados do Pokémon ou None
        """
        # Verifica cache primeiro (se disponível)
        if self.db_manager:
            try:
                cached = self.db_manager.get_cached(name.lower())
                if cached:
                    return cached
            except Exception as e:
                print(f"[AVISO API] Erro ao buscar cache: {e}")
        
        # Busca na API
        data = self._make_request(f'pokemon/{name.lower()}')
        
        if data and self.db_manager:
            try:
                # Salva no cache (se disponível)
                self.db_manager.save_cache(data)
            except Exception as e:
                print(f"[AVISO API] Erro ao salvar cache: {e}")
        
        return data
    
    def get_pokemon_list(self, limit: int = 151, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Lista Pokémon com paginação.
        
        Args:
            limit: Número máximo de resultados
            offset: Offset para paginação
            
        Returns:
            Lista de Pokémon resumidos
        """
        data = self._make_request(f'pokemon?limit={limit}&offset={offset}')
        
        if not data:
            return []
        
        return data.get('results', [])
    
    def get_pokemon_type_info(self, type_name: str) -> Optional[Dict[Any, Any]]:
        """
        Busca informações sobre um tipo de Pokémon.
        
        Args:
            type_name: Nome do tipo
            
        Returns:
            Dados do tipo ou None
        """
        return self._make_request(f'type/{type_name.lower()}')
    
    def get_evolution_chain(self, chain_id: int) -> Optional[Dict[Any, Any]]:
        """
        Busca cadeia de evolução.
        
        Args:
            chain_id: ID da cadeia de evolução
            
        Returns:
            Dados da cadeia de evolução ou None
        """
        return self._make_request(f'evolution-chain/{chain_id}')

