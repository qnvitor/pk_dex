"""Script para treinar o modelo MobileNetV2 com imagens de Pokémon da PokéAPI."""

import os
import sys
from pathlib import Path
import requests
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from tqdm import tqdm
import json

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.vision.model_loader import PokemonClassifierModel, ModelLoader
from src.api.pokeapi_client import PokeAPIClient


class PokemonDataset(Dataset):
    """Dataset de imagens de Pokémon."""
    
    def __init__(self, images_dir: str, transform=None):
        """
        Args:
            images_dir: Diretório com subpastas por ID de Pokémon (1/, 2/, etc.)
            transform: Transformações a aplicar
        """
        self.images_dir = Path(images_dir)
        self.transform = transform
        self.samples = []
        
        # Encontra todas as imagens
        for pokemon_dir in sorted(self.images_dir.iterdir()):
            if pokemon_dir.is_dir() and pokemon_dir.name.isdigit():
                pokemon_id = int(pokemon_dir.name)
                # Busca imagens com diferentes extensões
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                    for img_file in pokemon_dir.glob(ext):
                        self.samples.append((str(img_file), pokemon_id - 1))  # ID começa em 0 para PyTorch
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
        
        return image, label


def download_pokemon_images(num_pokemon: int = 151, output_dir: str = "data/pokemon_images"):
    """Baixa imagens de Pokémon da PokéAPI."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    api_client = PokeAPIClient()
    
    print(f"Baixando imagens de {num_pokemon} Pokémon...")
    
    for pokemon_id in tqdm(range(1, num_pokemon + 1), desc="Baixando"):
        try:
            pokemon_data = api_client.get_pokemon_by_id(pokemon_id)
            if not pokemon_data:
                continue
            
            # Obtém URL da imagem oficial
            sprite_url = pokemon_data.get('sprites', {}).get('other', {}).get('official-artwork', {}).get('front_default')
            if not sprite_url:
                sprite_url = pokemon_data.get('sprites', {}).get('front_default')
            
            pokemon_dir = output_path / str(pokemon_id)
            pokemon_dir.mkdir(exist_ok=True)
            
            # Baixa múltiplas versões de sprites para aumentar o dataset
            sprites = pokemon_data.get('sprites', {})
            
            # Lista de sprites para baixar
            sprite_urls = []
            
            # Sprite oficial (melhor qualidade)
            official = sprites.get('other', {}).get('official-artwork', {}).get('front_default')
            if official:
                sprite_urls.append(('official.png', official))
            
            # Sprite padrão
            front_default = sprites.get('front_default')
            if front_default:
                sprite_urls.append(('default.png', front_default))
            
            # Sprite shiny
            shiny = sprites.get('other', {}).get('official-artwork', {}).get('front_shiny')
            if shiny:
                sprite_urls.append(('shiny.png', shiny))
            
            # Baixa cada sprite
            for filename, url in sprite_urls:
                img_path = pokemon_dir / filename
                if not img_path.exists() and url:
                    try:
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            with open(img_path, 'wb') as f:
                                f.write(response.content)
                    except Exception as e:
                        print(f"  [AVISO] Erro ao baixar {filename} para Pokemon {pokemon_id}: {e}")
        except Exception as e:
            print(f"Erro ao baixar Pokémon {pokemon_id}: {e}")
    
    print(f"Imagens baixadas em {output_dir}")


def train_model(
    images_dir: str = "data/pokemon_images",
    model_save_path: str = "models/mobilenet_pokemon",
    num_epochs: int = 10,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    num_pokemon: int = 151
):
    """Treina o modelo MobileNetV2."""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando dispositivo: {device}")
    
    # Transformações para treinamento com data augmentation agressivo
    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomCrop(224),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Cria dataset
    dataset = PokemonDataset(images_dir, transform=train_transform)
    
    if len(dataset) == 0:
        print("[ERRO] Nenhuma imagem encontrada! Execute primeiro download_pokemon_images()")
        return
    
    # Divide em treino e validação (80/20)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Cria modelo
    model = PokemonClassifierModel(num_classes=num_pokemon)
    model.to(device)
    
    # Descongela mais camadas para fine-tuning (melhor para poucos dados)
    # Descongela as últimas 10 camadas
    for param in model.model.features[-10:].parameters():
        param.requires_grad = True
    # Descongela completamente a camada de classificação
    for param in model.model.classifier.parameters():
        param.requires_grad = True
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)
    
    print(f"\nTreinando modelo por {num_epochs} épocas...")
    print(f"Imagens de treino: {len(train_dataset)}")
    print(f"Imagens de validação: {len(val_dataset)}")
    
    best_val_acc = 0.0
    
    for epoch in range(num_epochs):
        # Treino
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for images, labels in tqdm(train_loader, desc=f"Época {epoch+1}/{num_epochs} [Treino]"):
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
        
        # Validação
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in tqdm(val_loader, desc=f"Época {epoch+1}/{num_epochs} [Validação]"):
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        train_acc = 100 * train_correct / train_total
        val_acc = 100 * val_correct / val_total
        
        print(f"\nÉpoca {epoch+1}/{num_epochs}:")
        print(f"  Treino - Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%")
        print(f"  Validação - Loss: {val_loss/len(val_loader):.4f}, Acc: {val_acc:.2f}%")
        
        # Salva melhor modelo
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            model_loader = ModelLoader(model_save_path)
            model_loader.save_model(model)
            print(f"  [OK] Melhor modelo salvo! (Acc: {val_acc:.2f}%)")
        
        scheduler.step()
    
    print(f"\n[OK] Treinamento concluido! Melhor acuracia: {best_val_acc:.2f}%")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Treina modelo MobileNetV2 para classificação de Pokémon")
    parser.add_argument("--download", action="store_true", help="Baixa imagens da PokéAPI primeiro")
    parser.add_argument("--train", action="store_true", help="Treina o modelo (padrão: True se não for --download)")
    parser.add_argument("--num-pokemon", type=int, default=151, help="Número de Pokémon (padrão: 151)")
    parser.add_argument("--epochs", type=int, default=10, help="Número de épocas (padrão: 10)")
    parser.add_argument("--batch-size", type=int, default=32, help="Tamanho do batch (padrão: 32)")
    
    args = parser.parse_args()
    
    if args.download:
        print("[INFO] Baixando imagens...")
        download_pokemon_images(num_pokemon=args.num_pokemon)
        print("[OK] Download concluido!")
    
    # Se não foi especificado --download apenas, ou se foi especificado --train, treina
    if args.train or not args.download:
        print("\n[INFO] Iniciando treinamento...")
        train_model(
            num_epochs=args.epochs,
            batch_size=args.batch_size,
            num_pokemon=args.num_pokemon
        )
    elif args.download and not args.train:
        print("\n[INFO] Para treinar o modelo, execute:")
        print(f"   python scripts/train_model.py --train --epochs {args.epochs} --batch-size {args.batch_size}")

