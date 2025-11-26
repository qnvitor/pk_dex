"""Cliente para Ollama API."""

import ollama
from typing import Optional, Dict, Any, List
from src.config import DEFAULT_OLLAMA_MODEL


class OllamaClient:
    """Cliente para interagir com Ollama API."""
    
    def __init__(self, model: str = DEFAULT_OLLAMA_MODEL):
        """
        Inicializa o cliente Ollama.
        
        Args:
            model: Nome do modelo a ser usado
        """
        self.model = model
        self.client = ollama.Client()
    
    def generate(
        self,
        prompt: str,
        context: str = "",
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Gera resposta usando Ollama.
        
        Args:
            prompt: Prompt/pergunta do usuário
            context: Contexto adicional (documentos recuperados)
            temperature: Controla aleatoriedade (0.0-1.0)
            max_tokens: Número máximo de tokens na resposta
            
        Returns:
            Resposta gerada pelo modelo
        """
        # Monta prompt completo
        if context:
            full_prompt = f"""Contexto relevante:
{context}

Pergunta: {prompt}

Resposta:"""
        else:
            full_prompt = f"Pergunta: {prompt}\n\nResposta:"
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=full_prompt,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "top_p": 0.9,
                }
            )
            
            return response['response'].strip()
        except Exception as e:
            print(f"[ERRO OLLAMA] Erro ao gerar resposta: {e}")
            return f"Erro ao gerar resposta: {str(e)}"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str:
        """
        Gera resposta usando formato de chat.
        
        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            temperature: Controla aleatoriedade
            
        Returns:
            Resposta do modelo
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={"temperature": temperature}
            )
            
            return response['message']['content'].strip()
        except Exception as e:
            print(f"[ERRO OLLAMA] Erro no chat: {e}")
            return f"Erro ao gerar resposta: {str(e)}"
    
    def check_model_available(self) -> bool:
        """
        Verifica se o modelo está disponível.
        
        Returns:
            True se o modelo está disponível, False caso contrário
        """
        try:
            models = self.client.list()
            available_models = [m['name'] for m in models.get('models', [])]
            
            # Verifica se o modelo exato ou uma variante está disponível
            return any(self.model in model for model in available_models)
        except Exception as e:
            print(f"[ERRO OLLAMA] Erro ao verificar modelos: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """
        Lista todos os modelos disponíveis.
        
        Returns:
            Lista de nomes de modelos
        """
        try:
            models = self.client.list()
            return [m['name'] for m in models.get('models', [])]
        except Exception as e:
            print(f"[ERRO OLLAMA] Erro ao listar modelos: {e}")
            return []
    
    def check_server_status(self) -> bool:
        """
        Verifica se o servidor Ollama está rodando.
        
        Returns:
            True se o servidor está ativo, False caso contrário
        """
        try:
            self.client.list()
            return True
        except Exception:
            return False
