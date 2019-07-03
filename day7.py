import pygame
import random
# 背景图
screen = pygame.display.set_mode((700, 700))

# 棋盘起始位置
bg = pygame.image.load("img/qipan_bg.jpg")
bgx = 50
bgy = 50

# 线条和棋子颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 坐标
zimu = []
shuzi = []

# 文字
pygame.init()
font = pygame.font.SysFont("", 23)
font1 = pygame.font.Font("fonts/msyh.ttf", 66)

# 重新开始按钮
restart = pygame.image.load("img/button1.jpg")
restart = pygame.transform.scale(restart, (restart.get_rect().width + 10, restart.get_rect().height))
restart2 = pygame.transform.scale(restart, (restart.get_rect().width + 10, restart.get_rect().height))
screen.blit(restart, (282, 650))
font3 = pygame.font.Font("fonts/msyh.ttf", 24)
re_text = font3.render("重新开始", True, (255, 0, 0))
screen.blit(re_text, (290, 650))

black_pos = []  # 棋盘上所有已被占的黑棋点
white_pos = []  # 棋盘上所有已被占的白棋点
player_pos = [(-70, -70)]  # 棋盘上所有已被占的棋点
all_pos = []  # 棋盘上所有棋点

# 棋盘上所有点赋值
for j in range(15):
    for i in range(15):
        all_pos.append((70 + 40 * i, 70 + 40 * j))

# 绘制棋盘
def paint():
    # 背景颜色
    pygame.draw.rect(screen, (0x99, 0x76, 0x3f), (0, 0, 800, 800), 800)
    # 在棋盘上绘制坐标
    for i in range(15):
        text = font.render(chr(65 + i), True, BLACK)
        screen.blit(text, (55 + i * 40, bgy - 5))
        num = font.render(str(1 + i), True, BLACK)
        screen.blit(num, (40, bgy + 20 + i * 40))

    # 绘制棋盘
    for i in range(15):
        if i % 2 == 0:
            # 画竖线
            pygame.draw.line(screen, WHITE, ((bgx + 20) + i * 40, (bgy + 20)),
                             ((bgx + 20) + i * 40, (bgy + 580)))

            # 画横线
            pygame.draw.line(screen, WHITE, ((bgx + 20), (bgy + 20) + i * 40),
                             ((bgx + 580), (bgy + 20) + i * 40))

        if i % 2 == 1:
            # 画竖线
            pygame.draw.line(screen, BLACK, ((bgx + 20) + i * 40, (bgy + 20)),
                             ((bgx + 20) + i * 40, (bgy + 580)))
            # 画横线
            pygame.draw.line(screen, BLACK, ((bgx + 20), (bgy + 20) + i * 40),
                             ((bgx + 580), (bgy + 20) + i * 40))

    # 50 是边距， 40 是格子间距 3 11 7 都是格子个数
    # 4 是星的宽度的一半， 8 是星的宽度, 5是画线的宽度
    pygame.draw.rect(screen, BLACK, (70 + 40 * 3 - 4, 70 + 40 * 3 - 4, 8, 8), 5)
    pygame.draw.rect(screen, BLACK, (70 + 40 * 11 - 4, 70 + 40 * 3 - 4, 8, 8), 5)
    pygame.draw.rect(screen, BLACK, (70 + 40 * 7 - 4, 70 + 40 * 7 - 4, 8, 8), 5)
    pygame.draw.rect(screen, BLACK, (70 + 40 * 11 - 4, 70 + 40 * 11 - 4, 8, 8), 5)
    pygame.draw.rect(screen, BLACK, (70 + 40 * 3 - 4, 70 + 40 * 11 - 4, 8, 8), 5)

# 状态
white_state = False
black_state = False
game_state = True


# 棋子位置
def get_pos(mx, my):
    for j in range(15):
        for i in range(15):
            if 70 - 20 + 40 * i < mx <= 70 + 20 + 40 * i and 70 - 20 + 40 * j < my <= 70 + 20 + 40 * j:
                return (70 + 40 * i, 70 + 40 * j)

    return (-70, -70)

# 检查五子连珠
def get_five(teseFive):
    for px, py in teseFive:
        if (px, py + 40) in teseFive and \
                (px, py + 40 * 2) in teseFive and \
                (px, py + 40 * 3) in teseFive and \
                (px, py + 40 * 4) in teseFive:
            return True
        if (px + 40, py) in teseFive and \
                (px + 40 * 2, py) in teseFive and \
                (px + 40 * 3, py) in teseFive and \
                (px + 40 * 4, py) in teseFive:
            return True
        if (px + 40, py + 40) in teseFive and \
                (px + 40 * 2, py + 40 * 2) in teseFive and \
                (px + 40 * 3, py + 40 * 3) in teseFive and \
                (px + 40 * 4, py + 40 * 4) in teseFive:
            return True

        if (px + 40, py - 40) in teseFive and \
                (px + 40 * 2, py - 40 * 2) in teseFive and \
                (px + 40 * 3, py - 40 * 3) in teseFive and \
                (px + 40 * 4, py - 40 * 4) in teseFive:
            return True


# 开关
switch = True

# 获取玩家周围位置
def get_one_point(white_point, player_point, all_point):
    tamp_points = []
    # 遍历白色棋子,判断上次白子附近的八个位置中的空位置加入tamp_points中
    for x, y in white_point:
        if (x, y-40) in all_point and \
                (x, y-40) not in player_point:
            tamp_points.append((x, y-40))

        if(x, y + 40) in all_point and \
                (x, y + 40) not in player_point:
            tamp_points.append((x, y + 40))

        if (x-40, y) in all_point and \
                (x-40, y) not in player_point:
            tamp_points.append((x-40, y))

        if (x+40, y) in all_point and \
                (x+40, y) not in player_point:
            tamp_points.append((x+40, y))

        if (x-40, y-40) in all_point and \
                (x-40, y-40) not in player_point:
            tamp_points.append((x-40, y-40))

        if (x+40, y-40) in all_point and \
                (x+40, y-40) not in player_point:
            tamp_points.append((x+40, y-40))

        if (x+40, y+40) in all_point and \
                (x+40, y+40) not in player_point:
            tamp_points.append((x+40, y+40))

        if (x-40, y+40) in all_point and \
                (x-40, y+40) not in player_point:
            tamp_points.append((x-40, y+40))
    return tamp_points

# 棋盘上所有活2棋子
def get_live_two_points(white_point, player_point, all_point):
    tamp_points = []
    for x, y in white_point:
        # 左右
        if (x-40, y) in all_point and \
                (x-40, y) not in player_point and \
                (x+40, y) in white_point and \
                (x+40*2, y) in all_point and \
                (x+40*2, y) not in player_point:
            tamp_points.append((x-40, y))
            tamp_points.append((x+40*2, y))

        # 左上右下
        if (x-40, y-40) in all_point and \
                (x-40, y-40) not in player_point and \
                (x+40, y+40) in white_point and \
                (x+40*2, y+40*2) in all_point and \
                (x+40*2, y+40*2) not in player_point:
            tamp_points.append((x-40, y-40))
            tamp_points.append((x+40*2, y+40*2))

        # 上下
        if (x, y-40) in all_point and \
                (x, y-40) not in player_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in all_point and \
                (x, y+40*2) not in player_point:
            tamp_points.append((x, y-40))
            tamp_points.append((x, y+40*2))

        # 左下右上
        if (x-40, y+40) in all_point and \
                (x-40, y+40) not in player_point and \
                (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in all_point and \
                (x+40*2, y-40*2) not in player_point:
            tamp_points.append((x-40, y+40))
            tamp_points.append((x+40*2, y-40*2))

    return tamp_points

# 活3
def get_live_three_points(white_point, player_point, all_point):
    temp_points = []
    for x, y in white_point:
        # 左右
        if (x-40, y) in all_point and \
                (x-40, y) not in player_point and \
                (x+40, y) in white_point and \
                (x+40*2, y) in white_point and \
                (x+40*3, y) in all_point and \
                (x+40*3, y) not in player_point:
            temp_points.append((x-40, y))
            temp_points.append((x+40*3, y))

        # 上下
        if (x, y-40) in all_point and \
                (x, y-40) not in player_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in all_point and \
                (x, y+40*3) not in player_point:
            temp_points.append((x, y-40))
            temp_points.append((x, y+40*3))

        # 左上右下
        if (x-40, y-40) in all_point and \
                (x-40, y-40) not in player_point and \
                (x+40, y+40) in white_point and \
                (x+40*2, y+40*2) in white_point and \
                (x+40*3, y+40*3) in all_point and \
                (x+40*3, y+40*3) not in player_point:
            temp_points.append((x-40, y-40))
            temp_points.append((x+40*3, y+40*3))

        # 左下右上
        if (x-40, y+40) in all_point and \
                (x-40, y+40) not in player_point and \
                (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in all_point and \
                (x+40*3, y-40*3) not in player_point:
            temp_points.append((x-40, y+40))
            temp_points.append((x+40*3, y-40*3))

    return temp_points

# 活4
def get_live_four_points(white_point, player_point, all_point):
    temp_points = []
    for x, y in white_point:
        # 左右
        if (x-40, y) in all_point and \
                (x-40, y) not in player_point and \
                (x+40, y) in white_point and \
                (x+40*2, y) in white_point and \
                (x+40*3, y) in white_point and \
                (x+40*4, y) in all_point and \
                (x+40*4, y) not in player_point:
            temp_points.append((x-40, y))
            temp_points.append((x+40*4, y))

        # 上下
        if (x, y-40) in all_point and \
                (x, y-40) not in player_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in white_point and \
                (x, y+40*4) in all_point and \
                (x, y+40*4) not in player_point:
            temp_points.append((x, y-40))
            temp_points.append((x, y+40*4))

        # 左上右下
        if (x-40, y-40) in all_point and \
                (x-40, y-40) not in player_point and \
                (x+40, y+40) in white_point and \
                (x+40*2, y+40*2) in white_point and \
                (x+40*3, y+40*3) in white_point and \
                (x+40*4, y+40*4) in all_point and \
                (x+40*4, y+40*4) not in player_point:
            temp_points.append((x-40, y-40))
            temp_points.append((x+40*4, y+40*4))

        # 左下右上
        if (x-40, y+40) in all_point and \
                (x-40, y+40) not in player_point and \
                (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in white_point and \
                (x+40*4, y-40*4) in all_point and \
                (x+40*4, y-40*4) not in player_point:
            temp_points.append((x-40, y+40))
            temp_points.append((x+40*4, y+40*4))

    return temp_points

# 冲4
def get_punching_four(white_point, black_point, player_point, all_point):
    # 16 种
    temp_points = []
    for x, y in white_point:
        # 边 8种
        # 冲上
        if (x, y+40) not in all_point and \
                (x, y-40) in white_point and \
                (x, y-40*2) in white_point and \
                (x, y-40*3) in white_point and \
                (x, y-40*4) in all_point and \
                (x, y-40*4) not in player_point:
            temp_points.append((x, y-40*4))

        # 冲右上
        if (x-40, y+40) not in all_point and \
                (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in white_point and \
                (x+40*4, y-40*4) in all_point and \
                (x+40*4, y-40*4) not in player_point:
            temp_points.append((x+40*4, y-40*4))

        # 冲右
        if (x-40, y) not in all_point and \
                (x+40, y) in white_point and \
                (x+40*2, y) in white_point and \
                (x+40*3, y) in white_point and \
                (x+40*4, y) in all_point and \
                (x+40*4, y) not in player_point:
            temp_points.append((x+40*4, y))

        # 冲右下
        if (x-40, y-40) not in all_point and \
                (x+40, y+40) in white_point and \
                (x+40*2, y+40*2) in white_point and \
                (x+40*3, y+40*3) in white_point and \
                (x+40*4, y+40*4) in all_point and \
                (x+40*4, y+40*4) not in player_point:
            temp_points.append((x+40*4, y+40*4))

        # 冲下
        if (x, y-40) not in all_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in white_point and \
                (x, y+40*4) in all_point and \
                (x, y+40*4) not in player_point:
            temp_points.append((x, y+40*4))

        # 冲左下
        if (x+40, y-40) not in all_point and \
                (x-40, y+40) in white_point and \
                (x-40*2, y+40*2) in white_point and \
                (x-40*3, y+40*3) in white_point and \
                (x-40*4, y+40*4) in all_point and \
                (x-40*4, y+40*4) not in player_point:
            temp_points.append((x-40*4, y+40*4))

        # 冲左
        if (x+40, y) not in all_point and \
                (x-40, y) in white_point and \
                (x-40*2, y) in white_point and \
                (x-40*3, y) in white_point and \
                (x-40*4, y) in all_point and \
                (x-40*4, y) not in player_point:
            temp_points.append((x-40*4, y))

        # 冲左上
        if (x+40, y+40) not in all_point and \
                (x-40, y-40) in white_point and \
                (x-40*2, y-40*2) in white_point and \
                (x-40*3, y-40*3) in white_point and \
                (x-40*4, y-40*4) in all_point and \
                (x-40*4, y-40*4) not in player_point:
            temp_points.append((x-40*4, y-40*4))

        # 中间
        # 冲上
        if (x, y+40) in black_point and \
                (x, y-40) in white_point and \
                (x, y-40*2) in white_point and \
                (x, y-40*3) in white_point and \
                (x, y-40*4) in all_point and \
                (x, y-40*4) not in player_point:
            temp_points.append((x, y-40*4))

        # 冲右上
        if (x-40, y+40) in black_point and \
                (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in white_point and \
                (x+40*4, y-40*4) in all_point and \
                (x+40*4, y-40*4) not in player_point:
            temp_points.append((x+40*4, y-40*4))

        # 冲右
        if (x-40, y) in black_point and \
                (x+40, y) in white_point and \
                (x+40*2, y) in white_point and \
                (x+40*3, y) in white_point and \
                (x+40*4, y) in all_point and \
                (x+40*4, y) not in player_point:
            temp_points.append((x+40*4, y))

        # 冲右下
        if (x-40, y-40) in black_point and \
                (x+40, y+40) in white_point and \
                (x+40*2, y+40*2) in white_point and \
                (x+40*3, y+40*3) in white_point and \
                (x+40*4, y+40*4) in all_point and \
                (x+40*4, y+40*4) not in player_point:
            temp_points.append((x+40*4, y+40*4))

        # 冲下
        if (x, y-40) in black_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in white_point and \
                (x, y+40*4) in all_point and \
                (x, y+40*4) not in player_point:
            temp_points.append((x, y+40*4))

        # 冲左下
        if (x+40, y-40) in black_point and \
                (x-40, y+40) in white_point and \
                (x-40*2, y+40*2) in white_point and \
                (x-40*3, y+40*3) in white_point and \
                (x-40*4, y+40*4) in all_point and \
                (x-40*4, y+40*4) not in player_point:
            temp_points.append((x-40*4, y+40*4))

        # 冲左
        if (x+40, y) in black_point and \
                (x-40, y) in white_point and \
                (x-40*2, y) in white_point and \
                (x-40*3, y) in white_point and \
                (x-40*4, y) in all_point and \
                (x-40*4, y) not in player_point:
            temp_points.append((x-40*4, y))

        # 冲左上
        if (x+40, y+40) in black_point and \
                (x-40, y-40) in white_point and \
                (x-40*2, y-40*2) in white_point and \
                (x-40*3, y-40*3) in white_point and \
                (x-40*4, y-40*4) in all_point and \
                (x-40*4, y-40*4) not in player_point:
            temp_points.append((x-40*4, y-40*4))

    return temp_points

# 眠5 12种
def get_sleep_five(white_point, player_point, all_point):
    temp_points = []
    for x, y in white_point:
        # 眠上、下 二空
        if (x, y+40) in all_point and \
                (x, y+40) not in player_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in white_point and \
                (x, y+40*4) in white_point:
            temp_points.append((x, y+40))

        # 眠上、下 三空
        if (x, y+40*2) in all_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) not in player_point and \
                (x, y+40*3) in white_point and \
                (x, y+40*4) in white_point:
            temp_points.append((x, y+40*2))

        # 眠上、下 四空
        if (x, y+40*3) in all_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) not in player_point and \
                (x, y+40*4) in white_point:
            temp_points.append((x, y+40*3))

        # 眠左、右 二空
        if (x + 40, y) in all_point and \
                (x + 40, y) not in player_point and \
                (x + 40 * 2, y) in white_point and \
                (x + 40 * 3, y) in white_point and \
                (x + 40 * 4, y) in white_point:
            temp_points.append((x + 40, y))

        # 眠左、右 三空
        if (x, y) in all_point and \
                (x + 40 * 2, y) in white_point and \
                (x + 40, y) not in player_point and \
                (x + 40 * 2, y) in white_point and \
                (x + 40 * 3, y) in white_point:
            temp_points.append((x + 40 * 2, y))

        # 眠左、右 四空
        if (x + 40 * 3, y) in all_point and \
                (x + 40, y) in white_point and \
                (x + 40 * 2, y) in white_point and \
                (x + 40 * 3, y) not in player_point and \
                (x + 40 * 4, y) in white_point:
            temp_points.append((x + 40 * 3, y))

        # 眠左下、右上 二空
        if (x+40, y-40) in all_point and \
                (x+40, y-40) not in player_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in white_point and \
                (x+40*4, y-40*4) in white_point:
            temp_points.append((x+40, y-40))

        # 眠 三空
        if (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in all_point and \
                (x+40*2, y-40*2) not in player_point and \
                (x+40*3, y-40*3) in white_point and \
                (x+40*4, y-40*4) in white_point:
            temp_points.append((x+40*2, y-40*2))

        # 眠 四空
        if (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in all_point and \
                (x+40*3, y-40*3) not in player_point and \
                (x+40*4, y-40*4) in white_point:
            temp_points.append((x+40*3, y-40*3))

        # 眠左上、右下 二空
        if (x - 40, y + 40) in all_point and \
                (x - 40, y + 40) not in player_point and \
                (x + 40 * 2, y + 40 * 2) in white_point and \
                (x + 40 * 3, y + 40 * 3) in white_point and \
                (x + 40 * 4, y + 40 * 4) in white_point:
            temp_points.append((x - 40, y + 40))

        # 眠 三空
        if (x - 40, y + 40) in white_point and \
                (x + 40 * 2, y + 40 * 2) in all_point and \
                (x + 40 * 2, y + 40 * 2) not in player_point and \
                (x + 40 * 3, y + 40 * 3) in white_point and \
                (x + 40 * 4, y + 40 * 4) in white_point:
            temp_points.append((x + 40 * 2, y + 40 * 2))

        # 眠 四空
        if (x - 40, y + 40) in white_point and \
                (x + 40 * 2, y + 40 * 2) in white_point and \
                (x + 40 * 3, y + 40 * 3) in all_point and \
                (x + 40 * 3, y + 40 * 3) not in player_point and \
                (x + 40 * 4, y + 40 * 4) in white_point:
            temp_points.append((x + 40 * 3, y + 40 * 3))

    return temp_points

# 任务
# 1. 冲3
def get_punching_three(white_point, black_point, player_point, all_point):
    # 16 种
    temp_points = []
    for x, y in white_point:
        # 边 8种
        # 冲上
        if (x, y+40) not in all_point and \
                (x, y-40) in white_point and \
                (x, y-40*2) in white_point and \
                (x, y-40*3) in all_point and \
                (x, y-40*3) not in player_point:
            temp_points.append((x, y-40*3))

        # 冲右上
        if (x-40, y+40) not in all_point and \
                (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in all_point and \
                (x+40*3, y-40*3) not in player_point:
            temp_points.append((x+40*3, y-40*3))

        # 冲右
        if (x-40, y) not in all_point and \
                (x+40, y) in white_point and \
                (x+40*2, y) in white_point and \
                (x+40*3, y) in all_point and \
                (x+40*3, y) not in player_point:
            temp_points.append((x+40*3, y))

        # 冲右下
        if (x-40, y-40) not in all_point and \
                (x+40, y+40) in white_point and \
                (x+40*2, y+40*2) in white_point and \
                (x+40*3, y+40*3) in all_point and \
                (x+40*3, y+40*3) not in player_point:
            temp_points.append((x+40*3, y+40*3))

        # 冲下
        if (x, y-40) not in all_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in all_point and \
                (x, y+40*3) not in player_point:
            temp_points.append((x, y+40*3))

        # 冲左下
        if (x+40, y-40) not in all_point and \
                (x-40, y+40) in white_point and \
                (x-40*2, y+40*2) in white_point and \
                (x-40*3, y+40*3) in all_point and \
                (x-40*3, y+40*3) not in player_point:
            temp_points.append((x-40*3, y+40*3))

        # 冲左
        if (x+40, y) not in all_point and \
                (x-40, y) in white_point and \
                (x-40*2, y) in white_point and \
                (x-40*3, y) in all_point and \
                (x-40*3, y) not in player_point:
            temp_points.append((x-40*3, y))

        # 冲左上
        if (x+40, y+40) not in all_point and \
                (x-40, y-40) in white_point and \
                (x-40*2, y-40*2) in white_point and \
                (x-40*3, y-40*3) in all_point and \
                (x-40*3, y-40*3) not in player_point:
            temp_points.append((x-40*3, y-40*3))

        # 中间
        # 冲上
        if (x, y+40) in black_point and \
                (x, y-40) in white_point and \
                (x, y-40*2) in white_point and \
                (x, y-40*3) in all_point and \
                (x, y-40*3) not in player_point:
            temp_points.append((x, y-40*3))

        # 冲右上
        if (x-40, y+40) in black_point and \
                (x+40, y-40) in white_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in all_point and \
                (x+40*3, y-40*3) not in player_point:
            temp_points.append((x+40*3, y-40*3))

        # 冲右
        if (x-40, y) in black_point and \
                (x+40, y) in white_point and \
                (x+40*2, y) in white_point and \
                (x+40*3, y) in all_point and \
                (x+40*3, y) not in player_point:
            temp_points.append((x+40*3, y))

        # 冲右下
        if (x-40, y-40) in black_point and \
                (x+40, y+40) in white_point and \
                (x+40*2, y+40*2) in white_point and \
                (x+40*3, y+40*3) in all_point and \
                (x+40*3, y+40*3) not in player_point:
            temp_points.append((x+40*3, y+40*3))

        # 冲下
        if (x, y-40) in black_point and \
                (x, y+40) in white_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in all_point and \
                (x, y+40*3) not in player_point:
            temp_points.append((x, y+40*3))

        # 冲左下
        if (x+40, y-40) in black_point and \
                (x-40, y+40) in white_point and \
                (x-40*2, y+40*2) in white_point and \
                (x-40*3, y+40*3) in all_point and \
                (x-40*3, y+40*3) not in player_point:
            temp_points.append((x-40*3, y+40*3))

        # 冲左
        if (x+40, y) in black_point and \
                (x-40, y) in white_point and \
                (x-40*2, y) in white_point and \
                (x-40*3, y) in all_point and \
                (x-40*3, y) not in player_point:
            temp_points.append((x-40*3, y))

        # 冲左上
        if (x+40, y+40) in black_point and \
                (x-40, y-40) in white_point and \
                (x-40*2, y-40*2) in white_point and \
                (x-40*3, y-40*3) in all_point and \
                (x-40*3, y-40*3) not in player_point:
            temp_points.append((x-40*3, y-40*3))

    return temp_points

# 2. 完善活2
# 3. 眠3
def get_sleep_three(white_point, player_point, all_point):
    temp_points = []
    for x, y in white_point:
        # 眠上、下
        if (x, y-40) in all_point and \
                (x, y-40) not in player_point and \
                (x, y+40) in all_point and \
                (x, y+40) not in player_point and \
                (x, y+40*2) in white_point and \
                (x, y+40*3) in all_point and \
                (x, y+40*3) not in player_point:
            temp_points.append((x, y+40))

        # 眠左、右
        if (x - 40, y) in all_point and \
                (x - 40, y) not in player_point and \
                (x + 40, y) in all_point and \
                (x + 40, y) not in player_point and \
                (x + 40 * 2, y) in white_point and \
                (x + 40 * 3, y) in all_point and \
                (x + 40 * 3, y) not in player_point:
            temp_points.append((x + 40, y))

        # 眠左下、右上 二空
        if (x-40, y+40) in all_point and \
                (x-40, y+40) not in player_point and \
                (x+40, y-40) in all_point and \
                (x+40, y-40) not in player_point and \
                (x+40*2, y-40*2) in white_point and \
                (x+40*3, y-40*3) in all_point and \
                (x+40*4, y-40*3) not in player_point:
            temp_points.append((x+40, y-40))

        # 眠左上、右下 二空
        if (x-40, y-40) in all_point and \
                (x-40, y-40) not in player_point and \
                (x + 40, y + 40) in all_point and \
                (x + 40, y + 40) not in player_point and \
                (x + 40 * 2, y + 40 * 2) in white_point and \
                (x + 40 * 3, y + 40 * 3) in all_point and \
                (x + 40 * 3, y + 40 * 3) not in player_point:
            temp_points.append((x + 40, y + 40))

    return temp_points

# 4. 眠4
# 5. 眠冲4
# 6. 眠冲3？

# 7. 双活3，双眠4，眠4活3
# 8. 4冲3
# 9. 双冲
# 10.双眠5
# 11.冲4眠五

# 决策树
def decisionTree(black_point, white_point, player_point, all_point):
    # 眠5进攻
    if get_sleep_five(black_point, player_point, all_point):
        return get_sleep_five(black_point, player_point, all_point)

    # 眠5防守
    elif get_sleep_five(white_point, player_point, all_point):
        return get_sleep_five(white_point, player_point, all_point)

    # 冲4进攻
    elif get_punching_four(black_point, white_point, player_point, all_point):
        return get_punching_four(black_point, white_point, player_point, all_point)

    # 冲4防守
    elif get_punching_four(white_point, black_point, player_point, all_point):
        return get_punching_four(white_point, black_point, player_point, all_point)

    # 活4进攻
    elif get_live_four_points(black_point, player_point, all_point):
        return get_live_four_points(black_point, player_point, all_point)

    # 活4 防守
    elif get_live_four_points(white_point, player_point, all_point):
        return get_live_four_points(white_point, player_point, all_point)

    # 活3进攻
    elif get_live_three_points(black_point, player_point, all_point):
        return get_live_three_points(black_point, player_point, all_point)

    # 活3防守
    elif get_live_three_points(white_point, player_point, all_point):
        return get_live_three_points(white_point, player_point, all_point)

    # 眠3进攻
    if get_sleep_three(black_point, player_point, all_point):
        return get_sleep_three(black_point, player_point, all_point)

    # 眠3防守
    elif get_sleep_three(white_point, player_point, all_point):
        return get_sleep_three(white_point, player_point, all_point)

    # 冲3进攻
    elif get_punching_three(black_point, white_point, player_point, all_point):
        return get_punching_three(black_point, white_point, player_point, all_point)

    # 冲3防守
    elif get_punching_three(white_point, black_point, player_point, all_point):
        return get_punching_three(white_point, black_point, player_point, all_point)

    # 活2进攻
    elif get_live_two_points(black_point, player_point, all_point):
        return get_live_two_points(black_point, player_point, all_point)

    # 活2防守
    elif get_live_two_points(white_point, player_point, all_point):
        return get_live_two_points(white_point, player_point, all_point)

    # 活1进攻
    elif get_one_point(black_point, player_point, all_point):
        return get_one_point(black_point, player_point, all_point)

    # 活1防守
    elif get_one_point(white_point, player_point, all_point):
        return get_one_point(white_point, player_point, all_point)

# 电脑下棋
def down_chess(black_point, white_point, player_point, all_point):

    # chx, chy = random.choice(list(set(all_point)-set(player_point)))
    chice = random.choice(decisionTree(black_point, white_point, player_point, all_point))
    black_pos.append(chice)
    player_pos.append(chice)

while True:

    paint()  # 画棋盘
    for x, y in black_pos:
        pygame.draw.circle(screen, BLACK, (x, y), 15, 15)

    for x, y in white_pos:
        pygame.draw.circle(screen, WHITE, (x, y), 15, 15)

    # 人走棋
    if len(black_pos) == len(white_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                gx, gy = get_pos(mx, my)
                if (gx, gy) not in player_pos and game_state:
                    white_pos.append((gx, gy))
                    player_pos.append((gx, gy))
                    switch = not switch

                    # 判断是否是五子连珠
                    if get_five(white_pos):
                        white_state = True
                        black_state = False
                        game_state = False

    # 电脑走棋
    else:
        down_chess(black_pos, white_pos, player_pos, all_pos)
        switch = not switch
        # 判断是否是五子连珠
        if get_five(black_pos):
            white_state = False
            black_state = True
            game_state = False

    # ------- 显示胜负 -------- #
    if black_state:
        text = font1.render("黑色棋子胜！", True, (255, 0, 0))
        screen.blit(text, (200, 80))

    elif white_state:
        text = font1.render("白色棋子胜!", True, (255, 0, 0))
        screen.blit(text, (200, 80))

    # ------- 重新开始 -------- #
    m1, m2, m3 = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    if m1 and 282 < mx < 282 + 120 and 650 < my < 650 + 50:
        screen.blit(restart2, (282, 650))
        game_state = True
        player_pos.clear()
        white_pos.clear()
        black_pos.clear()
        switch = True
        white_state = False
        black_state = False
        # text = font1.
    else:
        screen.blit(restart, (282, 650))
    screen.blit(re_text, (290, 650))

    pygame.display.update()
