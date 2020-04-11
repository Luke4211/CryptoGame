# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 04:30:12 2020

@author: lucas
"""

import os
import pygame as py
import CryptoGame as cg
py.init()
H, W = 750, 1050
window = py.display.set_mode((W,H))
clock = py.time.Clock()
speed = 3

py.display.set_caption("Cryptogame")

new_ability = py.image.load(os.path.join('backgrounds', 'new_ability.png')).convert()
vig = [py.image.load(os.path.join('backgrounds', 'vigenere_' + str(i) +  '.png' )).convert() 
    for i in range(1,8)]

'''
success = cg.scene_one(window, clock, speed)

while success == False:
    cg.player_died(window, clock)
    success = cg.scene_one(window, clock, speed)
cg.scene_two(window, clock, speed)


success = cg.scene_three(window, clock, speed)
while success == False:
    cg.player_died(window, clock, level=2)
    success = cg.scene_three(window, clock, speed)

success = cg.scene_four(window, clock, speed)
while success == False:
    cg.player_died(window, clock)
    success = cg.scene_four(window, clock, speed)

cg.story_screen(window, new_ability, clock)
for i in range(4):
    cg.story_screen(window, vig[i], clock)

answer = cg.scene_four_challenge(window, clock)
while not answer == "eetdgztowt":
    cg.story_screen(window, vig[6], clock)
    answer = cg.scene_four_challenge(window, clock)

cg.story_screen(window, vig[5], clock)
'''
success = cg.scene_five(window, clock, speed)
while success == False:
    cg.player_died(window, clock, level=3)
    success = cg.scene_five(window, clock, speed)

success = cg.scene_six(window, clock, speed)
while success == False:
    cg.player_died(window, clock)
    success = cg.scene_six(window, clock, speed)