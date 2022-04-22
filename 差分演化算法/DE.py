#差分演化算法
import numpy as np
import random

#差分演化算法类，包括参数和方法
class DE: #类名
    def __init__(self, min_range, max_range, dim, factor, rounds, size, object_func, CR=0.75): #构造函数
        self.min_range = min_range #个体向量中元素的下界
        self.max_range = max_range #个体向量中元素的上界
        self.dimension = dim #个体向量的维数
        self.factor = factor #缩放因子
        self.rounds = rounds #演化代数
        self.size = size #种群大小
        self.cur_round = 1 #初始代数
        self.CR = CR #杂交概率
        self.get_object_function_value = object_func #目标函数
        # 初始化种群
        self.individuality = [np.array([random.uniform(self.min_range, self.max_range) for s in range(self.dimension)])
                              for tmp in range(size)] #随机产生在上下界范围内的实数，以初始化种群向量
        self.object_function_values = [self.get_object_function_value(v) for v in self.individuality] #计算各向量的目标函数值
        self.mutant = None #存储差分变异得到的Vi(变异向量)

    #差分变异的函数实现
    def mutate(self): #函数名
        self.mutant = [] #初始化mutant列表
        #此处使用“DE/rand/1”经典差分变异算子
        for i in range(self.size): #进行种群大小次循环
            r0, r1, r2 = 0, 0, 0 #初始化r0，r1，r2
            while r0 == r1 or r1 == r2 or r0 == r2 or r0 == i: #随机选取三个向量的下标，并保证r0!=r1!=r2!=i
                r0 = random.randint(0, self.size - 1) #随机选取
                r1 = random.randint(0, self.size - 1) #同上
                r2 = random.randint(0, self.size - 1) #同上
            tmp = self.individuality[r0] + (self.individuality[r1] - self.individuality[r2]) * self.factor #计算向量Vi(变异向量)
            for t in range(self.dimension): #循环，对Vi(变异向量)每一维进行判断
                if tmp[t] > self.max_range or tmp[t] < self.min_range: #保证每一维都在范围内
                    tmp[t] = random.uniform(self.min_range, self.max_range) #否则随机赋值
            self.mutant.append(tmp) #将Vi(变异向量)加入到mutant列表中
    #杂交与选择的函数实现
    def crossover_and_select(self): #函数名
        for i in range(self.size): #循环种群大小次
            Jrand = random.randint(0, self.dimension) #生成0到维数范围内的随机数，即生成jrand
            for j in range(self.dimension): #对每一维
                if random.random() > self.CR and j != Jrand: #生成0到1之间的随机数rndint，若rndint大于杂交概率并且jrand不等于j，此处与ppt的条件相反
                    self.mutant[i][j] = self.individuality[i][j] #将xij(目标向量)赋值给uij
                #进行选择
                tmp = self.get_object_function_value(self.mutant[i]) #计算uij(实验向量)的目标函数值
                if tmp <= self.object_function_values[i]: #若ui(实验向量)的目标函数值小于等于xi的函数值
                    self.individuality[i] = self.mutant[i] #将ui赋值给xi
                    self.object_function_values[i] = tmp #同时改变其函数值
    #输出最优的个体
    def print_best(self): #函数名
        m = min(self.object_function_values) #找到最小的函数值
        i = self.object_function_values.index(m) #找到其下标
        print("轮数：" + str(self.cur_round)) #输出演化代数
        print("最佳个体：" + str(self.individuality[i])) #输出最佳个体
        print("目标函数值：" + str(m)) #输出最佳的目标函数值

    #演化控制函数
    def evolution(self): #函数名
        while self.cur_round < self.rounds: #当小于演化代数时
            self.mutate() #变异
            self.crossover_and_select() #杂交与选择
            self.print_best() #输出当前最佳
            self.cur_round = self.cur_round + 1 #代数加一


# 测试部分
if __name__ == "__main__": #main函数
    def f(v): #目标函数
        return -(v[1] + 47) * np.sin(np.sqrt(np.abs(v[1] + (v[0] / 2) + 47))) - v[0] * np.sin(np.sqrt(np.abs(v[0] - v[1] - 47))) #返回目标函数值
    p = DE(min_range=-513, max_range=513, dim=2, factor=0.8, rounds=100, size=100, object_func=f) #DE类的初始化
    p.evolution() #开始进行演化
