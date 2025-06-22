import pygame, sys
from settings import *
from level import Level
import os
class Game:
	def __init__(self):
		pygame.init()
		os.system("/bin/sh /bin/cpuclock 1900")
		self.screen = self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF, 16)
		pygame.display.set_caption('Sprout land')
		self.clock = pygame.time.Clock()
		self.level = Level()
		self.fps_font = pygame.font.Font(None, 30)
		self.max_fps = 60

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						pygame.quit()
						sys.exit()

			dt = self.clock.tick(self.max_fps) / 1000.0
			self.level.run(dt)

			# Display FPS
			fps = self.clock.get_fps()
			fps_text = self.fps_font.render('FPS: %.2f' % fps, True, (255, 255, 255))
			self.screen.blit(fps_text, (10, 10))

			pygame.display.flip()

if __name__ == '__main__':
	game = Game()
	game.run()

