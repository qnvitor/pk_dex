"""Gerenciador de banco de dados SQLite para cache de Pokémon."""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env - ignora se houver problema de encoding
try:
    load_dotenv()
except Exception:
    # Se houver erro ao carregar .env, usa valores padrão
    pass

DB_PATH = os.getenv('DB_PATH', 'data/pokemon_db.sqlite')
CACHE_TTL = int(os.getenv('POKEAPI_CACHE_TTL', 86400))  # 24 horas padrão


class DatabaseManager:
    """Gerenciador de banco de dados SQLite."""
    
    def __init__(self, db_path: str = DB_PATH):
        """Inicializa o gerenciador de banco de dados."""
        self.db_path = db_path
        self._initialized = False
        # Não inicializa imediatamente - apenas quando necessário
        try:
            self._ensure_db_directory()
            self._init_database()
            self._initialized = True
        except Exception as e:
            print(f"[ERRO DB] Erro ao inicializar DatabaseManager: {e}")
            self._initialized = False
    
    def _ensure_db_directory(self):
        """Garante que o diretório do banco existe."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """Inicializa a tabela de cache se não existir."""
        try:
            # Tenta conectar com timeout curto
            conn = sqlite3.connect(self.db_path, timeout=2.0)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pokemon_cache (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
        except sqlite3.OperationalError as e:
            # Se o banco estiver travado, apenas registra o erro
            print(f"[AVISO DB] Banco de dados pode estar travado: {e}")
            print(f"[AVISO DB] Continuando sem cache de banco de dados")
        except Exception as e:
            print(f"[ERRO DB] Erro ao inicializar banco de dados: {e}")
    
    def get_cached(self, identifier: str) -> Optional[Dict[Any, Any]]:
        """
        Busca Pokémon no cache por ID ou nome.
        
        Args:
            identifier: ID numérico ou nome do Pokémon
            
        Returns:
            Dados do Pokémon se encontrado e válido, None caso contrário
        """
        if not self._initialized:
            return None
        try:
            conn = sqlite3.connect(self.db_path, timeout=2.0)
            cursor = conn.cursor()
        except Exception as e:
            print(f"[ERRO DB] Erro ao conectar ao banco: {e}")
            return None
        
        # Tenta buscar por ID ou nome
        try:
            pokemon_id = int(identifier)
            cursor.execute(
                'SELECT data_json, created_at FROM pokemon_cache WHERE id = ?',
                (pokemon_id,)
            )
        except ValueError:
            cursor.execute(
                'SELECT data_json, created_at FROM pokemon_cache WHERE name = ?',
                (identifier.lower(),)
            )
        
        try:
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            data_json, created_at_str = result
            created_at = datetime.fromisoformat(created_at_str)
            
            # Verifica se o cache ainda é válido
            if datetime.now() - created_at > timedelta(seconds=CACHE_TTL):
                return None
            
            return json.loads(data_json)
        except Exception as e:
            print(f"[ERRO DB] Erro ao buscar cache: {e}")
            try:
                conn.close()
            except:
                pass
            return None
    
    def save_cache(self, pokemon_data: Dict[Any, Any]):
        """
        Salva dados de Pokémon no cache.
        
        Args:
            pokemon_data: Dicionário com dados do Pokémon da PokéAPI
        """
        if not self._initialized:
            return
        try:
            conn = sqlite3.connect(self.db_path, timeout=2.0)
            cursor = conn.cursor()
            
            pokemon_id = pokemon_data['id']
            name = pokemon_data['name'].lower()
            data_json = json.dumps(pokemon_data)
            created_at = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT OR REPLACE INTO pokemon_cache (id, name, data_json, created_at)
                VALUES (?, ?, ?, ?)
            ''', (pokemon_id, name, data_json, created_at))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERRO DB] Erro ao salvar cache: {e}")
    
    def clear_old_cache(self, days: int = 7):
        """
        Remove cache antigo do banco.
        
        Args:
            days: Número de dias para considerar como antigo
        """
        if not self._initialized:
            return
        try:
            conn = sqlite3.connect(self.db_path, timeout=2.0)
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            cursor.execute('DELETE FROM pokemon_cache WHERE created_at < ?', (cutoff_date,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERRO DB] Erro ao limpar cache antigo: {e}")
    
    def clear_all_cache(self):
        """Remove todo o cache do banco."""
        if not self._initialized:
            return
        try:
            conn = sqlite3.connect(self.db_path, timeout=2.0)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM pokemon_cache')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERRO DB] Erro ao limpar cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        if not self._initialized:
            return {'total': 0, 'valid': 0, 'expired': 0}
        try:
            conn = sqlite3.connect(self.db_path, timeout=2.0)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM pokemon_cache')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM pokemon_cache WHERE created_at > ?', 
                          ((datetime.now() - timedelta(seconds=CACHE_TTL)).isoformat(),))
            valid = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total': total,
                'valid': valid,
                'expired': total - valid
            }
        except Exception as e:
            print(f"[ERRO DB] Erro ao obter estatísticas: {e}")
            return {'total': 0, 'valid': 0, 'expired': 0}

