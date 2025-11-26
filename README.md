# ⚡ Pokédex com Inteligência Artificial

Sistema completo de Pokédex que combina **Visão Computacional**, **Processamento de Linguagem Natural** e **Busca Inteligente** para criar a experiência mais completa de exploração de Pokémon.

## 🚀 Funcionalidades

### 🔍 Busca Inteligente
- Busque Pokémon por nome ou ID
- Sistema de cache automático para respostas rápidas
- Informações completas sobre cada Pokémon (tipos, stats, habilidades, evoluções, etc.)
- Busca rápida com botões para Pokémon populares

### 📸 Reconhecimento de Imagem (96%+ de Acurácia!)
- Envie uma foto de um Pokémon
- Identificação automática usando **MobileNetV2 (PyTorch) treinado**
- **Modelo treinado especificamente para Pokémon com 96.15% de acurácia**
- Deep learning com transfer learning e fine-tuning
- Múltiplas predições com níveis de confiança ajustáveis
- Interface intuitiva com sliders e barras de progresso
- Compatível com Python 3.13

### 💬 Chatbot Interativo
- Faça perguntas sobre Pokémon em linguagem natural
- **RAG (Retrieval-Augmented Generation)** com Ollama + Llama 3.2:3b
- **Busca semântica** em base de conhecimento de 151 Pokémon
- **ChromaDB** para vector store e **Sentence Transformers** para embeddings
- Respostas contextualizadas e precisas baseadas em dados reais
- Histórico de conversação
- Exemplos de perguntas prontas

## 🛠️ Tecnologias

| Categoria | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Linguagem | **Python 3.13** | Suporte total a IA, PLN e visão |
| Arquitetura | **Monolítica** | Simples e ideal para MVP |
| Interface | **Streamlit** | Sistema de páginas múltiplas nativo |
| Visão Computacional | **MobileNetV2 (PyTorch)** | Modelo treinado com 96%+ acurácia |
| Chatbot / PLN | **RAG com Ollama (Llama 3.2:3b)** | Busca semântica + LLM para respostas contextualizadas |
| Vector Store | **ChromaDB** | Armazenamento de embeddings para RAG |
| Embeddings | **Sentence Transformers** | Geração de embeddings semânticos |
| Base de Dados | **PokéAPI** | API atualizada e aberta |
| Banco de Dados | **SQLite Local** | Cache inteligente com TTL |
| Hospedagem | **Streamlit Cloud / Localhost** | Gratuita e prática |
| Segurança | **LGPD + anonimização local** | Ético e seguro |

## 📋 Pré-requisitos

### Básico
- **Python 3.13** (recomendado) ou Python 3.8+
- pip (gerenciador de pacotes Python)
- Git (opcional)

### Para Chatbot RAG (Opcional)
- **Ollama** instalado ([Download](https://ollama.ai))
- **Modelo Llama 3.2:3b** baixado (`ollama pull llama3.2:3b`)
- ~2GB de espaço para o modelo
- 8GB+ RAM (16GB recomendado)

## 🔧 Instalação

1. **Clone o repositório** (ou baixe os arquivos):
```bash
git clone <repository-url>
cd dex_PI
```

2. **Crie um ambiente virtual** (recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente** (opcional):
```bash
# O arquivo .env será criado automaticamente pelo setup.py
# Você pode editá-lo para personalizar configurações
```

5. **Inicialize o projeto**:
```bash
python setup.py
```

## 🚀 Como Usar

### Executando a Aplicação

#### Opção 1: Execução Básica (Sem RAG/Chatbot IA)

```bash
# 1. Ative o ambiente virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# 2. Execute o Streamlit
streamlit run streamlit_app.py
```

A aplicação estará disponível em `http://localhost:8501`

#### Opção 2: Execução Completa (Com RAG/Chatbot IA)

**Pré-requisitos adicionais:**
- Ollama instalado ([Download](https://ollama.ai))
- Modelo Llama 3.2:3b baixado

**Passo a passo:**

```powershell
# Terminal 1 - Ollama (deixar rodando)
ollama serve

# Terminal 2 - Streamlit
cd <caminho-do-projeto>
.\venv\Scripts\Activate.ps1

# Primeira vez: Indexar base de conhecimento (2-3 min)
python scripts/index_pokemon_auto.py

# Executar aplicação
streamlit run streamlit_app.py
```

**Verificar instalação do Ollama:**
```powershell
# Verificar versão
ollama --version

# Listar modelos instalados
ollama list

# Baixar modelo (se necessário)
ollama pull llama3.2:3b
```

**Navegação:**
- A aplicação usa o sistema de páginas múltiplas nativo do Streamlit
- Navegue entre as páginas usando o menu lateral
- Cada página é um arquivo separado em `pages/`

### Recursos Necessários

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| RAM | 8GB | 16GB |
| Armazenamento | 5GB | 10GB |
| Python | 3.8+ | 3.13 |

**Portas utilizadas:**
- Streamlit: `8501`
- Ollama: `11434`

**Armazenamento:**
- Modelo Llama 3.2:3b: ~2GB
- Vector Store (ChromaDB): ~50MB
- Cache SQLite: ~10MB

### Funcionalidades Detalhadas

#### 🔍 Busca de Pokémon
- Digite o nome ou ID do Pokémon na barra de busca
- Use botões de busca rápida para Pokémon populares
- Visualize informações completas: tipos, stats, habilidades, altura, peso, evoluções
- Estatísticas do cache disponíveis

#### 📸 Reconhecimento de Imagem
- Faça upload de uma imagem de Pokémon
- Ajuste a **confiança mínima** e **número de predições** com os sliders
- O sistema identifica automaticamente usando o modelo treinado
- Receba múltiplas predições ordenadas por confiança
- Visualize detalhes completos dos Pokémon identificados
- Avisos automáticos quando a confiança é baixa

**Modelo Treinado:**
- **Acurácia:** 96.15% na validação
- **Dados:** 151 Pokémon da primeira geração
- **Múltiplas sprites** por Pokémon (oficial, padrão, shiny)
- **Data augmentation** para melhor generalização

#### 💬 Chatbot
- Faça perguntas em linguagem natural
- O chatbot reconhece padrões e busca informações na PokéAPI
- Histórico de conversação mantido durante a sessão
- Exemplos de perguntas:
  - "Qual é o tipo do Pikachu?"
  - "Quais são as estatísticas do Charizard?"
  - "Quem evolui do Eevee?"
  - "Quais são as habilidades do Bulbasaur?"
  - "Me fale sobre o Mewtwo"

## 📁 Estrutura do Projeto

```
dex_PI/
├── pages/                    # Páginas do Streamlit (sistema nativo)
│   ├── 1_Home.py            # Página inicial
│   ├── 2_Buscar.py          # Busca de Pokémon
│   ├── 3_Reconhecimento.py  # Reconhecimento de imagem
│   └── 4_Chatbot.py         # Chatbot RAG com Ollama
├── src/                      # Código fonte
│   ├── api/                 # Cliente PokéAPI
│   ├── vision/              # Visão computacional
│   │   ├── model_loader.py  # Carregador de modelo
│   │   └── pokemon_classifier.py # Classificador
│   ├── chatbot/             # Chatbot simples (fallback)
│   ├── rag/                 # Sistema RAG
│   │   ├── ollama_client.py # Cliente Ollama
│   │   ├── vector_store.py  # ChromaDB vector store
│   │   ├── embeddings.py    # Gerador de embeddings
│   │   ├── pokemon_knowledge.py # Base de conhecimento
│   │   └── rag_chatbot.py   # Chatbot RAG principal
│   ├── components/          # Componentes UI
│   │   ├── pokedex_card.py  # Cards de Pokémon
│   │   ├── search_bar.py    # Barra de busca
│   │   └── pokemon_card.py  # Card de exibição
│   ├── utils/               # Utilitários
│   │   └── theme_utils.py   # Tema Pokédex
│   ├── database/            # Gerenciamento SQLite
│   └── config.py            # Configuração centralizada
├── assets/                   # Recursos visuais
│   └── css/
│       └── pokedex.css      # Tema Pokédex customizado
├── scripts/                  # Scripts utilitários
│   ├── train_model.py       # Treinamento do modelo
│   ├── index_pokemon.py     # Indexação interativa
│   └── index_pokemon_auto.py # Indexação automática
├── models/                   # Modelos treinados (gitignored)
│   └── mobilenet_pokemon/   # Modelo MobileNetV2 treinado
├── data/                     # Dados e cache (gitignored)
│   ├── pokemon_images/      # Imagens para treinamento
│   ├── pokemon_db.sqlite    # Cache SQLite
│   └── chroma_db/           # Vector store ChromaDB
├── .streamlit/              # Configuração Streamlit
│   └── config.toml          # Tema Pokédex
├── streamlit_app.py         # Ponto de entrada principal
├── requirements.txt         # Dependências
├── setup.py                 # Script de inicialização
└── README.md                # Este arquivo
```

## 🧪 Treinamento do Modelo de Visão

O modelo MobileNetV2 foi treinado especificamente para Pokémon e está pronto para uso. Se quiser retreinar ou melhorar o modelo:

### Opção 1: Usar o Script Automático (Recomendado)

```bash
# 1. Baixa imagens da PokéAPI automaticamente
python scripts/train_model.py --download --num-pokemon 151

# 2. Treina o modelo (pode demorar alguns minutos)
python scripts/train_model.py --train --epochs 20 --batch-size 16
```

O script irá:
- Baixar múltiplas sprites por Pokémon (oficial, padrão, shiny)
- Aplicar data augmentation durante o treinamento
- Treinar com fine-tuning do MobileNetV2
- Salvar o melhor modelo automaticamente

### Opção 2: Usar Dados Próprios

1. Organize imagens de Pokémon em pastas por ID:
```
data/pokemon_images/
├── 1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── official.png
├── 2/
│   └── ...
└── 151/
```

2. Execute o treinamento:
```bash
python scripts/train_model.py --train --epochs 20 --batch-size 16
```

**Parâmetros de Treinamento:**
- `--epochs`: Número de épocas (padrão: 10, recomendado: 20-30)
- `--batch-size`: Tamanho do batch (padrão: 32, ajuste conforme memória)
- `--num-pokemon`: Número de Pokémon (padrão: 151)

**Resultado Esperado:**
- Modelo salvo em: `models/mobilenet_pokemon/model.pth`

## 📊 Performance do Modelo

O modelo atual foi treinado com:
- **151 Pokémon** da primeira geração
- **Múltiplas sprites** por Pokémon (oficial, padrão, shiny)
- **Data augmentation** agressivo (rotação, brightness, contrast, etc.)
- **Fine-tuning** das últimas 10 camadas do MobileNetV2

**Resultados:**
- **Acurácia de Treino:** 99.59%
- **Acurácia de Validação:** 96.15%
- **Loss Final:** 0.37 (validação)

## 🔒 Segurança e Privacidade

- **LGPD Compliant**: Dados armazenados localmente
- **Sem coleta de dados pessoais**: Sistema não coleta informações pessoais
- **Cache local**: Dados em SQLite local, não enviados para servidores externos
- **Anonimização**: Consultas são anonimizadas automaticamente
- **Timeout em requisições**: Proteção contra travamentos

## 📝 Licença

Este projeto é open source e está disponível para uso educacional e pessoal.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---
