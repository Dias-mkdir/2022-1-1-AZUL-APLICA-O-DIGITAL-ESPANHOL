
#Propósito: concatenar verticalmente as imagens de cada pasta vinda do passo 5
#Autor: Alexandre Nassar de Peder
#Criação: 02/10/2025
#Atualização: 03/06/2026

#OBS1: puxe a pasta "divididas-sem-bordas-do-meio" do passo 5 para essa pasta do passo 6
#OBS2: não compensa concatenar as páginas inteiras. Tenha isso em mente para o passo 7


from PIL import Image
import os
import re

pasta_imagens = "sem-bordas-externas"
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

# Função para extrair o número da página e ordenar corretamente
def get_sort_key(nome_arquivo):
    # Extrai o número da página
    numero = int(re.search(r'pagina_enem_(\d+)_', nome_arquivo).group(1))
    # Define a ordem: esquerda primeiro (0), depois direita (1)
    lado = 0 if 'esquerda' in nome_arquivo else 1
    return (numero, lado)

# Pegar e ordenar as imagens corretamente
arquivos = [f for f in os.listdir(pasta_imagens) if f.endswith('.png')]
arquivos.sort(key=get_sort_key)

# Abrir todas as imagens na ordem correta
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")  # Para verificar a ordem

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
imagem_final.save(os.path.join(pasta_saida, 'colunas_concatenadas_verticalmente.png'))
print("Imagens concatenadas na ordem correta!")
print(f"Ordem dos arquivos: {arquivos}")


#esse codigo concatena as imagens seguindo o padrao: esquerda1, em baixo esquerda2, embaixo direita1, em baixo direita 2, e assim por diante. para isso originalmente ele recebe imaagens de uma pasta, que essas imagens tem os sufixos _esquerda e _direita

#agora eu tenho imagnes que possuem esse sufixos, elas seguem o seguinte padrão: pagina_enem_1.png, pagina_enem_2.png e assim por diante

#agora altere esse codigo minimamente esse codigo, principalmente nas funções get_sort_key para concatenar as imagens que fiquem a 1, embaixo a 2, embaixo a 3 e assim por adiante
