import math
import random
import os
import pygame
import time
import datetime
from os import path

WIDTH = 460
HEIGHT = 600
FPS = 60

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (112, 118, 123)
YELLOW = (255, 255, 0)

#Clock is used to determine thee rate of Frames per second
clock = pygame.time.Clock()

#Directories for images and sound
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd') 

#pygame.init() will initiate the game and load all elements needed for game setup
pygame.init()
#must be added when the sounds and explosions are added
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

#Game images
background  = pygame.image.load(path.join(img_dir, "night.jpg")).convert()
background = pygame.transform.scale(background, (500, 600))
player_img = pygame.image.load(path.join(img_dir, "ship2.png")).convert_alpha()
player_bullet_img = pygame.image.load(path.join(img_dir, "rocket.png")).convert_alpha()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "bullet_enemy.png")).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (20, 20))
player_mini_img.set_colorkey(BLACK)

#load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
death_sound = pygame.mixer.Sound(path.join(snd_dir, 'Death.wav'))
enemy_shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'EnemyShoot.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
pygame_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))

#----------- Function used for drawing text on screen ------------
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

	
#----------------- draw function for lives -----------------------
def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 25* i
		img_rect.y = y + 10
		surf.blit(img, img_rect)

#this function keeps track of the score
def score(s):
	if s < 0:
		score.x = 0
	else:
		score.x += s
		return score.x
score.x = 0





#Function that keeps track of level
def level(L):
	if L < 0:
		level.x = 0
	else:
		level.x += L
		return level.x
level.x = 0






#--------------------- make enemies ------------------------------
enemy_spawn_positions = []
x_start = 20
x_end = 450
while x_start <= x_end:
	enemy_spawn_positions.append(x_start)
	x_start += 40 
rows_of_enemies = 8
enemies = []
def make_Enemies():
	y = 50
	count = 0
	for i in range(rows_of_enemies):		
		for index in enemy_spawn_positions:
			if i <= 2:
				enemy = Aliens(index, y, 1)
			elif i >= 2 and i < 5:
				enemy = Aliens(index, y, 2)
			else:
				enemy = Aliens(index, y, 3)
			enemies.append(enemy)
		y = y + 30
	for i in enemies:
		all_sprites.add(i)
		aliens.add(i)


#--------- this block is for when the game level changes ---------
def level_change():
	alive = True
	make_Enemies()
	player_bullets = pygame.sprite.Group()	
	enemy_bullets = pygame.sprite.Group()
	aliens = pygame.sprite.Group()
	start_time = int(time.time()) + 5
	player.rect.centerx = WIDTH/2
	player.rect.bottom = HEIGHT - 30
	while alive: 	
		passed_time = start_time - int(time.time())
		if passed_time == 0:
			alive = False
		screen.fill(BLACK)
		draw_text(screen, "LEVEL COMPLETED!", 40, WIDTH/2, HEIGHT/2, YELLOW)
		draw_text(screen, "Next level in " + str(passed_time) + " seconds", 40, WIDTH/2, HEIGHT/3, YELLOW)
		pygame.display.update()	
		pygame.display.flip()
	screen.fill(BLACK)
	pygame.display.update()	
	pygame.display.flip()
	game_loop()


#---- this block is for the start screen and to begin new levels ----
def show_go_screen():
	pygame.time.wait(100)
	screen.fill(BLACK)
	draw_text(screen, "SPACE INVADERS!", 62, WIDTH/2, HEIGHT/6, YELLOW)
	draw_text(screen, "Arrow keys to move, SPACE to fire weapon", 22, WIDTH/2, HEIGHT/3, WHITE)
	draw_text(screen, "Press a key to begin", 18, WIDTH/2, HEIGHT*3/4, WHITE)
	draw_text(screen, "Level: " + str(level(1)), 40, WIDTH/2, HEIGHT/2 - 40, RED)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False
				break
#---------------------------------------------------------------------

# This is the player class, 
class Player(pygame.sprite.Sprite):
	
	#This is the init fucntion of player works similar to constructor from Java 
	#the keyword self is similar to 'this' from java
	def __init__(self):
		#Player is initiated as a sprite in pygame
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (25, 25))
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width/3)
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 30
		self.speedx = 0
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()	
	
	#update method in player class is called every tick (60 times a second) and updates the player
	def update(self):
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1800:
			self.hidden = False
			self.rect.centerx = WIDTH/2
			self.rect.bottom = HEIGHT - 30
		self.speedx = 0
		if self.hidden == True:
			keystate = pygame.K_DOWN
			for self in enemy_bullets:
				self.kill()
		else:
			#Keystate is what detects when a key is pressed on the keyboard
			keystate = pygame.key.get_pressed()
			if keystate[pygame.K_LEFT]:
				self.speedx = -5
			if keystate[pygame.K_RIGHT]:
				self.speedx = 5
			if keystate[pygame.K_SPACE]:
				self.shoot()
			self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
	
	#method that is called a player pressess spacebar
	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			player_bullets.add(bullet)
			shoot_sound.play()
			
	#Hides the player when changing level or player dies	
	def hide(self):
		self.hidden = True 
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH/2, HEIGHT + 200)
		
#Bullet class for player, every time player pressess space a bullet is created 
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_bullet_img
		self.image = pygame.transform.scale(self.image, (20, 20))
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width/6)
		self.rect.x = x - 9
		self.rect.y = y - 10
		self.speedy = -4
	
	#Bullet update method that changes bullet's position
	def update(self):
		self.rect.y += self.speedy
		if self.rect.y < 0:
			self.kill()

			
class Aliens(pygame.sprite.Sprite):
	
	def __init__(self, x, y, enemy_type):
		pygame.sprite.Sprite.__init__(self)
		self.enemy_type = enemy_type
		filename = 'enemy{}.png'.format(self.enemy_type)
		img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
		self.image = img
		self.image = pygame.transform.scale(self.image, (16, 16))
		self.rect = self.image.get_rect()	
		self.radius = int(self.rect.width/3)
		self.rect.x = x
		self.rect.y = y
		self.speedx = 1
		self.score = 15
		
		for self in enemies:
			if self.enemy_type == 1:
				self.score = 25
			if self.enemy_type == 2:
				self.score = 15
			if self.enemy_type == 3:
				self.score = 10
		
	def update(self):
		self.rect.x += self.speedx
		if self.rect.x > WIDTH - 15:
			self.rect.x = WIDTH - 15
			for self in enemies:
				self.speedx *= -1
				self.rect.y += 5
		if self.rect.x < 0:
			self.rect.x = 0
			for self in enemies:
				self.speedx *= -1
				self.rect.y += 5		
						
	def shoot(self):
		bullet = EnemyBullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		enemy_bullets.add(bullet)
		enemy_shoot_sound.play()

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_bullet_img
		self.image = pygame.transform.scale(self.image, (20, 30))
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width/6)
		self.rect.x = x - 9
		self.rect.y = y - 10
		self.speedy = 4
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect.y > 600:
			self.kill()	
			
			
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, type):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		self.image = explosion_anim[self.type][8]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 200
		
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim[self.type]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.type][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

#---------------- image loading for explosions -----------------------
explosion_anim = {}
explosion_anim['aliens'] = []
explosion_anim['player'] = []
for i in range(9):
	filename = 'regularExplosion0{}.png'.format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
	img.set_colorkey(BLACK)
	img_aliens = pygame.transform.scale(img, (16, 16))
	explosion_anim['aliens'].append(img_aliens)
	filename = 'sonicExplosion0{}.png'.format(i)
	img_player = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
	img.set_colorkey(BLACK)
	explosion_anim['player'].append(img_player)
#---------------------------------------------------------------------

		
def game_loop():
	probability = 0.0005
	running = True
	game_over = True
	displayscore = score(0)
	enemyCount = len(aliens.sprites())
	aliensDead = 0
	while running:
		if game_over:
			show_go_screen()
			game_over = False
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		for alien in aliens:		
			hits = pygame.sprite.spritecollide(alien, player_bullets, True, pygame.sprite.collide_circle)
			for hit in hits:
				enemies.remove(alien)
				explosion_sound.play()
				score(alien.score)
				expl = Explosion(alien.rect.center, 'aliens')
				all_sprites.add(expl)
				alien.kill()
				aliensDead += 1
				if aliensDead == enemyCount/2:
					for alien in aliens:
						alien.speedx *= 2
						probability = 0.00070
				if aliensDead == (3*enemyCount)/4:
					for alien in aliens:
						alien.speedx *= 3/2
						probability = 0.0030
				if aliensDead == enemyCount - 1:
					for alien in aliens:
						alien.speedx *= 5/3
						probability = 0.0200
				if not enemies:
					for self in player_bullets:
						self.kill()
					for self in enemy_bullets:
						self.kill()
					for self in aliens:
						self.kill()
					enemies.clear()
					level_change()
		
		hits = pygame.sprite.spritecollide(player, aliens, False, pygame.sprite.collide_circle)
		if hits:
			alive = True
			pygame_die_sound.play()
			death_explosion2 = Explosion(player.rect.center, 'player')
			all_sprites.add(death_explosion2)
			while death_explosion2.alive():
				death_explosion2.update()
				all_sprites.draw(screen)
				pygame.display.flip()
			start_time = int(pygame.time.get_ticks()) + 3000
			while alive: 
				current_time = int(pygame.time.get_ticks())
				passed_time = start_time - current_time
				if passed_time <= 0:
					alive = False
				screen.fill(BLACK)
				draw_text(screen, "GAME OVER!", 64, WIDTH/2, HEIGHT/6, YELLOW)
				draw_text(screen, "Game loading...", 40, WIDTH/2, HEIGHT/2 - 40, RED)			
				pygame.display.update()	
				pygame.display.flip()
				for self in player_bullets:
					self.kill()
				for self in enemy_bullets:
					self.kill()
				for self in aliens:
					self.kill()
				enemies.clear()			
				level(-1)
				score(-1)
			done = True
			running = False
						
		hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)
		if hits:
			explosion_sound.play()
			expl = Explosion(player.rect.center, 'player')
			all_sprites.add(expl)
			while expl.alive():
				expl.update()
				all_sprites.draw(screen)
				pygame.display.flip()
			player.hide()
			player.lives -= 1
			for hit in hits:
				hit.kill()
			for self in enemy_bullets:
				self.kill()
				
		if player.lives == 0:
			screen.fill(BLACK)
			draw_text(screen, "GAME OVER!", 64, WIDTH/2, HEIGHT/6, YELLOW)
			draw_text(screen, "Game loading...", 40, WIDTH/2, HEIGHT/2 - 40, RED)
			pygame.display.flip()
			for self in player_bullets:
				self.kill()
			for self in enemy_bullets:
				self.kill()
			for self in aliens:
				self.kill()
			enemies.clear()
			score(-1)
			level(-1)
			pygame.time.wait(100)			
			running = False
			
		for enemy in enemies:
			fireChance = random.random()
			if (fireChance <= probability):
				x = enemy.rect.x
				y = enemy.rect.y
				enemy_bullet = EnemyBullet(enemy.rect.x, y)
				enemy_bullets.add(enemy_bullet)
				enemy.shoot()
			if enemy.rect.y > player.rect.bottom:
				pygame_die_sound.play()
				death_explosion2 = Explosion(player.rect.center, 'player')
				all_sprites.add(death_explosion2)
				while death_explosion2.alive():
					death_explosion2.update()
					all_sprites.draw(screen)
					pygame.display.flip()
				for self in player_bullets:
						self.kill()
				for self in enemy_bullets:
					self.kill()
				for self in aliens:
					self.kill()
				enemies.clear()
				level(-1)
				score(-1)
				running = False
				pygame.time.wait(100)
				screen.fill(BLACK)
				draw_text(screen, "GAME OVER!", 64, WIDTH/2, HEIGHT/6, YELLOW)
				draw_text(screen, "Game loading...", 40, WIDTH/2, HEIGHT/2 - 40, RED)
				pygame.display.flip()
				pygame.time.wait(100)
				break	

		screen.blit(background, (0,0))
		all_sprites.update()
		all_sprites.draw(screen)
		draw_text(screen, "Score: " + str(int(score(0))), 20, WIDTH/10, 10, WHITE)
		draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
		pygame.display.flip()	

while(True):		
	all_sprites = pygame.sprite.Group()
	aliens = pygame.sprite.Group()
	player_bullets = pygame.sprite.Group()
	enemy_bullets = pygame.sprite.Group()
	make_Enemies()
	player = Player()
	all_sprites.add(player)
	game_loop()
