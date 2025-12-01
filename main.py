from ultralytics import YOLO

def main():
    # 1. Carregar o modelo (usaremos o Nano v11, que é leve e rápido)
    print("Carregando modelo YOLOv11n...")
    model = YOLO("yolo11n.pt") 

    # 2. Treinar o modelo
    # epochs=30: Número de passadas 
    # imgsz=640: Tamanho padrão da imagem
    # plots=True: Garante que ele gere a Matriz de Confusão no final
    print("Iniciando treinamento...")
    results = model.train(data="data.yaml", epochs=30, imgsz=640, plots=True)

    # 3. Validar no conjunto de Teste a
    print("Avaliando no conjunto de teste...")
    metrics = model.val(split='test')
    
    print(f"Treinamento concluído. Resultados salvos na pasta 'runs/'")

if __name__ == '__main__':
    # Necessário para rodar no Windows sem erro de multiprocessamento
    main()