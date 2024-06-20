import pygame
pygame.init()
font = pygame.font.Font(None,30)

def depurar(info,y = 10, x = 10):
	mostranatela = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(mostranatela,'Black',debug_rect)
	mostranatela.blit(debug_surf,debug_rect)
