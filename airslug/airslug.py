import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# TODO: vision is to build air run and gun including start menu, score, end screen (win/lose) with restart

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # TODO: make plane helices animated. gif?
        # TODO: remove white spaces to make collision more accurate
        self.surf = pygame.image.load("airslug/assets/sprite/plane.png").convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.surf.get_rect()

    # move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -10)
            move_up_sound.play()
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 10)
            move_down_sound.play()
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(10, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("airslug/assets/sprite/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        # the starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # move the enemy based on speed
    # remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("airslug/assets/sprite/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        #the starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # move the cloud based on a constant speed
    # remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# setup for sounds, defaults are good
pygame.mixer.init()

# initialize pygame
pygame.init()

# setup the clock for a decent framerate
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()

# create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# load and play our background music
# sound source: http://ccmixter.org/files/Apoxode/59262
# license: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("airslug/assets/sfx/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# load all our sound files
# sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("airslug/assets/sfx/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("airslug/assets/sfx/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("airslug/assets/sfx/Collision.ogg")

# set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

running = True

# game loop
while running:
    # look at every event in the queue
    for event in pygame.event.get():
        # did the user hit a key?
        if event.type == pygame.KEYDOWN:
            # was it the Escape key? if so, stop the loop
            if event.key == pygame.K_ESCAPE:
                running = False

        # did the user click the window close button? If so, stop the loop
        elif event.type == pygame.QUIT:
            running = False

        # should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update the position of our enemies and clouds
    enemies.update()
    clouds.update()

    # fill the screen with sky blue
    screen.fill((135, 206, 250))

    # draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # if so, remove the player
        player.kill()

        # stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        # stop the loop
        running = False

    # flip everything to the display
    pygame.display.flip()

    # ensure we maintain a 30 frames per second rate
    clock.tick(30)

# at this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
