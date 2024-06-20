import pygame 
from config import * 

class Tileset(pygame.sprite.Sprite):
	def __init__(self,pos,groups,tipodeSprite,superficie = pygame.Surface((tamanhosprite,tamanhosprite))):
		super().__init__(groups)
		self.tipodeSprite = tipodeSprite
		self.image = superficie
		self.deslocamento_hitbox = deslocamento_hitbox[tipodeSprite]
		if tipodeSprite == "objetos":
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1]-tamanhosprite))
		else:
			self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,self.deslocamento_hitbox)
