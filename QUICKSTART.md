# Guia Rápido de Início

Este guia te ajudará a começar a usar o Pokédex com IA rapidamente.

## Instalação Rápida

### 1. Clone e Entre no Diretório
```bash
git clone <repository-url>
cd dex_PI
```

### 2. Crie e Ative o Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instale Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Projeto
```bash
python setup.py
```

### 5. Execute a Aplicação
```bash
streamlit run streamlit_app.py
```

Acesse: `http://localhost:8501`

## Treinamento do Modelo (Opcional)

O modelo já vem treinado, mas se quiser retreinar:

```bash
# Baixa imagens
python scripts/train_model.py --download --num-pokemon 151

# Treina o modelo (20 épocas recomendado)
python scripts/train_model.py --train --epochs 20 --batch-size 16
```

## Uso Básico

### Buscar Pokémon
1. Acesse a página "🔍 Buscar"
2. Digite o nome ou ID do Pokémon
3. Clique em "Buscar"

### Reconhecimento de Imagem
1. Acesse a página "📸 Reconhecimento"
2. Faça upload de uma imagem de Pokémon
3. Ajuste os sliders de confiança (se necessário)
4. Clique em "Identificar Pokémon"

### Chatbot
1. Acesse a página "💬 Chatbot"
2. Digite uma pergunta sobre Pokémon
3. Exemplos:
   - "Qual é o tipo do Pikachu?"
   - "Quais são as stats do Charizard?"
   - "Fale sobre o Mewtwo"

## Problemas Comuns

### Aplicação não inicia
- Verifique se o ambiente virtual está ativado
- Execute: `pip install -r requirements.txt`
- Limpe o cache: `streamlit cache clear`

### Modelo não funciona
- O modelo precisa estar treinado
- Execute o treinamento (veja acima)
- Verifique se o arquivo existe: `models/mobilenet_pokemon/model.pth`

### Erro de importação
- Certifique-se de estar no diretório raiz do projeto
- Verifique se todas as dependências estão instaladas

## Próximos Passos

- Leia o [README.md](README.md) completo para mais detalhes
- Veja o [CHANGELOG.md](CHANGELOG.md) para mudanças recentes
- Contribua seguindo o [CONTRIBUTING.md](CONTRIBUTING.md)

