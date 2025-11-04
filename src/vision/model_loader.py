"""Carregador de modelo MobileNetV2 para classificação de Pokémon usando PyTorch."""

import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env - ignora se houver problema de encoding
try:
    load_dotenv()
except Exception:
    pass

MODEL_PATH = os.getenv('MODEL_PATH', 'models/mobilenet_pokemon')


class PokemonClassifierModel(nn.Module):
    """Modelo de classificação de Pokémon baseado em MobileNetV2."""
    
    def __init__(self, num_classes: int = 151):
        """Inicializa o modelo."""
        super(PokemonClassifierModel, self).__init__()
        
        # Carrega MobileNetV2 pré-treinado
        base_model = models.mobilenet_v2(weights='IMAGENET1K_V1')
        
        # Congela parâmetros base para transfer learning
        for param in base_model.features.parameters():
            param.requires_grad = False
        
        # Substitui a camada de classificação
        base_model.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(base_model.last_channel, num_classes)
        )
        
        self.model = base_model
    
    def forward(self, x):
        """Forward pass."""
        return self.model(x)


class ModelLoader:
    """Carregador de modelo MobileNetV2 usando PyTorch."""
    
    def __init__(self, model_path: str = MODEL_PATH):
        """Inicializa o carregador de modelo."""
        self.model_path = model_path
        self.model: Optional[torch.nn.Module] = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.input_shape = (224, 224, 3)
        self.num_classes = 151  # Pokémon da primeira geração
    
    def load_model(self) -> torch.nn.Module:
        """
        Carrega o modelo MobileNetV2.
        Se não existir, cria um modelo base para transfer learning.
        
        Returns:
            Modelo PyTorch carregado ou criado
        """
        if self.model is not None:
            return self.model
        
        model_file = Path(self.model_path) / 'model.pth'
        
        if model_file.exists():
            # Carrega modelo existente
            self.model = PokemonClassifierModel(self.num_classes)
            self.model.load_state_dict(torch.load(str(model_file), map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
        else:
            # Cria modelo base MobileNetV2 para transfer learning
            self.model = self._create_base_model()
        
        return self.model
    
    def _create_base_model(self) -> torch.nn.Module:
        """
        Cria modelo base MobileNetV2 para transfer learning.
        
        Returns:
            Modelo PyTorch base
        """
        try:
            # Tenta carregar com progresso silencioso
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = PokemonClassifierModel(self.num_classes)
                model.to(self.device)
                model.eval()
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao criar modelo base: {e}")
    
    def save_model(self, model: torch.nn.Module):
        """
        Salva o modelo no disco.
        
        Args:
            model: Modelo PyTorch a ser salvo
        """
        Path(self.model_path).mkdir(parents=True, exist_ok=True)
        model_file = Path(self.model_path) / 'model.pth'
        torch.save(model.state_dict(), str(model_file))
        self.model = model
    
    def get_model(self) -> Optional[torch.nn.Module]:
        """Retorna o modelo carregado."""
        if self.model is None:
            self.load_model()
        return self.model

