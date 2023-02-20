import pygame, os, sys, random, time, math
from pygame.locals import *
from button import Button
from saving import load_save, write_save

pygame.init()
SAVE = load_save()
global RELOAD
RELOAD = SAVE["RELOAD"]
global HEALTH
BASE_HEALTH = SAVE["HEALTH"]
global SIZE
SIZE = WIDTH, HEIGHT = (800, 630)
FONT = pygame.font.SysFont('bahnschrift bold', 24)
FONT2 = pygame.font.SysFont('arial bold', 24)
DISPLAY = pygame.display.set_mode(SIZE)
global BG
BG = pygame.image.load(os.path.join('Assets', 'Background.png')).convert()
BG = pygame.transform.scale(BG,(WIDTH, HEIGHT))
def get_font(size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)
global COIN_COUNT
COIN_COUNT = SAVE["COIN_COUNT"]
def main_menu():
    write_save({"HEALTH": BASE_HEALTH, "RELOAD": RELOAD, "COIN_COUNT": COIN_COUNT})
    while True:
        DISPLAY.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(65).render("MAIN MENU", True, "#d000dd")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load(os.path.join('Assets',"Play Rect.png")), pos=(WIDTH//2, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#000000", hovering_color="White")
        SHOP_BUTTON = Button(image=pygame.image.load(os.path.join('Assets',"Play Rect.png")), pos=(WIDTH//2, 400), 
                            text_input="SHOP", font=get_font(75), base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(os.path.join('Assets',"Quit Rect.png")), pos=(WIDTH//2, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#000000", hovering_color="White")

        DISPLAY.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SHOP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(DISPLAY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if SHOP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shop()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
def play():
    FPS = pygame.time.Clock()
    global COIN_COUNT
    global BASE_HEALTH
    global WIDTH
    global HEIGHT
    DISPLAY = pygame.display.set_mode(SIZE)
    FPS = pygame.time.Clock()
    BASE_SPEED = 6
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    RED_OVERLAY = (255, 50, 50)
    global BG
    COIN = pygame.image.load(os.path.join('Assets', 'Coin.png')).convert_alpha()
    global RELOAD
    ZOMBIE_RELOAD = 3000
    Z_DEATH = pygame.mixer.Sound(os.path.join('Assets','zombie_death.wav'))
    Z_DEATH.set_volume(0.2)
    pygame.mixer.music.load(os.path.join('Assets','bg_music.wav'))
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.1)
    class Character(pygame.sprite.Sprite):
        def __init__(self, type):
            super().__init__()
            self.walk_anim = [
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run1.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run2.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run3.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run4.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run5.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run6.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run7.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run8.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run9.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run10.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run11.png")).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', type, f"{type}_run12.png")).convert_alpha(), (64, 64))
            ]
            self.surface = pygame.Surface((48, 48))
            self.direction = 1
            self.step_count = 0
        
    bullets = pygame.sprite.Group()
    
    class Player(Character):
        def __init__(self):
            Character.__init__(self, "Player")
            self.hurt = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Player", "Player_hurt.png")).convert_alpha(), (64, 64))
            self.rect = self.surface.get_rect(center = (WIDTH/2, HEIGHT/2))
            self.x_speed = BASE_SPEED
            self.y_speed = BASE_SPEED
            self.health = BASE_HEALTH

        def move(self):
            pressed_keys = pygame.key.get_pressed()

            if self.rect.left > 0 and pressed_keys[K_a]:
                if self.direction == 1:
                    self.step_count = 0
                self.direction = 0
                self.step_count += 1
                self.rect.move_ip(-BASE_SPEED, 0)

            if self.rect.right < WIDTH and pressed_keys[K_d]:
                if self.direction == 0:
                    self.step_count = 0
                self.direction = 1
                self.step_count += 1
                self.rect.move_ip(BASE_SPEED, 0)

            if self.rect.top > 0 and pressed_keys[K_w]:
                self.rect.move_ip(0, -BASE_SPEED)
                self.step_count += 1

            if self.rect.bottom < HEIGHT and pressed_keys[K_s]:
                self.rect.move_ip(0, BASE_SPEED)
                self.step_count += 1

            if self.step_count >= 47:
                self.step_count = 0

        def shoot(self):
            pos = pygame.mouse.get_pos()
            bullet = Bullet(self.rect.centerx, self.rect.centery, pos[0], pos[1])
            bullets.add(bullet)
        

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, startx, starty, mousex, mousey):
            super().__init__()
            self.x = startx
            self.y = starty
            self.radius = 5
            self.color = (255, 0, 0) 
            self.speed = 15
            dx = mousex - startx
            dy = mousey - starty
            self.angle = math.atan2(dy, dx)
            self.surface = pygame.Surface((10, 10))
        def update(self):
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed
            self.rect = self.surface.get_rect(center = (self.x, self.y))
            if (self.rect.right > WIDTH) or (self.rect.left < 0):
                self.kill
            if (self.rect.bottom > HEIGHT) or (self.rect.top < 0):
                self.kill
        def draw(self, surface):
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.x = random.randint(50, WIDTH-50)
            self.y = random.randint(75,HEIGHT-75)
            self.img = COIN
            self.surface = pygame.Surface((16, 16))
            self.rect = self.surface.get_rect(center = (self.x, self.y))

        

    class Zombie(Character):
        def __init__(self):
            Character.__init__(self, "Chiclen")        
            self.rect = self.surface.get_rect(center = (random.randint(50, WIDTH-50), random.randint(75,HEIGHT-75)))
            self.x_speed = random.randint(1,5)
            self.y_speed = random.randint(1,5)

        def move(self):
            if self.step_count >= 47:
                self.step_count = 0

            self.rect.move_ip(self.x_speed, self.y_speed)

            if (self.rect.right > WIDTH) or (self.rect.left < 0):
                self.x_speed *= -1
                self.direction *= -1

            if (self.rect.bottom > HEIGHT) or (self.rect.top < 0):
                self.y_speed *= -1
                

            self.step_count += 1
    SCORE = 0
    player = Player()
    zombie = Zombie()
    coin = Coin()
    coins = pygame.sprite.Group()
    zombie_count = 1

    zombies = pygame.sprite.Group()
    zombies.add(zombie)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(zombies, player)
    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, ZOMBIE_RELOAD)
    YES = pygame.USEREVENT + 2
    pygame.time.set_timer(YES, RELOAD)
    SPAWN_COIN = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_COIN, 4000)
    SCORE = 0
    CAN_SHOOT = False
    while True:
        DISPLAY.fill("black")
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if CAN_SHOOT:
                        player.shoot()
                        CAN_SHOOT = False
            if event.type == SPAWN_ENEMY:
                new_zombie = Zombie()
                zombies.add(new_zombie)
                all_sprites.add(new_zombie)
                zombie_count += 1
            if event.type == SPAWN_COIN:
                new_coin = Coin()
                coins.add(new_coin)
            if event.type == YES:
                CAN_SHOOT = True

        DISPLAY.blit(BG, (0, 0))

        for bullet in bullets:
            bullet.draw(DISPLAY)
            bullet.update()
            if pygame.sprite.spritecollide(bullet, zombies, dokill = True):
                Z_DEATH.play()
                COIN_COUNT += 1

        for coin in coins:
            current_coin = coin.img
            DISPLAY.blit(current_coin, coin.rect)

        for character in zombies:
            current_zombie_sprite = character.walk_anim[character.step_count//4]
            if character.direction == -1:
                current_zombie_sprite = pygame.transform.flip(current_zombie_sprite, True, False)
            DISPLAY.blit(current_zombie_sprite, character.rect)

        if pygame.sprite.spritecollideany(player, zombies):
            player.health -= 1
            current_player_sprite = player.hurt
            DISPLAY.fill(RED_OVERLAY, special_flags=BLEND_MULT)
        else:
            current_player_sprite = player.walk_anim[player.step_count//4]
        
        if pygame.sprite.spritecollide(player, coins, dokill = True):
            COIN_COUNT += 1

        pygame.draw.rect(DISPLAY, GREEN, (20, 20, player.health, 20))
        pygame.draw.rect(DISPLAY, RED, (player.health + 20, 20, BASE_HEALTH - player.health, 20))

        SCORE_TEXT = FONT.render(f"TIME SURVIVED: {SCORE//60}", True, (0, 0, 200))
        coin_text = FONT.render(f"COINS: {COIN_COUNT}", True, (0, 0, 200))
        DISPLAY.blit(SCORE_TEXT, (WIDTH//1.5, 20))
        DISPLAY.blit(coin_text, (WIDTH//2, 20))
        if SCORE//60 == 10:
            BG = pygame.image.load(os.path.join('Assets', 'Background_2.jpg')).convert()
            BG = pygame.transform.scale(BG,(WIDTH, HEIGHT))
            pygame.time.set_timer(SPAWN_ENEMY, ZOMBIE_RELOAD-1500)
            pygame.time.set_timer(SPAWN_COIN, 3000)
        else:
            pass
        if player.direction == 0:
            current_player_sprite = pygame.transform.flip(current_player_sprite, True, False)
        DISPLAY.blit(current_player_sprite, player.rect)
        pygame.display.update()

        SCORE += 1
        
        for character in all_sprites:
            character.move()

        if player.health <= 0:
            main_menu()
        FPS.tick(60)

def shop():
    global COIN_COUNT
    global RELOAD
    global BASE_HEALTH
    ERROR = FONT.render(f" ", True, (0, 0, 200))
    while True:
        DISPLAY.blit(BG, (0, 0))
        SHOP_MOUSE_POS = pygame.mouse.get_pos()

        SHOP_TEXT = get_font(100).render("SHOP", True, "#d000dd")
        SHOP_RECT = SHOP_TEXT.get_rect(center=(WIDTH//2, 100))

        COIN_TEXT = get_font(45).render(f"COINS: {COIN_COUNT}", True, (0, 0, 200))
        COIN_RECT = COIN_TEXT.get_rect(center=(WIDTH//2, 175))
        DISPLAY.blit(COIN_TEXT, COIN_RECT)
        DISPLAY.blit(SHOP_TEXT, SHOP_RECT)
        
        UPGRADE_RELOAD = Button(image=pygame.image.load(os.path.join('Assets',"Options Rect.png")), pos=(WIDTH//2, 250), 
                            text_input=f"RELOAD -0.2s({RELOAD/1000}s)", font=get_font(32), base_color="#000000", hovering_color="White")
        UPGRADE_HEALTH = Button(image=pygame.image.load(os.path.join('Assets',"Options Rect.png")), pos=(WIDTH//2, 400), 
                            text_input=f"HEALTH +20({BASE_HEALTH})", font=get_font(32), base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(os.path.join('Assets',"Quit Rect.png")), pos=(WIDTH//2, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#000000", hovering_color="White")
        for button in [UPGRADE_RELOAD, UPGRADE_HEALTH, QUIT_BUTTON]:
            button.changeColor(SHOP_MOUSE_POS)
            button.update(DISPLAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if UPGRADE_RELOAD.checkForInput(SHOP_MOUSE_POS):
                    if COIN_COUNT - 10 < 0:
                        ERROR = get_font(40).render(f"NOT ENOUGH COINS", True, (255, 0, 0))
                    else:
                        COIN_COUNT -= 10
                        RELOAD -= 200
                        if RELOAD < 100:
                            RELOAD = 100
                if UPGRADE_HEALTH.checkForInput(SHOP_MOUSE_POS):
                    if COIN_COUNT - 10 < 0:
                        ERROR = get_font(40).render(f"NOT ENOUGH COINS", True, (255, 0, 0))
                    else:
                        COIN_COUNT -= 10
                        BASE_HEALTH +=20
                if QUIT_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    write_save({"HEALTH": BASE_HEALTH, "RELOAD": RELOAD, "COIN_COUNT": COIN_COUNT})
                    main_menu()
        DISPLAY.blit(ERROR, (0, 0))
        pygame.display.update()

main_menu()