import pygame, enemy, time
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles,change_health):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		
		# dust particles 
		self.import_dust_run_particles()
		self.import_shield_particles()
		self.import_cast_particles()
		self.import_shield_particles2()

		self.is_casting2 = False
		self.cast_start_time = 0
		self.cast_duration = 5
		self.cast_cooldown = 10
		self.cast_animation_speed = 0.2
		self.cast_frame_index = 0

		self.is_casting = False
		self.shield_start_time = 0
		self.shield_duration = 5
		self.shield_cooldown = 10
		self.shield_frame_index = 0
		self.shield_frame_index2 = 0
		self.shield_animation_speed = 0.2

		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15

		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16
		self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		self.can_cast_shield = False
		self.can_cast = False

		# health management
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

		# audio 
		self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
		self.jump_sound.set_volume(0.1)
		self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')
		self.explode_sound = pygame.mixer.Sound('../audio/effects/explode.wav')
		self.shield_sound = pygame.mixer.Sound('../audio/effects/shield.wav')
		self.shield_sound.set_volume(4)
		self.cast_sound = pygame.mixer.Sound('../audio/effects/cast.wav')
		self.cast_sound.set_volume(4)

	def import_character_assets(self):
		character_path = '../graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

	def import_shield_particles(self):
		self.shield_particles = import_folder('../graphics/character/Counter')
	
	def import_shield_particles2(self):
		self.shield_particles2 = import_folder('../graphics/character/shield')

	def import_cast_particles(self):
		self.cast_particles = import_folder('../graphics/character/cast')

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
			self.rect.bottomleft = self.collision_rect.bottomleft
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image
			self.rect.bottomright = self.collision_rect.bottomright

		if self.invincible:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)		

	def run_dust_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	def cast_animation(self):
		if self.can_cast and time.time() - self.cast_start_time < self.cast_duration:
			self.is_casting2 = True
			self.is_casting = False
			self.cast_frame_index += self.cast_animation_speed
			if self.cast_frame_index >= len(self.cast_particles):
				self.cast_frame_index = 0

			cast_particle = self.cast_particles[int(self.cast_frame_index)]
			if self.facing_right:
				pos = self.rect.topleft - pygame.math.Vector2(100,90)
				self.display_surface.blit(cast_particle,pos)
			else:
				pos = self.rect.topright - pygame.math.Vector2(50,90)
				flipped_shield_particle = pygame.transform.flip(cast_particle,True,False)
				self.display_surface.blit(flipped_shield_particle,pos)
		else:
			self.is_casting2 = False


	def shield_animation(self):
		if self.can_cast_shield and time.time() - self.shield_start_time < self.shield_duration:
			self.is_casting = True
			self.is_casting2 = False
			self.shield_frame_index += self.shield_animation_speed
			if self.shield_frame_index >= len(self.shield_particles):
				self.shield_frame_index = 0
			if self.shield_frame_index2 >= len(self.shield_particles2):
				self.shield_frame_index2 = 0

			shield_particle = self.shield_particles[int(self.shield_frame_index)]
			shield_particle2 = self.shield_particles2[int(self.shield_frame_index2)]
			if self.facing_right:
				pos = self.rect.topright - pygame.math.Vector2(97,65)
				pos2 = self.rect.topleft - pygame.math.Vector2(30,30)
				self.display_surface.blit(shield_particle2, pos2)
				self.display_surface.blit(shield_particle,pos)
			else:
				pos = self.rect.topleft - pygame.math.Vector2(3,65)
				pos2 = self.rect.topright - pygame.math.Vector2(73, 30)
				flipped_shield_particle2 = pygame.transform.flip(shield_particle2, True, False)
				flipped_shield_particle = pygame.transform.flip(shield_particle,True,False)
				self.display_surface.blit(flipped_shield_particle,pos)
				self.display_surface.blit(flipped_shield_particle2, pos2)
		else:
			self.is_casting = False

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()
			self.create_jump_particles(self.rect.midbottom)
		
		if keys[pygame.K_f]:
			self.shield()

		elif keys[pygame.K_r]:
			self.cast()

	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.collision_rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed
		self.jump_sound.play()

	def shield(self):
		current_time = time.time()
		if current_time - self.shield_start_time >= self.shield_cooldown:
			self.is_casting = True
			self.can_cast = False
			self.shield_sound.play()
			self.can_cast_shield = True
			self.shield_start_time = current_time

	def cast(self):
		current_time = time.time()
		if current_time - self.cast_start_time >= self.cast_cooldown:
			self.is_casting2 = True
			self.can_cast_shield = False
			self.cast_sound.play()
			self.can_cast = True
			self.cast_start_time = current_time
			
	def get_damage(self):
		if not self.invincible:
			self.change_health(-20)
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return 255
		else: return 0

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.run_dust_animation()
		self.shield_animation()
		self.cast_animation()
		self.invincibility_timer()
		self.wave_value()
		