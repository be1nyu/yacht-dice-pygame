import pygame
from core.config import *
from core.score import *

def draw_center_text(screen, font, text, color, center_x, y):
    text_s = font.render(text, True, color)
    text_rect = text_s.get_rect()
    text_rect.centerx = center_x
    text_rect.y = y

    screen.blit(text_s, text_rect)

def draw_table(screen, font, state, layout, tx, scores, preview, active):
    y = layout["TABLE_Y"] - ROW_H

    pygame.draw.rect(screen, DGRAY, (tx, y, layout["TABLE_W"], ROW_H - 1))
    
    category_text = font.render("카테고리", True, WHITE)

    score_header = font.render("점수", True, WHITE)
    score_header_x = tx + layout["TABLE_W"] - score_header.get_width() - 4
    score_header_y = y + 9

    screen.blit(category_text, (tx + 4, y + 9))
    screen.blit(score_header, (score_header_x, score_header_y))

    y = layout["TABLE_Y"]

    for i in range(len(categories)):
        name, category = categories[i]

        rect_y = y + i * ROW_H
        
        if i >= 6:
            rect_y += 2 * ROW_H

        rect = pygame.Rect(tx, rect_y, layout["TABLE_W"], ROW_H - 1)

        done = type(scores[category]) == int
        hover = active and state["hover_category"] == category and not done

        if done:
            bg = SELECT
        elif hover:
            bg = GRAY
        elif i % 2:
            bg = BG
        else:
            bg = WHITE

        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, GRAY, rect, 1)
        
        name_text = font.render(name, True, BLACK)
        screen.blit(name_text, (rect.x + 4, rect.y + 7))

        if type(preview.get(category)) == int and not done:
            if preview[category] > 0:
                score_color = GREEN
            else:
                score_color = RED

            preview_text = font.render(str(preview[category]), True, score_color)
            preview_rect = preview_text.get_rect()
            preview_rect.right = rect.right - 4
            preview_rect.centery = rect.centery
            screen.blit(preview_text, preview_rect)

        if done:
            score_text = font.render(str(scores[category]), True, BLUE)
            score_rect = score_text.get_rect()
            score_rect.right = rect.right - 4
            score_rect.centery = rect.centery
            screen.blit(score_text, score_rect)

        if hover:
            pygame.draw.rect(screen, DGRAY, rect, 2)

    top_score = 0
    for i in range(6):
        category = categories[i][1]
        if type(scores[category]) == int:
            top_score += scores[category]

    got_bonus = top_score >= 63

    summary_y = layout["TABLE_Y"] + 6 * ROW_H
    summary_rect = pygame.Rect(tx, summary_y, layout["TABLE_W"], ROW_H - 1)
    pygame.draw.rect(screen, DGRAY, summary_rect)
    
    summary_text = font.render("상단 합계", True, WHITE)
    screen.blit(summary_text, (summary_rect.x + 4, summary_rect.y + 7))

    top_score_text = font.render(str(top_score) + "/63", True, WHITE)
    top_score_x = summary_rect.right - top_score_text.get_width() - 4
    top_score_y = summary_rect.y + 7
    screen.blit(top_score_text, (top_score_x, top_score_y))

    bonus_y = layout["TABLE_Y"] + 7 * ROW_H
    bonus_rect = pygame.Rect(tx, bonus_y, layout["TABLE_W"], ROW_H - 1)
    pygame.draw.rect(screen, BG, bonus_rect)
    
    bonus_label = font.render("+35 보너스", True, BLACK)
    screen.blit(bonus_label, (bonus_rect.x + 4, bonus_rect.y + 7))

    if got_bonus:
        bonus_text = font.render("35", True, BLACK)
    else:
        needed_score = 63 - top_score
        bonus_text = font.render(str(needed_score) + "점 부족", True, GRAY)

    bonus_text_x = bonus_rect.right - bonus_text.get_width() - 4
    bonus_text_y = bonus_rect.y + 7
    screen.blit(bonus_text, (bonus_text_x, bonus_text_y))

    total_y = layout["TABLE_Y"] + 14 * ROW_H + 2
    total_rect = pygame.Rect(tx, total_y, layout["TABLE_W"], ROW_H - 1)
    pygame.draw.rect(screen, DGRAY, total_rect)
    
    total_label = font.render("총 점수", True, WHITE)
    screen.blit(total_label, (total_rect.x + 4, total_rect.y + 7))

    final_score = total_score(scores)
    total_text = font.render(str(final_score), True, WHITE)
    total_text_x = total_rect.right - total_text.get_width() - 4
    total_text_y = total_rect.y + (ROW_H - total_text.get_height()) // 2
    screen.blit(total_text, (total_text_x, total_text_y))


def draw_game_over(screen, font, p_tot, c_tot):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    box_width = 320
    box_height = 240
    box_x = screen_width // 2 - box_width // 2
    box_y = screen_height // 2 - box_height // 2
    
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)

    if p_tot > c_tot:
        winner = "승리"
        color = DGRAY
    elif c_tot > p_tot:
        winner = "패배"
        color = RED
    else:
        winner = "무승부"
        color = DGRAY

    center = box_x + box_width // 2
    
    draw_center_text(screen, font, "게임 종료", BLACK, center, box_y + 22)
    draw_center_text(screen, font, winner, color, center, box_y + 60)
    draw_center_text(screen, font, "자신: " + str(p_tot) + "점", BLUE, center, box_y + 100)
    draw_center_text(screen, font, "컴퓨터: " + str(c_tot) + "점", DGRAY, center, box_y + 128)
    draw_center_text(screen, font, "엔터를 눌러 다시 시작", DGRAY, center, box_y + 175)


def draw_scene(screen, font, state, layout, dice_images, hold_images):
    player_total = total_score(state["player_scores"])
    cpu_total = total_score(state["cpu_scores"])

    is_player = False
    if state["turn"] == "player":
        is_player = True

    if is_player:
        left_bg = WHITE
        right_bg = BG
        player_status = "> 자신의 턴"
        player_color = BLACK
        cpu_status = "대기..."
        cpu_color = GRAY
    else:
        left_bg = BG
        right_bg = WHITE
        player_status = "대기..."
        player_color = GRAY
        cpu_status = "> 컴퓨터 생각 중..."
        cpu_color = BLACK

    pygame.draw.rect(screen, left_bg, (0, 0, screen_width // 2, screen_height))
    pygame.draw.rect(screen, right_bg, (screen_width // 2, 0, screen_width // 2, screen_height))

    player_status_text = font.render(player_status, True, player_color)
    screen.blit(player_status_text, (6, 3))
    
    cpu_status_text = font.render(cpu_status, True, cpu_color)
    screen.blit(cpu_status_text, (screen_width // 2 + 6, 3))

    for i in range(len(state["dice"])):
        x = layout["DICE_X"] + i * (DICE_SIZE + DICE_GAP)
        
        dice_number = state["dice"][i]
        img = dice_images.get(dice_number)
        
        if state["held"][i] == True:
            held_img = hold_images.get(dice_number)
            if held_img != None:
                img = held_img
                
        if img != None:
            img_rect = img.get_rect()
            img_rect.centerx = x + DICE_SIZE // 2
            img_rect.centery = DICE_Y + DICE_SIZE // 2
            screen.blit(img, img_rect)

    can_roll = is_player and state["rolls_left"] > 0 and not state["game_over"]
    
    if can_roll:
        roll_text = f"굴리기 ({state['rolls_left']}회 남음)"
        btn_bg = DGRAY
    else:
        roll_text = "카테고리 선택"
        btn_bg = GRAY
        
    roll_s = font.render(roll_text, True, WHITE)

    btn_width = screen_width // 2 - 8
    pygame.draw.rect(screen, btn_bg, (4, layout["BTN_Y"], btn_width, BTN_H))
    
    roll_s_x = screen_width // 4 - roll_s.get_width() // 2
    roll_s_y = layout["BTN_Y"] + (BTN_H - roll_s.get_height()) // 2
    screen.blit(roll_s, (roll_s_x, roll_s_y))

    if is_player:
        cpu_text = "CPU 대기 중"
    else:
        cpu_text = f"CPU 굴리기 남음: {state['rolls_left']}회"
        
    cpu_s = font.render(cpu_text, True, WHITE)

    cpu_btn_x = screen_width // 2 + 4
    pygame.draw.rect(screen, GRAY, (cpu_btn_x, layout["BTN_Y"], btn_width, BTN_H))
    
    cpu_s_x = screen_width * 3 // 4 - cpu_s.get_width() // 2
    cpu_s_y = layout["BTN_Y"] + (BTN_H - cpu_s.get_height()) // 2
    
    screen.blit(cpu_s, (cpu_s_x, cpu_s_y))

    draw_table(screen, font, state, layout, 6, state["player_scores"], state["p_preview"], True)
    draw_table(screen, font, state, layout, screen_width // 2 + 4, state["cpu_scores"], {}, False)

    if state["game_over"]:
        draw_game_over(screen, font, player_total, cpu_total)