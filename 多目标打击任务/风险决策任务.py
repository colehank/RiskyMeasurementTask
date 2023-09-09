"""任务通过点击目标物瞄准，按下空格键打击"""

import pygame
import sys
import math
import time
import random
import threading

fontpath = "Hiragino Sans GB.ttc"
pygame.font.init()
font = pygame.font.Font(fontpath, 36)
# 限制被试能够攻击的次数
limit = 120
LIMIT_ATTACK_COUNT = limit
attack_count = 0
# 颜色常量
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
# 画布尺寸
CANVAS_X = 1000  # 画布宽度
CANVAS_Y = 1000  # 画布高度
# 雷达界面参数
CENTER = (CANVAS_X // 2, CANVAS_Y // 2)  # 雷达中心点坐标
NUM_CIRCLES = 3  # 同心圆数量
MAX_RADIUS = 350  # 最大圆的半径
SPEED = 2  # 每秒旋转的角度数(s)
ROTATION_SPEED = 360 / SPEED  # 旋转速度
# 坐标轴参数
LINE_X1 = (CENTER[0] - MAX_RADIUS, CENTER[1])  # x轴起点
LINE_X2 = (CENTER[0] + MAX_RADIUS, CENTER[1])  # x轴终点
LINE_Y1 = (CENTER[0], CENTER[1] - MAX_RADIUS)  # y轴起点
LINE_Y2 = (CENTER[0], CENTER[1] + MAX_RADIUS)  # y轴终点
# 目标物属性
TARGET_RADIUS = 10  # 目标物半径
TARGET_COLOR = RED  # 目标物颜色
TARGET_COLOR_CLICKED = YELLOW  # 目标物被点击后的颜色
# 初始化Pygame
pygame.init()
screen = pygame.display.set_mode((CANVAS_X, CANVAS_Y))
pygame.display.set_caption('MTAM v1.7')
clock = pygame.time.Clock()
start_time = time.time()  # 记录起始时间
# 点击次数计数器
clicked_count = 0
#飞离次数
flyout_count = 0 # 成功打击的飞离与💥飞离集合
prob_fly_out_count = 0 #因概率飞离事件的次数——气球💥
# 初始概率和增加概率
base_p = 0.05
increment_p_values = {

    RED: 0.03,
    PURPLE: 0.05,
    CYAN: 0.1,
    BLUE: 0.4
    
}

# 目标物消灭计数器
total_destroyed_count = 0  # 目标物消灭总数
ROUND_NUM = [10,20,30,40,50,60,70,80,90,110,120]
# 是否可以击毁目标物的标志
destroy_active = True
# 帧率和飞离速度
FPS = 60  # 帧率
FLY_OUT_DURATION = 0.5  # 飞离屏幕的持续时间（秒）
FLY_OUT_SPEED = CANVAS_X / FPS / FLY_OUT_DURATION  # 每帧的移动距离
# 创建互斥锁对象
flyout_count_lock = threading.Lock()

class Target(pygame.sprite.Sprite):
    flyout_count = 0  # 飞离计数器（类属性）

    def __init__(self, center, radius, color, motion_radius, angular_speed, center_of_motion):
        """目标物的属性设置"""
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)#创建pygame.surface对象，长宽度都是【radius * 2】支持设置透明度pygame.SRCALPHA
        pygame.draw.circle(self.image, color, (radius, radius), radius)#在self.image上通过pygame.draw.circle绘制一个圆形，圆心 (radius, radius)，半径radius
        self.rect = self.image.get_rect(center=center)#使用get_rect()函数来获取self.image的矩形边界，并将其保存在self.rect中。矩形的中心坐标由center参数指定。
        self.angle = random.uniform(0, 2 * math.pi)#初始化了一个类的angle属性，该属性的值为0到2π之间的随机浮点数
        self.radius = motion_radius
        self.angular_speed = angular_speed
        self.color = color
        self.clicked = False#是否被点击
        self.moving_out = False#目标物是否正在向左飞离
        self.destroyed = False#目标物是否被击毁
        self.active = True  # 是否可以击毁目标物的标志
        self.fly_out_speed = FLY_OUT_SPEED #目标物飞离的速度
        self.center_of_motion = center_of_motion  # 新增：运动的中心点

        self.pos_offset_momentum_x = 0
        self.pos_offset_momentum_y = 0

        # Initialize the target position and the interpolation factor
        self.target_pos_x = self.center_of_motion[0] + self.radius * math.cos(self.angle)
        self.target_pos_y = self.center_of_motion[1] + self.radius * math.sin(self.angle)
        self.lerp_factor = 0.007
        self.acceleration_factor = 0.001  # Factor for controlling acceleration
        self.random_acceleration = 0.0001
        self.acceleration_decay = 1  # Decay factor for acceleration
        self.acceleration_counter = 0  # Counter for controlling acceleration changes
        self.random_position_change = 100






#如下都是目标物的方法
    def check_click(self, mouse_pos):
        #检查目标物是否被点击
        enlarged_rect = self.rect.inflate(10, 10)
        if enlarged_rect.collidepoint(mouse_pos):
            self.clicked = True
            return True
        return False
    def destroy(self):
        #将目标物设置为被击毁和不可击毁
        self.destroyed = True
        self.clicked = False
        self.active = False  # 不可击毁
        
    def fly_left(self):
        #将目标物设置为向左飞离，更新相关计数器
        global flyout_count
        self.moving_out = True
        self.active = False  # 设置为不可击毁
        self.clicked = False
        # 使用互斥锁保护计数器的访问

        flyout_count += 1  # 更新飞离计数器

    def draw(self, screen):
        screen.blit(self.image, self.rect)
       
    def update(self):
        """更新目标物的位置和状态"""
        if self.destroyed:
            #如果destroyed，x坐标-1000
            self.rect.x = -1000
        elif self.moving_out:
            #通过每帧移动fly_out_speed个像素到destroyed定义的位置
            self.rect.x -= self.fly_out_speed
        else:
            #如果没有被击中，继续做原来的运动
            self.angle += self.angular_speed
            pos_x = self.center_of_motion[0] + self.radius * math.cos(self.angle)
            pos_y = self.center_of_motion[1] + self.radius * math.sin(self.angle)
            self.rect.center = (pos_x, pos_y)

        if self.clicked:
            self.image.fill(TARGET_COLOR_CLICKED)#被点击后把image（矩形）填充为黄色
        else:
            self.image.fill(TRANSPARENT)#不然，透明

        pygame.draw.circle(self.image, self.color, (TARGET_RADIUS, TARGET_RADIUS), TARGET_RADIUS)
        #image对象上用color画一个圆心为(TARGET_RADIUS, TARGET_RADIUS)，半径为TARGET_RADIUS的圆

        if not self.destroyed and not self.moving_out:

            self.angle += self.angular_speed

            self.target_pos_x += random.uniform(-self.random_position_change, self.random_position_change)
            self.target_pos_y += random.uniform(-self.random_position_change, self.random_position_change)

            self.angular_speed += random.uniform(-self.random_acceleration, self.random_acceleration)

            pos_x = (1 - self.lerp_factor) * self.rect.center[0] + self.lerp_factor * self.target_pos_x
            pos_y = (1 - self.lerp_factor) * self.rect.center[1] + self.lerp_factor * self.target_pos_y

            self.rect.center = (pos_x, pos_y)

            # Control the acceleration changes
            self.acceleration_counter += 1
            if self.acceleration_counter >= 100:  # Adjust the counter value as needed
                self.random_acceleration *= -1  # Reverse the sign of random acceleration
                self.acceleration_counter = 0
            
            # Add a controlled random acceleration to the angular speed
            self.angular_speed += self.acceleration_factor * self.random_acceleration

        

        # 添加可见性判断
        if math.sqrt((self.rect.centerx - CENTER[0]) ** 2 + (self.rect.centery - CENTER[1]) ** 2) > MAX_RADIUS:
            self.image.set_alpha(0)  # 目标物在最大圆环外，设置透明度为0，使其不可见
        else:
            self.image.set_alpha(255)  # 目标物在最大圆环内，设置透明度为255，使其可见




# 创建目标物
num_targets_1 = 9
motion_radius_1 = 300
angular_speed_1 = 0.005
# 创建新目标物2
num_targets_2 = 4
motion_radius_2 = 200
angular_speed_2 = 0.001

targets = [
    Target(
        center=(CENTER[0] + (motion_radius_1 + i * 100) * math.cos(i * (2 * math.pi / num_targets_1)),
                CENTER[1] + (motion_radius_1 + i * 100) * math.sin(i * (2 * math.pi / num_targets_1))),
        radius=TARGET_RADIUS,
        color=TARGET_COLOR,
        motion_radius=motion_radius_1,
        angular_speed=angular_speed_1,
        center_of_motion=CENTER  # 新增：运动的中心点
    )
    for i in range(num_targets_1)
] + [
    Target(
        center=(CENTER[0] + (motion_radius_2 + i * 100) * math.cos(i * (2 * math.pi / num_targets_2)),
                CENTER[1] + (motion_radius_2 + i * 100) * math.sin(i * (2 * math.pi / num_targets_2))),
        radius=TARGET_RADIUS,
        color=TARGET_COLOR,
        motion_radius=motion_radius_2,
        angular_speed=angular_speed_2,
        center_of_motion=CENTER  # 新增：运动的中心点
    )
    for i in range(num_targets_2)
]

sprites = pygame.sprite.Group(*targets)

def show_welcome_message():
    welcome_message = ("欢迎来到多目标打击任务(Multi-target attack mission, MTAM)。\n"
                       "目前识别到四群敌方无人机，系统已用颜色进行了标注，\n请点击选择任意一个无人机群进行追踪。\n"
                       '\n'
                       "追踪后，你可以选择一个或多个无人机进行瞄准【Q键】，进而发射导弹【空格键】。\n"
                       '\n'
                       "请用有限的导弹尽可能多地击落无人机。"
                        "但请注意，随着瞄准数量增加，\n无人机逃逸的可能性会越来越大，从而导致已上膛的导弹失效。"
                       )
    welcome_font = pygame.font.Font(fontpath, 24)
    welcome_lines = welcome_message.splitlines()

    line_height = welcome_font.get_linesize()
    y = CANVAS_Y // 2 - (line_height * len(welcome_lines)) // 2

    for line in welcome_lines:
        welcome_text = welcome_font.render(line, True, WHITE)
        welcome_text_rect = welcome_text.get_rect(center=(CANVAS_X // 2, y))
        screen.blit(welcome_text, welcome_text_rect)
        y += line_height
    pygame.display.flip()
    # 等待玩家按下空格键开始游戏
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen.fill((0, 0, 0))  # 清空屏幕
                return                
            pygame.display.flip()



def color_choice():
    colors = {
        pygame.K_1: RED,
        pygame.K_2: PURPLE,
        pygame.K_3: CYAN,
        pygame.K_4: BLUE
    }

    centers = [
        (CANVAS_X // 4 + 40, CANVAS_Y // 4+20),
        (CANVAS_X // 4 * 3-40, CANVAS_Y // 4+20),
        (CANVAS_X // 4+ 40, CANVAS_Y // 4 * 3-20),
        (CANVAS_X // 4 * 3- 40, CANVAS_Y // 4 * 3-20)
    ]
    motion_radius = 130
    rects = [ pygame.Rect(center[0] - motion_radius, center[1] - motion_radius, motion_radius * 2, motion_radius * 2) for center in centers ] 
    # rects = [
    #     pygame.Rect(0, 0, CANVAS_X/2, CANVAS_Y/2),
    #     pygame.Rect(CANVAS_X/2, 0, CANVAS_X/2, CANVAS_Y/2),
    #     pygame.Rect(0, CANVAS_Y/2, CANVAS_X/2, CANVAS_Y/2),
    #     pygame.Rect(CANVAS_X/2, CANVAS_Y/2, CANVAS_X/2, CANVAS_Y/2)
    # ]

    # for center in centers:
    #         motion_radius = 5
    #         circle_rect = pygame.Rect(center[0] - motion_radius, center[1] - motion_radius, motion_radius * 2, motion_radius * 2)
    #         pygame.draw.ellipse(screen, (255, 0, 0), circle_rect, 2)
    

    


    target_colors = [RED, PURPLE, CYAN, BLUE]

    def create_targets(center, color):
        motion_radius_1 = 50
        motion_radius_2 = 100
        num_targets_a_1 = 9
        num_targets_a_2 = 7

        return [
            Target(
                center=(center[0] + (motion_radius + i * 100) * math.cos(i * (2 * math.pi / num_targets_a)),
                        center[1] + (motion_radius + i * 100) * math.sin(i * (2 * math.pi / num_targets_a))),
                radius= 5,
                color=color,
                motion_radius=motion_radius,
                angular_speed=angular_speed,
                center_of_motion=center
            )
            for motion_radius, num_targets_a, angular_speed in [(motion_radius_1, num_targets_a_1, angular_speed_1), (motion_radius_2, num_targets_a_2, angular_speed_2)]
            for i in range(num_targets_a)
        ]

    sprites = [pygame.sprite.Group(*create_targets(center, color)) for center, color in zip(centers, target_colors)]
    color_rects = list(zip(colors.values(), rects, sprites))



    text_prompt = font.render("请点击要打击的机群", True, WHITE)
    text_prompt_rect = text_prompt.get_rect()
    text_prompt_rect.center = (CANVAS_X // 2, CANVAS_Y//1.1)
    screen.blit(text_prompt, text_prompt_rect)

    text = font.render("已击毁无人机数量: " + str(total_destroyed_count), True, GREEN)  # 使用目标物消灭总数
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text, text_rect)

   # 绘制剩余可按空格的次数的文本
    misslie_remain = LIMIT_ATTACK_COUNT - attack_count - prob_fly_out_count

    remaining_text = font.render("导弹余量： " + str(misslie_remain) + '/120', True, GREEN)
    remaining_text_rect = remaining_text.get_rect()
    remaining_text_rect.topleft = (10, 50)
    screen.blit(remaining_text, remaining_text_rect)

    ing_text = font.render("多目标定位中..." , True, GREEN)
    ing_text_rect = ing_text.get_rect()
    ing_text_rect.topleft = (10, 90)
    screen.blit(ing_text, ing_text_rect)



    while True:
        screen.fill((0, 0, 0))
         # 绘制文本
        screen.blit(text, text_rect)
        screen.blit(text_prompt, text_prompt_rect)
        screen.blit(remaining_text, remaining_text_rect)
        screen.blit(ing_text, ing_text_rect)
        
        for color, rect, sprite_group in color_rects:
            # 如果鼠标悬浮在矩形上方，高亮该区域
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.ellipse(screen, (255, 255, 255), rect, 3)



        for i in range(1, NUM_CIRCLES + 1):
            pygame.draw.circle(screen, GREEN, CENTER, i * (MAX_RADIUS // NUM_CIRCLES), 1)

        pygame.draw.line(screen, GREEN, LINE_X1, LINE_X2, 1)
        pygame.draw.line(screen, GREEN, LINE_Y1, LINE_Y2, 1)

        for sprite in sprites:
            sprite.update()
            for target in sprite:
                if math.sqrt((target.rect.center[0] - CENTER[0]) ** 2 + (target.rect.center[1] - CENTER[1]) ** 2) <= MAX_RADIUS:
                    target.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for color, rect, _ in color_rects:
                    if rect.collidepoint(mouse_pos):
                        return color





def game_n(color_clicked):
    for target in targets:
        if target.active:
            target.color = color_clicked  # 设置目标物的颜色

####################
#游戏开始

show_welcome_message()
color_clicked = color_choice()

while True:
    #if LIMIT_ATTACK_COUNT == attack_count + prob_fly_out_count and all(target.rect.right < 0 or target.destroyed for target in targets):
    if any(attack_count + prob_fly_out_count == num for num in ROUND_NUM) and all(target.rect.right < 0 or target.destroyed for target in targets):
        #LIMIT_ATTACK_COUNT += limit
        color_clicked = color_choice()
        game_n(color_clicked)
        # 继续循环之前先更新游戏状态
        clicked_count = 0
        base_p = 0.03
        destroy_active = True
        for target in targets:
            target.clicked = False
            target.destroyed = False
            target.moving_out = False
            target.angle = random.uniform(0, 2 * math.pi)
            target.active = True
        start_time = time.time()

    game_n(color_clicked)
    screen.fill((0, 0, 0))
    #画雷达圆
    for i in range(1, NUM_CIRCLES + 1):
        pygame.draw.circle(screen, GREEN, CENTER, i * (MAX_RADIUS // NUM_CIRCLES), 1)
    #画坐标轴
    pygame.draw.line(screen, GREEN, LINE_X1, LINE_X2, 1)
    pygame.draw.line(screen, GREEN, LINE_Y1, LINE_Y2, 1)


    sprites.update()
    sprites.draw(screen)

    misslie_remain = LIMIT_ATTACK_COUNT - attack_count - prob_fly_out_count


    #text = font.render("Destroyed: " + str(total_destroyed_count), True, GREEN)  # 使用目标物消灭总数
    text = font.render("已击毁: " + str(total_destroyed_count)+ '+{}(已瞄准)'.format(clicked_count), True, GREEN)  # 使用目标物消灭总数
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text, text_rect)

   # 绘制剩余可按空格的次数的文本
    remaining_text = font.render("导弹余量： " + str(misslie_remain) + '/120', True, GREEN)
    remaining_text_rect = remaining_text.get_rect()
    remaining_text_rect.topleft = (10, 50)
    screen.blit(remaining_text, remaining_text_rect)




    pygame.display.flip()
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #被点击后，计算飞离概率
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for target in targets:
                if target.active and not target.clicked and target.check_click(mouse_pos):
                    #可击毁且未被点击；以及鼠标点击到了
                    clicked_count += 1
                    base_p += increment_p_values[color_clicked]  # 根据颜色获取对应的 increment_p 值
                    if base_p > random.random():
                        for target in targets:
                            target.fly_left()
                        prob_fly_out_count += 1  # 计算飞离事件的次数
                        destroy_active = False  # 禁止击毁目标物
                        break
        
        #增加Q键的选择机制
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # 添加对'q'键的处理
            active_targets = [target for target in targets if target.active and not target.clicked]
            if active_targets:  # 如果存在未被点击的、可击毁的目标物
                random_target = random.choice(active_targets)  # 随机选择一个
                random_target.clicked = True  # 将其设为已点击状态
                clicked_count += 1
                base_p += increment_p_values[color_clicked]  # 根据颜色获取对应的 increment_p 值
                if base_p > random.random():
                    destroy_active = False
                    for target in targets:
                        destroy_active = False  # 禁止击毁目标物
                        target.fly_left()
                    prob_fly_out_count += 1  # 计算飞离事件的次数

        
        #按ESC回到颜色选择页面
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            clicked_count = 0
            base_p = 0.03
            for target in targets:
                target.clicked = False
                target.destroyed = False
                target.moving_out = False
                target.angle = random.uniform(0, 2 * math.pi)
                target.active = True  # 重置为可击毁
            color_clicked = color_choice()



        #空格键后，收米
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if destroy_active:
                if attack_count + prob_fly_out_count < LIMIT_ATTACK_COUNT:  # 检查是否达到攻击次数限制
                    destroyed_count = 0  # 统计本次击毁的目标物数量
                    for target in targets:
                        if target.active and target.clicked:
                            target.destroy()
                            destroyed_count += 1  # 更新本次击毁的目标物数量
                            total_destroyed_count += 1  # 更新目标物消灭总数
                    if destroyed_count > 0:  # 如果本次击毁了目标物
                        attack_count += 1  # 更新击毁次数
                        for target in targets:
                            if target.active and not target.moving_out:
                                target.fly_left()
        


    # 目标物飞离进行下一轮试次
    if all(target.rect.right < 0 or target.destroyed for target in targets):
        clicked_count = 0
        base_p = 0.03
        destroy_active = True  # 允许击毁目标物
        for target in targets:
            target.clicked = False
            target.destroyed = False
            target.moving_out = False
            target.angle = random.uniform(0, 2 * math.pi)
            target.active = True  # 重置为可击毁
        start_time = time.time()

    