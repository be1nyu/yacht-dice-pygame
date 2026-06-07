screen_width, screen_height = 750, 710

categories = [
    ("1의 합", "ones"),
    ("2의 합", "twos"),
    ("3의 합", "threes"),
    ("4의 합", "fours"),
    ("5의 합", "fives"),
    ("6의 합", "sixes"),
    ("초이스", "choice"),
    ("포카드", "four_of_a_kind"),
    ("풀하우스", "full_house"),
    ("스몰 스트레이트", "small_straight"),
    ("라지 스트레이트", "large_straight"),
    ("요트", "yahtzee")
]

category_values = {
    "ones": 1,
    "twos": 2,
    "threes": 3,
    "fours": 4,
    "fives": 5,
    "sixes": 6
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
DGRAY = (80, 80, 80)

RED = (200, 0, 0)
GREEN = (0, 140, 0)
BLUE = (0, 0, 180)

SELECT = (255, 200, 80)
BG = (230, 230, 230)

DICE_SIZE = 94
DICE_GAP = 5
DICE_Y = 40

BTN_H = 34
ROW_H = 32

layout = {
    "DICE_X": (screen_width - 5 * DICE_SIZE - 4 * DICE_GAP) // 2,
    "BTN_Y": DICE_Y + DICE_SIZE + 15,
    "TABLE_Y": DICE_Y + DICE_SIZE + BTN_H + 55,
    "TABLE_W": screen_width // 2 - 10,
}