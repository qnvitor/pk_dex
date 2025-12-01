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


# =============================================================================
# POKEMONCLASSIFIERMODEL - Arquitetura do Modelo Neural
# =============================================================================
# 
#  O QUE FAZ:
#    - Define arquitetura do modelo: MobileNetV2 + camada customizada
#    - Congela camadas base (transfer learning)
#    - Substitui classificador ImageNet (1000 classes) por Pokémon (151 classes)
#
#  REFERÊNCIAS:
#    - Instanciado por ModelLoader.load_model() linha 69
#    - Treinado por scripts/train_model.py linha 161
#    - Usado por src/vision/pokemon_classifier.py para inferência

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


# =============================================================================
# MODELLOADER - Gerenciador de Carregamento e Persistencia do Modelo
# =============================================================================
# 
#  O QUE FAZ:
#    - Carrega modelo treinado de disco (se existir)
#    - Cria modelo base se não houver modelo treinado (fallback)
#    - Gerencia persistência do modelo após treinamento
#
#  REFERÊNCIAS:
#    - Usado por src/vision/pokemon_classifier.py linha 27
#    - Usado por scripts/train_model.py para salvar modelo (linha 230)
#    - Arquivo do modelo: models/mobilenet_pokemon/model.pth

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
        
        # ---------------------------------------------------------------------------
        # ESTRATÉGIA DE CARREGAMENTO
        # ---------------------------------------------------------------------------
        # 1. Tenta carregar modelo treinado de disco
        # 2. Se não encontrar, cria modelo base para treinamento
        # 
        # Arquivo esperado: models/mobilenet_pokemon/model.pth
        # ---------------------------------------------------------------------------
        if model_file.exists():
            # Carrega modelo existente
            self.model = PokemonClassifierModel(self.num_classes)
            self.model.load_state_dict(torch.load(str(model_file), map_location=self.device))
            self.model.to(self.device)
            self.model.eval()  # Modo de inferência (desativa dropout)
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

