"""Modelos de dados para o banco SQLite."""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import json


@dataclass
class PokemonCache:
    """Modelo para cache de Pokémon."""
    id: int
    name: str
    data: Dict[Any, Any]
    created_at: str


@dataclass
class PokemonData:
    """Modelo para dados de Pokémon."""
    id: int
    name: str
    types: list
    stats: Dict[str, int]
    abilities: list
    height: int
    weight: int
    sprites: Dict[str, str]
    evolution_chain_id: Optional[int] = None

