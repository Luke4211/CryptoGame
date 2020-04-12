# -*- coding: utf-8 -*-
"""
    CryptoGame.py ~ Contains loops for each level
    Written by Luke Gorski
"""
import pygame as py
import Core as core
import os

H, W = 750, 1050


# TODO: Create a function for each level. 

# TODO: Background music
def draw_health(window, humanoid, king = False):
        
    width = humanoid.hp
    x = humanoid.x - 30
    y = humanoid.y - 50
    red_rect = py.Rect(x, y, width, 4)
    
    w = 110
    if king:
        w = 160
    blk_rect = py.Rect(x - 5, y - 3 , w, 10)
    
    if not humanoid.dead:
        py.draw.rect(window, (0,0,0), blk_rect)
    
        if width > 0:
            py.draw.rect(window, (255,0,0), red_rect)

def draw_cooldown(window, humanoid):
    
    width = humanoid.cooldown() // 30
    
    x = humanoid.x - 30
    y = humanoid.y - 65
    blue_rect = py.Rect(x, y, width, 4)
    blk_rect = py.Rect(x - 5, y - 3 , 110, 10)
    
    if not humanoid.dead:
        py.draw.rect(window, (0,0,0), blk_rect)
    
        if width > 0:
            py.draw.rect(window, (0,0,255), blue_rect)
# Level One ~ Haunted Wood Fdorest
def scene_one(window, clock, speed):
    player = core.hero(250,500, H, W, window, speed, 1915, True, 100, 5, "hero", 3, 4, 4)
    robber = core.robber(player, .06, .05, 7, 900, 500, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    scroll = core.scroller(window, player, 'forest1', speed, [robber])
    
    arrow = core.arrow(window, 1760, 300)
    
    msg1 = core.sign(window, 200, 400, "Caesar's Forest", "sprites", "sign.png")
    msg2 = core.sign(window, 1500, 400, "Beware of Mad Wizard", "sprites", "sign.png")
    wiz_house = core.scenary(window, 1750, 293, "sprites", "WizardHouse.png")
    wiz_fence = core.scenary(window, 1800, 400, "sprites", "WizardFence.png")
    
    scrolls = [msg1, msg2, wiz_house, wiz_fence, arrow]
    
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
                throwing_star = core.projectile(window, player.x, player.y, player.attack_speed, player.last_dir)
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
                if projectiles[i].player and not robber.dead:
                    projectiles[i].dead = True
                    robber.hp -= 25
        
        
        if player.hp <= 0:
            run = False
            success = False
        if robber.hp <= 0:
            robber.dead = True
        
        if robber.dead:
            arrow.bounce()
            arrow.draw()
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
   
    last_jump = 0
    run = True   
    while run:
        clock.tick(60)
        
        keys = py.key.get_pressed()
        
        if keys[py.K_d]:
            player.move(1)
        if keys[py.K_a]:
            player.move(-1)
        if keys[py.K_SPACE]:
            if py.time.get_ticks() - last_jump > 600:    
                player.jump()       
                last_jump = py.time.get_ticks()
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
    
    arrow = core.arrow(window, 1810, 350)
    msg1 = core.sign(window, 350, 500, "Eve's Oasis", "sprites", "sign.png")
    
    eve_house = core.scenary(window, 1730, 320, "sprites", "eve_house.png")
    
    scrolls = [msg1, eve_house, arrow]
    
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
                throwing_star = core.projectile(window, player.x, player.y, player.attack_speed, player.last_dir)
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
            
        if len(robbers) == 0:
            arrow.bounce()
            arrow.draw()
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
    context_screen = py.image.load(os.path.join('backgrounds', 'eve_context' +  '.png' )).convert()
    eve = core.eve(player, .07, .02, 5, 800, 450, H, W, window, 1, 1915, False, 100, 5, "eve", 4, 4, 15, hitbox=90)
    
    eve_dia = [core.scenary(window, 400, 100, 
            "dialogue","eve_dia_" + str(i) + ".png") 
            for i in range(1,3)]
    hero_dia = [core.scenary(window, 260, 130,
            "dialogue", "hero_dia_" + str(i) + ".png")
            for i in range(6,8)]
    
    dialogue = [None]*(len(eve_dia) + len(hero_dia))
    dialogue[::2] = eve_dia
    dialogue[1::2] = hero_dia    
    drawers = [background, eve, player]
    
    last_jump = 0
    run = True
    while run:
        clock.tick(60)
        
        keys = py.key.get_pressed()
        
        if keys[py.K_d]:
            player.move(1)
        if keys[py.K_a]:
            if player.x > 240:
                player.move(-1)
        if keys[py.K_SPACE]:
            if py.time.get_ticks() - last_jump > 600:
                player.jump()
                last_jump = py.time.get_ticks()     
        if player.x > 550:
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

    while eve.x > 650:
        clock.tick(60)
        
        eve.move_njump()
        
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
      
        dialogue[cur_dia].draw()
        if player.is_jump == True:
            player.jump()
            
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
    
    
    story_screen(window, context_screen, clock)
    #TODO: Add another scene of dialogue before the boss fight
    #TODO: Go back to scene 2 and implement last_jump
    arrow = core.arrow(window, 930, 300)
    
    projectiles = []
    last_attack = 0
    last_jump = 0 
    success = True
    eve.aggro = True
    run = True

    while run:
        clock.tick(60)
        keys = py.key.get_pressed()
        
        if keys[py.K_d]:
            if player.x < 970:    
                player.move(1)
        if keys[py.K_a]:
            if player.x > 240:
                player.move(-1)
        if keys[py.K_SPACE]:
            if py.time.get_ticks() - last_jump > 600:
                player.jump()
                last_jump = py.time.get_ticks()  
        
        if keys[py.K_e]:
            if player.x > 950 and eve.dead:
                run = False
        if player.is_jump == True:
            player.jump()
        
        if eve.hp > 0:
            eve.move()
            #TODO: Undo the mess below
            eve_att = [eve.attack(), eve.rockfall()]
            
            for att in eve_att:
                if att != -1:
                    projectiles.append(att)

            
        else:
            eve.dead = True
            
        if py.mouse.get_pressed()[0]:
            if py.time.get_ticks() - last_attack > 700:
                throwing_star = core.projectile(window, player.x, player.y, player.attack_speed, player.last_dir)
                projectiles.append(throwing_star)
                last_attack = py.time.get_ticks()
        
        for draw in drawers:
            draw.draw()
        
        
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
                    player.hp -= 24
            if projectiles[i].rect.colliderect(eve.rect):
                if projectiles[i].player:
                    projectiles[i].dead = True
                    eve.hp -= 10

        
        if player.hp <= 0:
            run = False
            success = False
        
        draw_health(window, player)
        draw_health(window, eve)
        
        if eve.dead:
            arrow.bounce()
            arrow.draw()
       
        py.display.update() 
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
        
    return success

def scene_four_challenge(window, clock):
    screen = py.image.load(os.path.join('backgrounds', 'vigenere_5.png'))
    bg = py.Surface(window.get_size()).convert()
    bg.fill((0,0,0))
    window.blit(bg, (0,0))
    font = py.font.Font(os.path.join('font', 'AncientModernTales.ttf'), 40)
    text = font.render('', True, (255,255,255) )
    
    text_box = text.get_rect()
    
    text_box.center = (500, 470)
    in_string = ""
    run = True
    while run:
        clock.tick(60)
        window.blit(screen, (0,100))
        window.blit(text, text_box)
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
                    if len(in_string) < 10:
                        in_string += str(chr(event.key))
        text = font.render(in_string, True, (255,255,255))
        py.display.update()
    return in_string

def spawn_robbers(window, player, drawers, robbers, scroll=None, y=600):
    x1 = player.x - 300
    x2 = player.x + 300
    
    robber1 = core.robber(player, .07, .03, 5, x1, y, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    robber2 = core.robber(player, .07, .02, 5, x2, y, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    
    robbs = [robber1, robber2]
    if not scroll == None:
        scroll.add_enemies(robbs)
    drawers.extend(robbers)
    if scroll == None:
        robbers += robbs
def scene_five(window, clock, speed):
    player = core.hero(500,600, H, W, window, speed, 1915, True, 100, 5, "hero", 3, 4, 4, deflect = True)
    robber1 = core.robber(player, .07, .02, 5, 150, 600, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    robber2 = core.robber(player, .07, .02, 5, 1300, 600, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    robber3 = core.robber(player, .07, .02, 5, 0, 600, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
    
    arrow = core.arrow(window, 1965, 380)
    
    msg1 = core.sign(window, 350, 500, "Royal Swamp", "sprites", "sign.png")
     
    castle = core.scenary(window, 1790, 240, "sprites", "castle.png")
    
    scrolls = [msg1, castle, arrow]
    robbers = [robber1, robber2, robber3]
    scroll = core.scroller(window, player, 'swamp', speed, robbers)
    
    for scroller in scrolls:
        scroll.add_scrollable(scroller)
        
    drawers = [scroll]
    drawers += scrolls
    drawers.append(castle)
    drawers += robbers
    drawers.append(player)
    
    projectiles = []
    
    last_attack = 0
    last_jump = 0
    
    first_wave = True
    
    success = True
    run = True
    while run:
        clock.tick(60)
        
        if len(robbers) == 0 and first_wave == True:
            first_wave = False
            spawn_robbers(window, player, drawers, robbers, scroll=scroll)
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
                
                if player.hp < 100:
                    if player.hp + 15 > 100:
                        player.hp = 100
                    else:
                        player.hp += 15
            robber.move()
        
        for robber in dead_robbers:
            robbers.remove(robber)
        if player.is_jump == True:
            player.jump()
        for draw in drawers:
            draw.draw()
        if py.mouse.get_pressed()[0]:
            if py.time.get_ticks() - last_attack > 700:
                throwing_star = core.projectile(window, player.x, player.y, player.attack_speed, player.last_dir)
                projectiles.append(throwing_star)
                last_attack = py.time.get_ticks()
        if py.mouse.get_pressed()[2]:
            if player.cooldown() <= 0:
                player.deflect()
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
                    if not player.deflecting:
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
        draw_cooldown(window, player)
        for robber in robbers:
            draw_health(window, robber)
        
        if len(robbers) == 0:
            arrow.bounce()
            arrow.draw()
        py.display.update()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
    return success

def scene_six(window, clock, speed):
    player = core.hero(351,500, H, W, window, speed, 1050, False, 100, 5, "hero", 3, 4, 4, deflect = True)
    background = core.scenary(window, 0, 0, "backgrounds", "showdown.png", conv=True)   
    king = core.king(player, .07, .02, 5, 800, 470, H, W, window, 2, 1915, False, 150, 6, "king_charge", 2, 6, 4, hitbox=60)
    
    #TODO: Add dialogue
    drawers = [background, king, player]
    last_jump = 0
    run = True 
    #TODO: Add dialogue scene here
    
    projectiles = []
    robbers = []
    last_attack = 0
    last_jump = 0
    success = True
    king.aggro = True
    king.idle = False
    
    rock_count = 1
    last_spawn = py.time.get_ticks()
    run = True
    
    while run:
        clock.tick(60)
        keys = py.key.get_pressed()
        
        if keys[py.K_d]:
            if player.x < 820:    
                player.move(1)
        if keys[py.K_a]:
            if player.x > 350:
                player.move(-1)
        if keys[py.K_SPACE]:
            if py.time.get_ticks() - last_jump > 600:
                player.jump()
                last_jump = py.time.get_ticks()  
        
        if keys[py.K_e]:
            if player.x > 950 and king.dead:
                run = False
        if player.is_jump == True:
            player.jump()
            
        dead_robbers = []
        for robber in robbers:
            robb_att = robber.attack()
            if robb_att != -1:
                projectiles.append(robb_att)
            
            if robber.hp <= 0:
                robber.dead = True
                dead_robbers.append(robber)
                if player.hp < 100:
                    if player.hp + 15 > 100:
                        player.hp = 100
                    else:
                        player.hp += 15
            robber.move()
        
        for robber in dead_robbers:
            robbers.remove(robber)
        
        king.move()
        k_att = king.attack()
        if k_att:
            if not player.deflecting:
                player.hp -= 30
        if (py.time.get_ticks() - last_spawn) > 6000 and king.hp > 0:
            
            x1 = player.x - 300
            x2 = player.x + 300
    
            robber1 = core.robber(player, .07, .02, 5, x1, 500, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
            robber2 = core.robber(player, .07, .02, 5, x2, 500, H, W, window, 1, 1915, True, 100, 5, "robber", 3, 4, 15)
            robb = [robber1, robber2]
            drawers.extend(robb)
            robbers.extend(robb)
            last_spawn = py.time.get_ticks()
            
        
        for draw in drawers:
            draw.draw()
        
        if py.mouse.get_pressed()[0]:
            if py.time.get_ticks() - last_attack > 500:
                throwing_star = core.projectile(window, player.x, player.y, player.attack_speed, player.last_dir)
                projectiles.append(throwing_star)
                last_attack = py.time.get_ticks()
        if py.mouse.get_pressed()[2]:
            if player.cooldown() <= 0:
                player.deflect()
            
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
                    if not player.deflecting:
                        player.hp -= 15
                        king.hp += 5
            if projectiles[i].rect.colliderect(king.rect):
                if projectiles[i].player:
                    projectiles[i].dead = True
                    king.hp -= 7
            
            for robber in robbers:
                if projectiles[i].rect.colliderect(robber.rect):
                    if projectiles[i].player:
                        projectiles[i].dead = True
                        robber.hp -= 50
            
        if player.hp <= 0:
            run = False
            success = False
        if king.hp <= 0:
            king.hp = 0
            king.idle = True
            king.aggro = True
        else:
            king.idle = False
            king.aggro = True
            draw_health(window, king, king = True)
            
            if rock_count < 5:
                
                rock = king.rockfall(rock_count)
                if rock != -1:
                    rock_count += 1
            elif rock_count > 8:
                rock_count = 1
                rock = king.rockfall()
            else:
                rock = king.rockfall()
                if rock != -1:
                    rock_count += 1
            if rock != -1:
                projectiles.append(rock)
            
        draw_health(window, player)
        draw_cooldown(window, player)
        
        for robber in robbers:
            draw_health(window, robber)
        py.display.update() 
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
    return success
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
        
def story_screen(window, image, clock):
    run = True
    cur_t = py.time.get_ticks()
    bg = py.Surface(window.get_size()).convert()
    bg.fill((0,0,0))
    window.blit(bg, (0,0))
    while run:
        clock.tick(60)
        window.blit(image, (0,100))
        keys = py.key.get_pressed()
        
        if keys[py.K_e] and py.time.get_ticks() - cur_t > 600:
            run = False
            
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()
        py.display.update()
        