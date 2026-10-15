import pygame
import settings
import random
import math


class Entity(pygame.sprite.Sprite):

    def __init__(self, game, image, location):
        super().__init__()

        self.game = game
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = location


class Ship(Entity):

    def __init__(self, game, image, location, shield=settings.PLAYER_SHIELD):
        super().__init__(game, image, location)

        self.original_image = self.image
        self.angle = 0
        self.shield = shield
        self.velocity = pygame.Vector2(0, 0)

    def move_forward(self):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), -math.sin(radians))
        self.velocity += direction * settings.ACCELERATION

    # def move_left(self):
    # self.rect.x -= 5

    # def move_right(self):
    # self.rect.x += 5

    def rotate_right(self):
        self.angle -= 5
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_left(self):
        self.angle += 5
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        if self.game.spread_shot_active:
            directions = [0, 45, 90, 135, 180, 225, 270, 315]
            for angle in directions:
                radians = math.radians(angle)
                self.rotated_laser = pygame.transform.rotate(
                    self.game.laser_img, angle
                )
                dx = math.cos(radians)
                dy = math.sin(radians)
                laser = Laser(
                    self.game, self.rotated_laser, self.rect.center, angle
                )
                self.game.lasers.add(laser)
        else:
            angle = self.angle
            loc = self.rect.center
            self.rotated_laser = pygame.transform.rotate(
                self.game.laser_img, angle
            )
            laser = Laser(self.game, self.rotated_laser, loc, angle)
            self.game.lasers.add(laser)

    def check_asteroids(self):
        hits = pygame.sprite.spritecollide(
            self, self.game.asteroids, True, pygame.sprite.collide_mask
        )
        # makes the ship take damage
        self.shield -= len(hits)
        if self.shield <= 0:
            self.kill()

    def check_lasers(self):
        hits = pygame.sprite.spritecollide(
            self, self.game.enemy_lasers, True, pygame.sprite.collide_mask
        )
        # makes the ship take damage
        self.shield -= len(hits)
        if self.shield <= 0:
            self.kill()

    def check_powerups(self):
        hits = pygame.sprite.spritecollide(
            self, self.game.powerups, True, pygame.sprite.collide_mask
        )
        hits2 = pygame.sprite.spritecollide(
            self, self.game.spreadshots, True, pygame.sprite.collide_mask
        )

        for powerup in hits2:
            print("Location1")
            powerup.apply(self)
        for spreadshot in hits:
            print("Location2")
            spreadshot.apply(self)

    def update(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
        if self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.check_asteroids()
        self.check_powerups()
        self.check_lasers()


class Laser(Entity):

    def __init__(self, game, image, location, angle):
        super().__init__(game, image, location)

        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.angle = angle

    def update(self):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), -math.sin(radians))
        self.rect.center += direction * settings.SHIP_SPEED

        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > settings.SCREEN_WIDTH:
            self.kill()
        elif self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()


# class Enemy(Entity):

#     def __init__(self, game, image, location, shield=settings.ENEMY_SHIELD):
#         super().__init__(game, image, location)

#         self.shield = shield
#         self.value = shield * 10

#     def check_lasers(self):
#         hits = pygame.sprite.spritecollide(self, self.game.lasers, True, pygame.sprite.collide_mask)

#         self.shield -= len(hits)
#         if self.shield <= 0:
#             self.kill()
#             self.game.score += self.value * self.game.current_level

#     #def shoot(self):
#         #r = random.uniform(0, settings.FPS)

#         #if r < settings.ENEMY_SHOT_RATE:
#             #enemy_laser = EnemyLaser(self.game, self.game.enemy_laser_img, self.rect.center)
#             #self.game.enemy_lasers.add(enemy_laser)

#     def update(self):
#         self.check_lasers()
#         #self.shoot()


class Asteroid(Entity):

    def __init__(self, game, image, location, shield=settings.ENEMY_SHIELD):
        super().__init__(game, image, location)
        self.new_image = image
        self.shield = shield
        self.original_img = image
        self.value = shield * 10
        self.angle = 0  # Current facing angle
        self.velocity = pygame.Vector2(0, 0)

    def aim_towards_player(self):
        # Get world positions
        player_world_pos = pygame.Vector2(self.game.ship.rect.center)
        enemy_world_pos = self.rect.center

        # Player screen position
        enemy_screen_pos = enemy_world_pos

        if True:
            self.on_screen = True
            direction = player_world_pos - enemy_world_pos

            if direction.length_squared() > 0:
                target_angle = (
                    int(math.degrees(math.atan2(-direction.x, -direction.y)))
                    % 360
                )

                # Only rotate if angle changed significantly
                if abs(target_angle - self.angle) > 1:
                    if self.angle > target_angle:
                        self.angle -= 3
                    if self.angle < target_angle:
                        self.angle += 3

                    self.image = pygame.transform.rotate(
                        self.new_image, self.angle + 180
                    )
                    self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.on_screen = False
        # if self.rect.right < 0:
        #     self.kill()
        # elif self.rect.left > settings.SCREEN_WIDTH:
        #     self.kill()
        # elif self.rect.top > settings.SCREEN_HEIGHT:
        #     self.kill()
        # elif self.rect.bottom < 0:
        #     self.kill()

    def move(self):
        radians = math.radians(self.angle - 90)
        direction = pygame.Vector2(-math.cos(radians), math.sin(radians))
        self.rect.center += direction * settings.ASTEROID_SPEED

    def check_lasers(self):
        hits = pygame.sprite.spritecollide(
            self, self.game.lasers, True, pygame.sprite.collide_mask
        )

        self.shield -= len(hits)
        if self.shield <= 0:
            self.kill()
            self.game.score += self.value * self.game.current_level

    def shoot(self):
        r = random.uniform(0, settings.FPS)

        if r < settings.ENEMY_SHOT_RATE:
            enemy_laser = EnemyLaser(
                self.game, self.game.enemy_laser_img, self.rect.center
            )
            self.game.enemy_lasers.add(enemy_laser)

    def update(self):
        self.check_lasers()
        self.shoot()
        self.aim_towards_player()
        self.move()


class EnemyLaser(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

        self.game = game
        self.new_image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.angle = self.game.asteroid.angle

    def update(self):
        radians = math.radians(self.angle - 90)
        direction = pygame.Vector2(-math.cos(radians), math.sin(radians))
        self.rect.center += direction * settings.LASER_SPEED

        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > settings.SCREEN_WIDTH:
            self.kill()
        elif self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        self.image = pygame.transform.rotate(self.new_image, self.angle + 180)
        self.rect = self.image.get_rect(center=self.rect.center)


# class Fleet(pygame.sprite.Group):

#     def __init__(self, game):
#         super().__init__()

#         self.game = game
#         self.vx = settings.FLEET_SPEED

#     def update(self):
#         super().update()

#         hits_edge = False

#         for sprite in self.sprites():
#             sprite.rect.y += self.vx

#             if sprite.rect.top <= 0 or sprite.rect.bottom >= settings.SCREEN_HEIGHT:
#                 hits_edge = True

#         if hits_edge:
#             self.vx *= -1


class ShieldBoost(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

    def apply(self, ship):
        print("Apply")

        if ship.shield < 5:
            ship.shield += 1

    def update(self):
        self.rect.y += settings.POWERUP_SPEED

        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()


class SpreadShot(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

        self.active = False

    def apply(self, ship):
        self.game.spread_shot_active = True
        self.game.spread_shot_timer = 1

    def update(self):
        self.rect.y += settings.POWERUP_SPEED

        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()


class Stars(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

    def update(self):
        self.rect.x -= settings.STAR_SPEED

        if self.rect.right < 0:
            self.rect.x = random.randint(
                settings.SCREEN_WIDTH + 30, settings.SCREEN_WIDTH + 200
            )


# laser = Laser(self.game, self.rotated_laser, loc)
# self.game.lasers.add(laser)
