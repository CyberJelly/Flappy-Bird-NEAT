import pygame, time, random, os, neat
from pygame.locals import *
from bird import Bird
from pipe import Pipe
pygame.init()#initialize pygame
clock = pygame.time.Clock()#used for limiting FPS
screen = pygame.display.set_mode((500, 800))#open window
myfont=pygame.font.Font("font.ttf",128)#score font
small=pygame.font.SysFont("freesansbold",40)#generation font
generation = 0
background = pygame.transform.scale(pygame.image.load("bg.png"),(600,800))#load background image and scale to window size while maintaining aspect ratio
def leave():#close window
	pygame.display.quit()
	pygame.quit()
	quit()

def display():
	screen.blit(background,(0,0))#background
	for bird in birds:#blit all birds
		screen.blit(bird.sprite,bird.position)
	for i in range(len(pipes)):#blit all pipes
		for j in range(2):
			screen.blit(pipes[i][j].sprite,pipes[i][j].position)
	#render score and shadow
	mytext = myfont.render(str(score),False,(255,255,255))
	shadow = myfont.render(str(score),False,(0,0,0))
	#blit score and shadow
	screen.blit(shadow,(245,5))
	screen.blit(mytext,(240,0))
	#render generation and shadow
	mytext = small.render("Generation = "+str(generation),False,(255,255,255))
	shadow = small.render("Generation = "+str(generation),False,(0,0,0))
	#blit generation and shadow
	screen.blit(shadow,(13,33))
	screen.blit(mytext,(10,30))
	#refresh screen
	pygame.display.flip()

def main(genomes,config):
	nets = []
	ge = []
	global generation
	generation+=1#increment generation for use in display
	global birds
	birds = []
	for _,g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g,config)#create NN according to config file
		nets.append(net)#add NN to array of all NNs for all birds
		birds.append(Bird([74,100]))
		g.fitness = 0
		ge.append(g)

	global pipes
	pipes = []
	pipeTimer = 0
	pipeDelay = 2.5 #frequency of pipe spawning
	global score
	score = 0 
	while True:#game loop
		clock.tick(60)#limit to 60 FPS
		display()#function to render all sprites to screen
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#quit
				leave()
		#spawn a new pipe at random y position
		if pipeTimer+pipeDelay<time.time():
			offset = random.randint(-100,350)#generate random integer between -100 and 350
			pipes.append((Pipe([500,offset-390],True),Pipe([500,offset+390],False)))
			pipeTimer = time.time()#reset timer

		pipe_ind = 0
		if len(birds) > 0:
			if len(pipes) > 1 and birds[0].position[0] > pipes[0][0].position[0] + pipes[0][0].dimensions[0]:
				pipe_ind = 1
		else:
			#if all birds are dead then exit game loop and begin next generation
			break
		for x, bird in enumerate(birds):
			ge[x].fitness+=0.05
			#increase fitness for every frame they are alive
			output = nets[x].activate((bird.position[1],abs(bird.position[1] -pipes[pipe_ind][0].position[1]),abs(bird.position[1] -pipes[pipe_ind][1].position[1])))
			#if the output from the NN is greater than 0.5 then flap
			#the value used for this is somewhat arbitrary but basically represents the confidence threshold of which must be met to flap
			#however this value must be between -1 and 1 because we are using the tanH activation function for our output which only outputs between -1 and 1
			if output[0]>0.5:
				bird.flap()

		for i in range(len(pipes)):
			#the boolean scored is used here so we only count one bird per pipe, if we remove this then scoring will be inconsistent
			scored = False
			for bird in birds:
				if bird.position[0]==pipes[i][0].position[0]:#if the bird is exactly in the centre of the pipe
					if not scored:
						score+=1
						scored = True #stop another point being counted this frame
					for g in ge:
						g.fitness+=5#reward AI if it correctly passes through a pipe
			for j in range(2):
				pipes[i][j].position[0]-=2 #move pipes
				#set new rect for pipes
				pipes[i][j].rect = pipes[i][j].sprite.get_rect(center =(pipes[i][j].position[0]+pipes[i][j].dimensions[0]/2,pipes[i][j].position[1]+pipes[i][j].dimensions[1]/2))
				for x, bird in enumerate(birds):
					if pygame.Rect.colliderect(bird.rect,pipes[i][j].rect):
						#reduce fitness if bird collides with pipe
						ge[x].fitness-=5
						#pop is used in place of remove here as we are dealing with list indexes
						#alternatively, I think del could also be used
						birds.pop(x)
						nets.pop(x)
						ge.pop(x)
		#delete pipes that are off screen to the left
		if pipes[0][0].position[0]-pipes[0][0].dimensions[0]<-200:
			pipes.pop(0)
		for x, bird in enumerate(birds):#enumerate is used because we need the index of the item, and it is more efficient than using index() every time
			#increase acceleration by 0.5 every frame to simulate gravity
			bird.fall_speed+=0.5
			#move bird according to acceleration
			bird.position[1]+=bird.fall_speed
			#limit bird acceleration to 10 pixels/frame^2
			if bird.fall_speed>10:
				bird.fall_speed =10
			bird.rect = bird.sprite_root.get_rect(center =(bird.position[0]+bird.dimensions[0]/2,bird.position[1]+bird.dimensions[1]/2+10))#get rect of bird
			bird.sprite = pygame.transform.rotate(bird.sprite_root, bird.fall_speed*-2.5)#rotate bird sprite according to acceleration
			if bird.position[1]+bird.dimensions[1]>800 or bird.position[1]<-100:
				#reduce fitness if bird hits ground or flies too high
				ge[x].fitness -=5
				#pop is used in place of remove here as we are dealing with list indexes
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)

def run(config_path):#Setup for NEAT
	config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,#Parameters we set in config file
								neat.DefaultSpeciesSet, neat.DefaultStagnation,
								config_path)

	p = neat.Population(config)#Set population to what was specified in config
	#Output results of each generation to terminal
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	#Run main() as fitness function with generation
	winner = p.run(main,100)#100 is max generations before simulation ends
if __name__ == "__main__":
	#Load config file and pass it into run()
	local_dir = os.path.dirname(__file__)#path to current directory
	config_path = os.path.join(local_dir,"config-feedforward.txt")
	run(config_path)


