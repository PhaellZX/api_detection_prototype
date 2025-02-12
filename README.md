# YOLOv8 Object Detection API

Este projeto é uma API desenvolvida com FastAPI para detecção de objetos em imagens utilizando o modelo YOLOv8. A API permite o upload de imagens, processamento com YOLOv8 e exportação dos resultados em formato JSON compatível com Label Studio.

## Funcionalidades

- Upload de imagens para detecção de objetos.
- Processamento das imagens utilizando o modelo YOLOv8.
- Geração de anotações no formato JSON.
- Exportação de anotações separadas ou consolidadas em um único JSON.
- Exibição de imagens rotuladas.
- Limpeza do cache de imagens e anotações.

## Pré-requisitos

Antes de executar o projeto, instale os seguintes softwares:

- Python 3.8+
- Git
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)

## Instalação e Execução

Siga os passos abaixo para configurar e executar a API:

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o servidor FastAPI
```bash
python main.py
```

A API será iniciada e estará disponível em: `http://127.0.0.1:8000`

## Uso da API

### 1. Acesse a interface web
Abra no navegador: `http://127.0.0.1:8000` para acessar a página de upload de imagens.

### 2. Envio de Imagens
- Selecione imagens para upload.
- Informe as classes desejadas para detecção.
- Clique no botão para processar as imagens.

### 3. Exportação dos Resultados
A API permite exportar anotações:
- **JSONs separados:** `GET /export_separate_jsons` (gera um arquivo ZIP com todos os JSONs)
- **JSON consolidado:** `GET /export_consolidated_json` (gera um único JSON com todas as anotações)

### 4. Limpeza do Cache
Para limpar imagens e anotações processadas, acesse: `GET /clear_cache`

## Estrutura do Projeto
```
├── main.py               # Código principal da API
├── requirements.txt      # Dependências do projeto
├── templates/            # Arquivos HTML para interface web
├── static/               # Arquivos estáticos (CSS, JS, etc.)
├── temp_images/          # Pasta onde imagens são salvas temporariamente
├── temp_annotations/     # Pasta onde anotações JSON são armazenadas
└── README.md             # Documentação do projeto
```

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **YOLOv8 (Ultralytics)**: Modelo de detecção de objetos.
- **OpenCV**: Processamento de imagens.
- **Matplotlib**: Visualização das detecções.
- **Jinja2**: Renderização de templates HTML.
- **Uvicorn**: Servidor ASGI para FastAPI.

