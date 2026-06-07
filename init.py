import pygame
from core.cpu import *
from core.paths import *
from core.config import *
from core.state import *
from core.ui import *

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Yacht Dice")

font = pygame.font.Font(pygame.font.match_font("gulim"), 18)
clock = pygame.time.Clock()

dice_images = load_images("dice")
hold_images = load_images("holded_dice")

roll_sound = pygame.mixer.Sound(res_path(f"assets/sounds/roll_dice.mp3"))
click_sound = pygame.mixer.Sound(res_path(f"assets/sounds/click.mp3"))

game_state = init_state()

running = True
while running:
    mx, my = pygame.mouse.get_pos()
    game_state["hover_category"] = None

    if game_state["turn"] == "player" and not game_state["game_over"]:
        for i in range(len(categories)):
            key = categories[i][1]

            if type(game_state["player_scores"][key]) == int:
                continue

            score_y = layout["TABLE_Y"] + i * ROW_H

            if i >= 6:
                score_y += 2 * ROW_H

            score_rect = pygame.Rect(6, score_y, layout["TABLE_W"], ROW_H - 1)

            if score_rect.collidepoint(mx, my):
                game_state["hover_category"] = key
                break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if player_roll(game_state):
                    roll_sound.play()
            elif (event.key == pygame.K_RETURN and game_state["game_over"]):
                reset_state(game_state)
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if game_state["game_over"] or game_state["turn"] != "player":
                continue

            mx, my = event.pos

            for i in range(5):
                dice_rect = pygame.Rect(layout["DICE_X"] + i * (DICE_SIZE + DICE_GAP), DICE_Y, DICE_SIZE, DICE_SIZE)

                if dice_rect.collidepoint(mx, my):
                    player_toggle_hold(game_state, i)
                    click_sound.play()

            roll_btn = pygame.Rect(4, layout["BTN_Y"], screen_width // 2 - 8, BTN_H)

            if roll_btn.collidepoint(mx, my):
                if player_roll(game_state):
                    roll_sound.play()

            for i in range(len(categories)):
                category_name, key = categories[i]

                score_y = layout["TABLE_Y"] + i * ROW_H

                if i >= 6:
                    score_y += 2 * ROW_H
                    
                score_rect = pygame.Rect(6, score_y, layout["TABLE_W"], ROW_H - 1)

                if score_rect.collidepoint(mx, my):
                    player_record(game_state, key)
                    click_sound.play()
                    break

    if game_state["turn"] == "cpu" and not game_state["game_over"]:
        if cpu_step(game_state):
            roll_sound.play()

    draw_scene(screen, font, game_state, layout, dice_images, hold_images)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()