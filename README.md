# Detecção de Caracteres em Placas Veiculares (YOLOv11)

Projeto desenvolvido para a disciplina de Visão Computacional (Trabalho M3).
O objetivo é treinar uma rede neural YOLOv11 para identificar e reconhecer individualmente caracteres (letras e números) em placas de carros (padrão Mercosul e Cinza).

## Tecnologias Utilizadas

- **Python 3.11**
- **Ultralytics YOLOv11** (Modelo Nano)
- **OpenCV** (Processamento de imagem)

## Estrutura do Projeto

- `dataset_completo/`: Arquivos originais brutos (não versionados).
- `datasets/`: Dataset limpo e organizado automaticamente para o YOLO (train/val/test).
- `runs/`: Resultados do treinamento (gráficos, métricas e pesos `best.pt`).
- `main.py`: Script principal para treinamento e validação do modelo.
- `preparar_data.py`: Script que lê os rótulos, remove duplicatas (mesmo veículo) e organiza as pastas.
- `verificar_duplicatas.py`: Script de verificação visual das duplicatas do dataset.

## Como Executar

**1. Instale as dependências:**

```bash
pip install ultralytics
```

## Guia de Execução Passo a Passo

Para garantir o funcionamento correto do treinamento e evitar erros de arquivos não encontrados ou vazamento de dados (data leakage), siga rigorosamente a ordem abaixo.

### 1. Preparação dos Dados (Obrigatório)

Execute este script primeiro. Ele é responsável por ler o dataset bruto, interpretar os arquivos .txt para identificar o conteúdo da placa (ex: "ABC1234"), remover duplicatas (mesmo veículo em fotos diferentes) e criar a estrutura de pastas organizada.

```bash
python preparar_data.py
```
