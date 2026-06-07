import random
from core.config import *
from core.score import *

def fresh_dice():
    result = []
    for i in range(5):
        result.append(random.randint(1, 6))
        
    return result

def init_state():
    state = {
        "dice": fresh_dice(),
        "held": [False] * 5,
        "rolls_left": 3,
        "player_scores": {},
        "cpu_scores": {},
        "p_preview": {},
        "turn": "player",
        "game_over": False,
        "hover_category": None,
        "cpu_timer": 0,
        "cpu_phase": "roll"
    }

    for i, category in categories:
        state["player_scores"][category] = None
        state["cpu_scores"][category] = None

    return state

def reset_state(state):
    new_state = init_state()
    state.update(new_state)

def player_roll(state):
    if state["turn"] != "player" or state["rolls_left"] <= 0 or state["game_over"]:
        return False

    state["rolls_left"] -= 1

    for i in range(len(state["held"])):
        if not state["held"][i]:
            state["dice"][i] = random.randint(1, 6)

    state["p_preview"] = {}
    for i, category in categories:
        if type(state["player_scores"][category]) != int:
            state["p_preview"][category] = calc(category, state["dice"])
            
    return True

def player_toggle_hold(state, i):
    if state["turn"] != "player" or state["rolls_left"] == 3 or state["game_over"]:
        return

    state["held"][i] = not state["held"][i]

def player_record(state, category):
    if (state["turn"] != "player" or type(state["player_scores"][category]) == int or state["rolls_left"] == 3):
        return

    state["player_scores"][category] = calc(category, state["dice"])
    end_turn(state)

def end_turn(state):
    state["held"] = [False] * 5
    state["rolls_left"] = 3
    state["p_preview"] = {}

    game_over = True
    for i, category in categories:
        if type(state["player_scores"][category]) != int or type(state["cpu_scores"][category]) != int:
            game_over = False

    if game_over:
        state["game_over"] = True
        return

    if state["turn"] == "player":
        state["turn"] = "cpu"
        state["cpu_phase"] = "roll"
        state["cpu_timer"] = 45
    else:
        state["turn"] = "player"