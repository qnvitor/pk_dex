"""Classificador de imagens de Pokémon usando MobileNetV2 com PyTorch."""

import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from typing import List, Tuple, Optional
import os
from dotenv import load_dotenv

from src.vision.model_loader import ModelLoader

# Carrega .env - ignora se houver problema de encoding
try:
    load_dotenv()
except Exception:
    pass

NUM_PREDICTIONS = int(os.getenv('NUM_PREDICTIONS', 5))


# =============================================================================
# POKEMONCLASSIFIER - Sistema de Inferência para Reconhecimento de Imagens
# =============================================================================
# 
#  O QUE FAZ:
#    - Recebe imagem de Pokémon e retorna predições com níveis de confiança
#    - Pré-processa imagens (resize, normalização, etc.)
#    - Executa inferência usando modelo treinado
#    - Retorna top-N predições ordenadas por confiança
#
#  REFERÊNCIAS:
#    - Usado por pages/3_Reconhecimento.py linha 48
#    - Carrega modelo via src/vision/model_loader.py linha 27
#    - Modelo treinado em scripts/train_model.py

class PokemonClassifier:
    """Classificador de imagens de Pokémon."""
    
    def __init__(self, model_path: str = None):
        """Inicializa o classificador."""
        self.model_loader = ModelLoader(model_path) if model_path else ModelLoader()
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.input_shape = (224, 224)
        self.num_predictions = NUM_PREDICTIONS
        
        # ---------------------------------------------------------------------------
        # TRANSFORMAÇÕES DE PRÉ-PROCESSAMENTO
        # ---------------------------------------------------------------------------
        # - Resize 256x256 → CenterCrop 224x224: padrão MobileNetV2
        # - ToTensor: converte PIL Image (0-255) para Tensor (0.0-1.0)
        # - Normalize: usa média/desvio do ImageNet (padrão para modelos pré-treinados)
        # 
        # antialias=True: suaviza redimensionamento para melhor qualidade
        # ---------------------------------------------------------------------------
        self.transform = transforms.Compose([
            transforms.Resize((256, 256), antialias=True),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo."""
        try:
            self.model = self.model_loader.load_model()
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.model = None
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Pré-processa imagem para o modelo PyTorch com melhorias.
        
        Args:
            image: Imagem PIL
            
        Returns:
            Tensor PyTorch pré-processado
        """
        # Converte para RGB se necessário
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Melhora contraste e saturação levemente
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)  # Aumenta contraste em 10%
        
        # Aplica transformações
        tensor = self.transform(image)
        
        # Adiciona dimensão de batch
        tensor = tensor.unsqueeze(0)
        
        return tensor.to(self.device)
    
    def predict(self, image: Image.Image, min_confidence: float = 0.01) -> List[Tuple[int, float]]:
        """
        Classifica imagem e retorna top-N predições.
        
        Args:
            image: Imagem PIL para classificar
            min_confidence: Confiança mínima para incluir predição (padrão: 0.01 = 1%)
            
        Returns:
            Lista de tuplas (pokemon_id, confidence) ordenada por confiança
        """
        if self.model is None:
            raise ValueError("Modelo não carregado")
        
        # Pré-processa imagem
        processed = self.preprocess_image(image)
        
        # Faz predição
        with torch.no_grad():  # Desliga gradientes (economiza memória)
            outputs = self.model(processed)  # Forward pass
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)  # Converte para probabilidades
        
        # Obtém top-N predições
        top_probs, top_indices = torch.topk(probabilities, self.num_predictions)
        
        # Formata resultados: índice do tensor (0-150) → ID do Pokémon (1-151)
        top_predictions = [
            (int(idx.item() + 1), float(top_probs[i].item()))  # ID começa em 1
            for i, idx in enumerate(top_indices)
            if float(top_probs[i].item()) >= min_confidence  # Filtra por confiança mínima
        ]
        
        return top_predictions
    
    def predict_single(self, image: Image.Image) -> Optional[Tuple[int, float]]:
        """
        Retorna apenas a predição mais provável.
        
        Args:
            image: Imagem PIL para classificar
            
        Returns:
            Tupla (pokemon_id, confidence) ou None
        """
        predictions = self.predict(image)
        return predictions[0] if predictions else None
    
    def is_model_ready(self) -> bool:
        """Verifica se o modelo está pronto para uso."""
        return self.model is not None

