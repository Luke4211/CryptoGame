# -*- coding: utf-8 -*-
"""
    CryptoGame.py ~ Contains loops for each level
    Written by Luke Gorski
"""
import pygame as py
import Core as core

# TODO: Create a function for each level. 
# For development, this is fine

# Level ~ Haunted Wood Forest
def scene_one(window, clock, speed):
    player = core.hero(250,500, H, W, window, speed, 1915, True)
    scroll = core.scroller(window, player, 'forest1', speed)
    
    msg1 = core.sign(window, 200, 400, "Caesar's Forest")
    msg2 = core.sign(window, 1500, 400, "Beware of Mad Wizard")
    wiz_house = core.scenary(window, 1750, 293, "sprites", "WizardHouse.png")
    wiz_fence = core.scenary(window, 1800, 400, "sprites", "WizardFence.png")
    
    scrolls = [msg1, msg2, wiz_house, wiz_fence]
    
    for scr in scrolls:
        scroll.add_scrollable(scr)
        
    drawers = [scroll, msg1, msg2, wiz_fence, wiz_house, player]
    projectiles = []
    last_attack = 0
    run = True
    
    
    while run:
        clock.tick(60)
    
        
        keys = py.key.get_pressed()
        
        if keys[py.K_d]:
            scroll.move(1)
        if keys[py.K_a]:
            scroll.move(-1)
        if keys[py.K_SPACE]:
            player.jump()
        if keys[py.K_e]:
            if player.true_x >= 1900 and player.true_x <= 1920:
                run = False
        
        if player.is_jump == True:
            player.jump()
        for draw in drawers:
            draw.draw()
        if py.mouse.get_pressed()[0]:
            if py.time.get_ticks() - last_attack > 700:
                throwing_star = core.star(window, player.x, player.y, player.attack_speed, player.last_dir)
                projectiles.append(throwing_star)
                last_attack = py.time.get_ticks()
        
        deletes = []
        for proj in projectiles:
            if not proj.dead:
                proj.move()
                proj.draw()
            else:
                deletes.append(proj)
        for rm in deletes:
            projectiles.remove(rm)
        py.display.update() 
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
                

def scene_two(window, clock, speed):
    player = core.hero(250,700, H, W, window, speed, 1050, False)
    background = core.scenary(window, -600, 0, "backgrounds", "WizardHouse.png", conv=True)
    wizard = core.wizard(window, 800, 607, 10)
    
    
    drawers = [background, wizard, player]
    
    run = True
    
    while run:
        clock.tick(60)
        
        keys = py.key.get_pressed()
        
        if keys[py.K_d]:
            player.move(1)
        if keys[py.K_a]:
            player.move(-1)
        if keys[py.K_SPACE]:
            player.jump()
            
        wizard.move(0)
        
        if player.is_jump == True:
            player.jump()
            
        for draw in drawers:
            draw.draw()
        py.display.update() 
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
            
            
py.init()

H, W = 750, 1050
window = py.display.set_mode((W,H))
clock = py.time.Clock()
speed = 3


scene_one(window, clock, speed)
scene_two(window, clock, speed)


