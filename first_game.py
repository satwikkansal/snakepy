import pygame

#initailize
pygame.init()

#set up the display
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("PyPyper")

#update the display
pygame.display.update() 

gameExit = False
while not gameExit:
	for event in pygame.event.get():
		print(event)


#exit
pygame.quit()
quit()