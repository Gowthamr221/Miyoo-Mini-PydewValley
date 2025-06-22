import pygame
from os import getcwd 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic,Water,WildFlower,Tree
# import logging
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
# logger=logging.getLogger(__name__)
from pytmx.util_pygame import load_pygame
import os
from support import *



class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()

		# setup the level
		self.setup()
		self.overlay = Overlay(self.player)
	
	def setup(self):
		map_path = os.path.join(os.path.dirname(__file__), "..",'data', 'map.tmx')
		if getcwd().endswith('Sample'):
			map_path = '/mnt/SDCARD/App/Sample/data/map.tmx'
		tmx_data = load_pygame(map_path)

		# background
		Generic(
			pos = (0,0),
			surf = pygame.image.load(os.path.join(os.path.dirname(__file__), "..",'graphics', 'world', 'ground.png')).convert_alpha(),
			groups= self.all_sprites,
			z = LAYERS['ground']
		)

		#house
		for layer in ['HouseFloor','HouseFurnitureBottom']:
			for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites], z=LAYERS['house bottom'])
		
		#house walls & furniture
		for layer in ['HouseWalls','HouseFurnitureTop']:
			for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites], z=LAYERS['house top'])
		
		# render fence
		for x,y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites],z=LAYERS['ground'])

		# water
		water_frames = import_folder(os.path.join(os.path.dirname(__file__), "..",'graphics', 'water'))
		if getcwd().endswith('Sample'):
			water_frames = import_folder('/mnt/SDCARD/App/Sample/graphics/water')
		for x,y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, [self.all_sprites])



		# trees
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y),
				surf = obj.image,
				groups = [self.all_sprites,self.collision_sprites,self.tree_sprites],
				name = obj.name,
				player_add = self.player_add
			)

		# wild flowers
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower(
				pos = (obj.x, obj.y),
				surf = obj.image,
				groups = [self.all_sprites, self.collision_sprites])

		# collision tiles
		for x,y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic(pos= (x * TILE_SIZE, y * TILE_SIZE), surf=pygame.Surface((TILE_SIZE,TILE_SIZE)), groups= [self.collision_sprites])	
		
		# player
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos=(obj.x, obj.y),
					groups=self.all_sprites,
					collision_sprites=self.collision_sprites,
					tree_sprites=self.tree_sprites)
		
	def player_add(self,item):
		self.player.item_inventory[item] += 1
		
	def run(self,dt):
		# self.display_surface.fill((0, 0, 0))  # Clear the screen with black
		self.all_sprites.update(dt)
		self.all_sprites.custom_draw(self.player)
		self.overlay.display()
		print(self.player.item_inventory)  # Debugging line to check inventory


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self,player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2
		
		for layer in range(10):
			for sprite in sorted(self.sprites(),key = lambda sprite:sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)

					#analytics
					# if sprite == player:
					# 	pygame.draw.rect(self.display_surface, (255, 0, 0), offset_rect, 5)
					# 	hitbox_rect = sprite.hitbox.copy()
					# 	hitbox_rect.center = offset_rect.center
					# 	pygame.draw.rect(self.display_surface, (0, 255, 0), hitbox_rect, 5)
					# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
					# 	pygame.draw.circle(self.display_surface, (0, 0, 255),(int(target_pos[0]),int(target_pos[1])), 5)
					
