import pygame
import time
import random

#from agent import Agent

#initailize
pygame.init()

#dimenstions of the window
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

FPS = 20

font = pygame.font.SysFont("ubuntu", 25)
largefont = pygame.font.SysFont(None, 40)

icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)


def draw_snake(snakelist, block_size):
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
	textRect.center = (DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2)+y_displace
	gameDisplay.blit(textSurf, textRect)

#Defining colors (rgb values)
BACKGROUND_COLOR = (178, 217, 4)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)


#set up the display
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("PyPyper")

BLOCK_SIZE = 10

clock = pygame.time.Clock()

def initialize_random_position(display_width, display_height, block_size):
	x = round(random.randrange(0, display_width - block_size)/float(block_size))*block_size
	y = round(random.randrange(0, display_height - block_size)/float(block_size))*block_size
	print(x, y)
	return x, y

# Directions
ALLOWED_DIRS = ["LEFT", "RIGHT", "UP", "DOWN"]


class Environment(object):
	def __init__(self,
		         display_width,
		         display_height,
		         block_size,
		         valid_directions):

		self.world_width = display_width
		self.world_height = display_height
		self.block_size = block_size
		self.lead_x = display_width/2
		self.lead_y = display_height/2
		self.lead_x_change = 0
		self.lead_y_change = 0
		self.valid_actions = valid_directions

		self.appleX, self.appleY = initialize_random_position(self.world_width,
			                                                  self.world_height,
			                                                  self.block_size)

	def act(self, action):
		'''
		Given an action, return the reward.
		'''
		reward = -1
		is_boundary = self.is_wall_nearby()

		if is_boundary[action]:
			reward = -5
		else:
			self.move(action)
			if self.is_goal_state(self.lead_x, self.lead_y):
				reward = 5
				self.new_apple()
		return reward

	def move(self, direction):
		x_change = 0
		y_change = 0
		
		if direction in ALLOWED_DIRS:
			if direction == "LEFT":
				x_change = -self.block_size
				y_change = 0
			elif direction == "RIGHT":
				x_change = self.block_size
				y_change = 0
			elif direction == "UP":
				x_change = 0
				y_change = -self.block_size
			elif direction == "DOWN":
				x_change = 0
				y_change = self.block_size
		else:
			print("Invalid direction.")

		self.lead_x += x_change
		self.lead_y += y_change

	def is_wall_nearby(self):
		left, right, up, down = False, False, False, False
		if self.lead_x - self.block_size < 0:
			left = True
		if self.lead_x + self.block_size > self.world_width:
			right = True
		if self.lead_y - self.block_size < 0:
			up = True
		if self.lead_y + self.block_size > self.world_height:
			down = True

		return {
			"LEFT":left,
			"RIGHT":right,
			"UP":up,
			"DOWN":down
		}

	def get_state(self):

		head_position = self.get_head_position()
		wall_info = tuple(self.is_wall_nearby().values())
		
		# concatenating the tuples
		return head_position + wall_info
		
	def get_next_goal(self):
		return (self.appleX, self.appleY)

	def is_goal_state(self, x, y):
		if x == self.appleX and y == self.appleY:
			return True
		return False

	def get_head_position(self):
		return self.lead_x, self.lead_y

	def get_appple_position(self):
		return self.appleX, self.appleY

	def new_apple(self):
		self.appleX, self.appleY = initialize_random_position(self.world_width, self.world_width, self.block_size)


def gameloop():	
	# Initialize the environment	
	env = Environment(DISPLAY_WIDTH,
		              DISPLAY_HEIGHT,
		              BLOCK_SIZE,
		              ALLOWED_DIRS)

	#agent = Agent(initial_state, ALLOWED_DIRS, initial_goal)

	gameExit = False
	gameOver = False

	snakelist = []
	snakeLength = 1

	direction = ''
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
					direction = 'LEFT'
				elif event.key == pygame.K_RIGHT:
					direction = 'RIGHT'
				elif event.key == pygame.K_UP:
					direction = 'UP'
				elif event.key == pygame.K_DOWN:
					direction = 'DOWN'


		
		
		# Draw apple and background
		gameDisplay.fill(BACKGROUND_COLOR)
		apple = env.get_appple_position()

		if direction:
			
			reward = env.act(direction)
			print(reward)
			
			# Head of the snake
			snake_head = env.get_head_position()
			snakelist.append(snake_head)
			# check if the snake hit the wall
			if reward < -1:
				gameOver = True
			
			if len(snakelist) > snakeLength:
				del(snakelist[0])

			#when snake runs into itself
			if snake_head in snakelist[:-1] and snakeLength>1:
				print("snake ran over itself")
				gameOver = True

			if reward > 0:
				snakeLength += 1

			pygame.draw.rect(gameDisplay, red, [apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE])
			draw_snake(snakelist, BLOCK_SIZE)
			score(snakeLength-1)

		pygame.display.update()

			# if lead_x == appleX and lead_y==appleY:
			# 	print("Eat! you stupid!")
			# 	appleX, appleY = initialize_random_position(display_width, display_height, block_size)

			# when the snake eats the apple
			
		
		clock.tick(FPS)

	#exit
	pygame.quit()
	quit()




	# 	#lead_x, lead_y = random_move(lead_x, lead_y, block_size, direction)

	# 	# Defining the boundaries
	# 	if lead_x>=display_width or lead_x<0 or lead_y>=display_height or lead_y<0:
	# 			gameOver = True

	# 	snake_head = (lead_x, lead_y)
	# 	snakelist.append(snake_head)

	# 	gameDisplay.fill(BACKGROUND_COLOR)
		
	# 	pygame.draw.rect(gameDisplay, red, [appleX, appleY, block_size, block_size])
		
	# 	if len(snakelist) > snakeLength:
	# 		del(snakelist[0])

	# 	#when snake runs into itself
	# 	if snake_head in snakelist[:-1]:
	# 		gameOver = True
	# 	snake(snakelist, block_size)

	# 	score(snakeLength-1)

	# 	pygame.display.update()

	# 	if lead_x == appleX and lead_y==appleY:
	# 		print("Eat! you stupid!")
	# 		appleX, appleY = initialize_random_position(display_width, display_height, block_size)
	# 		snakeLength += 1
	# 	clock.tick(FPS) 

	# #exit
	# pygame.quit()
	# quit()

gameloop()