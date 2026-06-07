import pygame
import os, sys

def res_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, rel_path)

def load_images(name):
    imgs = {}

    for i in range(1, 7):
        img = pygame.image.load(res_path(f"assets/images/{name}_{i}.png"))
        imgs[i] = pygame.transform.scale(img, (82, 82))

    return imgs