"""Chatbot com RAG (Retrieval-Augmented Generation)."""

from typing import Optional, List, Dict
from src.config import DEFAULT_OLLAMA_MODEL, DEFAULT_RAG_ENABLED, DEFAULT_N_CONTEXT_DOCS
from src.rag.ollama_client import OllamaClient
from src.rag.vector_store import PokemonVectorStore
from src.api.pokeapi_client import PokeAPIClient


class RAGChatbot:
    """Chatbot inteligente com RAG para perguntas sobre Pokémon."""
    
    def __init__(
        self,
        model: str = DEFAULT_OLLAMA_MODEL,
        use_rag: bool = DEFAULT_RAG_ENABLED,
        n_context_docs: int = DEFAULT_N_CONTEXT_DOCS
    ):
        """
        Inicializa o chatbot RAG.
        
        Args:
            model: Nome do modelo Ollama
            use_rag: Se True, usa RAG; se False, usa apenas LLM
            n_context_docs: Número de documentos de contexto a recuperar
        """
        self.model = model
        self.use_rag = use_rag
        self.n_context_docs = n_context_docs
        
        # Inicializa componentes
        print(f"[RAG CHATBOT] Inicializando com modelo {model}...")
        
        try:
            self.ollama = OllamaClient(model=model)
            self.ollama_available = self.ollama.check_server_status()
            
            if not self.ollama_available:
                print("[RAG CHATBOT] AVISO: Ollama nao esta disponivel!")
            else:
                print("[RAG CHATBOT] Ollama conectado!")
                
                # Verifica se o modelo está disponível
                if not self.ollama.check_model_available():
                    print(f"[RAG CHATBOT] AVISO: Modelo {model} nao encontrado!")
                    print(f"[RAG CHATBOT] Modelos disponíveis: {self.ollama.list_models()}")
        except Exception as e:
            print(f"[RAG CHATBOT] ERRO ao conectar Ollama: {e}")
            self.ollama_available = False
        
        # Inicializa vector store e API client
        if use_rag:
            try:
                self.vector_store = PokemonVectorStore()
                print(f"[RAG CHATBOT] Vector store carregado: {self.vector_store.count()} Pokémon")
            except Exception as e:
                print(f"[RAG CHATBOT] AVISO: Erro ao carregar vector store: {e}")
                self.vector_store = None
        else:
            self.vector_store = None
        
        self.api_client = PokeAPIClient()
    
    def get_response(self, message: str) -> str:
        """
        Gera resposta para a mensagem do usuário.
        
        Args:
            message: Mensagem/pergunta do usuário
            
        Returns:
            Resposta do chatbot
        """
        # Verifica se Ollama está disponível
        if not self.ollama_available:
            return self._fallback_response(message)
        
        # 1. Recupera contexto relevante (se RAG ativado)
        context = ""
        if self.use_rag and self.vector_store:
            context = self._retrieve_context(message)
        
        # 2. Monta prompt com sistema
        prompt = self._build_prompt(message, context)
        
        # 3. Gera resposta
        try:
            response = self.ollama.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500
            )
            return response
        except Exception as e:
            print(f"[RAG CHATBOT] Erro ao gerar resposta: {e}")
            return self._fallback_response(message)
    
    def _retrieve_context(self, query: str) -> str:
        """
        Recupera contexto relevante do vector store.
        
        Args:
            query: Pergunta do usuário
            
        Returns:
            Contexto formatado
        """
        if not self.vector_store:
            return ""
        
        try:
            # Busca documentos similares
            results = self.vector_store.search(
                query=query,
                n_results=self.n_context_docs
            )
            
            if not results or not results.get('documents') or not results['documents'][0]:
                return ""
            
            # Formata contexto
            documents = results['documents'][0]
            metadatas = results.get('metadatas', [[]])[0]
            
            context_parts = []
            for i, (doc, meta) in enumerate(zip(documents, metadatas), 1):
                context_parts.append(f"[Documento {i}]\n{doc}")
            
            context = "\n\n".join(context_parts)
            return context
            
        except Exception as e:
            print(f"[RAG CHATBOT] Erro ao recuperar contexto: {e}")
            return ""
    
    def _build_prompt(self, question: str, context: str) -> str:
        """
        Constrói prompt para o LLM.
        
        Args:
            question: Pergunta do usuário
            context: Contexto recuperado
            
        Returns:
            Prompt formatado
        """
        system_prompt = """Você é um assistente especializado em Pokémon, amigável e prestativo.

INSTRUÇÕES:
- Responda perguntas sobre Pokémon de forma clara, concisa e informativa
- Use as informações fornecidas no contexto para responder
- Se o contexto não tiver a informação necessária, diga que não sabe
- Seja educado e mantenha um tom amigável
- Formate sua resposta de forma organizada
- Use markdown para destacar informações importantes
- Não invente informações que não estão no contexto

IMPORTANTE: Responda APENAS sobre Pokémon. Se a pergunta não for sobre Pokémon, 
diga educadamente que você só pode ajudar com perguntas sobre Pokémon."""
        
        if context:
            prompt = f"""{system_prompt}

CONTEXTO COM INFORMAÇÕES RELEVANTES:
{context}

PERGUNTA DO USUÁRIO: {question}

RESPOSTA:"""
        else:
            prompt = f"""{system_prompt}

PERGUNTA DO USUÁRIO: {question}

RESPOSTA:"""
        
        return prompt
    
    def _fallback_response(self, message: str) -> str:
        """
        Resposta de fallback quando Ollama não está disponível.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Mensagem de erro amigável
        """
        return """**Ollama nao esta disponivel**

Para usar o chatbot com IA, você precisa:

1. **Iniciar o servidor Ollama**:
   ```
   ollama serve
   ```

2. **Verificar se o modelo está instalado**:
   ```
   ollama list
   ```

3. **Se necessário, baixar o modelo**:
   ```
   ollama pull llama3.2:3b
   ```

Enquanto isso, você pode usar a página de **Busca** para encontrar informações sobre Pokémon!"""
    
    def check_server_status(self) -> bool:
        """
        Verifica se o servidor Ollama está rodando.
        
        Returns:
            True se disponível, False caso contrário
        """
        return self.ollama_available
    
    def get_stats(self) -> Dict[str, any]:
        """
        Retorna estatísticas do chatbot.
        
        Returns:
            Dicionário com estatísticas
        """
        stats = {
            "ollama_available": self.ollama_available,
            "model": self.model,
            "rag_enabled": self.use_rag,
            "vector_store_docs": 0
        }
        
        if self.vector_store:
            stats["vector_store_docs"] = self.vector_store.count()
        
        return stats
