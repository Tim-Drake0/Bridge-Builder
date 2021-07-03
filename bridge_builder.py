import pygame as pg
from pygame import mouse
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
circle_color = (200, 200, 200)
steel_color = (193, 83, 0)

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
    gridSize = 50
    snap_to_grid = False
    snap = True
    line_color = black

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
        for c in range(100, 800, self.gridSize):
            for r in range(100, 600, self.gridSize):
                pg.draw.rect(self.screen, grid, (c, r, self.gridSize, self.gridSize), 1)

        for part in self.drawn_parts:
            pg.draw.line(self.screen, part.color, part.start_point, part.end_point, 7)

        for ground in self.ground_list:
            pg.draw.rect(self.screen, ground.color, ground.rect)


        myfont = pg.font.SysFont('couriernew', 20)
        steel_text = myfont.render('Steel', True, black)
        road_text = myfont.render('Road', True, black)
        self.screen.blit(steel_text,(0, 0))
        self.screen.blit(road_text,(100, 0))


    def draw_line(self):
        if self.drawing:
            pg.draw.line(self.screen, self.line_color, self.start_coords, self.current_mouse_pos, 7)
            if self.snap:
                self.snap_end_to_grid()
        mouse = self.current_mouse_pos

        for r in range(100, 800 + self.gridSize, 25):
            for c in range(0, 600 + self.gridSize, 25):
                if mouse[0] <= r + 10 and mouse[0] >= r - 10 and mouse[1] <= c + 10 and mouse[1] >= c - 10:
                    pg.draw.circle(self.screen, circle_color, (r, c), 5)
                    pg.draw.circle(self.screen, black, (r, c), 5, 1)
                    if self.snap_parts and not self.drawing:
                        self.start_coords = (r, c)
                    self.snap_to_grid = True

    def snap_end_to_grid(self):
        mouse = self.current_mouse_pos
        for r in range(100, 800 + self.gridSize, 25):
            for c in range(0, 600 + self.gridSize, 25):
                if mouse[0] <= r + 10 and mouse[0] >= r - 10 and mouse[1] <= c + 10 and mouse[1] >= c - 10:
                    self.end_pos = (r, c)
    
    def check_button_pressed(self):
        if self.current_mouse_pos[0] < 100:
            self.line_color = steel_color
        elif self.current_mouse_pos[0] < 200 and self.current_mouse_pos[0] > 100:
            self.line_color = black

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
                    if self.current_mouse_pos[1] < 100:
                        self.check_button_pressed()
                    else:
                        if not self.snap_parts:
                            self.start_coords = self.current_mouse_pos
                        self.end_pos = 0
                        self.drawing = True
                if event.type == MOUSEBUTTONUP:
                    if self.current_mouse_pos[1] < 100:
                        pass
                    else:
                        self.drawing = False
                        if self.end_pos == 0:
                            self.end_pos = self.current_mouse_pos
                        self.drawn_parts.append(Part('Road', self.start_coords, self.end_pos, self.line_color))
                    
            
            if self.current_mouse_pos[1] > 100:
                self.draw_line()

            

            pg.display.flip()

window = Window()
window.gameLoop()