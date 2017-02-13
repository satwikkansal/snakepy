import pygame

#initailize
pygame.init()

#Defining colors (rgb values)
BACKGROUND_COLOR = (178, 217, 4)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


#set up the display
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("PyPyper")

gameExit = False

lead_x = 300
lead_y = 300

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				lead_x -= 10
			if event.key == pygame.K_RIGHT:
				lead_x += 10
			if event.key == pygame.K_UP:
				lead_y -= 10
			if event.key == pygame.K_DOWN:
				lead_y += 10

	gameDisplay.fill(BACKGROUND_COLOR)
	#display, color, [start_x, start_y, width, height]
	#start_x, start_y => top-left corner of the object drawn
	pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, 10, 100])
	#pygame.draw.rect(gameDisplay, red, [400,300,10,10])
	gameDisplay.fill(red, [lead_x, lead_y, 10, 10])
	pygame.display.update()


#exit
pygame.quit()
quit()