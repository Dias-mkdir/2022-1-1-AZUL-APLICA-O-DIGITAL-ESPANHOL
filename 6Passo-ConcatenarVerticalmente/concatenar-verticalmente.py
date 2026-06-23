from PIL import Image
import os
import re

pasta_imagens = "sem-bordas-externas"
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

# Função segura para ordenação
def get_sort_key(nome_arquivo):
    match = re.search(r'pagina_enem_(\d+)_', nome_arquivo)

    # Se não encontrar número, joga pro final
    numero = int(match.group(1)) if match else float('inf')

    # Define o lado: esquerda primeiro (0), depois direita (1)
    lado = 0 if 'esquerda' in nome_arquivo.lower() else 1

    return (numero, lado)

# Pegar e ordenar as imagens corretamente
arquivos = [f for f in os.listdir(pasta_imagens) if f.lower().endswith('.png')]
arquivos.sort(key=get_sort_key)

# Abrir todas as imagens na ordem correta
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    try:
        img = Image.open(caminho)
        imagens.append(img)
        print(f"Adicionando: {arquivo}")
    except Exception as e:
        print(f"Erro ao abrir {arquivo}: {e}")

if not imagens:
    raise Exception("Nenhuma imagem válida foi carregada.")

# Encontrar a largura máxima
largura_max = max(img.width for img in imagens)

# Concatenar verticalmente
altura_total = sum(img.height for img in imagens)
imagem_final = Image.new('RGB', (largura_max, altura_total))

y = 0
for img in imagens:
    imagem_final.paste(img, (0, y))
    y += img.height

# Salvar
saida = os.path.join(pasta_saida, 'colunas_concatenadas_verticalmente.png')
imagem_final.save(saida)

print("Imagens concatenadas na ordem correta!")
print(f"Ordem dos arquivos: {arquivos}")
print(f"Arquivo salvo em: {saida}")