# -*- coding: utf-8 -*-
"""
    Core.py ~ Contains classes for each object
    Written by Luke Gorski
"""
import os
import pygame as py
import random

class humanoid(object):
    def __init__(self, x, y, height, width, window, speed, 
                 bg_width, scrolling, hp, strength, image,
                 num_frames, seq_len, jump_mult, friendly=True, hitbox=45, deflect = False):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.window = window
        self.speed = int(1.5*speed)
        self.bg_width = bg_width
        self.hp = hp
        self.strength = strength
        self.num_frames = num_frames
        self.seq_len = seq_len
        self.jump_mult = jump_mult
        self.dead = False
        self.rect = py.rect.Rect((x,y), (hitbox,hitbox))
        self.unlocked = deflect
        self.cool = 3000
        self.shield = -1
        if self.unlocked:
            self.shield = py.image.load(os.path.join('sprites', 'shield.png')) 
        self.deflecting = False
        self.last_deflect = 0
        self.deflect_duration = 1000
        
        sequence = []
        
        for i in range(1, num_frames + 1):
            for j in range(0, seq_len):
                sequence.append(i)
        
        self.move_right = [py.image.load(os.path.join('sprites', image + '_right_' + str(i) + '.png')) for i in sequence]
        self.move_left = [py.image.load(os.path.join('sprites', image +  '_left_' + str(i) + '.png')) for i in sequence]
        
        self.move_count = 0
        self.last_dir = 1 # -1 to face left, 1 to face right
        
        if scrolling:
            self.r_bound = width - (width//5)
            self.l_bound = width//5
        else:
            self.r_bound = width - 40
            self.l_bound = 20
        self.true_x = 0
        self.attack_speed = 15
        self.is_jump = False
        self.y_speed = 0
        self.y_jump_start = self.y
        
        
    def draw(self):
        if self.deflecting:
            self.window.blit(self.shield, (self.x - 10, self.y - 15))
            if (py.time.get_ticks() - self.last_deflect) > self.deflect_duration:
                self.deflecting = False
                
        if self.last_dir == 1:
            self.window.blit(self.move_right[self.move_count%(self.num_frames*self.seq_len)], (self.x, self.y))
        else:
            self.window.blit(self.move_left[self.move_count%(self.num_frames*self.seq_len)], (self.x, self.y))
        
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
            
        elif direction == -2:
            self.move_count += 1
                
        self.rect.x = self.x
        
        return rtn   
    
    def jump(self):
        if self.is_jump == False:
            self.is_jump = True
            self.y_speed = self.speed * self.jump_mult
            self.y -= self.y_speed
        else:
            if self.y_jump_start <= self.y:
                self.is_jump = False
                self.y_speed = 0
                self.y = self.y_jump_start
            else:
                self.y -= self.y_speed
                self.y_speed -= 1
        self.rect.y = self.y

    def update_truex(self, direction):
        self.true_x += direction*self.speed
    def can_scroll_left(self):
        if self.true_x > 0 :
            return True
        else:
            return False
    def can_scroll_right(self):
        if self.true_x < self.bg_width:
            return True
        else:
            return False
    
    
class hero(humanoid):
    def __init__(self, *args, **kwargs):
        
        super(hero, self).__init__(*args, **kwargs)
        
    def deflect(self):
        if self.unlocked:
            self.deflecting = True
            self.last_deflect = py.time.get_ticks()
    
    def cooldown(self):
        return self.cool - (py.time.get_ticks() - self.last_deflect)

#TODO: Fix the scrolling speed issue here. Subtract from player speed
        #Robber speed and move that much
class robber(humanoid):
    def __init__(self, hero, jumprate, att_rate, att_speed, *args, **kwargs):
        super(robber, self).__init__(*args, **kwargs)
        self.friendly = False
        self.jumprate = jumprate
        self.att_rate = att_rate
        self.att_speed = att_speed
        self.hero = hero
        self.norm_speed = self.speed 
        self.last_attack = 0
        self.last_jump = py.time.get_ticks()
        #random.seed()
        
        
    def move(self):
        if not self.dead:
            if self.is_jump == False:
                j = random.random() 
                if j <= self.jumprate and py.time.get_ticks() - self.last_jump > 800:
                    self.jump()
                    self.last_jump = py.time.get_ticks()
            else:
                self.jump()
            diff = self.hero.x - self.x
            
    
                
            if abs(diff) < 29:
                direction = 0
            elif diff > 0:
                direction = 1
            else:
                direction = -1

            super(robber, self).move(direction)
    def attack(self):
        proj = -1
        
        if not self.dead:
            diff = self.hero.x - self.x
            
            if diff > 0:
                direction = 1
            else:
                direction = -1
            
            att = random.random()
            
            
            if att <= self.att_rate and py.time.get_ticks() - self.last_attack > 750:
                proj = projectile(self.window, self.x, self.y, self.att_speed, 
                                        direction, player=False, image = "spear_test", 
                                        num_frames = 1, omni_dir=False)
                self.last_attack = py.time.get_ticks()
        return proj
    
    def draw(self):
        if not self.dead:
            super(robber, self).draw()
    
class eve(robber):
    
    def __init__(self, *args, **kwargs):
        super(eve, self).__init__(*args, **kwargs)
        self.aggro = False
        self.last_rockfall = py.time.get_ticks()
        
    def attack(self):
        if self.aggro:
            proj = -1
        
            if not self.dead:
                diff = self.hero.x - self.x
                
                if diff > 0:
                    direction = 1
                else:
                    direction = -1
                
                att = random.random()             
                
                if att <= self.att_rate and py.time.get_ticks() - self.last_attack > 750:
                    proj = projectile(self.window, self.x, self.y+50, self.att_speed, 
                                            direction, player=False, image = "spear_test", 
                                            num_frames = 1, omni_dir=False)
                    self.last_attack = py.time.get_ticks()
            return proj
    
    def rockfall(self):
        proj = -1
        
        if not self.dead:
            att = random.random()
            
            if att <= self.att_rate and py.time.get_ticks() - self.last_rockfall > 500:
                proj = falling_rock(self.window, self.hero.x, 50, 4, 1, player=False, 
                                    image = "boulder", num_frames = 1)
                self.last_rockfall = py.time.get_ticks()
        return proj
    def move(self):
        
        super(eve, self).move()
    
    # Moves without any jump animation
    def move_njump(self):
        diff = self.hero.x - self.x
            
              
        if abs(diff) < 40:
            direction = 0
        elif diff > 0:
            direction = 1
        else:
            direction = -1
        super(robber, self).move(direction)
    
class king(eve):
    
    def __init__(self, *args, **kwargs):
        super(king, self).__init__(*args, **kwargs)
        self.idle_img = py.image.load(os.path.join('sprites', 'king_idle_left.png'))
        self.idle = True
        self.attack_timer = 1000
        
        self.attacking = False      
        self.attack_animation = [py.image.load(os.path.join('sprites', 'king_lunge_' + str(i) + '.png')) for i in range(1,5)]
        tmp = [None]*(2*len(self.attack_animation))
        tmp[::2] = self.attack_animation
        tmp[1::2] = self.attack_animation
        self.attack_animation = tmp
        self.attack_count = 0
    def draw(self):
        if self.idle:
            self.window.blit(self.idle_img, (self.x, self.y))
        elif self.attacking == True:
            if self.last_dir == 1:
                self.window.blit(self.attack_animation[self.attack_count], (self.x, self.y))
            else:
                self.window.blit(py.transform.flip(self.attack_animation[self.attack_count], True, False), (self.x, self.y))
            if self.attack_count == 3:
                self.attack_count = 0
                self.attacking = False
            else:
                self.attack_count += 1
        else:
            super(king, self).draw()
    
    def move(self):
        if not self.idle:
            if (py.time.get_ticks() - self.last_attack) > self.attack_timer:
                super(king, self).move()
    
    def attack(self):
        rtn = False
        if not self.idle:
            diff_x = abs(self.hero.x - self.x)
            diff_y = abs(self.hero.y - self.y)
            if diff_x < 30 and diff_y < 70 and (py.time.get_ticks() - self.last_attack) > self.attack_timer:
                rtn = True
                self.attacking = True
                self.last_attack = py.time.get_ticks()
        return rtn
    
    def jump(self):
        self.is_jump = False
        
    #TODO: Add code for his lunge attack, he will be melee only with mobs
class wizard(object):
    
    sequence = [1,1,1,1,1,1,1, 2,2,2,2,2,2,2, 3,3,3,3,3,3,3, 4,4,4,4,4,4,4, 3,3,3,3,3,3,3, 2,2,2,2,2,2,2]
    idle = [py.image.load(os.path.join("sprites", "wizard_idle_" + str(i) + ".png")) for i in sequence]
    idle_right = [py.image.load(os.path.join("sprites", "wizard_idle_right_" + str(i) + ".png")) for i in sequence]
    def __init__(self, window, x, y, speed):
        self.window = window
        self.x = x
        self.y = y
        self.speed = speed
        self.move_count = 0
        self.last_dir = 0
        self.facing = 1
        
    def move(self, direction):
        self.x += self.last_dir * self.speed
        self.move_count += 1
        self.last_dir = direction
    def draw(self):
        if self.last_dir == 0:
            if self.facing == 1:
                self.window.blit(self.idle_right[self.move_count%42], (self.x, self.y))
            else:
                self.window.blit(self.idle[self.move_count%42], (self.x, self.y))
            
    def turn_around(self):
        self.facing *= -1
class scroller(object):
    
    def __init__(self, window, player, background, speed, enemies):
        self.window = window
        self.player = player
        self.background = py.image.load(os.path.join('backgrounds', background + '.png')).convert()
        self.x1 = 0
        self.x2 = self.background.get_width()
        self.speed = speed
        self.draw()
        self.scrollables = []
        self.enemies = enemies
    
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

                self.player.move(-2)
                for enemy in self.enemies:
                    super(type(enemy), enemy).move(-2)
                self.player.update_truex(direction)
                
    def add_scrollable(self, scrollable):
        self.scrollables.append(scrollable)
    
    def add_enemies(self, monsters):
        self.enemies += monsters
        

class projectile(object):
    
    def __init__(self, window, x, y, speed, direction, player=True, image="star", num_frames = 5, omni_dir = True):
        self.window = window
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.move_count = 0
        self.rect = py.Rect((x,y), (30, 30))
        self.dead = False
        self.window_width, self.window_height = py.display.get_surface().get_size()
        self.player = player
        self.num_frames = num_frames
        self.omni_dir = omni_dir
        
        if self.num_frames > 1:
            self.animation = [py.image.load(os.path.join('sprites', image + str(i) + '.png')) for i in range(1,num_frames+1)]
        else:
            self.animation = [py.image.load(os.path.join('sprites', image + '.png'))]
    def draw(self):
        if not self.dead:
            if self.direction == 1 or self.omni_dir:
                self.window.blit(self.animation[self.move_count%self.num_frames], (self.x, self.y))
            else:
                self.window.blit(py.transform.flip(self.animation[self.move_count%self.num_frames], True, False), (self.x, self.y))
    def move(self):
        if not self.dead:
            self.x += self.direction*self.speed
            if self.x > 0 and self.x < self.window_width + 30:
                self.rect.move_ip(self.direction*self.speed, 0)
                self.move_count += 1
            else:
                self.dead = True

class falling_rock(projectile):
    def __init__(self, *args, **kwargs):
        super(falling_rock, self).__init__(*args, **kwargs)
        
    def move(self):
        if not self.dead:
            self.y += self.speed
            if self.y < 550:
                self.rect.move_ip(0, self.speed)
                self.move_count += 1
            else:
                self.dead = True

class sign(object):
    
    def __init__(self, window, x, y, message, folder, image, font_size=20):
        self.window = window
        self.x = x
        self.y = y
        self.message = message
        self.active = True
        self.sign = py.image.load(os.path.join(folder, image))
        self.font = py.font.Font(os.path.join('font', 'AncientModernTales.ttf'), font_size)
        
        self.text = self.font.render(self.message, True, (0,0,0) )
        
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
        
    def change_text(self, text):
        self.text = self.font.render(text, True, (0,0,0) )

class scenary(object):
    
    def __init__(self, window, x, y, folder, image, conv=False):
        self.window = window
        self.x = x
        self.y = y
        if not conv:
            self.image = py.image.load(os.path.join(folder, image))
        else:
            self.image = py.image.load(os.path.join(folder, image)).convert()
    
    def move(self, amount):
        self.x -= amount
    def draw(self):
        self.window.blit(self.image, (self.x, self.y))

class arrow(object):
    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.arrow = py.image.load(os.path.join('sprites', 'arrow.png'))
        self.movement = [3, 3, 3, 3, 3, 3, 3, -3, -3, -3, -3, -3, -3, -3]
        self.move_count = 0
        
    def draw(self):
        self.window.blit(self.arrow, (self.x, self.y))
    def bounce(self):
        self.y += self.movement[self.move_count%14]
        self.move_count += 1
    def move(self, amount):
        self.x -= amount