# -*- coding: utf-8 -*-
import pygame as py
import Core as core

# TODO: Create a function for each level. 
# For development, this is fine

            
py.init()

H, W = 750, 1050
window = py.display.set_mode((W,H))
clock = py.time.Clock()
speed = 5
player = core.hero(250,500, H, W, window, speed, 3000)

# Level ~ Haunted Wood Forest
scroll = core.scroller(window, player, 'forest1', speed)

msg1 = core.sign(window, 200, 400, "Haunted Wood Forest")
msg2 = core.sign(window, 1500, 400, "Beware of Mad Wizard")
scroll.add_scrollable(msg1)
scroll.add_scrollable(msg2)
drawers = [scroll, player, msg1, msg2]
projectiles = []
last_attack = 0
run = True


while run:
    clock.tick(50)

    
    keys = py.key.get_pressed()
    
    if keys[py.K_d]:
        scroll.move(1)
    if keys[py.K_a]:
        scroll.move(-1)
    
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
