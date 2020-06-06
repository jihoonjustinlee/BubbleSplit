import pygame
import random
import math
pygame.init()
font = pygame.font.Font('fonts/Retro_Gaming.ttf', 20)

#screen
screen_width = 1200
screen_height = 700
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)
background = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))
running = True

#clock
clock = pygame.time.Clock()
fps = 60


#100 x 100
character_sprite = pygame.image.load('images/character_sprite.png')
character = character_sprite.subsurface((0, 0, 100, 100))
character_width = character.get_rect().size[0]
character_height = character.get_rect().size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height
character_speed = 0.5
character_gun = 1
character_left = []
character_right = []
x = 0
for i in range (0, 10):
    character_left.append(character_sprite.subsurface(x, 200, 100, 100))
    character_right.append(character_sprite.subsurface(x, 300, 100, 100))
    x += 100

character_walk_count = 0
character_up = character_sprite.subsurface(0, 400, 80, 100)

#weapons
weapons = []
weapon = pygame.image.load('images/weapon.png')
weapon = pygame.transform.scale(weapon, (20, 60))
weapon_width = weapon.get_rect().size[0]
weapon_height = weapon.get_rect().size[1]
weapon_speed = 20

#balls
ball_default = pygame.image.load('images/ballon.png')
ball_images = []
ball_images.append(pygame.transform.scale(ball_default, (160, 160)))
ball_images.append(pygame.transform.scale(ball_default, (80, 80)))
ball_images.append(pygame.transform.scale(ball_default, (40, 40)))
ball_images.append(pygame.transform.scale(ball_default, (20, 20)))

balls = [
     {
        "image_idx": 0,
        "image": ball_images[0],
        "width": ball_images[0].get_rect().size[0],
        "height": ball_images[0].get_rect().size[1],
        "pos_x": random.randrange(0, screen_width - ball_images[0].get_rect().size[0]),
        "pos_y": 50,
        "move_x": -5,
        "move_y": 5,
        "bounce_up_to": -6
    }
]

#tracking
points = 0
game_over = False
current_stage = 1
points_text = font.render(f'Points: {str(points)}', 1, (0, 0, 0))
points_text_rect = points_text.get_rect()
points_text_width = points_text_rect.size[0]
points_text_height = points_text_rect.size[1]
points_text_x_pos = 10
points_text_y_pos = screen_height - points_text_height - 10

current_stage_text = font.render(f'Stage {str(current_stage)}', 1, (0,0,0))
current_stage_rect = current_stage_text.get_rect()
current_stage_width = current_stage_rect.size[0]
current_stage_height = current_stage_rect.size[1]
current_stage_x_pos = 10
current_stage_y_pos = screen_height - points_text_height - current_stage_height - 10

retry_button = pygame.image.load('images/retry_button.png')
retry_button_rect = retry_button.get_rect()
retry_button_width = retry_button_rect.size[0]
retry_button_height = retry_button_rect.size[1]
retry_button_x_pos = (screen_width / 2) - (retry_button_width/2)
retry_button_y_pos = (screen_height / 2) - (retry_button_height / 2)
retry_button_rect.left = retry_button_x_pos
retry_button_rect.top = retry_button_y_pos

retry_text = font.render("Retry?", 1, (255, 255, 255))
retry_text_rect = retry_text.get_rect()
retry_text_width = retry_text_rect.size[0]
retry_text_height = retry_text_rect.size[1]
retry_text_x_pos = (screen_width / 2) -  (retry_text_width / 2)
retry_text_y_pos = (screen_height / 2) - (retry_text_height / 2)


#items
item = pygame.image.load('images/item.png')
watermelon = pygame.image.load('images/watermelon.png')
watermelon = pygame.transform.scale(watermelon, (60, 60))
orange = pygame.image.load('images/orange.png')
orange = pygame.transform.scale(orange, (60, 60))
machine_gun = pygame.image.load('images/machine_gun.png')
machine_gun = pygame.transform.scale(machine_gun, (60, 60))
shotgun = pygame.image.load('images/shotgun.png')
shotgun = pygame.transform.scale(shotgun, (60, 30))
gatling_gun = pygame.image.load('images/gatling_gun.png')
gatling_gun = pygame.transform.scale(gatling_gun, (60, 50))
item_images = [machine_gun, shotgun, gatling_gun, watermelon, orange]
item_variations = ['machine_gun', 'shotgun', 'gatling_gun', 'watermelon', 'orange']
items = []
item_drop_speed = 3
item_disappear_time = 5000
item_rect = item.get_rect()
item_width = item_rect.size[0]
item_height = item_rect.size[1]
gun_gather_per_stage = 0
gun_ammo = "Infinite"
gun_ammo_text = font.render(f'Ammo: {str(gun_ammo)}', 1, (0, 0, 0))
gun_ammo_text_rect = gun_ammo_text.get_rect()
gun_ammo_text_width = gun_ammo_text_rect.size[0]
gun_ammo_text_height = gun_ammo_text_rect.size[1]
gun_ammo_text_x_pos = 10
gun_ammo_text_y_pos = screen_height - points_text_height - current_stage_height - gun_ammo_text_height - 10


while running:
    dt = clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key or pygame.K_LEFT or pygame.K_RIGHT:
                if event.key != pygame.K_SPACE:
                    character = character_sprite.subsurface(0, 0, 100, 100)
        if game_over == False and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if character_gun == 1:
                    if len(weapons) < 2:
                        weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width/2)
                        weapon_y_pos = screen_height - character_height
                        weapons.append([weapon_x_pos, weapon_y_pos])
                elif character_gun == 2:
                    gun_ammo -= 1
                    if len(weapons) < 9:
                        bullet_middle_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                        bullet_middle_y_pos = screen_height - character_height
                        bullet_left_x_pos = bullet_middle_x_pos - 30
                        bullet_left_y_pos = bullet_middle_y_pos
                        bullet_right_x_pos = bullet_middle_x_pos + 30
                        bullet_right_y_pos = bullet_middle_y_pos
                        weapons.append([bullet_left_x_pos, bullet_left_y_pos])
                        weapons.append([bullet_middle_x_pos, bullet_middle_y_pos])
                        weapons.append([bullet_right_x_pos, bullet_right_y_pos])

                elif character_gun == 3:
                    gun_ammo -= 1
                    weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width/2)
                    weapon_y_pos = screen_height - character_height
                    weapons.append([weapon_x_pos, weapon_y_pos])
                
                if gun_ammo == 0:
                    character_gun = 1
                    gun_ammo = "Infinite"

                gun_ammo_text = font.render(f'Ammo: {str(gun_ammo)}', 1, (0, 0, 0))

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and retry_button_rect.collidepoint(event.pos):
                current_stage = 0
                character_gun = 1
                gun_ammo = "Infinite"
                points_text = font.render(f'Points: {str(points)}', 1, (0, 0, 0))
                gun_ammo_text = font.render(f'Ammo: {str(gun_ammo)}', 1, (0, 0, 0))
                game_over = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        character = character_up
        if character_gun == 4:
            gun_ammo -= 1
            weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width/2)
            weapon_y_pos = screen_height - character_height
            weapons.append([weapon_x_pos, weapon_y_pos])
            if gun_ammo == 0:
                character_gun = 1
                gun_ammo = "Infinite"

            gun_ammo_text = font.render(f'Ammo: {str(gun_ammo)}', 1, (0, 0, 0))

    if pressed[pygame.K_LEFT]:
        character_x_pos -= character_speed * dt
        character = character_left[math.floor(character_walk_count / 2) % 10]
        character_walk_count += 1
    elif pressed[pygame.K_RIGHT]:
        character_x_pos += character_speed * dt
        character = character_right[math.floor(character_walk_count / 2) % 10]
        character_walk_count += 1
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    weapons = [[w[0], w[1] - weapon_speed] for w in weapons if w[1] > 0]
    
    for ball_idx, ball in enumerate(balls):
        if ball['pos_x'] > screen_width - ball['width'] or ball['pos_x'] < 0:
            ball['move_x'] *= -1

        if ball['pos_y'] > screen_height - ball['height']:
            ball['move_y'] = ball['bounce_up_to']
        else:
            ball['move_y'] += 0.05
        ball['pos_y'] += ball['move_y']
        ball['pos_x'] += ball['move_x']
        ball_rect = ball['image'].get_rect()
        ball_rect.left = ball['pos_x']
        ball_rect.top = ball['pos_y']

        if ball_rect.colliderect(character_rect):
            ball_x_comp = ball['pos_x'] + (ball['width'] / 2)
            char_x_comp = character_x_pos + (character_width/2)
            if abs(ball_x_comp - char_x_comp) < 20:
                balls = []
                weapons = []
                items = []  
                points = 0
                gun_gather_per_stage = 0
                game_over = True
           
        for weapon_idx, w in enumerate(weapons):
            weapon_rect = weapon.get_rect()
            weapon_rect.left = w[0]
            weapon_rect.top = w[1]

            if ball_rect.colliderect(weapon_rect):
                points += 300
                points_text = font.render(f'Points: {str(points)}', 1, (0, 0, 0))
                if ball['image_idx'] < 3:
                    new_image_idx = ball['image_idx']+1
                    balls.append({
                        'image_idx': new_image_idx,
                        'image': ball_images[new_image_idx],
                        'width': ball_images[new_image_idx].get_rect().size[0],
                        'height': ball_images[new_image_idx].get_rect().size[1],
                        'pos_x': ball['pos_x'],
                        'pos_y': ball['pos_y'],
                        'move_x': 5,
                        'move_y': -3,
                        'bounce_up_to': -6
                    })
                    balls.append({
                        'image_idx': new_image_idx,
                        'image': ball_images[new_image_idx],
                        'width': ball_images[new_image_idx].get_rect().size[0],
                        'height': ball_images[new_image_idx].get_rect().size[1],
                        'pos_x': ball['pos_x'],
                        'pos_y': ball['pos_y'],
                        'move_x': -5,
                        'move_y': -3,
                        'bounce_up_to': -6
                    })
                else:
                    item_spawn_rand = random.randint(0, 2)
                    item_type_rand = random.randint(0, len(item_variations)-1)
                            
                    if item_spawn_rand == 1:
                        if item_type_rand >= 0 and item_type_rand < 3:
                            gun_gather_per_stage += 1
                            if gun_gather_per_stage > 4:
                                item_type_rand = random.randint(3, 4)
                        if current_stage < 6 and item_type_rand == 2:
                            item_type_rand = 1

                        items.append({
                            'image': item_images[item_type_rand],
                            'image_idx': item_type_rand,
                            'item_name': item_variations[item_type_rand],
                            'width': item_images[item_type_rand].get_rect().size[0],
                            'height': item_images[item_type_rand].get_rect().size[1],
                            'pos_x': ball['pos_x'],
                            'pos_y': ball['pos_y'],
                            'item_spawn_time': pygame.time.get_ticks()
                        })
                del weapons[weapon_idx]
                del balls[ball_idx]

    for item_idx, item in enumerate(items):
        if item['pos_y'] <= screen_height - item['height']:
            item['pos_y'] += item_drop_speed
        else:
            if pygame.time.get_ticks() - item['item_spawn_time'] > item_disappear_time:
                del items[item_idx]
            
        item_rect.left = item['pos_x']
        item_rect.top = item['pos_y']

        if item_rect.colliderect(character_rect):
            if item['item_name'] == 'watermelon':
                points += 300
            elif item['item_name'] == 'orange':
                points += 500
            elif item['item_name'] == 'shotgun':
                character_gun = 2
                gun_ammo = 50
                gun_ammo_text = font.render(f'Ammo: {str(gun_ammo)}', 1, (0, 0, 0))
            elif item['item_name'] == 'machine_gun':
                character_gun = 3
                gun_ammo = 100
                gun_ammo_text = font.render(f'Ammo: {str(gun_ammo)}', 1, (0, 0, 0))
            elif item['item_name'] == 'gatling_gun':
                character_gun = 4
                gun_ammo = 1000
                gun_ammo_text = font.render(f'Ammo: {str(gun_ammo)}', 1, (0, 0, 0))
            del items[item_idx]

        
    if game_over == False and len(balls) == 0:
        if character_gun != 1:
            gun_gather_per_stage = 0
        current_stage += 1
        current_stage_text = font.render(f'Stage {str(current_stage)}', 1, (0,0,0))
        for i in range(current_stage):
            balls.append(
                {
                    "image_idx": 0,
                    "image": ball_images[0],
                    "width": ball_images[0].get_rect().size[0],
                    "height": ball_images[0].get_rect().size[1],
                    "pos_x": random.randrange(0, screen_width - ball_images[0].get_rect().size[0]),
                    "pos_y": 50,
                    "move_x": -5,
                    "move_y": 5,
                    "bounce_up_to": -6
                }
            )
                
    screen.blit(background, (0, 0))
    for w in weapons:
        screen.blit(weapon, (w[0], w[1]))
    for ball in balls:
        screen.blit(ball['image'], (ball['pos_x'], ball['pos_y']))
    for i in items:
        screen.blit(i['image'], (i['pos_x'], i['pos_y']))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(points_text, (points_text_x_pos, points_text_y_pos))
    screen.blit(current_stage_text, (current_stage_x_pos, current_stage_y_pos))
    screen.blit(gun_ammo_text, (gun_ammo_text_x_pos, gun_ammo_text_y_pos))
    if game_over == True:
        screen.blit(retry_button, (retry_button_x_pos, retry_button_y_pos))
        screen.blit(retry_text, (retry_text_x_pos, retry_text_y_pos))

    pygame.display.update()

pygame.quit()
