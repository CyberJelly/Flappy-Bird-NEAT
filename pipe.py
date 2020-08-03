import pygame
class Pipe:
	def __init__(self,position, down,dimensions = (100,575)):

		self.position = position
		if down:
			self.sprite = pygame.transform.scale(pygame.image.load("pipe down sprite.png"),dimensions)
		else:
			self.sprite = pygame.transform.scale(pygame.image.load("pipe up sprite.png"),dimensions)
		self.rect = self.sprite.get_rect(center =(position[0]+dimensions[0]/2,position[1]+dimensions[1]/2))
		self.dimensions = dimensions
