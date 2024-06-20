from csv import reader
from os import walk

import pygame
# pasta feita exclusivamente para auxilio na definição dos graficos do jogo em relação a cenário

def importar_layout(path):
    mapa = []
    # le o arquivo em csv do mapa e mostra suas especifidades pro codigo
    with open(path) as mapa_fase:
        layout = reader(mapa_fase,delimiter = ",")
        for linha in layout:
            mapa.append(list(linha))
        return mapa

def importar_pastas(path):
    listaD_superficies = []
    # identifica as pastas do arquivo e mostra em string o seu diretório
    for _,__,arquivo_img in walk(path):
        for image in arquivo_img:
            full_path = path + "/" + image
            superficie_image = pygame.image.load((full_path)).convert_alpha()
            listaD_superficies.append(superficie_image)
    return listaD_superficies


