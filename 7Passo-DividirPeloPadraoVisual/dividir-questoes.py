"""
Propósito: Dividir as questões do ENEM Digital por padrão de linhas divisórias.
Garante que a pergunta e suas alternativas fiquem unidas na mesma imagem.
"""

from PIL import Image
import os

def encontrar_faixa_divisoria(imagem, cor_alvo=(200, 200, 200), altura_faixa=3):
    """
    Encontra as coordenadas exatas Y de cada linha horizontal escura da prova.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    coluna_teste = int(largura * 0.1) # Analisa a coluna a 10% da largura da página
    
    y = 0
    while y < altura - altura_faixa:
        faixa_encontrada = True
        
        for dy in range(altura_faixa):
            pixel = pixels[coluna_teste, y + dy]
            
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Se encontrar fundo claro/branco, descarta
            if r > cor_alvo[0] or g > cor_alvo[1] or b > cor_alvo[2]:
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            # Registra o ponto exato da linha divisória
            posicoes_corte.append(y)
            print(f"Linha divisória de bloco detectada em y={y}")
            y += altura_faixa + 30  # Pula o bloco para evitar detecções duplicadas
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, num_inicial=7):
    """
    Recorta a imagem unindo o texto das questões às suas respectivas alternativas.
    """
    if not os.path.exists(caminho_imagem):
        print(f"Arquivo não encontrado: {caminho_imagem}. Pulando...")
        return

    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"\nProcessando: {caminho_imagem} ({largura}x{altura} px)")
    
    # Busca todas as linhas pretas/cinzas que separam os módulos de questões
    linhas_divisorias = encontrar_faixa_divisoria(imagem, cor_alvo=(180, 180, 180), altura_faixa=3)
    
    if not map:
        print("Nenhum padrão estrutural foi localizado na imagem!")
        return
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    contador_questao = num_inicial
    
    # Define a margem para cortar um pouco abaixo da linha escura (para que ela suma ou fique no topo da próxima)
    margem_corte = 5 
    
    for linha in linhas_divisorias:
        # Ponto de corte é ajustado ligeiramente abaixo da divisória para não cortar o texto do cabeçalho
        ponto_atual_corte = linha + margem_corte
        
        if ponto_atual_corte <= posicao_anterior:
            continue
            
        # Alvo do corte: vai do início do bloco até englobar o final das alternativas da questão atual
        area_corte = (0, posicao_anterior, largura, ponto_atual_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"questao_{contador_questao:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} com alternativas inclusas. ({secao.width}x{secao.height}px)")
        
        # O início da próxima questão será onde esta acabou de fechar
        posicao_anterior = ponto_atual_corte
        contador_questao += 1
    
    # Salva o bloco final restante da página (Última questão)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        nome_arquivo = f"questao_{contador_questao:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo última questão: {caminho_completo}")

if __name__ == "__main__":
    # Configuração de lote para os seus arquivos do ENEM Digital
    partes_prova = [
        {"imagem": "colunas_concatenadas_7-37.png", "saida": "questoes_parte_1", "inicio": 7},
        {"imagem": "colunas_concatenadas_38-78.png", "saida": "questoes_parte_2", "inicio": 38},
        {"imagem": "colunas_concatenadas_79-105.png", "saida": "questoes_parte_3", "inicio": 79}
    ]
    
    for parte in partes_prova:
        dividir_imagem_por_faixas(parte["imagem"], parte["saida"], parte["inicio"])
    
    print("\nProcessamento concluído com sucesso!")
