import os
import shutil
import random

# --- CONFIGURAÇÕES ---
caminho_origem = "dataset_completo/dataset" 
caminho_destino = "datasets/placas_m2" 

# Lista de Classes (Necessária para ler o .txt e descobrir o texto da placa)
CLASSES = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 'Y', 'Z'
]

# Proporção da divisão
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2

def criar_pastas():
    if os.path.exists(caminho_destino):
        shutil.rmtree(caminho_destino)
        
    for split in ['train', 'val', 'test']:
        for tipo in ['images', 'labels']:
            os.makedirs(f"{caminho_destino}/{split}/{tipo}", exist_ok=True)

def ler_placa_do_txt(caminho_txt):
    # Lê o arquivo .txt e retorna o texto da placa (ex: JOG3324)
    if not os.path.exists(caminho_txt):
        return None
    
    with open(caminho_txt, 'r') as f:
        linhas = f.readlines()
    
    if not linhas: return None

    caracteres = []
    for linha in linhas:
        partes = linha.strip().split()
        if len(partes) >= 2:
            classe_id = int(partes[0])
            pos_x = float(partes[1]) # Posição horizontal
            
            if 0 <= classe_id < len(CLASSES):
                caracteres.append((pos_x, CLASSES[classe_id]))
    
    # Ordena da esquerda para direita para formar a palavra certa
    caracteres.sort(key=lambda x: x[0])
    return "".join([c[1] for c in caracteres])

def separar_dados():
    print("Mapeando arquivos e removendo placas repetidas...")
    
    arquivos_brutos = [f for f in os.listdir(caminho_origem) if f.endswith('.png')]
    random.seed(42)
    random.shuffle(arquivos_brutos) # Embaralha antes de escolher
    
    arquivos_unicos = []
    placas_vistas = set() # Memória das placas que já vimos
    
    duplicatas = 0
    
    # --- FILTRO INTELIGENTE ---
    for arquivo_img in arquivos_brutos:
        nome_base = os.path.splitext(arquivo_img)[0]
        arquivo_txt = f"{nome_base}.txt"
        caminho_txt_completo = os.path.join(caminho_origem, arquivo_txt)
        
        texto_placa = ler_placa_do_txt(caminho_txt_completo)
        
        if texto_placa:
            if texto_placa in placas_vistas:
                duplicatas += 1
                # Ignora esta imagem pois já temos esse carro
            else:
                placas_vistas.add(texto_placa)
                arquivos_unicos.append(arquivo_img)
    
    print(f"--- Relatório ---")
    print(f"Total analisado: {len(arquivos_brutos)}")
    print(f"Placas REPETIDAS ignoradas: {duplicatas}")
    print(f"Placas ÚNICAS disponíveis: {len(arquivos_unicos)}")
    
    # --- CORTE PARA 2000 IMAGENS ---
    # Aqui garantimos que o treino será rápido
    arquivos_finais = arquivos_unicos[:2000]
    
    total = len(arquivos_finais)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)
    
    print(f"-----------------")
    print(f"Gerando dataset final com {total} imagens...")
    print(f"Treino: {train_end} | Validação: {int(total * VAL_RATIO)} | Teste: {total - val_end}")

    for i, arquivo_img in enumerate(arquivos_finais):
        if i < train_end: split = 'train'
        elif i < val_end: split = 'val'
        else: split = 'test'
            
        nome_base = os.path.splitext(arquivo_img)[0]
        arquivo_txt = f"{nome_base}.txt"
        
        src_img = os.path.join(caminho_origem, arquivo_img)
        src_txt = os.path.join(caminho_origem, arquivo_txt)
        
        dst_img = os.path.join(caminho_destino, split, 'images', arquivo_img)
        dst_txt = os.path.join(caminho_destino, split, 'labels', arquivo_txt)
        
        shutil.copy(src_img, dst_img)
        if os.path.exists(src_txt):
            shutil.copy(src_txt, dst_txt)

if __name__ == "__main__":
    print("Iniciando organização...")
    criar_pastas()
    separar_dados()
    print("Concluído! Dataset 'datasets/placas_m2' pronto e sem repetições.")