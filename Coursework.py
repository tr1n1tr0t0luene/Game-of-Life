# Імпортуємо потрібні бібліотеки
import pygame
import sys
import random

# Ініціалізуємо pygame
pygame.init()

# Створюємо вікно гри
win = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Life Game")

# Визначаємо розміри вікна та клітинок
win_w, win_h = win.get_size()
cell_w = 10
cell_h = 10

# Перевіряємо, що розміри вікна діляться на розміри клітинок
assert win_w % cell_w == 0 and win_h % cell_h == 0

# Визначаємо розміри дошки
desk_w = win_w//cell_w
desk_h = win_h//cell_h


# Визначаємо кольори
fill_c = (0, 255, 255)
empty_c = (0, 0, 0)
border_c = (30, 30, 30)


# Функція для створення нової дошки
def create_new_desk(w, h, fill_random=False):
    if fill_random:
        return [[random.randint(0, 1) for _ in range(w)] for _ in range(h)]
    else:
        return [[0]*w for _ in range(h)]


# Функція для перевірки стану клітинки
def verify(_desk, _x, _y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == j == 0) and (0 <= i+_y < desk_h) and (0 <= j+_x < desk_w):
                count += _desk[i+_y][j+_x]
    if _desk[_y][_x]:
        if count == 2 or count == 3:
            return True
    if not _desk[_y][_x]:
        if count == 3:
            return True
    return False


# Функція для оновлення дошки
def refresh(_desk):
    new_board = create_new_desk(desk_w, desk_h)
    for i in range(desk_h):
        for j in range(desk_w):
            new_board[i][j] = verify(_desk, j, i)
    return new_board


# Функція для відображення дошки
def render(_win, _desk):
    for i in range(desk_h):
        for j in range(desk_w):
            if _desk[i][j]:
                pygame.draw.rect(_win, fill_c, (j*cell_w, i*cell_h, cell_w, cell_h))
            else:
                pygame.draw.rect(_win, empty_c,  (j*cell_w, i*cell_h, cell_w, cell_h))
            pygame.draw.rect(_win, border_c,  (j*cell_w, i*cell_h, cell_w, cell_h), 1)


# Створюємо початкову дошку
desk = create_new_desk(desk_w, desk_h, fill_random=False)
refreshing = False
dragging = False
pressed = False
DragValue = False

# Створюємо годинник для регулювання FPS
clock = pygame.time.Clock()
FPS = 30

# Головний цикл гри
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x, y = x//cell_w, y//cell_h
            pressed = True
            DragValue = not desk[y][x]
            if not dragging:
                desk[y][x] = not desk[y][x]
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                refreshing = not refreshing
            elif event.key == pygame.K_RIGHT:
                desk = refresh(desk)
            elif event.key == pygame.K_f:
                dragging = not dragging
    if dragging and pressed:
        x, y = pygame.mouse.get_pos()
        x, y = x//cell_w, y//cell_h
        desk[y][x] = DragValue
    if refreshing:
        desk = refresh(desk)

    render(win, desk)
    pygame.display.update()
    pygame.display.set_caption("Game Of Life. " "FPS: " + str(int(clock.get_fps()) + 1))
    clock.tick(FPS)
