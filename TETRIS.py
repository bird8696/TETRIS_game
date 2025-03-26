import pygame
import random

# 초기화
pygame.init()

# 상수 설정
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 10, 20
SCREEN_WIDTH = 600
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (50, 50, 50)  # 은은한 배경 선 색상

# 테트리스 블록 모양과 색상 정의
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Classic")

# 폰트 설정 (영어 지원)
font = pygame.font.SysFont("Arial", 24)  # Arial 폰트 사용
font_large = pygame.font.SysFont("Arial", 36)

# 게임 상태 정의
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_SETTINGS = "settings"

# 초기 상태
game_state = STATE_MENU
game_speed = 5  # 기본 속도

# 키 설정
key_left = pygame.K_LEFT  # 왼쪽 이동
key_right = pygame.K_RIGHT  # 오른쪽 이동
key_down = pygame.K_DOWN  # 아래 이동
key_rotate_cw = pygame.K_x  # 시계 방향 회전 (X 키)
key_rotate_ccw = pygame.K_z  # 반시계 방향 회전 (Z 키)
key_hard_drop = pygame.K_SPACE  # 하드 드롭 (스페이스바)
key_hold = pygame.K_c  # 홀드 (C 키)

# 움직임 속도 제어
move_delay = 100  # 밀리초 단위로 움직임 딜레이 설정 (기본값: 100ms)
last_move_time = 0  # 마지막 움직임 시간 기록

def draw_menu():
    screen.fill(BLACK)
    title_text = font_large.render("Tetris Classic", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    pygame.draw.rect(screen, BLUE, (200, 250, 200, 50))  # Start 버튼
    start_text = font.render("Start Game", True, WHITE)
    screen.blit(start_text, (300 - start_text.get_width() // 2, 275 - start_text.get_height() // 2))

    pygame.draw.rect(screen, GREEN, (200, 350, 200, 50))  # Settings 버튼
    settings_text = font.render("Settings", True, WHITE)
    screen.blit(settings_text, (300 - settings_text.get_width() // 2, 375 - settings_text.get_height() // 2))

def draw_settings():
    screen.fill(BLACK)
    settings_title = font_large.render("Settings", True, WHITE)
    screen.blit(settings_title, (SCREEN_WIDTH // 2 - settings_title.get_width() // 2, 50))

    speed_label = font.render("Speed:", True, WHITE)
    screen.blit(speed_label, (150, 150))
    speed_value = font.render(f"{game_speed}", True, YELLOW)
    screen.blit(speed_value, (300, 150))

    pygame.draw.rect(screen, RED, (350, 140, 30, 30))  # 속도 증가 버튼
    plus_text = font.render("+", True, WHITE)
    screen.blit(plus_text, (365 - plus_text.get_width() // 2, 155 - plus_text.get_height() // 2))

    pygame.draw.rect(screen, RED, (400, 140, 30, 30))  # 속도 감소 버튼
    minus_text = font.render("-", True, WHITE)
    screen.blit(minus_text, (415 - minus_text.get_width() // 2, 155 - minus_text.get_height() // 2))

    back_button = font.render("Back to Menu", True, WHITE)
    pygame.draw.rect(screen, BLUE, (200, 400, 200, 50))  # Back 버튼
    screen.blit(back_button, (300 - back_button.get_width() // 2, 425 - back_button.get_height() // 2))

# 블록 클래스
class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate_clockwise(self):
        original_shape = self.shape[:]  # 원래 모양 저장
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        if game.check_collision(0, 0):  # Tetris 클래스의 check_collision 호출
            self.shape = original_shape  # 충돌 시 원래 모양으로 복원

    def rotate_counterclockwise(self):
        original_shape = self.shape[:]  # 원래 모양 저장
        self.shape = [list(row) for row in zip(*self.shape)][::-1]
        if game.check_collision(0, 0):  # Tetris 클래스의 check_collision 호출
            self.shape = original_shape  # 충돌 시 원래 모양으로 복원

# 게임 클래스
class Tetris:
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_block = self.new_block()
        self.next_block = self.new_block()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.hold_block = None  # 홀드된 블록
        self.hold_used = False  # 현재 턴에서 홀드 사용 여부

    def new_block(self):
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        return Block(shape, color)

    def check_collision(self, dx, dy):
        for y, row in enumerate(self.current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_block.x + x + dx
                    new_y = self.current_block.y + y + dy
                    # 충돌 감지 로직 수정
                    if new_x < 0 or new_x >= GRID_WIDTH:  # 왼쪽 또는 오른쪽 벽 충돌
                        return True
                    if new_y >= GRID_HEIGHT:  # 아래쪽 벽 충돌
                        return True
                    if new_y >= 0 and 0 <= new_x < GRID_WIDTH and self.grid[new_y][new_x] != BLACK:  # 다른 블록과 충돌
                        return True
        return False

    def move_block(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.current_block.x += dx
            self.current_block.y += dy

    def hard_drop(self):
        while not self.check_collision(0, 1):
            self.current_block.y += 1

    def lock_block(self):
        for y, row in enumerate(self.current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_block.x + x
                    grid_y = self.current_block.y + y
                    # 유효한 범위 내에서만 블록을 고정
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = self.current_block.color
        self.clear_lines()
        self.current_block = self.next_block
        self.next_block = self.new_block()
        self.reset_hold()  # 턴이 끝날 때 홀드 상태 초기화

        # 블록이 천장에 닿으면 게임 종료
        if any(cell != BLACK for cell in self.grid[0]):  # 최상단 행에 블록이 있으면
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        cleared = GRID_HEIGHT - len(new_grid)
        if cleared > 0:
            self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(cleared)] + new_grid
            self.score += cleared * 100
            self.lines += cleared
            self.level = self.lines // 10 + 1

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(screen, self.grid[y][x],
                                 (x * BLOCK_SIZE + 150, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                # 은은한 배경 선 추가
                pygame.draw.rect(screen, GRAY,
                                 (x * BLOCK_SIZE + 150, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_block(self, block, offset_x, offset_y):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, block.color,
                                     ((block.x + x) * BLOCK_SIZE + offset_x,
                                      (block.y + y) * BLOCK_SIZE + offset_y,
                                      BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE,
                                     ((block.x + x) * BLOCK_SIZE + offset_x,
                                      (block.y + y) * BLOCK_SIZE + offset_y,
                                      BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_next_block(self):
        label = font.render("NEXT", True, WHITE)
        screen.blit(label, (20, 20))
        for y, row in enumerate(self.next_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_block.color,
                                     (20 + x * BLOCK_SIZE, 60 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE,
                                     (20 + x * BLOCK_SIZE, 60 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_hold_block(self):
        label = font.render("HOLD", True, WHITE)
        screen.blit(label, (20, 300))
        if self.hold_block:
            for y, row in enumerate(self.hold_block.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.hold_block.color,
                                         (20 + x * BLOCK_SIZE, 340 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(screen, WHITE,
                                         (20 + x * BLOCK_SIZE, 340 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_info(self):
        screen.blit(font.render(f"SCORE", True, WHITE), (480, 50))
        screen.blit(font.render(f"{self.score}", True, YELLOW), (480, 80))
        screen.blit(font.render(f"LINES", True, WHITE), (480, 140))
        screen.blit(font.render(f"{self.lines}", True, ORANGE), (480, 170))
        screen.blit(font.render(f"LEVEL", True, WHITE), (480, 230))
        screen.blit(font.render(f"{self.level}", True, RED), (480, 260))

    def hold_current_block(self):
        if not self.hold_used:  # 현재 턴에서 홀드가 사용되지 않은 경우
            if self.hold_block is None:
                self.hold_block = self.current_block
                self.current_block = self.new_block()
            else:
                self.hold_block, self.current_block = self.current_block, self.hold_block
                self.hold_block.x = GRID_WIDTH // 2 - len(self.hold_block.shape[0]) // 2
                self.hold_block.y = 0
            self.hold_used = True  # 홀드 사용 상태로 설정

    def reset_hold(self):
        self.hold_used = False  # 턴이 끝날 때 홀드 사용 상태 초기화

    def get_ghost_position(self):
        ghost_y = self.current_block.y
        while not self.check_collision(0, ghost_y - self.current_block.y + 1):
            ghost_y += 1
        return ghost_y

    def draw_ghost_block(self):
        ghost_y = self.get_ghost_position()
        for y, row in enumerate(self.current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, GRAY,
                                     ((self.current_block.x + x) * BLOCK_SIZE + 150,
                                      (ghost_y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)  # 내부를 채운 사각형

# 메인 루프
clock = pygame.time.Clock()
game = Tetris()
running = True

while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()  # 키 상태 확인
    current_time = pygame.time.get_ticks()  # 현재 시간 가져오기
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 200 <= mouse_x <= 400 and 250 <= mouse_y <= 300:  # Start 버튼 클릭
                    game_state = STATE_PLAYING
                elif 200 <= mouse_x <= 400 and 350 <= mouse_y <= 400:  # Settings 버튼 클릭
                    game_state = STATE_SETTINGS

        elif game_state == STATE_SETTINGS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 350 <= mouse_x <= 380 and 140 <= mouse_y <= 170:  # 속도 증가 버튼
                    game_speed = min(game_speed + 1, 10)
                elif 400 <= mouse_x <= 430 and 140 <= mouse_y <= 170:  # 속도 감소 버튼
                    game_speed = max(game_speed - 1, 1)
                elif 200 <= mouse_x <= 400 and 400 <= mouse_y <= 450:  # Back 버튼
                    game_state = STATE_MENU

        elif game_state == STATE_PLAYING:
            if not game.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == key_hard_drop:  # 하드 드롭
                        game.hard_drop()
                    elif event.key == key_rotate_cw:  # 시계 방향 회전
                        game.current_block.rotate_clockwise()
                    elif event.key == key_rotate_ccw:  # 반시계 방향 회전
                        game.current_block.rotate_counterclockwise()
                    elif event.key == key_hold:  # 홀드
                        game.hold_current_block()
            else:  # 게임 오버 상태에서 버튼 클릭 처리
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 200 <= mouse_x <= 400 and 300 <= mouse_y <= 350:  # 종료 버튼 클릭
                        running = False
                    elif 200 <= mouse_x <= 400 and 400 <= mouse_y <= 450:  # 메인 화면으로 이동 버튼 클릭
                        game_state = STATE_MENU
                        game = Tetris()  # 게임 상태 초기화

    if game_state == STATE_PLAYING:
        if not game.game_over:
            # 키 상태에 따라 블록 이동 (딜레이 적용)
            if current_time - last_move_time > move_delay:
                if keys[key_left]:  # 왼쪽으로 이동
                    game.move_block(-1, 0)
                    last_move_time = current_time
                if keys[key_right]:  # 오른쪽으로 이동
                    game.move_block(1, 0)
                    last_move_time = current_time
                if keys[key_down]:  # 아래로 이동
                    game.move_block(0, 1)
                    last_move_time = current_time

            if game.check_collision(0, 1):
                game.lock_block()
                game.reset_hold()  # 턴이 끝날 때 홀드 상태 초기화
            else:
                game.current_block.y += 1

        game.draw_grid()
        game.draw_ghost_block()  # 유령 블록 표시
        game.draw_block(game.current_block, 150, 0)
        game.draw_next_block()
        game.draw_hold_block()  # 홀드 블록 표시
        game.draw_info()

        if game.game_over:  # 게임 오버 메시지와 버튼 표시
            game_over_text = font_large.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))

            # 종료 버튼
            pygame.draw.rect(screen, RED, (200, 300, 200, 50))
            exit_text = font.render("Exit", True, WHITE)
            screen.blit(exit_text, (300 - exit_text.get_width() // 2, 325 - exit_text.get_height() // 2))

            # 메인 화면으로 이동 버튼
            pygame.draw.rect(screen, BLUE, (200, 400, 200, 50))
            main_menu_text = font.render("Main Menu", True, WHITE)
            screen.blit(main_menu_text, (300 - main_menu_text.get_width() // 2, 425 - main_menu_text.get_height() // 2))

    elif game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_SETTINGS:
        draw_settings()

    pygame.display.flip()
    clock.tick(game_speed)

pygame.quit()
