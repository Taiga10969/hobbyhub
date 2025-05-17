import random

import pygame

# ウィンドウサイズ／グリッドサイズ設定
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH    = 300  # 10列 * ブロック30px
PLAY_HEIGHT   = 600  # 20行 * ブロック30px
BLOCK_SIZE    = 30

TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# テトリミノの定義（回転パターン）
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (0, 255,  0),  # S
    (255, 0,   0),  # Z
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (255, 165, 0),  # J
    (0,   0, 255),  # L
    (128, 0, 128)   # T
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # 回転状態（インデックス）

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        for j, char in enumerate(line):
            if char == '0':
                positions.append((piece.x + j, piece.y + i))
    # テトリミノの図形定義は余白を含むのでオフセット調整
    return [(x - 2, y - 4) for x, y in positions]

def valid_space(piece, grid):
    accepted = [(x, y) for y in range(20) for x in range(10) if grid[y][x] == (0,0,0)]
    for pos in convert_shape_format(piece):
        x, y = pos
        if (x, y) not in accepted and y > -1:
            return False
    return True

def check_lost(positions):
    return any(y < 1 for (_, y) in positions)

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def clear_rows(grid, locked):
    cleared = 0
    for i in range(len(grid)-1, -1, -1):
        if (0,0,0) not in grid[i]:
            cleared += 1
            for j in range(len(grid[i])):
                locked.pop((j, i), None)
    if cleared > 0:
        # 上の行を下に詰める
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            new_y = y + cleared if y < i else y
            locked[(x, new_y)] = locked.pop(key)
    return cleared

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, (
        TOP_LEFT_X + PLAY_WIDTH/2 - label.get_width()/2,
        TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2
    ))

def draw_grid(surface, grid):
    sx, sy = TOP_LEFT_X, TOP_LEFT_Y
    # 中のグリッド線
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128),
                         (sx, sy + i*BLOCK_SIZE),
                         (sx + PLAY_WIDTH, sy + i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128),
                             (sx + j*BLOCK_SIZE, sy),
                             (sx + j*BLOCK_SIZE, sy + PLAY_HEIGHT))

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next:', True, (255,255,255))
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + 100  # Next プレビューの Y 位置を上に移動
    surface.blit(label, (sx, sy))
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        for j, char in enumerate(line):
            if char == '0':
                pygame.draw.rect(surface, piece.color,
                                 (sx + j*BLOCK_SIZE, sy + 30 + i*BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_window(surface, grid, score=0):
    surface.fill((0,0,0))
    # ブロック描画
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (TOP_LEFT_X + j*BLOCK_SIZE,
                              TOP_LEFT_Y + i*BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE), 0)
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0),
                     (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

    # タイトルを上部余白に描画（赤枠と重ならないよう位置とサイズを調整）
    font = pygame.font.SysFont('comicsans', 40, bold=True)
    label = font.render('TETRIS', True, (255,255,255))
    surface.blit(label, (
        TOP_LEFT_X + PLAY_WIDTH//2 - label.get_width()//2,
        5  # 上から5px下がった位置
    ))
    # スコアをグリッド上部に描画
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', True, (255,255,255))
    surface.blit(label, (
        TOP_LEFT_X + PLAY_WIDTH + 50,
        TOP_LEFT_Y + 10  # グリッド上部から少し下に表示
    ))

def main():
    pygame.init()  # pygame の各モジュール（font など）を初期化
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    current_piece = get_shape()
    next_piece    = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # 自動落下
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True

        # 入力処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        # ピース描画
        for x, y in convert_shape_format(current_piece):
            if y > -1:
                grid[y][x] = current_piece.color

        # ピース固定
        if change_piece:
            for pos in convert_shape_format(current_piece):
                locked_positions[(pos[0], pos[1])] = current_piece.color
            score += clear_rows(grid, locked_positions) * 10
            current_piece = next_piece
            next_piece    = get_shape()
            change_piece  = False

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("Game Over", 60, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    pygame.quit()

if __name__ == '__main__':
    main() 