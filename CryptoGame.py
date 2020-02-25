# -*- coding: utf-8 -*-
"""
    CryptoGame.py ~ Contains loops for each level
    Written by Luke Gorski
"""
import pygame as py
import Core as core

# TODO: Create a function for each level. 


# Level ~ Haunted Wood Forest
def scene_one(window, clock, speed):
    player = core.hero(250,500, H, W, window, speed, 1915, True)
    scroll = core.scroller(window, player, 'forest1', speed)
    
    msg1 = core.sign(window, 200, 400, "Caesar's Forest", "sprites", "sign.png")
    msg2 = core.sign(window, 1500, 400, "Beware of Mad Wizard", "sprites", "sign.png")
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
    
    wizard_dia = [core.scenary(window, 600, 300, 
            "dialogue","wizard_dia_" + str(i) + ".png") 
            for i in range(1,6)]
    hero_dia = [core.scenary(window, 280, 380,
            "dialogue", "hero_dia_" + str(i) + ".png")
            for i in range(1,6)]
    
    dialogue = [None]*(len(wizard_dia) + len(hero_dia))
    dialogue[::2] = wizard_dia
    dialogue[1::2] = hero_dia
    
    
    
    
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
        if player.true_x > 322:
            run = False
            
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
                
    run = True
    cur_dia = 0
    last_enter = 0
    while run:
        clock.tick(60)        
        keys = py.key.get_pressed()
                     
        for draw in drawers:
            draw.draw()
        
        
        
        wizard.move(0)
        
        if player.is_jump == True:
            player.jump()
            
        if keys[py.K_e]:
            if py.time.get_ticks() - last_enter > 1000:             
                cur_dia += 1
                last_enter = py.time.get_ticks()
                if cur_dia == 9:
                    run = False
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
        dialogue[cur_dia].draw()
        
        py.display.update()
        
    answer = scene_two_challenge(window, clock, drawers, player, wizard, dialogue[cur_dia-1])
    wizard_wrong = core.scenary(window, 600, 300, "dialogue", "wizard_wrong_1.png")
    wizard_right = [core.scenary(
            window, 600, 300, "dialogue", "wizard_right_" + str(i) + ".png")
            for i in range(1,4)]
    while not answer == "a spell":
        run = True
        last_enter = py.time.get_ticks()
        while run:
            clock.tick(60)        
            keys = py.key.get_pressed()
                         
            for draw in drawers:
                draw.draw()
                            
            wizard.move(0)
            
            if keys[py.K_e]:
                if py.time.get_ticks() - last_enter > 1000:             
                    run = False
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False
                    py.quit()
                    quit()
            wizard_wrong.draw()
            py.display.update()
        answer = scene_two_challenge(window, clock, drawers, player, wizard, dialogue[cur_dia-1])
    
    run = True
    last_enter = py.time.get_ticks()
    cur_dia = 0
    while run:
        clock.tick(60)        
        keys = py.key.get_pressed()
                         
        for draw in drawers:
            draw.draw()
                            
        wizard.move(0)
        wizard_right[cur_dia].draw()
        if keys[py.K_e]:
            if py.time.get_ticks() - last_enter > 1000:             
                cur_dia += 1
                last_enter = py.time.get_ticks()
                if cur_dia == 4:
                    run = False
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
        
        
        py.display.update()
    
def scene_two_challenge(window, clock, drawers, player, wizard, question):
    run = True
    player_response = core.sign(window, 470, 550, "", "dialogue", "hero_dia_5.png", font_size=30)
    player_response.text_box.center = (430, 515)
    in_string = ""
    while run:
        clock.tick(60)
                     
        for draw in drawers:
            draw.draw()
        player_response.draw()
        question.draw()
        
        wizard.move(0)
        if player.is_jump == True:
            player.jump()  
           
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
            if event.type == py.KEYDOWN:   
                if event.key == py.K_RETURN:
                    run = False
                elif event.key == py.K_BACKSPACE:
                    if len(in_string) > 0:
                        in_string = in_string[0:-1]
                else:
                    if len(in_string) < 7:
                        in_string += str(chr(event.key))
        player_response.change_text(in_string)
        py.display.update()
    return in_string
    
py.init()

H, W = 750, 1050
window = py.display.set_mode((W,H))
clock = py.time.Clock()
speed = 3


scene_one(window, clock, speed)
scene_two(window, clock, speed)


