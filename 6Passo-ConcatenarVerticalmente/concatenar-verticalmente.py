import os
import re
from PIL import Image

pasta_imagens = "sem-bordas-externas"
pasta_saida = "concatenadas-79-105"
os.makedirs(pasta_saida, exist_ok=True)


def get_sort_key(nome_arquivo):
    match = re.search(r"pagina_enem_(\d+)", nome_arquivo)
    return int(match.group(1)) if match else -1


# 1. Filtra apenas arquivos .png que estão estritamente no intervalo de 60 a 105
arquivos = []
for f in os.listdir(pasta_imagens):
    if f.endswith(".png"):
        match = re.search(r"pagina_enem_(\d+)", f)
        if match:
            numero = int(match.group(1))
            if 79 <= numero <= 105:  # Define o intervalo desejado
                arquivos.append(f)

# 2. Ordena os arquivos filtrados
arquivos.sort(key=get_sort_key)

# 3. Carrega as imagens na memória
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")

# Evita erro caso a pasta esteja vazia ou nenhum arquivo combine com o filtro
if not imagens:
    print("Nenhuma imagem encontrada no intervalo de 60 a 105.")
    exit()

# 4. Calcula dimensões e cria a imagem final
largura_max = max(img.width for img in imagens)
altura_total = sum(img.height for img in imagens)
imagem_final = Image.new("RGB", (largura_max, altura_total))

# 5. Cola as imagens verticalmente
y = 0
for img in imagens:
    imagem_final.paste(img, (0, y))
    y += img.height

# 6. Salva o resultado
imagem_final.save(os.path.join(pasta_saida, "colunas_concatenadas_79-105.png"))
print("\nImagens concatenadas na ordem correta!")
print(f"Ordem dos arquivos processados: {arquivos}")
