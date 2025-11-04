"""Script de inicialização do projeto Pokédex com IA."""

import os
import sys
from pathlib import Path


def create_directories():
    """Cria diretórios necessários."""
    directories = [
        'data',
        'data/pokemon_images',
        'models',
        'models/mobilenet_pokemon',
        'scripts',
        'pages'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"[OK] Diretorio criado/verificado: {directory}")


def create_env_file():
    """Cria arquivo .env se não existir."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("[OK] Arquivo .env criado a partir de .env.example")
        else:
            # Cria .env básico
            env_content = """# Configurações da PokéAPI
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
POKEAPI_CACHE_TTL=86400

# Configurações do Modelo de Visão
MODEL_PATH=models/mobilenet_pokemon
NUM_PREDICTIONS=5

# Banco de Dados
DB_PATH=data/pokemon_db.sqlite
"""
            env_file.write_text(env_content, encoding='utf-8')
            print("[OK] Arquivo .env criado com configuracoes padrao")
    else:
        print("[OK] Arquivo .env ja existe")


def init_database():
    """Inicializa o banco de dados SQLite."""
    try:
        from src.database.db_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        print("[OK] Banco de dados SQLite inicializado")
    except Exception as e:
        print(f"[AVISO] Erro ao inicializar banco de dados: {e}")


def check_dependencies():
    """Verifica se as dependências principais estão instaladas."""
    required_packages = {
        'streamlit': 'Streamlit',
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'PIL': 'Pillow',
        'requests': 'Requests',
        'dotenv': 'python-dotenv',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'tqdm': 'tqdm'
    }
    
    missing = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"[OK] {name} instalado")
        except ImportError:
            missing.append(name)
            print(f"[ERRO] {name} nao encontrado")
    
    if missing:
        print(f"\n[AVISO] Pacotes faltando: {', '.join(missing)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    return True


def check_python_version():
    """Verifica a versão do Python."""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERRO] Python 3.8 ou superior e necessario")
        return False
    
    if version.major == 3 and version.minor >= 13:
        print("[OK] Python 3.13+ - Suporte completo")
    elif version.major == 3 and version.minor >= 8:
        print("[OK] Python 3.8+ - Compativel")
    
    return True


def main():
    """Função principal de inicialização."""
    print("=" * 50)
    print("Inicializando Projeto Pokedex com IA")
    print("=" * 50)
    print()
    
    # Verifica versão do Python
    print("[1/5] Verificando versao do Python...")
    if not check_python_version():
        sys.exit(1)
    print()
    
    # Cria diretórios
    print("[2/5] Criando diretorios...")
    create_directories()
    print()
    
    # Cria arquivo .env
    print("[3/5] Configurando variaveis de ambiente...")
    create_env_file()
    print()
    
    # Inicializa banco de dados
    print("[4/5] Inicializando banco de dados...")
    try:
        init_database()
    except Exception as e:
        print(f"[AVISO] Nao foi possivel inicializar banco: {e}")
    print()
    
    # Verifica dependências
    print("[5/5] Verificando dependencias...")
    deps_ok = check_dependencies()
    print()
    
    print("=" * 50)
    if deps_ok:
        print("[OK] Inicializacao concluida!")
        print()
        print("Para executar a aplicacao:")
        print("  streamlit run streamlit_app.py")
        print()
        print("Para treinar o modelo de visao:")
        print("  python scripts/train_model.py --download --num-pokemon 151")
        print("  python scripts/train_model.py --train --epochs 20")
    else:
        print("[AVISO] Algumas dependencias estao faltando.")
        print("Execute: pip install -r requirements.txt")
    print("=" * 50)


if __name__ == "__main__":
    main()
