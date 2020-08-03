import pygame, time, random
from pygame.locals import *
from bird import Bird
from pipe import Pipe
pygame.init()
clock = pygame.time.Clock()
bird = Bird((0,0))
pipes = []
myfont=pygame.font.Font("font.ttf",128)
background = pygame.transform.scale(pygame.image.load("bg.png"),(600,800))
def leave():#close window
	pygame.display.quit()
	pygame.quit()
	quit()
def display():
	screen.blit(background,(0,0))
	#pygame.draw.rect(screen,(255,0,0),bird.rect)
	screen.blit(bird.sprite,bird.position)

	for i in range(len(pipes)):
		for j in range(2):
			screen.blit(pipes[i][j].sprite,pipes[i][j].position)
	mytext = myfont.render(str(score),False,(255,255,255))
	shadow = myfont.render(str(score),False,(0,0,0))
	screen.blit(shadow,(245,5))
	screen.blit(mytext,(240,0))
	pygame.display.flip()

def main():
	bird.position = [74,100]
	pipeTimer = 0
	pipeDelay = 2.5
	fall_speed = 0
	global pipes
	pipes = []
	global score
	score = 0 
	while True:
		clock.tick(60)
		bird.sprite = pygame.transform.rotate(bird.sprite_root, bird.fall_speed*-2.5)

		display()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				leave()
			elif event.type == pygame.KEYDOWN:
			# Figure out if it was an arrow key. If so adjust speed
				if event.key == pygame.K_SPACE:
					bird.flap()
		if pipeTimer+pipeDelay<time.time():
			offset = random.randint(-100,350)
			pipes.append((Pipe([500,offset-390],True),Pipe([500,offset+390],False)))
			pipeTimer = time.time()
		for i in range(len(pipes)):
			if bird.position[0]==pipes[i][0].position[0]:
				score+=1
			for j in range(2):
				pipes[i][j].position[0]-=2
				pipes[i][j].rect = pipes[i][j].sprite.get_rect(center =(pipes[i][j].position[0]+pipes[i][j].dimensions[0]/2,pipes[i][j].position[1]+pipes[i][j].dimensions[1]/2))

				if pygame.Rect.colliderect(bird.rect,pipes[i][j].rect):
					display()
					return

		if len(pipes)>0:
			if pipes[0][0].position[0]-pipes[0][0].dimensions[0]<-200:
				del pipes[0]
		bird.fall_speed+=0.5
		bird.position[1]+=bird.fall_speed
		if bird.fall_speed>10:
			bird.fall_speed =10
		bird.rect = bird.sprite_root.get_rect(center =(bird.position[0]+bird.dimensions[0]/2,bird.position[1]+bird.dimensions[1]/2+10))
		if bird.position[1]+bird.dimensions[1]>800 or bird.position[1]<-100:
			return
screen = pygame.display.set_mode((500, 800))
while True:
	main()
	time.sleep(0.25)
	#pipes = []
