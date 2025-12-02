import os
import shutil
import random
from collections import defaultdict

# --- CONFIGURAÇÕES ---
caminho_origem = "dataset_completo/dataset"
caminho_destino_auditoria = "placas_repetidas" # Onde será salvada as pastas organizadas

# Lista de Classes (Mesma do data.yaml para tradução correta)
CLASSES = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 'Y', 'Z'
]

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
            pos_x = float(partes[1])
            
            if 0 <= classe_id < len(CLASSES):
                caracteres.append((pos_x, CLASSES[classe_id]))
    
    # Ordena da esquerda para direita
    caracteres.sort(key=lambda x: x[0])
    return "".join([c[1] for c in caracteres])

def organizar_para_verificacao():
    # Limpa a pasta anterior se existir
    if os.path.exists(caminho_destino_auditoria):
        shutil.rmtree(caminho_destino_auditoria)
    os.makedirs(caminho_destino_auditoria, exist_ok=True)

    print(f"Lendo arquivos de: {caminho_origem}")
    arquivos_img = [f for f in os.listdir(caminho_origem) if f.endswith('.png')]
    
    # Dicionário para agrupar: chave = 'JOG3324', valor = ['img1.png', 'img2.png']
    agrupamento = defaultdict(list)
    sem_rotulo = []

    print("Agrupando imagens por conteúdo da placa...")
    for arquivo_img in arquivos_img:
        nome_base = os.path.splitext(arquivo_img)[0]
        arquivo_txt = f"{nome_base}.txt"
        caminho_txt = os.path.join(caminho_origem, arquivo_txt)
        
        texto_placa = ler_placa_do_txt(caminho_txt)
        
        if texto_placa:
            agrupamento[texto_placa].append(arquivo_img)
        else:
            sem_rotulo.append(arquivo_img)

    # --- CRIANDO AS PASTAS ---
    total_placas = len(agrupamento)
    placas_com_duplicatas = 0
    
    print(f"\nCriando pastas em '{caminho_destino_auditoria}'...")
    
    for placa, lista_arquivos in agrupamento.items():
        # Só cria pasta se tiver mais de 1 arquivo (duplicata) OU se você quiser ver todas.
        # Aqui vou criar para TODAS para você conferir tudo.
        
        if len(lista_arquivos) > 1:
            placas_com_duplicatas += 1
            
        # Cria a pasta com o nome da placa (ex: auditoria_visual/JOG3324)
        pasta_placa = os.path.join(caminho_destino_auditoria, placa)
        os.makedirs(pasta_placa, exist_ok=True)
        
        for arq in lista_arquivos:
            src_img = os.path.join(caminho_origem, arq)
            src_txt = os.path.join(caminho_origem, os.path.splitext(arq)[0] + ".txt")
            
            dst_img = os.path.join(pasta_placa, arq)
            dst_txt = os.path.join(pasta_placa, os.path.splitext(arq)[0] + ".txt")
            
            shutil.copy(src_img, dst_img)
            # Copia o txt também para conferência se quiser
            if os.path.exists(src_txt):
                shutil.copy(src_txt, dst_txt)

    # Pasta extra para erros/sem rótulo
    if sem_rotulo:
        os.makedirs(f"{caminho_destino_auditoria}/_SEM_ROTULO", exist_ok=True)
        for arq in sem_rotulo:
            shutil.copy(os.path.join(caminho_origem, arq), f"{caminho_destino_auditoria}/_SEM_ROTULO/{arq}")

    print("\n--- VERIFICADOR DE PLACAS DUPLICATAS ---")
    print(f"Total de placas únicas encontradas: {total_placas}")
    print(f"Placas que possuem duplicatas (mais de 1 foto): {placas_com_duplicatas}")
    print(f"Imagens sem rótulo/erro: {len(sem_rotulo)}")
    print(f"--------------------------------")
    print(f"Abra a pasta '{caminho_destino_auditoria}' para conferir visualmente.")

if __name__ == "__main__":
    organizar_para_verificacao()