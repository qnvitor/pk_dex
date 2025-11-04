# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.0.0] - Novembro 2025

### Adicionado
- Sistema de páginas múltiplas nativo do Streamlit
- Modelo MobileNetV2 treinado especificamente para Pokémon (96.15% acurácia)
- Script de treinamento automático (`scripts/train_model.py`)
- Download automático de imagens da PokéAPI para treinamento
- Interface melhorada para reconhecimento de imagem:
  - Sliders para ajustar confiança mínima e número de predições
  - Barras de progresso visuais
  - Avisos quando a confiança é baixa
  - Preview da imagem enviada
- Melhorias no pré-processamento de imagens (contraste, antialiasing)
- Sistema de cache SQLite com timeout e tratamento de erros
- Tratamento robusto de erros em todas as páginas
- Logs de debug para troubleshooting

### Modificado
- Migração de TensorFlow/Keras para PyTorch (compatibilidade Python 3.13)
- Migração de Rasa para chatbot simples com pattern matching
- Sistema de navegação: de implementação customizada para páginas múltiplas nativas
- Melhorias no tratamento de erros do DatabaseManager
- Timeout reduzido em requisições HTTP (5s)
- Estrutura do projeto: adicionada pasta `pages/` e `scripts/`

### Corrigido
- Problema de tela branca ao navegar entre páginas
- Erros de encoding no Windows (UnicodeEncodeError)
- Problemas de travamento com SQLite (timeout e tratamento de erros)
- Navegação entre páginas funcionando corretamente
- Carregamento de modelo com tratamento de erros

### Removido
- Dependências pesadas (Rasa, TensorFlow)
- Sistema de navegação customizado (substituído por páginas múltiplas)

### Notas
- O projeto agora requer Python 3.13 (ou 3.8+) para melhor compatibilidade
- O modelo treinado está disponível em `models/mobilenet_pokemon/model.pth`
- Rasa pode ser usado opcionalmente com Python 3.8-3.11 (configuração em `rasa/`)

