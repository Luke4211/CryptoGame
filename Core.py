# -*- coding: utf-8 -*-
"""
    Core.py ~ Contains classes for each object
    Written by Luke Gorski
"""
import os
import pygame as py

class hero(object):
    sequence = [1,1,1,1, 2,2,2,2, 3,3,3,3]
    move_right = [py.image.load(os.path.join('sprites', 'hero_right_' + str(i) + '.png')) for i in sequence]
    move_left = [py.image.load(os.path.join('sprites', 'hero_left_' + str(i) + '.png')) for i in sequence]
    
    def __init__(self, x, y, height, width, window, speed, bg_width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.window = window
        self.speed = int(1.5*speed)
        self.bg_width = bg_width
        self.move_count = 0
        self.last_dir = 1 # -1 to face left, 1 to face right
        self.r_bound = width - (width//4)
        self.l_bound = width//4
        self.true_x = 0
        self.attack_speed = 10
        self.is_jump = False
        self.y_speed = 0
        self.y_jump_start = self.y

        
    def draw(self):
        print(str(self.true_x))
        if self.last_dir == 1:
            self.window.blit(self.move_right[self.move_count%12], (self.x, self.y))
        else:
            self.window.blit(self.move_left[self.move_count%12], (self.x, self.y))
        
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
            
        elif direction == -1:
            if (self.x - self.speed) > self.l_bound:
                self.last_dir = -1
                self.x -= self.speed            
                self.move_count += 1
                self.update_truex(direction)
            else: 
                rtn = False
            
        else:
            self.move_count += 1
                
        return rtn   
    
    def jump(self):
        if self.is_jump == False:
            self.is_jump = True
            self.y_speed = self.speed * 2 
            self.y -= self.y_speed
        else:
            if self.y_jump_start <= self.y:
                self.is_jump = False
                self.y_speed = 0
                self.y = self.y_jump_start
            else:
                self.y -= self.y_speed
                self.y_speed -= 1

    def update_truex(self, direction):
        self.true_x += direction*self.speed
    def can_scroll_left(self):
        if self.true_x > 0 :
            return True
        else:
            return False
    def can_scroll_right(self):
        if self.true_x + self.r_bound < self.bg_width:
            return True
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
        self.scrollables = []
        
    
    def draw(self):
        self.window.blit(self.background, (self.x1,  0))
        self.window.blit(self.background, (self.x2, 0))
        
    def move(self, direction):

        player_moved = self.player.move(direction)
        if(player_moved == False):
            if (direction == 1 and self.player.can_scroll_right()) or (direction == -1 and self.player.can_scroll_left()):
                self.x1 -= direction*self.speed
                self.x2 -= direction*self.speed
                
                for scrollable in self.scrollables:
                    scrollable.move(direction*self.speed)
                """
                if self.x1 < self.background.get_width() * -1:
                    self.x1 = self.background.get_width()
                    
                if self.x2 < self.background.get_width() * -1:
                    self.x2 = self.background.get_width()
                """
                self.player.move(0)
                self.player.update_truex(direction)
                
    def add_scrollable(self, scrollable):
        self.scrollables.append(scrollable)
        

class star(object):
    
    def __init__(self, window, x, y, speed, direction):
        self.window = window
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.animation = [py.image.load(os.path.join('sprites', 'star' + str(i) + '.png')) for i in range(1,6)]
        self.move_count = 0
        self.rect = py.Rect((x,y), (30, 30))
        self.dead = False
        self.window_width, _ = py.display.get_surface().get_size()
        
    def draw(self):
        if not self.dead:
            self.window.blit(self.animation[self.move_count%5], (self.x, self.y))
    def move(self):
        if not self.dead:
            self.x += self.direction*self.speed
            if self.x > 0 and self.x < self.window_width + 30:
                self.rect.move_ip(self.direction*self.speed, 0)
                self.move_count += 1
            else:
                self.dead = True

class sign(object):
    
    def __init__(self, window, x, y, message):
        self.window = window
        self.x = x
        self.y = y
        self.message = message
        self.active = True
        self.sign = py.image.load(os.path.join('sprites', 'sign.png'))
        font = py.font.Font(os.path.join('font', 'AncientModernTales.ttf'), 20)
        
        self.text = font.render(self.message, True, (0,0,0) )
        
        self.text_box = self.text.get_rect()
        
        self.text_box.center = (self.x, self.y - 35)
        self.image_box = self.sign.get_rect()
        self.image_box.center = (self.x, self.y)
        
    def draw(self):
        self.window.blit(self.sign, self.image_box)
        self.window.blit(self.text, self.text_box)
    
    def move(self, amount):
        self.x -= amount
        self.text_box.center = (self.x, self.y - 35)
        self.image_box.center = (self.x, self.y)
        
        
    
        