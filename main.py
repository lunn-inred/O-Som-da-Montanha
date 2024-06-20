import pygame
import sys
from config import *
from fase import Fase
from menu_inicial import main_menu

# Jogo inspirado no video do Clear Code: Creating a Zelda style game in Python [with some Dark Souls elements] = https://youtu.be/QU1pPzEGrqw?si=HfbgoClJbrH8OLh8https://youtu.be/QU1pPzEGrqw?si=HfbgoClJbrH8OLh8
# Funcionalidade de camera no video:Cameras in Pygame = https://youtu.be/u7LPRqrzry8?si=A1851Fu_BHZhLtq5
# Funcionalidade do menu baseado no video: How to Create a Menu in Pygame = https://youtu.be/2iyx8_elcYg?si=FXBmEvpUjbR6SOS7 porem aplicado com a estrutura de menu de upgrade do Clear Code
# Assets: itch.io : Cenário: https://cainos.itch.io/pixel-art-top-down-basic ; Protagonista: https://9e0.itch.io/witches-pack ; Inimigos: https://pixel-boy.itch.io/ninja-adventure-asset-pack
# Trilha sonora: itch.io: https://void1gaming.itch.io/free-game-menu-music-pack
# Efeitos sonoros: itch.io: https://pixel-boy.itch.io/ninja-adventure-asset-pack
# Imagem do background do menu principal: Kiana Mosser: https://twitter.com/kianamosser/status/1447341626959937537

class Jogo:
    def __init__(self):
        self.image = pygame.image.load("./graficos/icon/B_witch.gif")
        # definições gerais
        pygame.init()
        self.mouse = pygame.image.load("./graficos/cursor/cursor.png")
        pygame.mouse.set_cursor(pygame.cursors.Cursor((0,0),self.mouse))
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('O Som da Montanha')
        pygame.display.set_icon(self.image)
        self.clock = pygame.time.Clock()
        self.fases = Fase()
        self.main_menu = main_menu(self.fases)
        # audios
        self.soundtrack_menu = pygame.mixer.Sound("./audio/1. Palm Tree Shade.wav")
        self.soundtrack_menu.set_volume(volume["musica"])
        self.soundtrack_menu.play(loops=-1)


    # loop principal do jogo
    def rodar(self):

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
            if self.fases.personagem.rodando:
                self.main_menu.tela()
            elif self.fases.personagem.jogando:
                self.fases.rodar()
            pygame.display.update()
            self.clock.tick(fps)
            self.tela.fill("#73741c")
            self.soundtrack_menu.set_volume(volume["musica"])

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                Jogo().rodar()
Jogo().rodar()
