# forward declare types
from __future__ import annotations

import pygame
from UTM.constants import BLOCK_SIZE, BLACK, WHITE, WINDOW_WIDTH, WINDOW_HEIGHT, Action2D, priorityImageMap
import os
if not pygame.get_init:
    pygame.init()
    
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

DRAW_ARROWS = False

IMG_CACHE = dict()


# https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
def drawAlphaRect(rect, color=(*BLACK, 1), surface=SCREEN):
    rectSurf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(rectSurf, color, rectSurf.get_rect(), 0)
    surface.blit(rectSurf, rect)

def drawAlphaCoordBlock(x, y, color=(*BLACK, 1), surface=SCREEN, border=0):
    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    rectSurf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(rectSurf, color, rectSurf.get_rect(), border)
    surface.blit(rectSurf, rect)

def drawCoordBlock(x, y, color=BLACK, surface=SCREEN, border=0):
    pygame.draw.rect(surface, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), border)

def drawDroneIcon(x, y, priority, surface=SCREEN):
    if not priorityImageMap[priority] in IMG_CACHE:
        IMG_CACHE[priorityImageMap[priority]] = pygame.image.load(os.path.join(priorityImageMap[priority]))
        IMG_CACHE[priorityImageMap[priority]].convert()
    image = IMG_CACHE[priorityImageMap[priority]] 

    surface.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))


def drawArrow(x, y, dir: Action2D, color=WHITE, surface=SCREEN, border=0):
    if (not DRAW_ARROWS)    : return
    if (dir == Action2D.NOP): return
    __dir_map = {
        Action2D.EAST: (
            (x * BLOCK_SIZE +  6, y * BLOCK_SIZE +  4),
            (x * BLOCK_SIZE +  6, y * BLOCK_SIZE + 27),
            (x * BLOCK_SIZE + 25, y * BLOCK_SIZE + 15)
        ),
        Action2D.WEST: (
            (x * BLOCK_SIZE + 25, y * BLOCK_SIZE +  4),
            (x * BLOCK_SIZE + 25, y * BLOCK_SIZE + 27),
            (x * BLOCK_SIZE +  6, y * BLOCK_SIZE + 16)
        ),
        Action2D.NORTH: (
            (x * BLOCK_SIZE +  4, y * BLOCK_SIZE + 25),
            (x * BLOCK_SIZE + 27, y * BLOCK_SIZE + 25),
            (x * BLOCK_SIZE + 15, y * BLOCK_SIZE +  6)
        ),
        Action2D.SOUTH: (
            (x * BLOCK_SIZE +  4, y * BLOCK_SIZE +  6),
            (x * BLOCK_SIZE + 27, y * BLOCK_SIZE +  6),
            (x * BLOCK_SIZE + 16, y * BLOCK_SIZE + 25)
        )
    }
    pygame.draw.polygon(
        surface,
        color,
        __dir_map[dir],
        border
    )

"""
Defining a renderable element:
any element that can render to pygame's SCREEN should implement a render(zIdx) method 
Defining an updatable element:
any element who's state updates with a simulation frame should have an update() method
"""

#TODO: icon for drone, remove arrows, 