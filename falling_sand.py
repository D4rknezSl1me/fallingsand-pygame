import pygame
import random
import colorsys
from sys import exit


WIDTH = 700
HEIGHT = 800
COLS, ROWS = 70, 80
cell_height = HEIGHT//ROWS
cell_width = WIDTH//COLS

def draw_map(screen, world):
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(screen, world[i][j][1], (j*cell_width, i*cell_height, cell_width, cell_height))

def spawn_sand(world, cell_y, cell_x, hue):
    if world[cell_y][cell_x][0] == 0:
        r,g,b = colorsys.hls_to_rgb(hue, .5, 1)
        r, g, b = [x*255.0 for x in (r, g, b)]
        try:
            world[cell_y][cell_x] = (1, (r,g,b))
            world[cell_y+1][cell_x] = (1, (r,g,b)) if cell_y<ROWS-1 else 0
            world[cell_y-1][cell_x] = (1, (r,g,b)) if cell_y>0 else 0
            world[cell_y][cell_x+1] = (1, (r,g,b)) if cell_x<COLS-1 else 0
            world[cell_y][cell_x-1] = (1, (r,g,b)) if cell_x>0 else 0
        except IndexError:
            pass
        return (hue+.001)%1
    return hue

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Falling Sand")
    clock = pygame.time.Clock()
    
    world = [[(0, (20,20,20)) for j in range(COLS)] for i in range(ROWS)]
    hue = 0

    draw_map(screen, world)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                cell_x = COLS-1 - mx//cell_width
                cell_y = ROWS - my//cell_height
                hue = spawn_sand(world, cell_y, cell_x, hue)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    world = [[(0, (20,20,20)) for j in range(COLS)] for i in range(ROWS)]
        
        for i in range(ROWS):
            for j in range(COLS):
                try:
                    if world[i][j][0]==1:
                        if world[i-1][j][0] == 0 and i-1>-1:
                            world[i][j], world[i-1][j] = world[i-1][j], world[i][j]
                        elif world[i-1][j][0] == 1 and world[i-1][j-1][0] == 0 and world[i-1][j+1][0] == 0:
                            slide = random.choice([1, -1])
                            world[i][j], world[i-1][j+slide] = world[i-1][j+slide], world[i][j]
                        elif world[i-1][j][0] == 1 and world[i-1][j-1][0] == 0:
                            world[i][j], world[i-1][j-1] = world[i-1][j-1], world[i][j]
                        elif world[i-1][j][0] == 1 and world[i-1][j+1][0] == 0:
                            world[i][j], world[i-1][j+1] = world[i-1][j+1], world[i][j]
                except IndexError:
                    pass
                        
        draw_map(screen, world)
        screen.blit(pygame.transform.rotate(screen, 180), (0, 0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()