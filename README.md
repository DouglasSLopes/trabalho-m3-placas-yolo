# Detecção de Caracteres em Placas Veiculares (YOLOv11)

Projeto desenvolvido para a disciplina de Visão Computacional (Trabalho M3).
O objetivo é treinar uma rede neural **YOLOv11** para identificar e reconhecer individualmente caracteres (letras e números) em placas de carros.

## Tecnologias Utilizadas

- **Python 3.11**
- **Ultralytics YOLOv11** (Modelo Nano)
- **OpenCV** (Processamento de imagem)

## Estrutura do Projeto

- `dataset_completo/`: Arquivos originais (ignorados no git).
- `datasets/`: Estrutura organizada automaticamente para o YOLO (train/val/test).
- `runs/`: Resultados do treinamento (gráficos e pesos).
- `main.py`: Script principal de treino e avaliação.
- `preparar_data.py`: Script de organização e limpeza do dataset.

## Como Executar

1. **Instale as dependências:**
   ```bash
   pip install ultralytics
   ```
2. **Depois escreva o comando no Terminal:**

   ```bash
   python preparar_data.py
   ```

3. **Excecute o comando:**
   ```bash
   python main.py
   ```

### Configuração do Treino Realizada

- Imagens: 2.000 amostras (selecionadas aleatoriamente).

- Épocas: 30

- Modelo: YOLOv11n (Nano)
