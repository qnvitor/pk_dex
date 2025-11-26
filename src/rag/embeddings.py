"""Gerador de embeddings para busca semântica."""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import os
from src.config import EMBEDDING_MODEL, EMBEDDING_CACHE_DIR


class EmbeddingGenerator:
    """Gerador de embeddings usando Sentence Transformers."""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Inicializa o gerador de embeddings.
        
        Args:
            model_name: Nome do modelo de embedding
                       all-MiniLM-L6-v2: Leve, rápido, multilíngue (~80MB)
                       paraphrase-multilingual-MiniLM-L12-v2: Melhor para português
        """
        self.model_name = model_name
        print(f"[EMBEDDINGS] Carregando modelo {model_name}...")
        
        try:
            self.model = SentenceTransformer(
                model_name,
                cache_folder=EMBEDDING_CACHE_DIR
            )
            print(f"[EMBEDDINGS] Modelo carregado com sucesso!")
        except Exception as e:
            print(f"[ERRO EMBEDDINGS] Erro ao carregar modelo: {e}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Gera embedding para um texto.
        
        Args:
            text: Texto para gerar embedding
            
        Returns:
            Array numpy com o embedding
        """
        try:
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True  # Normaliza para cálculo de similaridade
            )
            return embedding
        except Exception as e:
            print(f"[ERRO EMBEDDINGS] Erro ao gerar embedding: {e}")
            # Retorna embedding zero em caso de erro
            return np.zeros(self.model.get_sentence_embedding_dimension())
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Gera embeddings para múltiplos textos.
        
        Args:
            texts: Lista de textos
            
        Returns:
            Array numpy com os embeddings (shape: [n_texts, embedding_dim])
        """
        try:
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=len(texts) > 10  # Mostra barra apenas para muitos textos
            )
            return embeddings
        except Exception as e:
            print(f"[ERRO EMBEDDINGS] Erro ao gerar embeddings: {e}")
            # Retorna embeddings zeros em caso de erro
            dim = self.model.get_sentence_embedding_dimension()
            return np.zeros((len(texts), dim))
    
    def similarity(
        self,
        emb1: Union[np.ndarray, str],
        emb2: Union[np.ndarray, str]
    ) -> float:
        """
        Calcula similaridade de cosseno entre dois embeddings ou textos.
        
        Args:
            emb1: Embedding ou texto 1
            emb2: Embedding ou texto 2
            
        Returns:
            Similaridade (0.0 a 1.0, onde 1.0 é idêntico)
        """
        # Converte textos em embeddings se necessário
        if isinstance(emb1, str):
            emb1 = self.generate_embedding(emb1)
        if isinstance(emb2, str):
            emb2 = self.generate_embedding(emb2)
        
        # Calcula similaridade de cosseno
        # Como os embeddings já são normalizados, é só o produto escalar
        similarity = np.dot(emb1, emb2)
        
        return float(similarity)
    
    def get_embedding_dimension(self) -> int:
        """
        Retorna a dimensão dos embeddings.
        
        Returns:
            Dimensão do embedding
        """
        return self.model.get_sentence_embedding_dimension()
