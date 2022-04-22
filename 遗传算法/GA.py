#利用遗传算法求解f(x)=x^2在(0,31)内整数解的最大值
import matplotlib.pyplot as plt
import numpy as np
import random

#种群初始化
def initialize(n): # n为种群规模
    population=[] # 存储种群的列表
    for i in range(n): #根据种群规模对每个个体循环初始化
        x = random.randint(0, 31) #利用python内置函数randint生成范围内的随机数以初始化一个个体
        population.append(x) #将个体添加进种群
    return population #返回种群

#编码，将整型转化为二进制编码
def encode(population): #population为种群列表
    population_chromosome = [] #存储种群染色体的列表
    for i in range(len(population)):  # 循环对个体进行编码
        chro=bin(population[i]) #利用bin函数将十进制转化为二进制
        chro=chro[2:] #去除头部0b
        for j in range(5-len(chro)): #算出高位缺失的个数
            chro="0"+chro #循环高位补0
        population_chromosome.append(chro) #将染色体加入列表
    return population_chromosome #返回染色体列表

#将二进制编码转化为十进制
def decode(chro): #chro为二进制染色体
    result=0 #存储十进制结果
    for i in range(5):
        result=result+int(chro[i])*2**(4-i) #利用二进制十进制的转化原理
    return result #返回结果

#适应度函数
def fitness_func(population_chromosome): #population_chromosome为种群染色体
    fitness = [] #适应度列表
    for i in range(len(population_chromosome)): #循环解码
        x=decode(population_chromosome[i]) #转化为十进制
        value=x**2 #将目标函数当作适应度
        fitness.append(value) #加入适应度列表
    return fitness #返回适应度列表

#轮盘赌选择
def select(population_chromosome): #传入种群染色体列表
    fitness = fitness_func(population_chromosome) #计算适应度列表
    sum_fitness = 0 #存储适应度之和
    for i in range(len(fitness)): #循环计算适应度之和
        sum_fitness += fitness[i] #累加
    probability = [] #存储各个个体被选择的概率列表
    for i in range(len(fitness)): #循环计算各个个体的选择概率
        probability.append(fitness[i] / sum_fitness) #加入到概率列表
    probability_disrtib = [] #概率分布列表
    for i in range(len(fitness)): #循环计算概率分布
        if i == 0: probability_disrtib.append(probability[i]) #第一个时，直接加
        else: probability_disrtib.append(probability_disrtib[i - 1] + probability[i]) #后面进行累加
    population_chromosome_new=[] #存储新种群
    for i in range(len(population_chromosome)): #进行种群规模次轮盘赌
        p=random.random() #生成0到1之间的随机浮点数
        for j in range(len(probability_disrtib)): #进行轮盘赌
            if j==0: #轮盘的开始部分的情况
                if p <= probability_disrtib[0]: #若在这部分
                    population_chromosome_new.append(population_chromosome[0]) #将选择的个体染色体加入到新种群染色体列表中
                    break #结束循环
            if p > probability_disrtib[j] and p <= probability_disrtib[j+1]: #找到轮盘停止的位置
                population_chromosome_new.append(population_chromosome[j]) #将选择的个体染色体加入到新种群染色体列表中
                break #结束循环
    return population_chromosome_new #返回经过选择的种群染色体列表

#单点杂交
def crossover(population_chromosome_new): #传入经过选择的种群染色体列表
    for i in range(len(population_chromosome_new)-1): #对每个个体染色体与后一个进行交叉
        is_cross = random.random() #生成0到1之间的随机浮点数
        if is_cross < 0.7: #交叉概率为0.7
            temp=population_chromosome_new[i][0:2]  #以第2位后为交叉点
            population_chromosome_new[i]=population_chromosome_new[i+1][0:2]+population_chromosome_new[i][2:] #交叉
            population_chromosome_new[i+1]=temp+population_chromosome_new[i+1][2:] #交叉
    return  population_chromosome_new #返回经过交叉后的种群染色体列表

#变异
def mutation(population_chromosome_new): #传入经过杂交的种群染色体列表
    for i in range(len(population_chromosome_new)): #对其中每一个个体
        is_mutation = random.random() #随机生成一个0到1实数
        if is_mutation < 0.1: #变异概率0.005
            rand = random.randint(0, 4) #随机选择一个位置进行变异
            if population_chromosome_new[i][rand] == '0':
                population_chromosome_new[i] = population_chromosome_new[i][0:rand] + '1' + population_chromosome_new[i][rand + 1:]
            else:
                population_chromosome_new[i] = population_chromosome_new[i][0:rand] + '0' + population_chromosome_new[i][rand + 1:]
    return population_chromosome_new

if __name__ == '__main__':  #main
    # 初始化原始种群, 一百个个体
    num = 100
    ori_popular = initialize(num)
    # 得到原始种群的染色体
    ori_popular_gene = encode(ori_popular)  # 染色体
    new_popular_gene = ori_popular_gene
    y = []
    for i in range(100):  # 迭代次数
        new_popular_gene = select(new_popular_gene)  # 选择
        new_popular_gene = crossover(new_popular_gene)  # 交叉
        new_popular_gene = mutation(new_popular_gene)  # 变异
        # 取当代所有个体适应度平均值
        new_fitness = fitness_func(new_popular_gene)
        print(max(new_fitness))
        sum_new_fitness = 0
        for j in new_fitness:
            sum_new_fitness += j
        y.append(sum_new_fitness / len(new_fitness))

    # 画图
    x = np.linspace(0, 100, 100)
    fig = plt.figure()  # 相当于一个画板
    axis = fig.add_subplot(111)  # 坐标轴
    axis.plot(x, y)
    plt.show()
