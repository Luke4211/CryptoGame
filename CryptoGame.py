# -*- coding: utf-8 -*-
import os
import sys
import math
import pygame as py
from pygame.locals import *


class hero(object):
    sequence = [1,1,1,1,2,2,2,2,3,3,3,3]
    move_right = [py.image.load(os.path.join('sprites', 'hero_right_' + str(i) + '.png')) for i in sequence]
    move_left = [py.image.load(os.path.join('sprites', 'hero_left_' + str(i) + '.png')) for i in sequence]
    
    def __init__(self, x, y, height, width, window, speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.window = window
        self.speed = speed
        self.move_count = 0
        self.last_dir = 1 # -1 to face left, 1 to face right
        self.r_bound = width - (width//4)
        self.l_bound = width//4
        self.true_x = 0
    def move(self, direction):
        
        rtn = True
        if direction == 1:
            if (self.x + self.speed) < self.r_bound:
                self.last_dir = 1
                self.x += self.speed                
                self.move_count += 1
                self.update_truex(direction)
            else:
                rtn = False
            self.window.blit(self.move_right[self.move_count%12], (self.x, self.y))
        elif direction == -1:
            if (self.x - self.speed) > self.l_bound:
                self.last_dir = -1
                self.x -= self.speed            
                self.move_count += 1
                self.update_truex(direction)
            else: 
                rtn = False
            self.window.blit(self.move_left[self.move_count%12], (self.x, self.y))
        else:
            if(self.last_dir == 1):
                self.move_count +=1
                self.window.blit(self.move_right[self.move_count%12], (self.x, self.y))
            else:
                self.move_count += 1
                self.window.blit(self.move_left[self.move_count%12], (self.x, self.y))
        return rtn
    
    def update_truex(self, direction):
        self.true_x += direction*speed
        print(str(self.true_x))
    def can_scroll_left(self):
        if self.true_x > 0 :
            return True
            print('yay')
        else:
            return False

class scroller(object):
    
    def __init__(self, window, player, background, speed):
        self.window = window
        self.player = player
        self.background = py.image.load(os.path.join('backgrounds', background + '.png')).convert()
        self.x1 = 0
        self.x2 = self.background.get_width()
        self.speed = speed
        self.draw()
        

    def draw(self):
        self.window.blit(self.background, (self.x1,  0))
        self.window.blit(self.background, (self.x2, 0))
        
    def move(self, direction):
        self.draw()
        player_moved = self.player.move(direction)
        if(player_moved == False):
            if direction == 1 or self.player.can_scroll_left():
                self.x1 -= direction*self.speed
                self.x2 -= direction*self.speed
                
                if self.x1 < self.background.get_width() * -1:
                    self.x1 = self.background.get_width()
                    
                if self.x2 < self.background.get_width() * -1:
                    self.x2 = self.background.get_width()
                self.player.move(0)
                self.player.update_truex(direction)
            

py.init()

H, W = 750, 1050
window = py.display.set_mode((W,H))
clock = py.time.Clock()
speed = 5
player = hero(250,500, H, W, window, speed)
scroll = scroller(window, player, 'forest1', speed)
run = True
while run:
    clock.tick(50)

    
    keys = py.key.get_pressed()
    
    if keys[py.K_RIGHT]:
        scroll.move(1)
    if keys[py.K_LEFT]:
        scroll.move(-1)
    py.display.update() 
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
            py.quit()
            quit()
