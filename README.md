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
- Pergunte sobre tipos, stats, evoluções e habilidades
- **Chatbot simples com pattern matching** (compatível Python 3.13)
- Histórico de conversação
- Exemplos de perguntas prontas

## 🛠️ Tecnologias

| Categoria | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Linguagem | **Python 3.13** | Suporte total a IA, PLN e visão |
| Arquitetura | **Monolítica** | Simples e ideal para MVP |
| Interface | **Streamlit** | Sistema de páginas múltiplas nativo |
| Visão Computacional | **MobileNetV2 (PyTorch)** | Modelo treinado com 96%+ acurácia |
| Chatbot / PLN | **Chatbot Simples (Pattern Matching)** | Leve, sem dependências pesadas, compatível Python 3.13 |
| Base de Dados | **PokéAPI** | API atualizada e aberta |
| Banco de Dados | **SQLite Local** | Cache inteligente com TTL |
| Hospedagem | **Streamlit Cloud / Localhost** | Gratuita e prática |
| Segurança | **LGPD + anonimização local** | Ético e seguro |

## 📋 Pré-requisitos

- **Python 3.13** (recomendado) ou Python 3.8+
- pip (gerenciador de pacotes Python)
- Git (opcional)

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

### Executando a Aplicação Streamlit

```bash
streamlit run streamlit_app.py
```

A aplicação estará disponível em `http://localhost:8501`

**Navegação:**
- A aplicação usa o sistema de páginas múltiplas nativo do Streamlit
- Navegue entre as páginas usando o menu lateral
- Cada página é um arquivo separado em `pages/`

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
│   ├── 1_🏠_Home.py         # Página inicial
│   ├── 2_🔍_Buscar.py       # Busca de Pokémon
│   ├── 3_📸_Reconhecimento.py # Reconhecimento de imagem
│   └── 4_💬_Chatbot.py      # Chatbot interativo
├── app/                      # Componentes auxiliares (legado)
│   ├── components/          # Componentes reutilizáveis
│   └── pages/               # Páginas antigas (não usadas)
├── src/                      # Código fonte
│   ├── api/                 # Cliente PokéAPI
│   ├── vision/             # Visão computacional
│   │   ├── model_loader.py  # Carregador de modelo
│   │   └── pokemon_classifier.py # Classificador
│   ├── chatbot/             # Chatbot simples (pattern matching)
│   └── database/            # Gerenciamento SQLite
├── scripts/                  # Scripts utilitários
│   └── train_model.py       # Treinamento do modelo
├── models/                   # Modelos treinados (gitignored)
│   └── mobilenet_pokemon/   # Modelo MobileNetV2 treinado
├── data/                     # Dados e cache (gitignored)
│   ├── pokemon_images/      # Imagens para treinamento
│   └── pokemon_db.sqlite    # Cache SQLite
├── rasa/                     # Configuração Rasa (opcional, para uso futuro)
├── streamlit_app.py          # Ponto de entrada principal
├── requirements.txt          # Dependências
├── setup.py                  # Script de inicialização
└── README.md                 # Este arquivo
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
- Acurácia de validação: 90%+ (com dados suficientes)
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

## 🐛 Troubleshooting

### Problema: Aplicação não inicia ou páginas ficam brancas
**Solução**: 
- Certifique-se de usar Python 3.13 ou 3.8+
- Instale todas as dependências: `pip install -r requirements.txt`
- Limpe o cache do Streamlit: `streamlit cache clear`
- Reinicie o Streamlit

### Problema: Modelo de visão com baixa precisão
**Solução**: 
- O modelo base (não treinado) tem precisão baixa
- Treine o modelo: `python scripts/train_model.py --train --epochs 20`
- Use imagens similares às sprites oficiais para melhor resultado
- Ajuste o slider de "Confiança mínima" na interface

### Problema: Chatbot não entende minha pergunta
**Solução**: O chatbot usa pattern matching simples. Tente reformular usando palavras-chave como:
- "tipo do [nome]"
- "stats do [nome]" ou "estatísticas do [nome]"
- "habilidades do [nome]"
- "evoluções do [nome]" ou "quem evolui do [nome]"
- "fale sobre [nome]"

**Nota sobre Rasa:** O projeto originalmente usava Rasa, mas foi migrado para um chatbot simples compatível com Python 3.13. Se quiser usar Rasa no futuro (requer Python 3.8-3.11), os arquivos de configuração estão na pasta `rasa/`.

### Problema: Erro ao buscar Pokémon
**Solução**: 
- Verifique sua conexão com a internet (PokéAPI requer acesso web)
- O cache local ajudará em requisições subsequentes
- Timeout de 5 segundos pode ser ajustado no código

### Problema: PyTorch não instala
**Solução**: 
- PyTorch tem excelente suporte para Python 3.13
- Verifique a versão: `python --version`
- Instale diretamente: `pip install torch torchvision`
- Se persistir, verifique: https://pytorch.org/get-started/locally/

### Problema: Erro de encoding no Windows
**Solução**: 
- Alguns arquivos podem ter problemas de encoding
- O código já trata erros de encoding automaticamente
- Se necessário, salve arquivos `.env` com encoding UTF-8

### Problema: Banco de dados SQLite travado
**Solução**: 
- O código já tem timeout de 2 segundos nas conexões
- Se persistir, delete o arquivo `data/pokemon_db.sqlite` e reinicie
- O banco será recriado automaticamente

## 🎯 Melhorias Futuras

- [ ] Suporte para mais gerações de Pokémon
- [ ] Treinamento com mais imagens por Pokémon
- [ ] Melhorias no chatbot (mais padrões)
- [ ] Comparação visual entre Pokémon
- [ ] Exportação de dados em PDF/JSON
- [ ] Histórico de buscas

## 📝 Licença

Este projeto é open source e está disponível para uso educacional e pessoal.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando tecnologias de código aberto**

**Versão:** 1.0.0  
**Última atualização:** Novembro 2025
