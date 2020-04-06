import collections
import random
import time
from os import path
import pygame

WIDTH = 460
HEIGHT = 600
FPS = 60

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (112, 118, 123)
YELLOW = (255, 255, 0)

# Clock is used to determine thee rate of Frames per second
clock = pygame.time.Clock()

# Directories for images and sound
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# pygame.init() will initiate the game and load all elements needed for game setup
pygame.init()
# must be added when the sounds and explosions are added
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Game images
background = pygame.image.load(path.join(img_dir, "night.jpg")).convert()
background = pygame.transform.scale(background, (500, 600))
player_img = pygame.image.load(path.join(img_dir, "ship2.png")).convert_alpha()
player_bullet_img = pygame.image.load(path.join(img_dir, "rocket.png")).convert_alpha()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "bullet_enemy.png")).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (20, 20))
player_mini_img.set_colorkey(BLACK)
player_img_bulletstop = pygame.image.load(path.join(img_dir, "ship2BulletStop.png")).convert_alpha()
player_img_godmode = pygame.image.load(path.join(img_dir, "ship2GodMode.png")).convert_alpha()
player_ultimate_img = pygame.image.load(path.join(img_dir, "ult.png")).convert_alpha()
barrier_100hp_img = pygame.image.load(path.join(img_dir, "barrier_hp_100.png")).convert_alpha()
barrier_75hp_img = pygame.image.load(path.join(img_dir, "barrier_hp_75.png")).convert_alpha()
barrier_50hp_img = pygame.image.load(path.join(img_dir, "barrier_hp_50.png")).convert_alpha()
barrier_25hp_img = pygame.image.load(path.join(img_dir, "barrier_hp_25.png")).convert_alpha()

# load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
death_sound = pygame.mixer.Sound(path.join(snd_dir, 'Death.wav'))
enemy_shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'EnemyShoot.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
pygame_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))

# ----------- Function used for drawing text on screen ------------
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# -----------------------------------------------------------------

# ----------------- draw function for lives -----------------------
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 25 * i
        img_rect.y = y + 10
        surf.blit(img, img_rect)


# -----------------------------------------------------------------

def score(s):
    if s < 0:
        score.x = 0
    else:
        score.x += s
        return score.x


score.x = 0


def level(L):
    if L < 0:
        level.x = 0
    else:
        level.x += L
        return level.x


level.x = 0

# --------------------- make enemies ------------------------------
enemy_spawn_positions = []
x_start = 20
x_end = 450
while x_start <= x_end:
    enemy_spawn_positions.append(x_start)
    x_start += 40
rows_of_enemies = 8
enemies = []
enemiesCopy = []


def make_Enemies():
    y = 50
    count = 0
    for i in range(rows_of_enemies):
        for index in enemy_spawn_positions:
            if i <= 2:
                enemy = Aliens(index, y, 1)
            elif i >= 2 and i < 5:
                enemy = Aliens(index, y, 2)
            else:
                enemy = Aliens(index, y, 3)
            enemies.append(enemy)
            enemiesCopy.append(enemy)
        y = y + 30
    for i in enemies:
        all_sprites.add(i)
        aliens.add(i)


# -----------------------------------------------------------------
def make_barriers():
    if player.difficulty == 0:
        barrier_start = 25
        for i in range(5):
            b = Barrier(barrier_start, 500)
            barriers.add(b)
            all_sprites.add(b)
            barrier_start += 90
    elif player.difficulty == 1:
        barrier_start = 95
        for i in range(3):
            b = Barrier(barrier_start, 500)
            barriers.add(b)
            all_sprites.add(b)
            barrier_start += 110
    elif player.difficulty == 2:
        barrier1 = Barrier(205, 500)
        barriers.add(barrier1)
        all_sprites.add(barrier1)


def reset_barriers(creation_toggle):
    for barrier in barriers:
        all_sprites.remove(barrier)
        barriers.remove(barrier)
    if creation_toggle:
        make_barriers()


def reset_enemies():
    if (level(0) + 1) <= 1:
        reset_barriers(True)
        for enemy in enemiesCopy:
            enemy.rect.x = enemy.originX
            enemy.rect.y = enemy.originY
            enemy.speedx = 1
            enemy.is_dead = False
            enemies.append(enemy)
            all_sprites.add(enemy)
            aliens.add(enemy)
    elif (level(0) + 1) >= 2:
        reset_barriers(True)
        for enemy in enemiesCopy:
            random_enemy_type = random.randint(1, 9)
            enemy.set_enemy_type(random_enemy_type)
            enemy.enemy_type = random_enemy_type
            enemy.rect.x = enemy.originX
            enemy.rect.y = enemy.originY
            enemy.speedx = 1
            enemy.is_dead = False
            enemies.append(enemy)
            all_sprites.add(enemy)
            aliens.add(enemy)


# --------- this block is for when the game level changes ---------
def level_change():
    alive = True
    start_time = int(time.time()) + 5
    player.rect.centerx = WIDTH / 2
    player.rect.bottom = HEIGHT - 30
    while alive:
        passed_time = start_time - int(time.time())
        if passed_time == 0:
            alive = False
        screen.fill(BLACK)
        draw_text(screen, "LEVEL COMPLETED!", 40, WIDTH / 2, HEIGHT / 2, YELLOW)
        draw_text(screen, "Next level in " + str(passed_time) + " seconds", 40, WIDTH / 2, HEIGHT / 3, YELLOW)
        pygame.display.update()
        pygame.display.flip()
    screen.fill(BLACK)
    pygame.display.update()
    pygame.display.flip()
    reset_enemies()
    game_loop()


# -----------------------------------------------------------------

# ---- this block is for the start screen and to begin new levels ----
def show_go_screen():
    screen.fill(BLACK)
    draw_text(screen, "SPACE INVADERS!", 50, WIDTH / 2, HEIGHT / 6, YELLOW)
    draw_text(screen, "Arrow keys to move, SPACE to fire weapon", 22, WIDTH / 2, HEIGHT / 3, WHITE)
    draw_text(screen, "Level: " + str(level(1)), 40, WIDTH / 2, HEIGHT / 2 - 40, RED)
    pygame.display.flip()
    pygame.time.wait(2000)


# ---------------------------------------------------------------------
def show_scores(current_score):
    f = open("High_Scores.txt", "w+")
    f.write("")
    top_scores[Score(username)] = current_score
    sorted_tuple = sorted(top_scores.items(), key=lambda kv: kv[1])
    sorted_scores = collections.OrderedDict(sorted_tuple)
    count = 1
    height = 0
    for key in reversed(sorted_scores.copy()):
        if count <= 5:
            f.write("%s %d\n" % (key.name, sorted_scores[key]))
            draw_text(screen, "%d. %s: %d" % (count, key.name, sorted_scores[key]), 22, WIDTH / 2, HEIGHT / 2 + height,
                      WHITE)
            height += 30
        else:
            del sorted_scores[key]
        count += 1
    update_scores(sorted_scores)
    f.close()


def update_scores(sorted):
    top_scores = sorted


class Score(object):
    def __init__(self, name):
        self.name = name


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (25, 25))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 3)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 30
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.ultimateSelected = 2
        self.ultThreshold = 0
        self.ultReady = False
        self.ultUsed = False
        self.godMode = False
        self.zawarudo = False
        self.kills = 0
        self.user = "SI-Player"
        self.difficulty = 0

    def set_threshold(self):
        if self.ultimateSelected == 0:
            self.ultThreshold = 13
        elif self.ultimateSelected == 1:
            self.ultThreshold = 15
        elif self.ultimateSelected == 2:
            self.ultThreshold = 20

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1800:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30
        self.speedx = 0

        if self.ultReady:
            draw_text(screen, "Press Q for Ultimate", 20, 95, 35, YELLOW)
        else:
            draw_text(screen, "Ultimate Not Ready", 20, 95, 35, YELLOW)

        if self.hidden:
            keystate = pygame.K_DOWN
            for self in enemy_bullets:
                self.kill()
            for self in player_bullets:
                self.kill()
        else:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_q]:
                if self.ultReady:
                    self.ultUsed = True
                    self.ultReady = False
                    if self.ultimateSelected == 0:
                        self.multi_bullet()
                    elif self.ultimateSelected == 1:
                        self.invincible()
                    elif self.ultimateSelected == 2:
                        self.za_warudo()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            if keystate[pygame.K_SPACE]:
                self.shoot()
            self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, False)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def multi_bullet(self):
        bullet1 = Bullet(self.rect.centerx, self.rect.top - 25, True)
        bullet2 = Bullet(self.rect.centerx - 50, self.rect.top, True)
        bullet3 = Bullet(self.rect.centerx + 50, self.rect.top, True)
        bullet4 = Bullet(self.rect.centerx - 100, self.rect.top + 25, True)
        bullet5 = Bullet(self.rect.centerx + 100, self.rect.top + 25, True)

        all_sprites.add(bullet1)
        player_bullets.add(bullet1)
        all_sprites.add(bullet2)
        player_bullets.add(bullet2)
        all_sprites.add(bullet3)
        player_bullets.add(bullet3)
        all_sprites.add(bullet4)
        player_bullets.add(bullet4)
        all_sprites.add(bullet5)
        player_bullets.add(bullet5)

    def invincible(self):
        self.godMode = True
        self.image = pygame.transform.scale(player_img_godmode, (25, 25))

    def undo_invincible(self):
        self.godMode = False
        self.image = pygame.transform.scale(player_img, (25, 25))

    def za_warudo(self):
        self.zawarudo = True
        self.image = pygame.transform.scale(player_img_bulletstop, (25, 25))

    def undo_za_warudo(self):
        self.zawarudo = False
        self.kills = 0
        self.image = pygame.transform.scale(player_img, (25, 25))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, isUltimate):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_bullet_img
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 6)
        self.rect.x = x - 9
        self.rect.y = y - 10
        self.speedy = -4
        self.isUltimate = isUltimate
        if self.isUltimate:
            self.image = player_ultimate_img

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(barrier_100hp_img, (50, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_destroyed = False
        self.radius = int(self.rect.width / 2)
        self.health = 100

    def update(self):
        if 50 < self.health <= 75:
            self.image = pygame.transform.scale(barrier_75hp_img, (50, 25))
        elif 25 < self.health <= 50:
            self.image = pygame.transform.scale(barrier_50hp_img, (50, 25))
        elif self.health <= 25:
            self.image = pygame.transform.scale(barrier_25hp_img, (50, 25))


class Aliens(pygame.sprite.Sprite):

    def __init__(self, x, y, enemy_type):
        pygame.sprite.Sprite.__init__(self)
        self.enemy_type = enemy_type
        filename = 'enemy{}.png'.format(self.enemy_type)
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        self.image = img
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 3)
        self.rect.x = x
        self.rect.y = y
        self.speedx = 1
        self.score = 15
        self.zawarudo = False
        self.is_dead = False
        self.originX = x
        self.originY = y
        self.state = False
        if self.enemy_type == 11:
            self.score = 1000

        for self in enemies:
            if self.enemy_type == 1:
                self.score = 25
            if self.enemy_type == 2:
                self.score = 15
            if self.enemy_type == 3:
                self.score = 10

    def update(self):
        if not self.zawarudo:
            self.rect.x += self.speedx

        if not self.state:
            if self.rect.x > WIDTH - 15:
                self.rect.x = WIDTH - 15
                for enemy in enemies:
                    enemy.speedx *= -1
                    enemy.rect.y += 5
            if self.rect.x < 0:
                if self.enemy_type == 11:
                    self.is_dead = True
                    all_sprites.remove(self)
                    aliens.remove(self)
                    enemies.remove(self)
                else:
                    self.rect.x = 0
                    for enemy in enemies:
                        enemy.speedx *= -1
                        enemy.rect.y += 5
        else:
            for enemy in enemies:
                if enemy.rect.x > WIDTH - 15:
                    enemy.rect.x = WIDTH - 15
                    enemy.speedx *= -1
                    enemy.rect.y += 5
                if enemy.rect.x < 0:
                    if enemy.enemy_type == 11:
                        enemy.is_dead = True
                        all_sprites.remove(enemy)
                        aliens.remove(enemy)
                        enemies.remove(enemy)
                    else:
                        enemy.rect.x = 0
                        enemy.speedx *= -1
                        enemy.rect.y += 5

    def shoot(self):
        if not self.zawarudo:
            bullet = EnemyBullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            enemy_shoot_sound.play()

    def set_enemy_type(self, enemy_type):
        filename = 'enemy{}.png'.format(enemy_type)
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        self.image = img
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet_img
        self.image = pygame.transform.scale(self.image, (20, 30))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 6)
        self.rect.x = x - 9
        self.rect.y = y - 10
        self.speedy = 4
        self.zawarudo = False

    def update(self):
        if not self.zawarudo:
            self.rect.y += self.speedy
        if self.rect.y > 600:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = explosion_anim[self.type][8]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# ---------------- image loading for explosions -----------------------
explosion_anim = {}
explosion_anim['aliens'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img.set_colorkey(BLACK)
    img_aliens = pygame.transform.scale(img, (16, 16))
    explosion_anim['aliens'].append(img_aliens)
    filename = 'sonicExplosion0{}.png'.format(i)
    img_player = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img_player)


# ---------------------------------------------------------------------


def game_loop():
    probability = 0.0
    if player.difficulty == 0:
        probability = 0.0001
    elif player.difficulty == 1:
        probability = 0.0004
    elif player.difficulty == 2:
        probability = 0.0007

    running = True
    game_over = True
    displayscore = score(0)
    enemyCount = len(aliens.sprites())
    aliensDead = 0

    ult_counter = 0

    while running:
        if game_over:
            show_go_screen()
            game_over = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if player.kills > 6:
            for alien in aliens:
                alien.zawarudo = False
            for self in enemy_bullets:
                self.zawarudo = False
            player.undo_za_warudo()

        if player.zawarudo and player.kills <= 0:
            for alien in aliens:
                alien.zawarudo = True
            for self in enemy_bullets:
                self.zawarudo = True

        if player.ultUsed:
            if player.ultimateSelected == 0:
                ult_counter = 0
                player.ultUsed = False
            elif player.ultimateSelected == 1 and not player.godMode:
                ult_counter = 0
                player.ultUsed = False
            elif player.ultimateSelected == 2 and not player.zawarudo:
                ult_counter = 0
                player.ultUsed = False

        if not player.ultUsed and ult_counter >= player.ultThreshold:
            player.ultReady = True

        for alien in aliens:
            hits = pygame.sprite.spritecollide(alien, player_bullets, True, pygame.sprite.collide_circle)
            for hit in hits:
                alien.is_dead = True
                explosion_sound.play()
                score(alien.score)
                expl = Explosion(alien.rect.center, 'aliens')
                all_sprites.add(expl)
                all_sprites.remove(alien)
                aliens.remove(alien)
                enemies.remove(alien)
                hit.kill()
                aliensDead += 1
                ult_counter += 1
                if player.zawarudo:
                    player.kills += 1
                if aliensDead == enemyCount / 2:
                    for alien in aliens:
                        alien.speedx *= 2
                        if player.difficulty == 0:
                            probability = 0.0004
                        elif player.difficulty == 1:
                            probability = 0.0007
                        elif player.difficulty == 2:
                            probability = 0.0010
                        boolean_value = random.randint(0, 1)
                        if alien.enemy_type != 11:
                            if boolean_value == 0:
                                alien.speedx *= -1
                            else:
                                alien.speedx *= 1
                        alien.state = True
                    miniBoss = Aliens(0, 20, 11)
                    all_sprites.add(miniBoss)
                    aliens.add(miniBoss)
                    enemies.append(miniBoss)

                if aliensDead == (3 * enemyCount) / 4:
                    for alien in aliens:
                        alien.speedx *= 3 / 2
                        if player.difficulty == 0:
                            probability = .001
                        elif player.difficulty == 1:
                            probability = .004
                        elif player.difficulty == 2:
                            probability = .007

                if aliensDead == enemyCount - 1:
                    for alien in aliens:
                        alien.speedx *= 5 / 3
                        if player.difficulty == 0:
                            probability = .015
                        elif player.difficulty == 1:
                            probability = .045
                        elif player.difficulty == 2:
                            probability = .075

                if not enemies:
                    for self in player_bullets:
                        self.kill()
                    for self in enemy_bullets:
                        self.kill()
                    level_change()

        hits = pygame.sprite.spritecollide(player, aliens, False, pygame.sprite.collide_circle)
        if hits:
            player.hide()
            pygame_die_sound.play()
            death_explosion2 = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion2)
            while death_explosion2.alive():
                death_explosion2.update()
                all_sprites.draw(screen)
                pygame.display.flip()
                for self in player_bullets:
                    self.kill()
                for self in enemy_bullets:
                    self.kill()
                for self in aliens:
                    all_sprites.remove(self)
                    aliens.remove(self)
                    enemies.remove(self)

            running = False
            level(-1)
            score(-1)
            player.lives = 3
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER!", 64, WIDTH / 2, HEIGHT / 6, YELLOW)
            draw_text(screen, "Game loading...", 40, WIDTH / 2, HEIGHT / 2 + 230, RED)
            show_scores(score(0))
            pygame.display.flip()
            pygame.time.wait(3000)
            reset_enemies()
            game_loop()

        hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)
        if hits:
            if player.godMode:
                for hit in hits:
                    hit.kill()
                player.undo_invincible()
            else:
                explosion_sound.play()
                expl = Explosion(player.rect.center, 'player')
                all_sprites.add(expl)
                while expl.alive():
                    expl.update()
                    all_sprites.draw(screen)
                    pygame.display.flip()
                player.hide()
                player.lives -= 1
                for hit in hits:
                    hit.kill()
                for self in enemy_bullets:
                    self.kill()

        if player.lives == 0:
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER!", 64, WIDTH / 2, HEIGHT / 6, YELLOW)
            draw_text(screen, "Game loading...", 40, WIDTH / 2, HEIGHT / 2 - 40, RED)
            show_scores(score(0))
            pygame.display.flip()
            for self in player_bullets:
                self.kill()
            for self in enemy_bullets:
                self.kill()
            for self in aliens:
                all_sprites.remove(self)
                aliens.remove(self)
                enemies.remove(self)
            score(-1)
            level(-1)
            pygame.time.wait(3000)
            running = False
            player.lives = 3
            reset_enemies()
            game_loop()

        for barrier in barriers:
            if barrier.health <= 0:
                barrier.kill()
            hits = pygame.sprite.spritecollide(barrier, enemy_bullets, False, pygame.sprite.collide_circle)
            for hit in hits:
                hit.kill()
                barrier.health -= 26
            hits = pygame.sprite.spritecollide(barrier, aliens, False, pygame.sprite.collide_circle)
            if hits:
                barrier.kill()

        for enemy in enemies:
            fireChance = random.random()
            if (fireChance <= probability):
                x = enemy.rect.x
                y = enemy.rect.y
                enemy_bullet = EnemyBullet(enemy.rect.x, y)
                enemy_bullets.add(enemy_bullet)
                enemy.shoot()
            if enemy.rect.y > player.rect.bottom:
                pygame_die_sound.play()
                death_explosion2 = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion2)
                while death_explosion2.alive():
                    death_explosion2.update()
                    all_sprites.draw(screen)
                    pygame.display.flip()
                for self in player_bullets:
                    self.kill()
                for self in enemy_bullets:
                    self.kill()
                for self in aliens:
                    all_sprites.remove(self)
                    aliens.remove(self)
                    enemies.remove(self)
                level(-1)
                score(-1)
                running = False
                pygame.time.wait(100)
                screen.fill(BLACK)
                draw_text(screen, "GAME OVER!", 64, WIDTH / 2, HEIGHT / 6, YELLOW)
                draw_text(screen, "Game loading...", 40, WIDTH / 2, HEIGHT / 2 - 40, RED)
                show_scores(score(0))
                pygame.display.flip()
                pygame.time.wait(3000)
                reset_enemies()
                game_loop()

        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        draw_text(screen, "Score: " + str(int(score(0))), 20, WIDTH / 10, 10, WHITE)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
        pygame.display.flip()


top_scores = {}
try:
    f = open("High_Scores.txt", "r")
    f1 = f.readlines()
    for line in f1:
        name_score = line.split()
        top_scores[Score(name_score[0])] = int(name_score[1])
except:
    f = open("High_Scores.txt", "w+")
    f.close()

all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
barriers = pygame.sprite.Group()
player = Player()
player.set_threshold()
make_Enemies()
make_barriers()
all_sprites.add(player)
username = player.user
game_loop()
