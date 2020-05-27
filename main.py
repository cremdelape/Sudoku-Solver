import os
import pygame
from pygame import mixer
from puzzle import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

TILESIZE = 64
DIST = TILESIZE * 9
DARKBLUE = (0, 48, 143)
LIGHTBLUE = (201, 255, 229)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((DIST, DIST))
all_sprites = pygame.sprite.Group()
board = []
pygame.mixer.music.load('gallery/melodyloops-adrenaline.mp3')
pygame.display.set_caption('Sudoku Solver')
running = True


class Numbers(pygame.sprite.Sprite):
    def __init__(self, num, row, column, state):
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        self.num = num
        image = pygame.image.load(f'gallery/{self.state}/{str(self.num)}.png').convert_alpha()
        image = pygame.transform.scale(image, (32, 32))
        self.image = image
        self.rect = self.image.get_rect()
        self.column = column * TILESIZE + TILESIZE / 2
        self.row = row * TILESIZE + TILESIZE / 2
        self.rect.center = (self.column, self.row)

    def update(self):
        self.rect.center = (self.column, self.row)


def generate():
    global board
    for i in range(0, 81, 9):
        board.append(puzzle[i:i + 9])
    for row, i in enumerate(board):
        board[row] = list(board[row])
        for column, j in enumerate(i):
            if j != '.' and j != '':
                new = Numbers(j, row, column, 'default')
                all_sprites.add(new)
                pass
            else:
                board[row][column] = ''


# Find empty spaces
def find_empty():
    global board
    for i in range(9):
        for j in range(9):
            if board[i][j] == '':
                return i, j
    return None


# Check if the number can be placed under present conditions
def is_safe(num, row, column):
    global board
    # Check if number present in that row
    if str(num) in board[row]:
        return False
    # Check if number present in column
    for i in range(9):
        if str(num) == board[i][column]:
            return False
    # Check if number present in sub groups
    sub_r = (row // 3) * 3  # The index of sub groups
    sub_c = (column // 3) * 3
    for i in range(sub_r, sub_r + 3):
        for j in range(sub_c, sub_c + 3):
            if board[i][j] == str(num):
                return False
    return True


# Solving algorith!

def solve():
    global board
    empty_space = find_empty()
    if not empty_space:
        return True
    i, j = empty_space
    for num in range(1, 10):
        if is_safe(num, i, j):
            board[i][j] = str(num)
            new = Numbers(num, i, j, 'entry')
            all_sprites.add(new)
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.update()
            pygame.time.delay(DELAY)
            if solve():
                return True
            board[i][j] = ''
            new.kill()
            screen.fill(WHITE)
            draw_grid()
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.update()
            pygame.time.delay(DELAY)
    return False


def draw_grid():
    for x in range(0, DIST, TILESIZE):
        pygame.draw.line(screen, LIGHTBLUE, (x, 0), (x, DIST))
    for y in range(0, DIST, TILESIZE):
        pygame.draw.line(screen, LIGHTBLUE, (0, y), (DIST, y))
    for x in range(0, DIST, TILESIZE * 3):
        pygame.draw.line(screen, DARKBLUE, (x, 0), (x, DIST))
    for y in range(0, DIST, TILESIZE * 3):
        pygame.draw.line(screen, DARKBLUE, (0, y), (DIST, y))


generate()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.music.play(loops=-1)
                solve()
    pygame.mixer.music.fadeout(500)
    draw_grid()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.update()
