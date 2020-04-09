import pygame
from settings import *
import time
from playsound import playsound
vec = pygame.math.Vector2

PAC_RIGHT_IMG = 'pac_right.gif'
PAC_LEFT_IMG = 'pac_left.gif'
PAC_UP_IMG = 'pac_up.gif'
PAC_DOWN_IMG = 'pac_down.gif'
MISSILE_IMAGE = 'missile_image.gif'
GHOST_IMAGE = 'ghost_image.png'

PAC_EATING_COIN_SOUND = 'pacman_chomp.wav'


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 1
        self.rect = pygame.Rect(pos, (5, 5))
        self.ate_pill = False
        self.pill_cooldown = 99999

        self.able_to_teleport = False

        self.pac_right_image = pygame.image.load(PAC_RIGHT_IMG)
        self.pac_left_image = pygame.image.load(PAC_LEFT_IMG)
        self.pac_up_image = pygame.image.load(PAC_UP_IMG)
        self.pac_down_image = pygame.image.load(PAC_DOWN_IMG)

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.able_to_teleport:
            pass
            # self.pix_pos
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        self.able_to_teleport = self.can_teleport()

        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1
        if self.on_coin():
            self.eat_coin()
        elif self.on_pill():
            self.eat_pill()
            self.pill_cooldown = self.current_score

        # if self.ate_pill and (self.current_score - self.pill_cooldown) >= 15:
        #     for enemy in self.app.enemies:
        #         enemy.toggle_scared()
        #         # print("{}".format(enemy.personality))
        #     self.ate_pill = False

    def draw(self):
        self.rect.center = (int(self.pix_pos.x-5), int(self.pix_pos.y-10))

        if self.direction == (1, 0):
            self.app.screen.blit(self.pac_right_image, self.rect)
        elif self.direction == (-1, 0):
            self.app.screen.blit(self.pac_left_image, self.rect)
        elif self.direction == (0, -1):
            self.app.screen.blit(self.pac_up_image, self.rect)
        elif self.direction == (0, 1):
            self.app.screen.blit(self.pac_down_image, self.rect)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (30 + 20*x, HEIGHT - 15), 7)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def on_pill(self):
        if self.grid_pos in self.app.pills:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_pill(self):
        self.app.pills.remove(self.grid_pos)
        # self.ate_pill = True
        # for enemy in self.app.enemies:
        #     enemy.toggle_scared()

    def on_portal(self):
        pass

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

        print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True

    def can_teleport(self):
        for portal in self.app.portals:
            if vec(self.grid_pos+self.direction) == portal:
                return True
                print("({}, {})".format(self.pix_pos.x, self.pix_pos.y))
        return False
