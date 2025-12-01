import os
import shutil
import random

# --- CONFIGURAÇÕES ---
# Caminho onde estão suas imagens e txts misturados agora
caminho_origem = "dataset_completo/dataset" 

# Caminho onde vamos criar a estrutura organizada
caminho_destino = "datasets/placas_m2" 

# Proporção da divisão
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
# O restante (0.1) vai para teste

def criar_pastas():
    # Se a pasta já existir, apaga ela para garantir que não misture dados antigos
    if os.path.exists(caminho_destino):
        shutil.rmtree(caminho_destino)
        
    for split in ['train', 'val', 'test']:
        for tipo in ['images', 'labels']:
            os.makedirs(f"{caminho_destino}/{split}/{tipo}", exist_ok=True)

def separar_dados():
    # Pega todos os arquivos .png
    arquivos = [f for f in os.listdir(caminho_origem) if f.endswith('.png')]
    
    # Embaralha para garantir aleatoriedade
    random.seed(42) 
    random.shuffle(arquivos)
    
    # --- CORREÇÃO AQUI: LIMITAR PARA 2000 IMAGENS ---
    arquivos = arquivos[:2000]
    
    # --- CORREÇÃO AQUI: CALCULAR USANDO O TOTAL (NÚMERO) ---
    total = len(arquivos)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)
    
    print(f"Total de imagens selecionadas: {total}")
    print(f"Treino: {train_end} | Validação: {int(total * VAL_RATIO)} | Teste: {total - val_end}")

    for i, arquivo_img in enumerate(arquivos):
        # Define para qual pasta vai
        if i < train_end:
            split = 'train'
        elif i < val_end:
            split = 'val'
        else:
            split = 'test'
            
        # Nomes dos arquivos
        nome_base = os.path.splitext(arquivo_img)[0]
        arquivo_txt = f"{nome_base}.txt"
        
        # Caminhos completos
        src_img = os.path.join(caminho_origem, arquivo_img)
        src_txt = os.path.join(caminho_origem, arquivo_txt)
        
        dst_img = os.path.join(caminho_destino, split, 'images', arquivo_img)
        dst_txt = os.path.join(caminho_destino, split, 'labels', arquivo_txt)
        
        # Copia os arquivos
        shutil.copy(src_img, dst_img)
        # Só copia o txt se ele existir (evita erro se faltar label)
        if os.path.exists(src_txt):
            shutil.copy(src_txt, dst_txt)

if __name__ == "__main__":
    print("Iniciando organização do dataset...")
    criar_pastas()
    separar_dados()
    print("Concluído! Pasta 'datasets/placas_m2' criada com sucesso.")