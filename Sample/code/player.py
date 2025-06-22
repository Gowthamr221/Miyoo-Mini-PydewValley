import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,collision_sprites,tree_sprites):
        pygame.sprite.Sprite.__init__(self,groups)
        
     
        self.import_assets()
        
        self.status = 'down_idle'  # default status
        self.frame_index = 0
        self.animation_speed = 0.15  # speed of animation frames

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-126, -70)  # reduce the hitbox size
        self.z = LAYERS['main']  # set the z-index for rendering order

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.hitbox = self.rect.inflate(-126, -70)  # reduce the hitbox size
        self.collision_sprites = collision_sprites

        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0  # index for the selected tool
        self.selected_tool = self.tools[self.tool_index]  # default selected tool

        # seeds
        self.seeds = ['corn','tomato']
        self.seed_index = 0  
        self.selected_seed = self.seeds[self.seed_index]  

        # player inventory
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),  # 500 ms for tool use
            'tool switch':Timer(200),
            'seed use': Timer(350, self.use_seed),  # 500 ms for tool use
            'seed switch':Timer(200)
        }

        # interaction
        self.tree_sprites = tree_sprites

    def use_tool(self):
        print('Using tool:', self.selected_tool)
        if self.selected_tool == 'hoe':
            pass
        elif self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.hitbox.collidepoint(self.target_pos):
                    tree.damage()
                    
        elif self.selected_tool == 'water':
            pass
    
    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        # print(self.selected_seed)
        pass
    
    def import_assets(self):
        self.animations = {'up':[],
                           'down':[],
                           'left':[],
                           'right':[],
                           'right_idle':[],
                           'left_idle':[],
                           'up_idle':[],
                           'down_idle':[],
                           'right_hoe':[],
                           'left_hoe':[],
                           'up_hoe':[],
                           'down_hoe':[],
                           'right_axe':[],
                           'left_axe':[],
                           'up_axe':[],
                           'down_axe':[],
                           'right_water':[],
                           'left_water':[],
                           'up_water':[],
                           'down_water':[]
                        }
        for animation in self.animations.keys():
            full_path = '../graphics/character/'+animation
            if getcwd().endswith('Sample'):
                full_path = '/mnt/SDCARD/App/Sample/graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self,dt):
        # update the frame index based on the animation speed
        self.frame_index += 4* dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0        
        # set the image to the current frame
        self.image = self.animations[self.status][int(self.frame_index)]
        

    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.timers['tool use'].active:  # only allow movement if tool is not in use
            # directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0


            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
            
            # tool use
            if keys[pygame.K_SPACE]:
                # timer for tool use
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()  # stop movement while using tool
                self.frame_index = 0  # reset frame index for tool use animation
               
            
            if keys[pygame.K_LCTRL] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                # switch tool
                self.tool_index += 1
                if self.tool_index < len(self.tools):
                    self.tool_index = self.tool_index
                else:
                    self.tool_index = 0
                # update the status to reflect the selected tool
                self.selected_tool = self.tools[self.tool_index]
            
            # seed use
            if keys[pygame.K_LSHIFT]:
                # timer for seed use
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()  # stop movement while using tool
                self.frame_index = 0  # reset frame index for tool use animation
                
            # change seed
            if keys[pygame.K_TAB] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                # switch seed
                self.seed_index += 1
                if self.seed_index < len(self.seeds):
                    self.seed_index = self.seed_index
                else:
                    self.seed_index = 0
                # update the status to reflect the selected seed
                self.selected_seed = self.seeds[self.seed_index]
                



    def get_status(self):
        # idle
        if self.direction.length() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()        

    def collision(self,direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    
                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        #normalize the direction vector to prevent faster diagonal movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.y
        self.collision('vertical')


    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)