import pygame, os
from tiles import AnimatedTile
from random import randint
from support import import_folder

# enemy_group = pygame.sprite.Group()

class Ufo(AnimatedTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,'../graphics/enemy/ufo')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(1,3)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()

class Enemy(AnimatedTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,'../graphics/enemy/run')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(1,4)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()

