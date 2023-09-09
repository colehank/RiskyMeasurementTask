import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import interp1d

def discrete_gaussian_pmf(x, mean, std_dev):
    pdf = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev)**2)
    pmf = pdf / np.sum(pdf)
    return pmf

def cardA():
    # 分布1
    mean1 = 100
    std_dev1 = 25
    x_values1 = np.arange(mean1-100, mean1+101)
    pmf1 = discrete_gaussian_pmf(x_values1, mean1, std_dev1)
    pmf1 *= 0.5 / np.sum(pmf1)

    # 分布2
    mean2 = -150
    std_dev2 = 25
    x_values2 = np.arange(mean2-100, mean2+101)
    pmf2 = discrete_gaussian_pmf(x_values2, mean2, std_dev2)
    pmf2 *= 0.5 / np.sum(pmf2)

    # 合并两个分布的取值范围和取值
    x_values = np.concatenate([x_values1, x_values2])
    total_pmf = np.concatenate([pmf1, pmf2])

    return x_values, total_pmf

def cardB():
    # 生成分布1
    mean1 = -100
    std_dev1 = 25
    x_values1 = np.arange(mean1-100, mean1+101)
    pmf1 = discrete_gaussian_pmf(x_values1, mean1, std_dev1)
    pmf1 *= 0.9 / np.sum(pmf1)

    # 生成分布2
    mean2 = -1150
    std_dev2 = 25
    x_values2 = np.arange(mean2-100, mean2+101)
    pmf2 = discrete_gaussian_pmf(x_values2, mean2, std_dev2)
    pmf2 *= 0.1 / np.sum(pmf2)

    # 合并两个分布的取值范围和取值
    x_values = np.concatenate([x_values1, x_values2])
    total_pmf = np.concatenate([pmf1, pmf2])

    return x_values, total_pmf

def cardC():
    # 生成分布1
    mean1 = 50
    std_dev1 = 25
    x_values1 = np.arange(mean1-100, mean1+101)
    pmf1 = discrete_gaussian_pmf(x_values1, mean1, std_dev1)
    pmf1 *= 0.5 / np.sum(pmf1)

    # 生成分布2
    mean2 = 0
    std_dev2 = 25
    x_values2 = np.arange(mean2-100, mean2+101)
    pmf2 = discrete_gaussian_pmf(x_values2, mean2, std_dev2)
    pmf2 *= 0.5 / np.sum(pmf2)

    # 合并两个分布的取值范围和取值
    x_values = np.concatenate([x_values1, x_values2])
    total_pmf = np.concatenate([pmf1, pmf2])

    return x_values, total_pmf

def cardD():
    # 生成分布1
    mean1 = 50
    std_dev1 = 25
    x_values1 = np.arange(mean1-100, mean1+101)
    pmf1 = discrete_gaussian_pmf(x_values1, mean1, std_dev1)
    pmf1 *= 0.9 / np.sum(pmf1)

    # 生成分布2
    mean2 = -200
    std_dev2 = 25
    x_values2 = np.arange(mean2-100, mean2+101)
    pmf2 = discrete_gaussian_pmf(x_values2, mean2, std_dev2)
    pmf2 *= 0.1 / np.sum(pmf2)

    # 合并两个分布的取值范围和取值
    x_values = np.concatenate([x_values1, x_values2])
    total_pmf = np.concatenate([pmf1, pmf2])

    return x_values, total_pmf


# 修改期望值的函数
def modify_expectation(original_card_func, target_expectation):
    x_values, pmf = original_card_func()
    original_expectation = np.sum(x_values * pmf)
    delta = target_expectation - original_expectation
    new_x_values = x_values + delta
    
    def new_card_func():
        return new_x_values, pmf
    
    return new_card_func

# 根据新的要求生成函数
def generate_modified_functions(exp_A, exp_B, exp_C, exp_D):
    new_cardA = modify_expectation(cardA, exp_A)
    new_cardB = modify_expectation(cardB, exp_B)
    new_cardC = modify_expectation(cardC, exp_C)
    new_cardD = modify_expectation(cardD, exp_D)
    return new_cardA, new_cardB, new_cardC, new_cardD

#设置的难度范围
ranges = [(-190, 190), (-180, 180), (-170, 170), (-160, 160), (-150, 150), (-140, 140), (-130, 130), (-120,120),(-110,110),(-100,100),(-90,90),(-80,80),(-70,70),(-60,60),(-50,50),(-40,40),(-30,30),(-20,20),(-10,10)]

# 初始化存储结果的字典
results = {}

# 在不同范围内调用 generate_modified_functions 函数
for i, (start, end) in enumerate(ranges, 1):
    new_cardA, new_cardB, new_cardC, new_cardD = generate_modified_functions(start, start, end, end)
    results[f'new_cardA{i}'] = new_cardA
    results[f'new_cardB{i}'] = new_cardB
    results[f'new_cardC{i}'] = new_cardC
    results[f'new_cardD{i}'] = new_cardD




#原始IGT收益分布
cardA
cardB
cardC
cardD

#难度设置下的IGT收益分布
cardA1 = results['new_cardA1']()
cardB1 = results['new_cardB1']()
cardC1 = results['new_cardC1']()
cardD1 = results['new_cardD1']()

cardA2 = results['new_cardA2']()
cardB2 = results['new_cardB2']()
cardC2 = results['new_cardC2']()
cardD2 = results['new_cardD2']()

cardA3 = results['new_cardA3']()
cardB3 = results['new_cardB3']()
cardC3 = results['new_cardC3']()
cardD3 = results['new_cardD3']()

cardA4 = results['new_cardA4']()
cardB4 = results['new_cardB4']()
cardC4 = results['new_cardC4']()
cardD4 = results['new_cardD4']()

cardA5 = results['new_cardA5']()
cardB5 = results['new_cardB5']()
cardC5 = results['new_cardC5']()
cardD5 = results['new_cardD5']()

cardA6 = results['new_cardA6']()
cardB6 = results['new_cardB6']()
cardC6 = results['new_cardC6']()
cardD6 = results['new_cardD6']()

cardA7 = results['new_cardA7']()
cardB7 = results['new_cardB7']()
cardC7 = results['new_cardC7']()
cardD7 = results['new_cardD7']()

cardA8 = results['new_cardA8']()
cardB8 = results['new_cardB8']()
cardC8 = results['new_cardC8']()
cardD8 = results['new_cardD8']()

cardA9 = results['new_cardA9']()
cardB9 = results['new_cardB9']()
cardC9 = results['new_cardC9']()
cardD9 = results['new_cardD9']()

cardA10 = results['new_cardA10']()
cardB10 = results['new_cardB10']()
cardC10 = results['new_cardC10']()
cardD10 = results['new_cardD10']()

cardA11 = results['new_cardA11']()
cardB11 = results['new_cardB11']()
cardC11 = results['new_cardC11']()
cardD11 = results['new_cardD11']()

cardA12 = results['new_cardA12']()
cardB12 = results['new_cardB12']()
cardC12 = results['new_cardC12']()
cardD12 = results['new_cardD12']()

cardA13 = results['new_cardA13']()
cardB13 = results['new_cardB13']()
cardC13 = results['new_cardC13']()
cardD13 = results['new_cardD13']()

cardA14 = results['new_cardA14']()
cardB14 = results['new_cardB14']()
cardC14 = results['new_cardC14']()
cardD14 = results['new_cardD14']()

cardA15 = results['new_cardA15']()
cardB15 = results['new_cardB15']()
cardC15 = results['new_cardC15']()
cardD15 = results['new_cardD15']()

cardA16 = results['new_cardA16']()
cardB16 = results['new_cardB16']()
cardC16 = results['new_cardC16']()
cardD16 = results['new_cardD16']()

cardA17 = results['new_cardA17']()
cardB17 = results['new_cardB17']()
cardC17 = results['new_cardC17']()
cardD17 = results['new_cardD17']()

cardA18 = results['new_cardA18']()
cardB18 = results['new_cardB18']()
cardC18 = results['new_cardC18']()
cardD18 = results['new_cardD18']()

cardA19 = results['new_cardA19']()
cardB19 = results['new_cardB19']()
cardC19 = results['new_cardC19']()
cardD19 = results['new_cardD19']()










