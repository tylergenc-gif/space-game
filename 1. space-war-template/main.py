import pygame
import os
from game import Game


def get_player_name_pygame(screen):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 48)
    input_box = pygame.Rect(700, 1080 / 2, 600, 60)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    active = True
    text = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        prompt = font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(prompt, (input_box.x, input_box.y - 50))

        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text if text.strip() else "Player"


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Enter Name")

    player_name = get_player_name_pygame(screen)

    g = Game(player_name)
    g.run()


if __name__ == "__main__":
    main()
