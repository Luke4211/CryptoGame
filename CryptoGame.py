# -*- coding: utf-8 -*-


import pygame as py
import Core as core
from pygame.locals import *



            

py.init()

H, W = 750, 1050
window = py.display.set_mode((W,H))
clock = py.time.Clock()
speed = 5
player = core.hero(250,500, H, W, window, speed)
scroll = core.scroller(window, player, 'forest1', speed)
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
