import pygame
import time
import random

from agent import Agent

#initailize
pygame.init()

#dimenstions of the window
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600
BLOCK_SIZE = 30

FPS = 1000

font = pygame.font.SysFont("ubuntu", 25)
largefont = pygame.font.SysFont(None, 40)

icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)


def draw_snake(snakelist, block_size):
	for x,y in snakelist:
		pygame.draw.rect(gameDisplay, blue, [x, y, block_size, block_size])


def display_score(score):
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


clock = pygame.time.Clock()

def initialize_random_position(display_width, display_height, block_size):
	x = random.randrange(0, display_width, step=block_size)
	y = random.randrange(0, display_height, step=block_size)
	# x = round(random.randrange(0, display_width - block_size,)/float(block_size))*block_size
	# y = round(random.randrange(0, display_height - block_size)/float(block_size))*block_size
	# print(x, y)
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

		self.highest_score_so_far = -1

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
				reward = 20
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
		if self.lead_x + self.block_size >= self.world_width:
			right = True
		if self.lead_y - self.block_size < 0:
			up = True
		if self.lead_y + self.block_size >= self.world_height:
			down = True

		return {
			"LEFT":left,
			"RIGHT":right,
			"UP":up,
			"DOWN":down
		}

	def get_state(self):

		head_position = self.get_head_position()
		apple_position = self.get_appple_position()
		# apple_quadrant = self.get_apple_quadrant()
		wall_info = tuple(self.is_wall_nearby().values())
		
		# concatenating the tuples
		return head_position + apple_position + wall_info
		
	def get_next_goal(self):
		return (self.appleX, self.appleY)

	def is_goal_state(self, x, y):
		if (x-self.block_size < self.appleX <x + self.block_size  and 
			y-self.block_size < self.appleY <y + self.block_size):
			return True
		return False

	def get_head_position(self):
		return self.lead_x, self.lead_y

	def get_appple_position(self):
		return self.appleX, self.appleY

	def new_apple(self):
		self.appleX, self.appleY = initialize_random_position(self.world_width, self.world_height, self.block_size)

	def get_apple_quadrant(self):
		appleX, appleY = self.get_appple_position()
		x, y = self.get_head_position()
		quadrant = 0

		#shift the origin
		appleX -= x
		appleY -= y

		if appleX > 0 and appleY > 0: 
			quadrant = 1
		elif appleX < 0 and appleY > 0:
			quadrant = 2
		elif appleX < 0 and appleY < 0:
			quadrant = 3
		elif appleX > 0 and appleY < 0:
			quadrant = 4
		elif appleX == 0:
			if appleY > 0:
				quadrant = random.choice([1, 2])
			if appleY < 0:
				quadrant = random.choice([3, 4])
		elif appleY == 0:
			if appleX > 0:
				quadrant = random.choice([1, 4])
			if appleX < 0:
				quadrant = random.choice([2, 3])
		return quadrant

	def set_high_score(self, val):
		self.highest_score_so_far = val

	def high_score(self):
		return self.highest_score_so_far

# Initialize the environment	
env = Environment(DISPLAY_WIDTH,
	              DISPLAY_HEIGHT,
	              BLOCK_SIZE,
	              ALLOWED_DIRS)

agent = Agent(env)

gameExit = False
gameOver = False

snakelist = []
snakeLength = 1

direction = ''

while True:
	
	# for event in pygame.event.get():
	# 	if event.type == pygame.QUIT:
	# 		gameExit = True
	# 		gameOver = False
	# 	if event.type == pygame.KEYDOWN:
	# 		if event.key == pygame.K_LEFT:
	# 			direction = 'LEFT'
	# 		elif event.key == pygame.K_RIGHT:
	# 			direction = 'RIGHT'
	# 		elif event.key == pygame.K_UP:
	# 			direction = 'UP'
	# 		elif event.key == pygame.K_DOWN:
	# 			direction = 'DOWN'

	direction = agent.get_action()
	
	# Draw apple and background
	gameDisplay.fill(BACKGROUND_COLOR)
	apple = env.get_appple_position()

	if direction:
		
		reward = env.act(direction)

		agent.update(direction, reward)

		# Head of the snake
		snake_head = env.get_head_position()
		snakelist.append(snake_head)
		score = snakeLength-1

		# check if the snake hit the wall
		if reward < -1:
			gameOver = True
			if score > env.high_score():
				print("score:",score, env.high_score())
				env.set_high_score(score)
				snakelist = []
				snakeLength = 1
		
		if len(snakelist) > snakeLength:
			del(snakelist[0])

		#when snake runs into itself
		# if snake_head in snakelist[:-1] and snakeLength>1:
		# 	print("snake ran over itself",snakeLength-1)
		# 	gameOver = True

		if reward > 0:
			snakeLength += 1

		pygame.draw.rect(gameDisplay, red, [apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE])
		draw_snake(snakelist, BLOCK_SIZE)
		display_score(snakeLength-1)

	pygame.display.update()
	clock.tick(FPS)


