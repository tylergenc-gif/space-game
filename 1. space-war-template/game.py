# Imports
import pygame
import leaderboard
import entities
import settings
import random


# Main game class
class Game:

    # Scenes
    START = 0
    PLAYING = 1
    LOSE = 2
    WIN = 3
    LEADERBOARD = 4

    def __init__(self, player_name):
        # Initialize pygame
        pygame.mixer.pre_init()
        pygame.init()
        self.player_name = player_name
        # Make window
        self.screen = pygame.display.set_mode(
            [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT]
        )
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Set up game
        self.load_assets()
        self.new_game()
        self.highscore = 0

        self.spread_shot_active = False
        self.spread_shot_timer = False

    def spawn_powerup(self):
        x = random.randint(100, settings.SCREEN_WIDTH - 100)
        self.powerups.add(
            entities.ShieldBoost(self, self.heart_powerup_img, [x, -100])
        )

    def load_assets(self):
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)

        self.ship_img = pygame.transform.rotate(
            pygame.image.load(settings.SHIP_IMG).convert_alpha(), -90
        )
        self.laser_img = pygame.transform.rotate(
            pygame.image.load(settings.LASER_IMG).convert_alpha(), 90
        )
        self.asteroid_img = pygame.image.load(
            settings.ASTEROID_IMG
        ).convert_alpha()
        self.bomber_img = pygame.image.load(
            settings.BOMBER_IMG
        ).convert_alpha()
        self.empty_heart_img = pygame.image.load(
            settings.EMPTY_HEART_IMG
        ).convert_alpha()
        self.full_heart_img = pygame.image.load(
            settings.FULL_HEART_IMG
        ).convert_alpha()
        self.heart_powerup_img = pygame.transform.scale(
            self.full_heart_img, (43.4285714284, 40)
        )
        self.star_img = pygame.image.load(settings.STAR_IMG).convert_alpha()
        self.enemy_laser_img = pygame.image.load(
            settings.ENEMY_LASER_IMG
        ).convert_alpha()
        self.spreadshot_img = pygame.image.load(
            settings.SPREADSHOT_IMG
        ).convert_alpha()

    def new_game(self):
        self.player = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.tick = 0
        settings.NUM_OF_ENEMIES = 1
        self.stars = pygame.sprite.Group()
        self.create_stars()
        self.spreadshots = pygame.sprite.Group()

        self.ship = entities.Ship(
            self, self.ship_img, [0 + 300, settings.SCREEN_HEIGHT // 2]
        )
        self.player.add(self.ship)

        self.scene = Game.START
        self.current_level = 1
        self.load_current_level()

        self.score = 0

        settings.ASTEROID_SPEED = 10
        settings.MIN_SIZE = 100
        settings.MAX_SIZE = 300
        settings.RATE_OF_ASTEROIDS = 900

    def load_current_level(self):
        asteroid_locs = []

        # x = 1000
        # y = settings.SCREEN_HEIGHT/2
        if self.current_level <= 5:
            for i in range(round(settings.NUM_OF_ENEMIES)):
                self.asteroid = entities.Asteroid(
                    self, self.asteroid_img, self.make_enemy_coords()
                )
                self.asteroids.add(self.asteroid)
        else:
            for i in range(round(settings.NUM_OF_ENEMIES)):
                self.asteroid = entities.Asteroid(
                    self, self.bomber_img, self.make_enemy_coords(), 2
                )
                self.asteroids.add(self.asteroid)

        # if self.current_level == 1:
        #     asteroid_locs.append([400, 300])
        #     # for i in range(random.randint(3, 5)):
        #     #     x = random.randint(2100 + (i*700), 2500 + (i*700))
        #     #     y = random.randint(300, settings.SCREEN_HEIGHT - 300)
        #     #     asteroid_locs.append([x, y])

        # if self.current_level == 2:
        #     asteroid_locs.append([1000, 500])
        #     # for i in range(random.randint(8, 12)):
        #     #     x = random.randint(2100 + (i*700), 2500 + (i*700))
        #     #     y = random.randint(10, settings.SCREEN_HEIGHT - 10)
        #     #     asteroid_locs.append([x, y])

        # for locs in asteroid_locs:
        #     self.asteroid = entities.Asteroid(self, self.asteroid_img, locs)
        #     self.asteroids.add(self.asteroid)

        if self.current_level != 0:
            self.spawn_powerup()

    def play(self):
        self.scene = Game.PLAYING

    def win(self):
        self.scene = Game.WIN

    def advance(self):
        self.current_level += 1
        self.load_current_level()
        if settings.NUM_OF_ENEMIES < 5:
            settings.NUM_OF_ENEMIES += 0.5

    def lose(self):
        self.scene = Game.LOSE
        leaderboard.update_leaderboard(self.player_name, self.highscore)

    def show_title_screen(self):
        text = self.title_font.render(settings.TITLE, True, settings.WHITE)
        rect = text.get_rect()
        rect.midbottom = (
            settings.SCREEN_WIDTH // 2,
            settings.SCREEN_HEIGHT // 2 - 8,
        )
        self.screen.blit(text, rect)

        text = self.subtitle_font.render(
            "Press 'SPACE' to start.", True, settings.WHITE
        )
        rect = text.get_rect()
        rect.midtop = (
            settings.SCREEN_WIDTH // 2,
            settings.SCREEN_HEIGHT // 2 + 8,
        )
        self.screen.blit(text, rect)

    def show_end_screen(self):
        text = self.title_font.render("Game over", True, settings.WHITE)
        rect = text.get_rect()
        rect.midbottom = (
            settings.SCREEN_WIDTH // 2,
            settings.SCREEN_HEIGHT // 2 - 8,
        )
        self.screen.blit(text, rect)

        text = self.subtitle_font.render(
            "Press 'r' to play again or 'esc' to end game or 'L' to view the leaderboard",
            True,
            settings.WHITE,
        )
        rect = text.get_rect()
        rect.midtop = (
            settings.SCREEN_WIDTH // 2,
            settings.SCREEN_HEIGHT // 2 + 8,
        )
        self.screen.blit(text, rect)

        text = self.title_font.render(
            "HIGHSCORE:" + str(round(self.highscore)), True, settings.WHITE
        )
        rect = text.get_rect()
        rect.midtop = (
            settings.SCREEN_WIDTH // 2,
            settings.SCREEN_HEIGHT // 2 + 100,
        )
        self.screen.blit(text, rect)

    def show_win_screen(self):
        text = self.title_font.render("You Win!", True, settings.WHITE)
        rect = text.get_rect()
        rect.midbottom = (
            settings.SCREEN_WIDTH // 2,
            settings.SCREEN_HEIGHT // 2 - 8,
        )
        self.screen.blit(text, rect)

        text = self.subtitle_font.render(
            "Press 'r' to play again or 'esc' to end game.",
            True,
            settings.WHITE,
        )
        rect = text.get_rect()
        rect.midtop = (
            settings.SCREEN_WIDTH // 2,
            settings.SCREEN_HEIGHT // 2 + 8,
        )
        self.screen.blit(text, rect)

    def show_level(self):
        text = self.title_font.render(
            "Level: " + str(self.current_level), True, settings.WHITE
        )
        rect = text.get_rect()
        rect.topleft = 0, 0
        self.screen.blit(text, rect)

    def show_hud(self):
        for i in range(self.ship.shield):
            self.screen.blit(self.full_heart_img, [80 * i + 10, 900])

        self.show_level()

        text = self.title_font.render(
            str(round(self.score)), True, settings.WHITE
        )
        rect = text.get_rect()
        rect.center = settings.SCREEN_WIDTH // 2, 32
        self.screen.blit(text, rect)

        text = self.title_font.render(
            "Highscore: " + str(round(self.highscore)), True, settings.WHITE
        )
        rect = text.get_rect()
        rect.topright = settings.SCREEN_WIDTH - 16, 16
        self.screen.blit(text, rect)

    def process_input(self):
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leaderboard.update_leaderboard(
                        self.player_name, self.highscore
                    )
                    self.running = False
                if event.key == pygame.K_r:
                    self.new_game()

                if self.scene == Game.START:
                    if event.key == pygame.K_SPACE:
                        self.play()

                elif self.scene == Game.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.ship.shoot()
                elif self.scene == Game.LOSE:
                    if event.key == pygame.K_l:
                        self.scene = Game.LEADERBOARD
        if self.scene == Game.PLAYING:
            if pressed[settings.UP] or pressed[pygame.K_w]:
                self.ship.move_forward()
            self.ship.velocity *= settings.FRICTION
            if self.ship.velocity.length() > settings.SHIP_SPEED:
                self.ship.velocity.scale_to_length(settings.SHIP_SPEED)
            self.ship.rect.center += self.ship.velocity

            if pressed[pygame.K_d]:
                self.ship.rotate_right()

            if pressed[pygame.K_a]:
                self.ship.rotate_left()

    def highscore_tracker(self):
        if self.score >= self.highscore:
            self.highscore = self.score

    def random_powerup(self):
        r = random.randint(1, 100)
        if r == 2:
            self.spawn_powerup()

    def random_spreadshot(self):
        r = random.randint(1, 200)
        if r == 2:
            self.spawn_spreadshot()

    def create_stars(self):
        for i in range(settings.NUMBER_OF_STARS):
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(0, settings.SCREEN_HEIGHT)
            self.stars.add(entities.Stars(self, self.star_img, [x, y]))

    def scroll_screen(self):
        self.stars.update()
        self.ship.rect.x -= settings.SCROLL_SPEED

    def make_enemy_coords(self):
        r = random.randint(1, 4)
        if r == 1:
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(-500, 0)

        if r == 2:
            x = random.randint(
                settings.SCREEN_WIDTH, settings.SCREEN_WIDTH + 500
            )
            y = random.randint(0, settings.SCREEN_HEIGHT)

        if r == 3:
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(
                settings.SCREEN_HEIGHT, settings.SCREEN_HEIGHT + 500
            )

        if r == 4:
            x = random.randint(-500, 0)
            y = random.randint(0, settings.SCREEN_HEIGHT)

        return [x, y]

    def spawn_asteroids(self, i):
        x = random.randint(2100 + (i * 700), 2500 + (i * 700))
        y = random.randint(10, settings.SCREEN_HEIGHT - 10)
        size = random.randint(
            round(settings.MIN_SIZE), round(settings.MAX_SIZE)
        )
        self.scaled_asteroid_img = pygame.transform.scale(
            self.asteroid_img, (size, size)
        )
        self.asteroids.add(
            entities.Asteroid(self, self.scaled_asteroid_img, [x, y])
        )

    def spawn_spreadshot(self):
        x = random.randint(100, settings.SCREEN_WIDTH - 100)
        self.spreadshots.add(
            entities.SpreadShot(self, self.spreadshot_img, [x, -100])
        )

    def spread_shot_timing(self):
        if self.spread_shot_timer == 0:
            return
        if self.spread_shot_timer >= 1:
            self.spread_shot_timer += 1
        if self.spread_shot_timer > 60 * 5:
            self.spread_shot_timer = 0
            self.spread_shot_active = False

    def show_leaderboard(self):
        font = self.subtitle_font
        leaderboard.display_leaderboard(self.screen, font)
        pygame.display.flip()

    def update(self):
        i = 0
        if self.scene == Game.PLAYING:
            self.scroll_screen()
            self.player.update()
            self.asteroids.update()
            self.powerups.update()
            self.random_powerup()
            self.enemy_lasers.update()
            self.score += 0.01
            self.spreadshots.update()
            self.random_spreadshot()
            self.spread_shot_timing()
            # settings.MIN_SIZE += 0.01
            # settings.MAX_SIZE += 0.01
            # settings.ASTEROID_SPEED += 0.01
            # settings.RATE_OF_ASTEROIDS -= 0.01
            self.tick += 0.1
            i += 1
            r = random.randint(1, round(settings.RATE_OF_ASTEROIDS))
            if r == 1:
                # self.spawn_asteroids(i)
                pass
            if len(self.asteroids) < 3:
                # self.spawn_asteroids(i)
                pass
            if self.ship.shield <= 0:
                self.lose()
            elif len(self.asteroids) == 0:

                if self.current_level < settings.NUM_OF_LEVELS:
                    self.advance()
                else:
                    self.win()

        self.lasers.update()

        if self.scene == Game.LOSE:
            self.asteroids.update()

        self.highscore_tracker()
        # print(len(self.lasers))
        # print(len(self.asteroids))

    def render(self):
        self.screen.fill(settings.BLACK)
        self.stars.draw(self.screen)

        if self.scene == Game.PLAYING:
            self.show_hud()

            self.enemy_lasers.draw(self.screen)
            self.powerups.draw(self.screen)
            self.spreadshots.draw(self.screen)

        if self.scene == Game.START:
            self.show_title_screen()

        if self.scene == Game.LOSE:
            self.show_end_screen()

        if self.scene == Game.LEADERBOARD:
            self.show_leaderboard()

        if self.scene == Game.WIN:
            self.show_win_screen()

        self.lasers.draw(self.screen)
        self.asteroids.draw(self.screen)
        self.player.draw(self.screen)

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()

            pygame.display.update()
            self.clock.tick(settings.FPS)

        pygame.quit()
