import pygame
import time
import random

#initailize
pygame.init()

#dimenstions of the window
display_width = 800
display_height = 600

FPS = 30
	
font = pygame.font.SysFont("ubuntu", 25)
largefont = pygame.font.SysFont(None, 40)

icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)

def snake(snakelist, block_size):
	for x,y in snakelist:
		pygame.draw.rect(gameDisplay, blue, [x, y, block_size, block_size])

def score(score):
	text = largefont.render("Score: "+str(score), True, black)
	gameDisplay.blit(text, [10,10])

def create_text_object(text, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0):
	textSurf, textRect =  create_text_object(msg, color)
	textRect.center = (display_width/2), (display_height/2)+y_displace
	gameDisplay.blit(textSurf, textRect)

#Defining colors (rgb values)
BACKGROUND_COLOR = (178, 217, 4)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)


#set up the display
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("PyPyper")



block_size = 10

clock = pygame.time.Clock()

def initialize_random_position(display_width, display_height, block_size):
	x = round(random.randrange(0, display_width - block_size)/float(block_size))*block_size
	y = round(random.randrange(0, display_height - block_size)/float(block_size))*block_size
	print(x,y)
	return x,y

def gameloop():

	gameExit = False
	gameOver = False

	lead_x = display_width/2
	lead_y = display_height/2
	lead_x_change = 0
	lead_y_change = 0

	snakelist = []
	snakeLength = 1

	appleX, appleY = initialize_random_position(display_width, display_height, block_size)	
	
	while not gameExit:
		
		while gameOver==True:
			gameDisplay.fill(white)
			message_to_screen("Game over! Restarting...", red)
			pygame.display.update()
			time.sleep(1)
			gameloop()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
				gameOver = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					lead_y_change = block_size
					lead_x_change = 0

		# Defining the boundaries
		if lead_x>=display_width or lead_x<0 or lead_y>=display_height or lead_y<0:
				gameOver = True

		lead_x += lead_x_change
		lead_y += lead_y_change

		snake_head = (lead_x, lead_y)
		snakelist.append(snake_head)

		gameDisplay.fill(BACKGROUND_COLOR)
		
		pygame.draw.rect(gameDisplay, red, [appleX, appleY, block_size, block_size])
		
		if len(snakelist) > snakeLength:
			del(snakelist[0])
		#when snake runs into itself
		if snake_head in snakelist[:-1]:
			gameOver = True
		snake(snakelist, block_size)

		score(snakeLength-1)

		pygame.display.update()

		if lead_x == appleX and lead_y==appleY:
			print("Eat! you stupid!")
			appleX, appleY = initialize_random_position(display_width, display_height, block_size)
			snakeLength += 1
		clock.tick(FPS) 

	#exit
	pygame.quit()
	quit()

gameloop()