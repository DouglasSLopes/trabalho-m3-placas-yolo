import zipfile

arquivo_zip = 'dataset_completo.zip'

print("Descompactando o arquivo...")

# Abre o arquivo em modo de leitura e extrai todo o seu conteúdo
with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
    zip_ref.extractall('dataset_completo')

print("Descompactação concluída.")