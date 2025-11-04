"""Chatbot simples sem Rasa usando pattern matching."""

import re
from typing import Optional
from src.api.pokeapi_client import PokeAPIClient


class SimpleChatbot:
    """Chatbot simples para responder perguntas sobre Pokémon."""
    
    def __init__(self):
        """Inicializa o chatbot."""
        self.api_client = PokeAPIClient()
        
        # Padrões de reconhecimento
        self.patterns = {
            'tipo': [
                r'tipo\s+do\s+(\w+)',
                r'que\s+tipo\s+é\s+o?\s+(\w+)',
                r'qual\s+tipo\s+do\s+(\w+)',
                r'(\w+)\s+é\s+de?\s+que\s+tipo',
                r'(\w+)\s+tipo'
            ],
            'stats': [
                r'stats?\s+do\s+(\w+)',
                r'estat[íi]sticas?\s+do\s+(\w+)',
                r'atributos?\s+do\s+(\w+)',
                r'poder\s+do\s+(\w+)',
                r'defesa\s+do\s+(\w+)',
                r'ataque\s+do\s+(\w+)'
            ],
            'habilidade': [
                r'habilidades?\s+do\s+(\w+)',
                r'ability\s+do\s+(\w+)',
                r'poderes?\s+do\s+(\w+)',
                r'skills?\s+do\s+(\w+)'
            ],
            'info': [
                r'fale\s+sobre\s+o?\s+(\w+)',
                r'informa[çc][õo]es?\s+sobre\s+o?\s+(\w+)',
                r'me\s+fale\s+sobre\s+o?\s+(\w+)',
                r'quero\s+saber\s+sobre\s+o?\s+(\w+)',
                r'dados?\s+do\s+(\w+)',
                r'pok[ée]mon\s+(\w+)'
            ],
            'evolucao': [
                r'evolu[çc][ãa]o\s+do\s+(\w+)',
                r'quem\s+evolui\s+do\s+(\w+)',
                r'para\s+quem\s+o\s+(\w+)\s+evolui',
                r'evolu[çc][õo]es?\s+de\s+(\w+)',
                r'cadeia\s+de\s+evolu[çc][ãa]o\s+do\s+(\w+)'
            ]
        }
    
    def _extract_pokemon_name(self, message: str, intent: str) -> Optional[str]:
        """Extrai o nome do Pokémon da mensagem."""
        message_lower = message.lower()
        
        for pattern in self.patterns.get(intent, []):
            match = re.search(pattern, message_lower)
            if match:
                return match.group(1).strip()
        
        # Tenta encontrar qualquer palavra que possa ser nome de Pokémon
        words = message_lower.split()
        for word in words:
            # Remove pontuação
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 2 and word not in ['qual', 'que', 'quem', 'sobre', 'sobre', 'do', 'da', 'dos', 'das']:
                return word
        
        return None
    
    def _detect_intent(self, message: str) -> str:
        """Detecta a intenção da mensagem."""
        message_lower = message.lower()
        
        # Verifica cada tipo de intenção
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        # Se não encontrou, assume que é busca geral
        return 'info'
    
    def _format_type_response(self, pokemon_data: dict) -> str:
        """Formata resposta sobre tipo."""
        types = [t['type']['name'].title() for t in pokemon_data.get('types', [])]
        type_str = " e ".join(types) if len(types) == 1 else " / ".join(types)
        name = pokemon_data.get('name', '').title()
        return f"{name} é do tipo {type_str}."
    
    def _format_stats_response(self, pokemon_data: dict) -> str:
        """Formata resposta sobre stats."""
        stats = pokemon_data.get('stats', [])
        stats_list = []
        for stat in stats:
            stat_name = stat['stat']['name'].replace('-', ' ').title()
            stat_value = stat['base_stat']
            stats_list.append(f"{stat_name}: {stat_value}")
        
        name = pokemon_data.get('name', '').title()
        return f"As estatísticas de {name} são:\n" + "\n".join(stats_list)
    
    def _format_ability_response(self, pokemon_data: dict) -> str:
        """Formata resposta sobre habilidades."""
        abilities = [
            a['ability']['name'].replace('-', ' ').title() 
            for a in pokemon_data.get('abilities', [])
        ]
        ability_str = ", ".join(abilities)
        name = pokemon_data.get('name', '').title()
        return f"As habilidades de {name} são: {ability_str}."
    
    def _format_info_response(self, pokemon_data: dict) -> str:
        """Formata resposta geral."""
        pokemon_id = pokemon_data.get('id', 'N/A')
        name = pokemon_data.get('name', '').title()
        types = [t['type']['name'].title() for t in pokemon_data.get('types', [])]
        types_str = " / ".join(types)
        height = pokemon_data.get('height', 0) / 10
        weight = pokemon_data.get('weight', 0) / 10
        
        abilities = [
            a['ability']['name'].replace('-', ' ').title() 
            for a in pokemon_data.get('abilities', [])[:3]
        ]
        abilities_str = ", ".join(abilities)
        
        return f"""**{name}** (#{pokemon_id:03d})

**Tipo:** {types_str}
**Altura:** {height:.1f}m
**Peso:** {weight:.1f}kg
**Habilidades:** {abilities_str}

Para mais informações, use a página de busca!"""
    
    def _format_evolution_response(self, pokemon_data: dict) -> str:
        """Formata resposta sobre evolução."""
        name = pokemon_data.get('name', '').title()
        return f"Informações detalhadas sobre a evolução de {name} estão disponíveis na Pokédex completa. Use a busca para ver mais detalhes!"
    
    def get_response(self, message: str) -> str:
        """
        Obtém resposta para a mensagem do usuário.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Resposta do chatbot
        """
        # Detecta intenção
        intent = self._detect_intent(message)
        
        # Extrai nome do Pokémon
        pokemon_name = self._extract_pokemon_name(message, intent)
        
        if not pokemon_name:
            return "Não consegui identificar o nome do Pokémon na sua pergunta. Tente perguntar como: 'Qual é o tipo do Pikachu?'"
        
        # Busca dados do Pokémon
        pokemon_data = self.api_client.get_pokemon_by_name(pokemon_name.lower())
        
        if not pokemon_data:
            return f"Não encontrei informações sobre '{pokemon_name}'. Tente com outro nome ou ID."
        
        # Formata resposta baseada na intenção
        if intent == 'tipo':
            return self._format_type_response(pokemon_data)
        elif intent == 'stats':
            return self._format_stats_response(pokemon_data)
        elif intent == 'habilidade':
            return self._format_ability_response(pokemon_data)
        elif intent == 'evolucao':
            return self._format_evolution_response(pokemon_data)
        else:  # info ou padrão
            return self._format_info_response(pokemon_data)
    
    def check_server_status(self) -> bool:
        """Sempre retorna True para chatbot simples."""
        return True

