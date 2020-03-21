# -*- coding: utf-8 -*-
"""
    CryptoGame.py ~ Contains loops for each level
    Written by Luke Gorski
"""
import pygame as py
import Core as core
import os

# TODO: Create a function for each level. 


def draw_health(window, humanoid):
        
    width = humanoid.hp
    x = humanoid.x - 30
    y = humanoid.y - 50
    red_rect = py.Rect(x, y, width, 4)
    blk_rect = py.Rect(x - 5, y - 3 , 110, 10)
    
    if not humanoid.dead:
        py.draw.rect(window, (0,0,0), blk_rect)
    
        if width > 0:
            py.draw.rect(window, (255,0,0), red_rect)

# Level One ~ Haunted Wood Fdorest
def scene_one(window, clock, speed):
    player = core.hero(250,500, H, W, window, speed, 1915, True, 100, 5, "hero", 3, 4, 4)
    robber = core.robber(player, .06, .05, 7, 900, 500, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    scroll = core.scroller(window, player, 'forest1', speed, [robber])
    
    
    
    msg1 = core.sign(window, 200, 400, "Caesar's Forest", "sprites", "sign.png")
    msg2 = core.sign(window, 1500, 400, "Beware of Mad Wizard", "sprites", "sign.png")
    wiz_house = core.scenary(window, 1750, 293, "sprites", "WizardHouse.png")
    wiz_fence = core.scenary(window, 1800, 400, "sprites", "WizardFence.png")
    
    scrolls = [msg1, msg2, wiz_house, wiz_fence]
    
    for scr in scrolls:
        scroll.add_scrollable(scr)
        
    drawers = [scroll, msg1, msg2, wiz_fence, wiz_house, robber, player]
    projectiles = []
    last_attack = 0
    last_jump = 0
    
    success = True
    run = True        
    while run:
        clock.tick(60)    
        
        keys = py.key.get_pressed()
        
        if keys[py.K_d]:
            scroll.move(1)
        if keys[py.K_a]:
            scroll.move(-1)
        if keys[py.K_SPACE]:
            if py.time.get_ticks() - last_jump > 600:
                player.jump()
                last_jump = py.time.get_ticks()
        if keys[py.K_e]:
            if player.true_x >= 1900 and player.true_x <= 1920 and robber.dead:
                run = False
        
        robber.move()
        
        
        if player.is_jump == True:
            player.jump()
        for draw in drawers:
            draw.draw()
        if py.mouse.get_pressed()[0]:
            if py.time.get_ticks() - last_attack > 700:
                throwing_star = core.enemy_projectile(window, player.x, player.y, player.attack_speed, player.last_dir)
                projectiles.append(throwing_star)
                last_attack = py.time.get_ticks()
                
        robb_att = robber.attack()
        if robb_att != -1:
            projectiles.append(robb_att)
            
        deletes = []
        for proj in projectiles:
            if not proj.dead:
                proj.move()
                proj.draw()
            else:
                deletes.append(proj)
        for rm in deletes:
            projectiles.remove(rm)
            
        
        for i in range(len(projectiles)):
            if projectiles[i].rect.colliderect(player.rect):
                if not projectiles[i].player:
                    projectiles[i].dead = True
                    player.hp -= 40
            if projectiles[i].rect.colliderect(robber.rect):
                if projectiles[i].player:
                    projectiles[i].dead = True
                    robber.hp -= 25
        
        
        if player.hp <= 0:
            run = False
            success = False
        if robber.hp <= 0:
            robber.dead = True
        
        draw_health(window, player)
        draw_health(window, robber)
        py.display.update() 
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
                
        
        
    return success
                
# Level Two ~ Wizard's House
def scene_two(window, clock, speed):
    player = core.hero(250,700, H, W, window, speed, 1050, False, 100, 5, "hero", 3, 4, 4)
    background = core.scenary(window, -600, 0, "backgrounds", "WizardHouse.png", conv=True)
    wizard = core.wizard(window, 800, 607, 10)
    
    wizard_dia = [core.scenary(window, 600, 300, 
            "dialogue","wizard_dia_" + str(i) + ".png") 
            for i in range(1,6)]
    hero_dia = [core.scenary(window, 280, 380,
            "dialogue", "hero_dia_" + str(i) + ".png")
            for i in range(1,6)]
    
    # Splice the two lists into one, alternating
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
    
    wizard.turn_around()
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
    hero_right = core.scenary(window, 280, 380, "dialogue", "hero_right_1.png")
    wizard_right.append(hero_right)
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
                if py.time.get_ticks() - last_enter > 500:             
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
                if cur_dia > 3:
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
    
def scene_three(window, clock, speed):
    player = core.hero(500,600, H, W, window, speed, 1915, True, 100, 5, "hero", 3, 4, 4)
    
    # Quick fix. If I were getting paid I'd properly fix this issue, but
    # for school this is fine.
    player.true_x = 250
    
    
    robber1 = core.robber(player, .07, .03, 5, 150, 600, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    robber2 = core.robber(player, .07, .03, 5, 1200, 600, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    robber3 = core.robber(player, .07, .02, 5, 1350, 600, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    
    msg1 = core.sign(window, 350, 500, "Eve's Oasis", "sprites", "sign.png")
    
    eve_house = core.scenary(window, 1730, 320, "sprites", "eve_house.png")
    
    scrolls = [msg1, eve_house]
    
    robbers = [robber1, robber2, robber3]
    scroll = core.scroller(window, player, 'desert', speed, robbers)
    
    for scroller in scrolls:
        scroll.add_scrollable(scroller)

    drawers = [scroll]
    drawers += scrolls
    drawers.append(eve_house)
    drawers += robbers
    drawers.append(player)
    
    projectiles = []
    
    last_attack = 0
    last_jump = 0
    
    success = True
    
    run = True
    
    while run:
        clock.tick(60)
        keys = py.key.get_pressed()
        if keys[py.K_d]:
            scroll.move(1)
        if keys[py.K_a]:
            scroll.move(-1)
        if keys[py.K_SPACE]:
            if py.time.get_ticks() - last_jump > 600:
                player.jump()
                last_jump = py.time.get_ticks()
        if keys[py.K_e]:
            if player.true_x > 1912 and len(robbers) == 0:
                run = False
        
        dead_robbers = []
        for robber in robbers:
            robb_att = robber.attack()
            if robb_att != -1:
                projectiles.append(robb_att)
            
            if robber.hp <= 0:
                robber.dead = True
                dead_robbers.append(robber)
            robber.move()
        
        for robber in dead_robbers:
            robbers.remove(robber)
        if player.is_jump == True:
            player.jump()
        for draw in drawers:
            draw.draw()
        if py.mouse.get_pressed()[0]:
            if py.time.get_ticks() - last_attack > 700:
                throwing_star = core.enemy_projectile(window, player.x, player.y, player.attack_speed, player.last_dir)
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
            
        for i in range(len(projectiles)):
            if projectiles[i].rect.colliderect(player.rect):
                if not projectiles[i].player:
                    projectiles[i].dead = True
                    player.hp -= 30
            for robber in robbers:
                if projectiles[i].rect.colliderect(robber.rect):
                    if projectiles[i].player:
                        projectiles[i].dead = True
                        robber.hp -= 40
        if player.hp <= 0:
            run = False
            success = False
        draw_health(window, player)
        
        for robber in robbers:
            draw_health(window, robber)
        py.display.update()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
    return success
        
    
def scene_four(window, clock, speed):
    player = core.hero(250,500, H, W, window, speed, 1050, False, 100, 5, "hero", 3, 4, 4)
    background = core.scenary(window, 0, 0, "backgrounds", "eve_house.png", conv=True)
    eve = core.eve(player, .07, .03, 5, 800, 450, H, W, window, 1, 1915, True, 100, 5, "eve", 3, 4, 15)
    
    drawers = [background, eve, player]
    
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
        if player.true_x > 500:
            run = False
            
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
def player_died(window, clock, level=1):
    
    death_screen = py.image.load(os.path.join('backgrounds', 'dead_screen_' + str(level) + '.jpg' )).convert()
    run = True
    
    bg = py.Surface(window.get_size())
    
    bg = bg.convert()
    
    while run:
        clock.tick(60)
        bg.fill((0,0,0))
        window.blit(bg, (0,0))
        window.blit(death_screen, (-70,0))
        
        keys = py.key.get_pressed()
        
        if keys[py.K_e]:
            run = False
        
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
            
        py.display.update()
        
        
        
py.init()

H, W = 750, 1050
window = py.display.set_mode((W,H))
clock = py.time.Clock()
speed = 3


success = scene_one(window, clock, speed)

while(success == False):
    player_died(window, clock)
    success = scene_one(window, clock, speed)
scene_two(window, clock, speed)


success = scene_three(window, clock, speed)
while success == False:
    player_died(window, clock, level=2)
    success = scene_three(window, clock, speed)

scene_four(window, clock, speed)