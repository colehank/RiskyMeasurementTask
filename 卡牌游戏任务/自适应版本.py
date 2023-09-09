#IGT爱荷华赌博任务
import os
import pygame
import random
import sys
import time
import datetime
import numpy as np
from module import difficulty as df

name = input('请输入您的名字拼音：')
# 初始化
pygame.init()
cur_path = os.path.dirname(__file__)
# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# 窗口大小
WINDOW_WIDTH,WINDOW_HEIGHT = 1000, 800
CARD_WIDTH, CARD_HEIGHT = 150, 225
# 字体
font = pygame.font.Font('Hiragino Sans GB.ttc', 40)

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



def show_welcome_message():
    welcome_message = ("欢迎来到卡牌游戏任务。\n"
                       "这是一个在四个卡牌中学习哪张卡牌长期收益最多的游戏,\n"
                       '\n'
                       "在游戏开始时会奖励您2000元。\n"
                       '\n'
                       "在难度自适应版本中,"
                        "系统会根据您的表现判断是否升级或降级,\n每次升级将会获得一定奖金，每次降级将会导致资产缩水。"
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

# 设置初始化难度
difficulty = 10#初始难度
card_positions = []
# 卡牌收益计算器
def expectation(card):
    return np.sum(np.array(card[0]) * np.array(card[1]))
# 生成卡片位置
card_spacing = (WINDOW_WIDTH - 4 * CARD_WIDTH) // 5
for i in range(4):
    x = card_spacing * (i + 1) + CARD_WIDTH * i
    y = 50
    card_positions.append((x, y))


#创建一个储存卡牌位置和标识的字典
card_mapping = {}
new_card = cards_dict[difficulty]
random.shuffle(new_card)
for i, (x, y) in enumerate(card_positions):
    card_mapping[(x, y)] = new_card[i]
print("card_mapping的keys:", ', '.join(str(key) for key in card_mapping.keys()))
print("card_mapping函数的期望:", ', '.join(str(expectation(value)) for value in card_mapping.values()))

# 判断鼠标是否在卡片上
def is_mouse_over_card(card_position, mouse_pos):
    x, y = card_position
    return x < mouse_pos[0] < x + CARD_WIDTH and y < mouse_pos[1] < y + CARD_HEIGHT

def expectation(card):
    return np.sum(np.array(card[0]) * np.array(card[1]))


# 初始化游戏参数
running = True
iswaiting = True
reward = 0
lost = 0
earnings = 2000
total_clicks = 0
flexibility_clicks = 0
difficulty_range = range(1,20,1)
#answer = False
# 初始化记录
records = { 'reward': [], 'click_num': [], 'earning': [], 'chosencardexpectation': [], 'difficulty': [],'goodorbad':[], 'quest_click':[], 'confidence_click':[]}
quest_records = []
confidence_records = []

difficulty = 10

# 生成好牌坏牌列表
good_dict = {}
good_cards = []
bad_cards = [] 


T0 = time.time()
# 开始游戏
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
while running:
    
    # listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            # 鼠标点击卡牌
            mouse_pos = pygame.mouse.get_pos()

            if any(mouse_check:=[is_mouse_over_card(_, mouse_pos) for _ in card_positions]):
                print('Mouse check',mouse_check)
                print('card_positions',card_positions)
                waiting_judge = True
                total_clicks += 1
                records['click_num'].append(total_clicks)
                # 获取card
                card_position = card_positions[np.where(np.array(mouse_check)==True)[0][0]]
                print(f"点击了卡牌{card_position}")
                card = card_mapping[card_position]
                # 产生收益
                x_values, pmf = card
                # 在收益分布中，随机取一个值
                reward = np.random.choice(x_values, p=pmf)
                print("本次奖金:", reward,'选择期望:',expectation(card))
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
                records['chosencardexpectation'].append(expectation(card))
                # 记录难度
                records['difficulty'].append(difficulty)
                
                    
                # 生成本轮好牌坏牌列表
                good_pos = []
                bad_pos = []   
                for pos,_card in card_mapping.items():
                    # 计算卡片期望值
                    exp = expectation(_card)
                    # 根据期望值进行牌的属性分类
                    if exp > 0:
                        good_pos.append(pos) 
                    else:
                        bad_pos.append(pos) 
                # 记录点击牌的属性
                if card_position in good_pos:
                    records['goodorbad'].append(True)
                    print('点击了好牌')
                elif card_position in bad_pos:
                    records['goodorbad'].append(False)
                    print('点击了坏牌')
        

    screen.fill(pygame.Color("black"))
    for x, y in card_positions:
        screen.blit(card_image, (x, y))
    
    for (x, y),card in card_mapping.items():
        # 获取当前卡片的期望值
        card_expectation = expectation(card)  # 假设计算期望值的函数

        # 创建要显示的文本
        expectation_text = font.render(" {:.2f}".format(card_expectation), True, pygame.Color("white"))
        # 计算文本的位置，使其在卡片下方居中显示
        text_x = x + (CARD_WIDTH - expectation_text.get_width()) // 2
        text_y = y + CARD_HEIGHT + 40
        # 将期望值文本绘制在屏幕上
        #screen.blit(expectation_text, (text_x, text_y))

    if total_clicks % 7 == 0 and total_clicks != 0 and waiting_judge:
        records['quest_click'].append(total_clicks)
        judge_text = font.render("请选择长期来看收益最高的两张牌", True, pygame.Color("white"))
        screen.blit(judge_text, (WINDOW_WIDTH // 2 - judge_text.get_width() // 2, 500))
        pygame.display.flip()
        
        #记录玩家选择
        response = []
        last_selected_card = None  # 记录上次选择的卡牌
        while len(response) < 2:
            #绘制选择卡牌以及设置两次不能点一个卡牌，记录用户选择
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if any(mouse_check:=[is_mouse_over_card(_, mouse_pos) for _ in card_positions]):
                        card_pos = card_positions[np.where(np.array(mouse_check)==1)[0][0]]
                        if last_selected_card is None or last_selected_card != card_pos:
                            response.append(card_pos)
                            print("选择了卡牌", card_pos)
                            last_selected_card = card_pos

                            # 使用绿色框框常亮玩家选择
                            highlight_rect = pygame.Rect(card_pos[0] - 5, card_pos[1] - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
                            pygame.draw.rect(screen, pygame.Color(GREEN), highlight_rect, 3)
                        pygame.display.flip()
                        # 第二次选择后暂停200ms
                        if len(response) == 2:  
                            #判断玩家选择是否正确
                            answer = set(response)==set(good_pos)
                            print('玩家选择是否正确:',answer)
                            quest_records.append(answer)
                            print('quest_records:',quest_records)
                            waiting_judge = False
                            pygame.time.wait(400)

        if total_clicks % 21 == 0:
            records['confidence_click'].append(total_clicks)
            screen.fill(pygame.Color("black"))
            # 圆环绘制
            circle_rects = []
            circle_radius = 30
            circle_spacing = 100
            for i in range(7):
                circle_x = (WINDOW_WIDTH - (circle_spacing * 6)) // 2 + i * circle_spacing
                circle_y = WINDOW_HEIGHT // 2
                circle_rect = pygame.draw.circle(screen, WHITE, (circle_x, circle_y), circle_radius, 2)
                circle_rects.append(circle_rect)

                text_surface = font.render(str(i + 1), True, WHITE)
                text_rect = text_surface.get_rect(center=circle_rect.center)
                screen.blit(text_surface, text_rect)

            # 遍历圆环位置
            for i, circle_rect in enumerate(circle_rects):
                if circle_rect.collidepoint(mouse_pos):
                    pygame.draw.circle(screen,GREEN, circle_rect.center, circle_radius + 5, 3)
                else:
                    pygame.draw.circle(screen, WHITE, circle_rect.center, circle_radius, 2)

                text_surface = font.render(str(i + 1), True, WHITE)
                text_rect = text_surface.get_rect(center=circle_rect.center)
                screen.blit(text_surface, text_rect)
            
            # 绘制信心评价文本
            confidence_text_lines = [
                "请对您刚刚选择的信心程度进行判断，",
                "分数越高，表示越有信心。"
            ]

            for line_num, line in enumerate(confidence_text_lines):
                line_text = font.render(line, True, WHITE)
                text_x = WINDOW_WIDTH // 2 - line_text.get_width() // 2
                text_y = 150 + line_num * (line_text.get_height() + 10)  # 增加垂直间距
                screen.blit(line_text, (text_x, text_y))
            pygame.display.flip()
            print('信心判断ing')
            confidence_part = False
            while not confidence_part:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if any(mouse_check:=[circle_rect.collidepoint(mouse_pos) for circle_rect in circle_rects]):
                            selected_circle = np.where(np.array(mouse_check)==1)[0][0] + 1
                            print("信心选择为:", selected_circle)
                            confidence_records.append(selected_circle)
                            confidence_part = True  # 设置标志变量为 True，退出循环
 
        # 难度以及奖励机制
        if len(records["difficulty"]) >= 14:
            print('当前难度：',difficulty, '已点击', records['click_num'][-1])
            if quest_records[-2::] == [True, True] and difficulty == records['difficulty'][-10]:#判断为学会
                print('判断为学会')
                max_value = max(difficulty_range)
                difficulty = np.ceil((max_value + difficulty) / 2)
                print('奖励2000元')
                earnings += 2000#学会奖励两千
                print('随机化卡牌位置')
                # 好牌位置放新的坏牌
                new_card = cards_dict[difficulty]
                if random.random() < 0.5:
                    candidates = [good_pos, good_pos[::-1]]
                    chosen_pos = random.choice(candidates)
                    for i, pos in enumerate(chosen_pos):
                        card_mapping[pos] = new_card[i]
                    # 坏牌位置放新的好牌 
                    candidates = [bad_pos, bad_pos[::-1]]
                    chosen_pos = random.choice(candidates)
                    for i, pos in enumerate(chosen_pos):
                        card_mapping[pos] = new_card[i+2]
                else:
                    random.shuffle(new_card)
                    for i, (x, y) in enumerate(card_positions):
                        card_mapping[(x, y)] = new_card[i]
            elif quest_records[-2::] == [False, False] and difficulty == records['difficulty'][-10]:#判断为没有学会
                print('判断为没有学会')
                min_value = min(difficulty_range)
                difficulty = int((min_value + difficulty) / 2)
                print('原基础惩罚50%')
                earnings = earnings*0.5
                print('随机化卡牌位置')
                new_card = cards_dict[difficulty]
                if random.random() < 0.5:
                    # 好牌位置放新的坏牌
                    candidates = [good_pos, good_pos[::-1]]
                    chosen_pos = random.choice(candidates)
                    for i, pos in enumerate(chosen_pos):
                        card_mapping[pos] = new_card[i]
                    # 坏牌位置放新的好牌 
                    candidates = [bad_pos, bad_pos[::-1]]
                    chosen_pos = random.choice(candidates)
                    for i, pos in enumerate(chosen_pos):
                        card_mapping[pos] = new_card[i+2]
                else:
                    random.shuffle(new_card)
                    for i, (x, y) in enumerate(card_positions):
                        card_mapping[(x, y)] = new_card[i]
            else:
                if time.time() - T0 > 20*60 or (len(records['difficulty'])>35 and len(np.unique(records['difficulty'][-35::]))==1):
                    filename = f"{cur_path}/IGT_adaption_{name}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.npy"
                    data = np.array([{'record':records, 'quest':quest_records, 'confidence':confidence_records}])
                    np.save(filename, data, allow_pickle=True)
                    running = False
                print('判断为不确定，保持难度')
                
            print('随机化卡牌位置')
            # 好牌位置放新的坏牌
            new_card = cards_dict[difficulty]
            candidates = [good_pos, good_pos[::-1]]
            chosen_pos = random.choice(candidates)
            for i, pos in enumerate(chosen_pos):
                card_mapping[pos] = new_card[i]
            # 坏牌位置放新的好牌 
            candidates = [bad_pos, bad_pos[::-1]]
            chosen_pos = random.choice(candidates)
            for i, pos in enumerate(chosen_pos):
                card_mapping[pos] = new_card[i+2]      
        else:
            print('未到难度更新条件')

    else:
        reward_text = font.render("总收益: {:.2f}¥".format(earnings), True, pygame.Color("white"))
        result_text = font.render("本次结果: {:.2f}¥".format(reward), True, pygame.Color("white"))
        #total_click_text = font.render("总点击数: {:.2f}".format(total_clicks), True, pygame.Color("white"))
        #difficulty_text = font.render("难度等级: {:.2f}".format(difficulty), True, pygame.Color("white"))
        
        screen.blit(reward_text, (420, 500))
        screen.blit(result_text, (420, 550))
        #screen.blit(total_click_text, (420, 600))
        #screen.blit(difficulty_text, (420, 650))
    
        #绘制收益条
        bar_width = 1000
        bar_height = 50
        earnings_length = int(earnings / 10000 * bar_width)
        pygame.draw.rect(screen, GREEN, pygame.Rect(0, 400, earnings_length, bar_height))
        if time.time() - T0 > 20*60 or (len(records['difficulty'])>35 and len(np.unique(records['difficulty'][-35::]))==1):
            filename = f"{cur_path}/IGT_adaption_{name}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.npy"
            data = np.array([{'record':records, 'quest':quest_records, 'confidence':confidence_records}])
            np.save(filename, data, allow_pickle=True)
            running = False
    

    
    mouse_pos = pygame.mouse.get_pos()
    for card_pos in card_positions:
        if is_mouse_over_card(card_pos, mouse_pos):
            highlight_rect = pygame.Rect(card_pos[0] - 5, card_pos[1] - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
            pygame.draw.rect(screen, pygame.Color("yellow"), highlight_rect, 3)


    
    pygame.display.flip()

