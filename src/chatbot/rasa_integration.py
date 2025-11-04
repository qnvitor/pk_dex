"""Integração com servidor Rasa para chatbot (OPCIONAL).

Este módulo é mantido para uso futuro caso queira usar Rasa.
O projeto atual usa SimpleChatbot (pattern matching) que não requer Rasa.
Para usar Rasa, é necessário Python 3.8-3.11 (não compatível com Python 3.13).
"""

import requests
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Carrega .env - ignora se houver problema de encoding
try:
    load_dotenv()
except Exception:
    pass

RASA_SERVER_URL = os.getenv('RASA_SERVER_URL', 'http://localhost:5005')
RASA_WEBHOOK_URL = os.getenv('RASA_WEBHOOK_URL', 'http://localhost:5005/webhooks/rest/webhook')


class RasaIntegration:
    """Integração com servidor Rasa."""
    
    def __init__(self, server_url: str = RASA_SERVER_URL, webhook_url: str = RASA_WEBHOOK_URL):
        """Inicializa a integração com Rasa."""
        self.server_url = server_url
        self.webhook_url = webhook_url
        self.session = requests.Session()
    
    def send_message(self, message: str, sender_id: str = "user") -> List[Dict[str, Any]]:
        """
        Envia mensagem para o Rasa e recebe resposta.
        
        Args:
            message: Mensagem do usuário
            sender_id: ID do remetente
            
        Returns:
            Lista de respostas do Rasa
        """
        try:
            payload = {
                "sender": sender_id,
                "message": message
            }
            
            response = self.session.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com Rasa: {e}")
            return []
    
    def get_response(self, message: str, sender_id: str = "user") -> str:
        """
        Obtém resposta textual do Rasa.
        
        Args:
            message: Mensagem do usuário
            sender_id: ID do remetente
            
        Returns:
            Resposta textual do Rasa ou mensagem de erro
        """
        responses = self.send_message(message, sender_id)
        
        if not responses:
            return "Desculpe, não consegui processar sua mensagem. O servidor Rasa pode estar offline."
        
        # Concatena todas as respostas
        text_responses = [
            resp.get('text', '') for resp in responses 
            if resp.get('text')
        ]
        
        return '\n'.join(text_responses) if text_responses else "Sem resposta disponível."
    
    def check_server_status(self) -> bool:
        """
        Verifica se o servidor Rasa está online.
        
        Returns:
            True se o servidor está online, False caso contrário
        """
        try:
            response = self.session.get(
                f"{self.server_url}/status",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def parse_intent(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Faz parse da intenção da mensagem.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Dicionário com intenção e entidades ou None
        """
        try:
            payload = {
                "text": message
            }
            
            response = self.session.post(
                f"{self.server_url}/model/parse",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer parse da intenção: {e}")
            return None

