import pygame

#initailize
pygame.init()

#dimenstions of the window
display_width = 800
display_height = 600

FPS = 30

#Defining colors (rgb values)
BACKGROUND_COLOR = (178, 217, 4)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


#set up the display
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("PyPyper")

gameExit = False

lead_x = 300
lead_y = 300
lead_x_change = 0
lead_y_change = 0

block_size = 5

clock = pygame.time.Clock()

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
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
			gameExit = True

	lead_x += lead_x_change
	lead_y += lead_y_change

	gameDisplay.fill(BACKGROUND_COLOR)
	#display, color, [start_x, start_y, display_width, display_height]
	#start_x, start_y => top-left corner of the object drawn
	pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, 10, 100])
	#pygame.draw.rect(gameDisplay, red, [400,300,10,10])
	gameDisplay.fill(red, [lead_x, lead_y, 10, 10])
	pygame.display.update()

	#frames per second
	clock.tick(FPS) 


#exit
pygame.quit()
quit()