import pygame
from math import sin

class Entidades(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.indice_frame = 0
        self.vel_animaaco = 0.15
        self.direcao = pygame.math.Vector2()

    def movimento(self, speed):
        # faz o deslocamento do personagem baseado na entrada que o jogo recebeu e sua velocidade
        if self.direcao.magnitude() != 0:
            self.direcao = self.direcao.normalize()

        self.hitbox.x += self.direcao.x * speed
        self.colisao('horizontal')
        self.hitbox.y += self.direcao.y * speed
        self.colisao('vertical')
        self.rect.center = self.hitbox.center  # faz o sprite do player seguir a hitbox

    def colisao(self, direcao):
        # mecanica de colisao, detecta a localizaçao do personagem e dos obejetos e suas interações
        if direcao == 'horizontal':
            for sprite in self.obstaculos:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direcao.x > 0:  # colisao pra direita
                        self.hitbox.right = sprite.hitbox.left
                    if self.direcao.x < 0:  # colisao pra esquerda
                        self.hitbox.left = sprite.hitbox.right

        if direcao == 'vertical':
            for sprite in self.obstaculos:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direcao.y > 0:  # colisao pra baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direcao.y < 0:  # colisao pra baixo
                        self.hitbox.top = sprite.hitbox.bottom

    def valor_flutuante(self):
        valor = sin(pygame.time.get_ticks())
        if valor >= 0:
            return 255
        else:
            return 0