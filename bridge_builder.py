import pygame as pg
from pygame.locals import *

pg.init()

red = (255,0,0)
black = (0,0,0)
orange = (255, 73, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
green = (0, 255, 0)
teal = (0, 255, 255)
blue = (0, 0, 255)
purple = (104, 0, 255)
brown = (63, 49, 41)
grid = (40, 40, 40)

class Ground:
    def __init__(self, size, left, color):
        self.size = size
        self.color = color
        self.image = pg.Surface((self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (left, window.screenSize[1] - self.size[1])

class Part:
    def __init__(self, name, start_point, end_point, color):
        self.name = name
        self.color = color
        self.start_point = start_point
        self.end_point = end_point

        

class Window:
    screenSize = (900,900)

    def __init__(self):
        self.width = self.screenSize[0]
        self.height = self.screenSize[1]
        self.screen = pg.display.set_mode(self.screenSize, RESIZABLE, 32)

    def start_game(self):
        self.left_ground = Ground((100, 300), 0, green)
        self.right_ground = Ground((100, 300), 800, green)
        self.water = Ground((700, 150), 100, teal)

        self.ground_list = [self.left_ground, self.right_ground, self.water]
        self.drawn_parts = []

        self.drawing = False
        self.snap_parts = True

    def draw_window(self):
        for part in self.drawn_parts:
            pg.draw.line(self.screen, part.color, part.start_point, part.end_point, 4)

        for ground in self.ground_list:
            pg.draw.rect(self.screen, ground.color, ground.rect)


    def draw_line(self):
        if self.drawing:
            pg.draw.line(self.screen, black, self.start_coords, self.current_mouse_pos, 4)

            self.snap_end_to_ground()

        for ground in self.ground_list:
            if ground.color == green:
                mouse = self.current_mouse_pos
                rect = ground.rect

                if ground.rect.left > 450:
                    if mouse[0] <= rect.left + 10 and mouse[0] >= rect.left - 10 and mouse[1] <= rect.bottom + 10 and mouse[1] >= rect.top - 10:
                        pg.draw.circle(self.screen, grid, rect.topleft, 5)
                        self.ground_snapped = ground
                        if self.snap_parts and not self.drawing:
                            self.start_coords = rect.topleft
                else:
                    if mouse[0] <= rect.right + 10 and mouse[0] >= rect.right - 10 and mouse[1] <= rect.bottom + 10 and mouse[1] >= rect.top - 10:
                        pg.draw.circle(self.screen, grid, rect.topright, 5)
                        self.ground_snapped = ground
                        if self.snap_parts and not self.drawing:
                            self.start_coords = rect.topright

    def snap_end_to_ground(self):
        for ground in self.ground_list:
            if ground.color == green:
                mouse = self.current_mouse_pos
                rect = ground.rect
                if ground != self.ground_snapped:
                    if ground.rect.left > 450:
                        if mouse[0] <= rect.left + 15 and mouse[0] >= rect.left - 15 and mouse[1] <= rect.bottom + 15 and mouse[1] >= rect.top - 15:
                            self.end_pos = ground.rect.topleft
                    else:
                        if mouse[0] <= rect.right + 15 and mouse[0] >= rect.right - 15 and mouse[1] <= rect.bottom + 15 and mouse[1] >= rect.top - 15:
                            self.end_pos = ground.rect.topright
                    

    def snap_to_part(self):
        pass

    def gameLoop(self):
        self.start_game()
        while True:
            self.screen.fill(white)
            self.draw_window()
            self.current_mouse_pos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if not self.snap_parts:
                        self.start_coords = pg.mouse.get_pos()
                    self.end_pos = 0
                    self.drawing = True
                if event.type == MOUSEBUTTONUP:
                    self.drawing = False
                    if self.end_pos == 0:
                        self.end_pos = self.current_mouse_pos
                    self.drawn_parts.append(Part('Road', self.start_coords, self.end_pos, black))
                    
            
            
            self.draw_line()

            

            pg.display.flip()

window = Window()
window.gameLoop()