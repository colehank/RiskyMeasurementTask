#IGT爱荷华赌博任务

import pygame
import random
import numpy as np
from module import difficulty as df
import sys

# 初始化
pygame.init()
# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# 窗口大小
WINDOW_WIDTH,WINDOW_HEIGHT = 1000, 800
CARD_WIDTH, CARD_HEIGHT = 150, 225
# 新增界面相关常量
BLOCK_START_X, BLOCK_START_Y = 50, 50
BLOCK_COLOR_NORMAL = (100, 100, 100)
BLOCK_COLOR_HOVER = (150, 150, 150)
BLOCK_COLOR_CLICKED = (200, 200, 200)
# 新的方块大小和间隔
BLOCK_WIDTH, BLOCK_HEIGHT = 200, 100
BLOCK_SPACING_X = 40
BLOCK_SPACING_Y = 40
NUM_COLS = 4
NUM_ROWS = 5

selected_difficulty = None

# 绘制难度方块
def draw_difficulty_blocks():

    for i in range(1, 20):
        col = (i - 1) % NUM_COLS
        row = (i - 1) // NUM_COLS
        x = BLOCK_START_X + col * (BLOCK_WIDTH + BLOCK_SPACING_X)
        y = BLOCK_START_Y + row * (BLOCK_HEIGHT + BLOCK_SPACING_Y)
        block_rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

        if is_mouse_over_block(block_rect):
            color = BLOCK_COLOR_HOVER
        else:
            color = BLOCK_COLOR_NORMAL

        pygame.draw.rect(screen, color, block_rect)
        text = font.render(f"难度 {i}", True, pygame.Color("white"))
        text_x = x + (BLOCK_WIDTH - text.get_width()) // 2
        text_y = y + (BLOCK_HEIGHT - text.get_height()) // 2
        screen.blit(text, (text_x, text_y))
        


def is_mouse_over_block(block_rect):
    mouse_pos = pygame.mouse.get_pos()
    return block_rect.collidepoint(mouse_pos)

                






# 载入卡片
card_image = pygame.image.load("card.png")
card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
cards_dict = {1:[df.cardA1,df.cardB1,df.cardC1,df.cardD1],
            2:[df.cardA2,df.cardB2,df.cardC2,df.cardD2],
            3:[df.cardA3,df.cardB3,df.cardC3,df.cardD3],
            4:[df.cardA4,df.cardB4,df.cardC4,df.cardD4],
            5:[df.cardA5,df.cardB5,df.cardC5,df.cardD5],
            6:[df.cardA6,df.cardB6,df.cardC6,df.cardD6],
            7:[df.cardA7,df.cardB7,df.cardC7,df.cardD7],
            8:[df.cardA8,df.cardB8,df.cardC8,df.cardD8],
            9:[df.cardA9,df.cardB9,df.cardC9,df.cardD9],
            10:[df.cardA10,df.cardB10,df.cardC10,df.cardD10],
            11:[df.cardA11,df.cardB11,df.cardC11,df.cardD11],
            12:[df.cardA12,df.cardB12,df.cardC12,df.cardD12],
            13:[df.cardA13,df.cardB13,df.cardC13,df.cardD13],
            14:[df.cardA14,df.cardB14,df.cardC14,df.cardD14],
            15:[df.cardA15,df.cardB15,df.cardC15,df.cardD15],
            16:[df.cardA16,df.cardB16,df.cardC16,df.cardD16],
            17:[df.cardA17,df.cardB17,df.cardC17,df.cardD17],
            18:[df.cardA18,df.cardB18,df.cardC18,df.cardD18],
            19:[df.cardA19,df.cardB19,df.cardC19,df.cardD19],}
# 设置窗口
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("IGT V1.0")

# 设置卡片位置
card_spacing = (WINDOW_WIDTH - 4 * CARD_WIDTH) // 5
card_positions = []
# 生成卡片位置
for i in range(4):
    x = card_spacing * (i + 1) + CARD_WIDTH * i
    y = 50
    card_positions.append((x, y))

# 字体
font = pygame.font.Font('Hiragino Sans GB.ttc', 40)

# 绘制卡片
def draw_cards():
    for x, y in card_positions:
        screen.blit(card_image, (x, y))

def exp_txt(difficulty):
    for i, (x, y) in enumerate(card_positions):
        # 获取当前卡片的期望值
        card = cards_dict[difficulty][i]  # 假设获取当前卡片
        card_expectation = expection(card)  # 假设计算期望值的函数

        # 创建要显示的文本
        expectation_text = font.render(" {:.2f}".format(card_expectation), True, pygame.Color("white"))

        # 计算文本的位置，使其在卡片下方居中显示
        text_x = x + (CARD_WIDTH - expectation_text.get_width()) // 2
        text_y = y + CARD_HEIGHT + 40

        # 将期望值文本绘制在屏幕上
        screen.blit(expectation_text, (text_x, text_y))

# 判断鼠标是否在卡片上
def is_mouse_over_card(card_position, mouse_pos):
    x, y = card_position
    return x < mouse_pos[0] < x + CARD_WIDTH and y < mouse_pos[1] < y + CARD_HEIGHT



# 卡牌收益计算器
def expection(card):
    x_values, pmf = card
    return np.sum(x_values * pmf)


# 随机重新排列卡牌位置
def randomize_card_positions():
    random.shuffle(card_positions)

    # 卡牌收益计算器
def expection(card):
    x_values, pmf = card
    return np.sum(x_values * pmf)


def show_welcome_message():
    welcome_message = ("欢迎来到卡牌游戏任务。\n"
                       "这是一个在四个卡牌中学习哪张卡牌长期收益最多的游戏,\n"
                       '\n'
                       "在游戏开始时会奖励您2000元。\n"
                       '\n'
                       "在难度分级版本中,"
                        "您将会选择特定难度进行游戏,\n在进行过程中，您可以通过按键【esc】回到难度选择界面。"
                       )
    welcome_font = pygame.font.Font('Hiragino Sans GB.ttc', 24)
    welcome_lines = welcome_message.splitlines()

    line_height = welcome_font.get_linesize()
    y = WINDOW_HEIGHT // 2 - (line_height * len(welcome_lines)) // 2

    for line in welcome_lines:
        welcome_text = welcome_font.render(line, True, WHITE)
        welcome_text_rect = welcome_text.get_rect(center=(WINDOW_WIDTH // 2, y))
        screen.blit(welcome_text, welcome_text_rect)
        y += line_height

    pygame.display.flip()

# 主函数
def main():
    # 初始化游戏参数
    running = True
    reward = 0
    lost = 0
    earnings = 2000
    total_clicks = 0
    flexibility_clicks = 0
    difficulty = 0
    #answer = False
    # 初始化记录
    records = { 'reward': [], 'click_num': [], 'earning': [], 'cardexpectation': [], 'difficulty': [],'response':[],'flexibility_clicks':[]}
    quest_records = []
    flexibliity = False



    # 在主函数中定义游戏状态
    difficulty_selection = "difficulty_selection"
    card_game = "card_game"
    current_game_state = difficulty_selection

    
    isintro = True
    while isintro:
        show_welcome_message()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                isintro = False
                break


    # 开始游戏
    while running:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('回到难度选择界面')
                current_game_state = difficulty_selection
                earnings = 2000
                total_clicks = 0
                reward = 0

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 获取鼠标位置
                mouse_pos = pygame.mouse.get_pos()

                # 判断当前游戏状态为难度选择
                if current_game_state == difficulty_selection:
                    # 遍历每个难度块
                    for i in range(1, 20):
                        col = (i - 1) % NUM_COLS
                        row = (i - 1) // NUM_COLS
                        x = BLOCK_START_X + col * (BLOCK_WIDTH + BLOCK_SPACING_X)
                        y = BLOCK_START_Y + row * (BLOCK_HEIGHT + BLOCK_SPACING_Y)
                        block_rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

                        # 判断鼠标点击是否在难度块上
                        if block_rect.collidepoint(mouse_pos):
                            print('难度选择')
                            selected_difficulty = i
                            difficulty = i  # 将难度值传递给 difficulty 变量
                            print('难度值为', difficulty)
                            current_game_state = card_game  # 切换游戏状态为 card_game
                            break  # 退出循环，不需要继续判断其他难度块



                # 判断当前游戏状态为卡牌游戏
                elif current_game_state == card_game:
                    print('游戏状态')
                    #若执行灵活性测试模块
                    if flexibliity == True:
                        ...
                    #若不执行灵活性测试模块
                    else:
                        # 根据难度选择卡牌对应的收益分布
                        cards = cards_dict[selected_difficulty]
                        # 卡牌期望计算方法
                        expectations = [expection(card) for card in cards]
                        # 根据期望值判断好牌，生成好牌列表
                        good_cards = [i for i, expectation in enumerate(expectations) if expectation >= 0]
                        bad_cards = [i for i, expectation in enumerate(expectations) if expectation < 0]
                        # random.shuffle(good_cards)
                        # random.shuffle(bad_cards)
                        # 遍历卡片位置
                        ipos = np.where(np.array([ is_mouse_over_card(pos, mouse_pos) for pos in card_positions ])==1)[0]
                        if ipos.size ==1:
                            # 记录点击次数
                            total_clicks += 1
                            records['click_num'].append(total_clicks)
                            card = cards[ipos[0]]

                            # 获取当前难度下收益和概率
                            x_values, pmf = card
                            # 计算函数总体期望
                            exceptation = expection(card)
                            # 在收益分布中，随机取一个值
                            reward = np.random.choice(x_values, p=pmf)
                            if reward > 0:
                                earnings += reward
                            else:
                                lost += abs(reward)
                                earnings += reward
                            # 记录收益
                            records['reward'].append(reward)
                            # 记录总收益
                            records['earning'].append(earnings)
                            # 记录卡片期望
                            records['cardexpectation'].append(exceptation)
                            # 记录难度
                            records['difficulty'].append(difficulty)

                            if total_clicks % 20 == 0 and total_clicks != 0:
                                print('bad',bad_cards,'  good',good_cards)  
                                new_cards =  [None, None, None, None]
                                for i,pos in enumerate(bad_cards):
                                    new_cards[pos] = cards[good_cards[i]]
                                for i,pos in enumerate(good_cards):
                                    new_cards[pos] = cards[bad_cards[i]]
                                cards = new_cards



                    
        
                            
        # 根据当前游戏状态进行绘制
        screen.fill(pygame.Color("black"))
        if current_game_state == difficulty_selection:
            draw_difficulty_blocks()
            pygame.display.flip()

        elif current_game_state == card_game:
            draw_cards()
            #exp_txt(difficulty)
            mouse_pos = pygame.mouse.get_pos()
            for card_pos in card_positions:
                if is_mouse_over_card(card_pos, mouse_pos):
                    highlight_rect = pygame.Rect(card_pos[0] - 5, card_pos[1] - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
                    pygame.draw.rect(screen, pygame.Color("yellow"), highlight_rect, 3)

            reward_text = font.render("总收益: {:.2f}¥".format(earnings), True, pygame.Color("white"))
            result_text = font.render("本次结果: {:.2f}¥".format(reward), True, pygame.Color("white"))
            #total_click_text = font.render("总点击数: {:.2f}".format(total_clicks), True, pygame.Color("white"))
            #difficulty_text = font.render("难度等级: {:.2f}".format(difficulty), True, pygame.Color("white"))
            #flexibility_clicks_text = font.render("灵活性测试点击数: {:.2f}".format(flexibility_clicks), True, pygame.Color("white"))


            screen.blit(reward_text, (420, 500))
            screen.blit(result_text, (420, 550))
            #screen.blit(total_click_text, (420, 600))
            #screen.blit(difficulty_text, (420, 650))
            #screen.blit(flexibility_clicks_text, (420, 700))

            #绘制收益条
            bar_width = 1000
            bar_height = 50
            total_earnings = 10000
            earnings_length = int(earnings / total_earnings * bar_width)
            pygame.draw.rect(screen, GREEN, pygame.Rect(0, 400, earnings_length, bar_height))
            pygame.display.flip()


if __name__ == "__main__":
    main()

