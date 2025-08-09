import pygame
import time
import random

# 初始化 pygame
pygame.init()

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 设置显示窗口
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('贪吃蛇游戏 by AI')

# 设置游戏时钟
clock = pygame.time.Clock()

# 蛇的大小和速度
snake_block = 10
snake_speed = 15

# 设置字体
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# 显示得分
def your_score(score):
    value = score_font.render("得分: " + str(score), True, black)
    dis.blit(value, [0, 0])

# 绘制蛇
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# 显示消息
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# 游戏主循环
def gameLoop():
    game_over = False
    game_close = False

    # 初始化蛇的位置
    x1 = dis_width / 2
    y1 = dis_height / 2

    # 初始化蛇的移动方向
    x1_change = 0
    y1_change = 0

    # 初始化蛇的身体
    snake_List = []
    Length_of_snake = 1

    # 随机生成食物位置
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(white)
            message("游戏结束! 按Q-退出 或 C-再玩一次", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 检查是否撞墙
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        
        # 绘制食物
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        
        # 更新蛇的身体
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        # 删除多余的蛇身段
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 绘制蛇
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # 检查是否吃到食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # 控制游戏速度
        clock.tick(snake_speed)

    # 退出游戏
    pygame.quit()
    quit()

# 启动游戏
gameLoop()
