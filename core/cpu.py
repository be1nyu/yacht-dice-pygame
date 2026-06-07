import random
from core.score import *
from core.config import *
from core.state import *

def get_best_category(dice, scores):
    best_category = None
    best_score = -1

    for category in scores:
        if type(scores[category]) == int:
            continue

        score = calc(category, dice)

        if score > best_score:
            best_score = score
            best_category = category
    
    return best_category

def cpu_choose_hold(dice, scores):
    best_category = get_best_category(dice, scores)

    for rule in ([1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]):
        count = 0
        for number in rule:
            if dice.count(number) > 0:
                count += 1
        if count == 4:
            held, used = [], []
            for v in dice:
                if rule.count(v) > 0 and used.count(v) == 0:
                    held.append(True)
                    used.append(v)
                else:
                    held.append(False)

            return held

    counts = {}
    for number in dice:
        counts[number] = dice.count(number)

    target = None
    target_count = 0
    for number in counts:
        if counts[number] > target_count:
            target_count = counts[number]
            target = number

    if target_count >= 3 or best_category == "four_of_a_kind" or best_category == "full_house" or best_category == "yahtzee":
        held = []
        for number in dice:
            held.append(number == target)
            
        return held

    if type(category_values.get(best_category)) == int:
        held = []
        for number in dice:
            held.append(number == category_values[best_category])

        return held

    if best_category == "small_straight" or best_category == "large_straight":
        held, seen = [], []
        for number in dice:
            if seen.count(number) == 0:
                held.append(True)
                seen.append(number)
            else:
                held.append(False)

        return held

    if best_category == "choice":
        held = []
        for number in dice:
            held.append(number >= 4)

        return held

    return [False] * 5

def cpu_step(state):
    if state["turn"] != "cpu" or state["game_over"]:
        return False

    state["cpu_timer"] -= 1

    if state["cpu_timer"] > 0:
        return False

    if state["cpu_phase"] == "record":
        category = get_best_category(state["dice"], state["cpu_scores"])
        if type(category) == str:
            state["cpu_scores"][category] = calc(category, state["dice"])
        end_turn(state)
        
        return False

    if state["rolls_left"] <= 0:
        state["cpu_phase"] = "record"
        state["cpu_timer"] = 42

        return False

    best_category = get_best_category(state["dice"], state["cpu_scores"])
    current_score = calc(best_category, state["dice"]) if best_category else 0

    if type(category_values.get(best_category)) == int:
        max_score = category_values[best_category] * 5
    else:
        if best_category == "choice":
            max_score = 30
        elif best_category == "four_of_a_kind":
            max_score = 30
        elif best_category == "full_house":
            max_score = 25
        elif best_category == "small_straight":
            max_score = 30
        elif best_category == "large_straight":
            max_score = 40
        elif best_category == "yahtzee":
            max_score = 50
        else:
            max_score = 0

    chasing_large = (best_category == "small_straight" and current_score == 30 and type(state["cpu_scores"]["large_straight"]) != int)
    already_max = (best_category and current_score >= max_score and not chasing_large and state["rolls_left"] < 3)

    if already_max:
        state["cpu_phase"] = "record"
        state["cpu_timer"] = 42
        return False

    if state["rolls_left"] == 3:
        state["held"] = [False] * 5
    else:
        state["held"] = cpu_choose_hold(state["dice"], state["cpu_scores"])

    state["rolls_left"] -= 1

    for i in range(len(state["held"])):
        if not state["held"][i]:
            state["dice"][i] = random.randint(1, 6)

    if state["rolls_left"] > 0:
        state["cpu_timer"] = 38
    else:
        state["cpu_phase"] = "record"
        state["cpu_timer"] = 42

    return True