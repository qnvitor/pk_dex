"""Ações customizadas do Rasa para interagir com PokéAPI."""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.api.pokeapi_client import PokeAPIClient


class ActionGetPokemonType(Action):
    """Ação para buscar tipo de Pokémon."""
    
    def name(self) -> Text:
        return "action_get_pokemon_type"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pokemon_name = tracker.get_slot("pokemon_name")
        
        if not pokemon_name:
            dispatcher.utter_message("Não consegui identificar o nome do Pokémon.")
            return []
        
        api_client = PokeAPIClient()
        pokemon_data = api_client.get_pokemon_by_name(pokemon_name.lower())
        
        if not pokemon_data:
            dispatcher.utter_message(
                f"Não encontrei informações sobre {pokemon_name}."
            )
            return []
        
        types = [t['type']['name'].title() for t in pokemon_data.get('types', [])]
        type_str = " e ".join(types) if len(types) == 1 else " / ".join(types)
        
        dispatcher.utter_message(
            response="utter_ask_type",
            pokemon_name=pokemon_name.title(),
            type_info=type_str
        )
        
        return []


class ActionGetPokemonStats(Action):
    """Ação para buscar stats de Pokémon."""
    
    def name(self) -> Text:
        return "action_get_pokemon_stats"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pokemon_name = tracker.get_slot("pokemon_name")
        
        if not pokemon_name:
            dispatcher.utter_message("Não consegui identificar o nome do Pokémon.")
            return []
        
        api_client = PokeAPIClient()
        pokemon_data = api_client.get_pokemon_by_name(pokemon_name.lower())
        
        if not pokemon_data:
            dispatcher.utter_message(
                f"Não encontrei informações sobre {pokemon_name}."
            )
            return []
        
        stats = pokemon_data.get('stats', [])
        stats_list = []
        for stat in stats:
            stat_name = stat['stat']['name'].replace('-', ' ').title()
            stat_value = stat['base_stat']
            stats_list.append(f"{stat_name}: {stat_value}")
        
        stats_str = ", ".join(stats_list)
        
        dispatcher.utter_message(
            response="utter_ask_stats",
            pokemon_name=pokemon_name.title(),
            stats_info=stats_str
        )
        
        return []


class ActionGetPokemonEvolution(Action):
    """Ação para buscar evolução de Pokémon."""
    
    def name(self) -> Text:
        return "action_get_pokemon_evolution"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pokemon_name = tracker.get_slot("pokemon_name")
        
        if not pokemon_name:
            dispatcher.utter_message("Não consegui identificar o nome do Pokémon.")
            return []
        
        api_client = PokeAPIClient()
        pokemon_data = api_client.get_pokemon_by_name(pokemon_name.lower())
        
        if not pokemon_data:
            dispatcher.utter_message(
                f"Não encontrei informações sobre {pokemon_name}."
            )
            return []
        
        # Busca informações da espécie para obter cadeia de evolução
        species_url = pokemon_data.get('species', {}).get('url', '')
        
        if not species_url:
            dispatcher.utter_message(
                f"Não encontrei informações de evolução para {pokemon_name}."
            )
            return []
        
        # Extrai ID da cadeia de evolução (simplificado)
        evolution_info = "Informações de evolução disponíveis na Pokédex completa."
        
        dispatcher.utter_message(
            response="utter_ask_evolution",
            evolution_info=evolution_info
        )
        
        return []


class ActionGetPokemonAbility(Action):
    """Ação para buscar habilidades de Pokémon."""
    
    def name(self) -> Text:
        return "action_get_pokemon_ability"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pokemon_name = tracker.get_slot("pokemon_name")
        
        if not pokemon_name:
            dispatcher.utter_message("Não consegui identificar o nome do Pokémon.")
            return []
        
        api_client = PokeAPIClient()
        pokemon_data = api_client.get_pokemon_by_name(pokemon_name.lower())
        
        if not pokemon_data:
            dispatcher.utter_message(
                f"Não encontrei informações sobre {pokemon_name}."
            )
            return []
        
        abilities = [
            a['ability']['name'].replace('-', ' ').title() 
            for a in pokemon_data.get('abilities', [])
        ]
        ability_str = ", ".join(abilities)
        
        dispatcher.utter_message(
            response="utter_ask_ability",
            pokemon_name=pokemon_name.title(),
            ability_info=ability_str
        )
        
        return []


class ActionSearchPokemon(Action):
    """Ação para buscar informações gerais de Pokémon."""
    
    def name(self) -> Text:
        return "action_search_pokemon"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pokemon_name = tracker.get_slot("pokemon_name")
        
        if not pokemon_name:
            dispatcher.utter_message("Não consegui identificar o nome do Pokémon.")
            return []
        
        api_client = PokeAPIClient()
        pokemon_data = api_client.get_pokemon_by_name(pokemon_name.lower())
        
        if not pokemon_data:
            dispatcher.utter_message(
                f"Não encontrei informações sobre {pokemon_name}."
            )
            return []
        
        # Formata informações básicas
        pokemon_id = pokemon_data.get('id', 'N/A')
        types = [t['type']['name'].title() for t in pokemon_data.get('types', [])]
        types_str = " / ".join(types)
        height = pokemon_data.get('height', 0) / 10
        weight = pokemon_data.get('weight', 0) / 10
        
        info = (
            f"#{pokemon_id:03d}, Tipo: {types_str}, "
            f"Altura: {height:.1f}m, Peso: {weight:.1f}kg"
        )
        
        dispatcher.utter_message(
            response="utter_pokemon_info",
            pokemon_name=pokemon_name.title(),
            info=info
        )
        
        return []

