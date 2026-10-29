import pygame
from lain.game import LainLab

if __name__ == "__main__":
    pygame.init()
    lab = LainLab()
    lab.run()
    pygame.quit()
