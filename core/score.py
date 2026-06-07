from core.config import *

def calc(category, dice):
    current = [0] * 6
    for value in dice:
        current[value - 1] += 1

    if type(category_values.get(category)) == int:
        value = category_values[category]
        
        return current[value - 1] * value

    if category == "choice":
        return sum(dice)

    if category == "four_of_a_kind":
        if max(current) >= 4:
            return sum(dice)
        
        return 0

    if category == "full_house":
        for count in current:
            if count == 2:
                break
        else:
            return 0

        for count in current:
            if count == 3:
                return 25

        return 0

    if category == "small_straight":
        for value in range(3):
            found = True
            for target in range(value, value + 4):
                if current[target] == 0:
                    found = False
                    break

            if found:
                return 30
            
        return 0
    
    if category == "large_straight":
        for value in range(2):
            found = True
            for target in range(value, value + 5):
                if current[target] == 0:
                    found = False
                    break

            if found:
                return 40
            
        return 0
    
    if category == "yahtzee":
        if dice.count(dice[0]) == 5:
            return 50

        return 0
    
def total_score(scores):
    upper_score, lower_score = 0, 0
    for category in range(len(categories)):
        value = categories[category][1]

        if type(scores[value]) == int:
            if category < 6:
                upper_score += scores[value]
            else:
                lower_score += scores[value]

    bonus = 0
    if upper_score >= 63:
        bonus = 35

    return upper_score + bonus + lower_score