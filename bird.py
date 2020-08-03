import pygame
class Bird:
	def __init__(self,position,dimensions = (70,50)):
		self.position = position
		self.fall_speed = 0
		self.sprite = pygame.transform.scale(pygame.image.load("bird sprite.png"),dimensions)
		self.sprite_root = pygame.transform.scale(pygame.image.load("bird sprite.png"),dimensions)
		self.rect = self.sprite.get_rect(center =(position[0]+dimensions[0]/2,position[1]+dimensions[1]/2))
		self.dimensions = dimensions
	def flap(self):
		self.fall_speed= -10