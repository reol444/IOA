import math
import random
import matplotlib.pyplot as plt

from typing import List

#问题模型类
class ProblemModel:

    def __init__(self, bounds=None):#构造函数
        self.bounds = bounds #上下界初始化

    def getIndependentVar(self): #初始化个体
        if self.bounds is not None: #若上下界已初始化
            independentVar = [] #利用列表存储结果
            for bound in self.bounds: #对每一维的上下界
                independentVar.append(bound[0] + random.random() * (bound[1] - bound[0])) #利用上下界对个体随机初始化
            return independentVar #返回初始化的个体值
        else: #否则
            pass #跳过

    def getNewVar(self, var_1, var_2): #更新蜜源
        if self.bounds is not None: #若上下界已经初始化
            newVar = [] #利用列表存结果
            step_random = random.random() #获取随机0到1的实数
            for v_1, v_2 in zip(var_1, var_2): #对每一个xi和xk
                newVar.append(v_1 + step_random * (v_2 - v_1)) #更新xi，公式在ppt中
            return newVar #返回结果
        else: #否则
            pass #跳过

    def getValue(self, variable): #目标函数
        if len(variable) == 2: #判断维数
            x = variable[0] #得到x1
            y = variable[1] #得到x2
            return 1 + (x ** 2 + y ** 2) / 4000 - (math.cos(x) * math.cos(y / math.sqrt(2))) #返回函数值
            # return -(x**2-10*math.cos(2*math.pi*x)+10)+(y**2-10*math.cos(2*math.pi*y)+10)
            # return -20*math.exp(-0.2*math.sqrt((x**2+y**2)/2))-math.exp((math.cos(2*math.pi*x)+math.cos(2*math.pi*y))/2)+20+math.e
        else: #否则
            return 1 #返回1

#蜜源类
class NectarSource:
    problem_src = None  # 问题模型

    def __init__(self, position): #构造函数
        self.position = position #蜜源位置
        self.value = self.problem_src.getValue(position) #蜜源的目标函数值
        #计算适应值
        if self.value >= 0:  #若目标函数大于0
            self.fitness = 1 / (1 + self.value) #ppt公式
        else: #否则
            self.fitness = 1 + math.fabs(self.value) #ppt公式
        # this definition of fitness means looking for the minimum
        self.trail = 0 #更新失败次数

#abc算法主体类
class ABCAlgor:
    LIMIT = 10  # 蜜源更新次数限制

    def __init__(self, problem, employedNum, onlookerNum, maxIteration): #构造函数
        NectarSource.problem_src = problem #问题模型
        self.problem = problem  # type:ProblemModel #问题模型
        self.employedNum = employedNum#雇佣蜂个数
        self.onlookerNum = onlookerNum #观察蜂个数
        self.maxIteration = maxIteration #侦查蜂个数
        self.nectarSrc = []  # type:List[NectarSource] #蜜源列表
        self.bestNectar = NectarSource(self.problem.getIndependentVar()) #最好蜜源，随意赋初值
        self.resultRecord = [] #结果记录
        for i in range(self.employedNum): #对每一个雇佣蜂
            self.nectarSrc.append(NectarSource(self.problem.getIndependentVar())) #随机初始化

    def updateNectarSrc(self, index): #更新蜜源
        src = self.nectarSrc[index] #得到蜜源
        src_another = random.choice(self.nectarSrc)  # type:NectarSource #随机选择另外一个蜜源
        while src_another is src: #若蜜源相等
            src_another = random.choice(self.nectarSrc) #重新选择
        src_new = NectarSource(self.problem.getNewVar(src.position, src_another.position)) #调用更新蜜源函数得到新蜜源
        if src_new.fitness > src.fitness: #锦标赛选择
            self.nectarSrc[index] = src_new #大于则更新
        else:#否则
            self.nectarSrc[index].trail += 1 #增加次数

    def employedProcedure(self): #雇佣蜂
        length = len(self.nectarSrc)  # 蜜源大小，雇佣蜂
        for i in range(length): #对每个雇佣蜂
            self.updateNectarSrc(i) #更新蜜源

    def onlookerProcedure(self): #观察蜂
        sum_fitness = 0 #适应值和
        for src in self.nectarSrc: #对每一个蜜源
            sum_fitness += src.fitness #累加适应值
        probability_fit=[] #适应值概率列表
        #轮盘赌
        fit=0 #适应值概率轮盘
        for i in range(len(self.nectarSrc)): #对每一个蜜源
            fit += self.nectarSrc[i].fitness / sum_fitness #累加
            probability_fit.append(fit)#加入列表
        for i in range(self.onlookerNum): #对每一个观察蜂
            rand=random.random() #生成0到1的随机实数
            if rand<=probability_fit[0]: #若小于第一个
                self.updateNectarSrc(0) #则选择第一个蜜源
            for j in range(1,len(probability_fit)): #从第二个开始
                if probability_fit[j - 1] < rand <= probability_fit[j]: #判断轮盘选择的位置
                    self.updateNectarSrc(j) #更新选择的蜜源

    def updateBestNectar(self): #更新最好的蜜源
        # use the fitness to select the best, if the problem is finding the max, change the definition of fitness
        for src in self.nectarSrc:#对每个蜜源
            if src.fitness > self.bestNectar.fitness: #与最好蜜源比较
                self.bestNectar = src #若大于则更新

    def scoutProcedure(self): #侦查蜂
        length = len(self.nectarSrc) #获取蜜源个数
        for i in range(length): #对每个蜜源
            if self.nectarSrc[i].trail >= self.LIMIT: #判断其未更新次数是否超过限制
                self.nectarSrc[i] = NectarSource(self.problem.getIndependentVar()) #是的话对此蜜源重新初始化

    def solve(self): #问题解决
        for i in range(self.maxIteration): #每次迭代
            self.employedProcedure() #雇佣蜂阶段
            self.onlookerProcedure() #观察蜂阶段
            self.updateBestNectar() #更新最好蜜源
            self.scoutProcedure() #侦查蜂
            self.updateBestNectar() #更新最好蜜源
            self.resultRecord.append(self.bestNectar.value) #记录当前最好蜜源

    def showResult(self): #展示结果
        for result in self.resultRecord: #对每一个结果
            print(result) #打印
        print('best solution:', self.bestNectar.position) #最好位置
        print('best value:', self.bestNectar.value) #最好值
        plt.plot(self.resultRecord) #画图
        plt.title('result curve') #标题
        plt.tight_layout() #自动调整
        plt.show() #展示


if __name__ == '__main__':
    beesNum = 100 #蜜蜂总数
    employedNum = int(beesNum / 2) #雇佣蜂数量
    onlookerNum = int(beesNum / 2) #观察蜂数量
    maxIteration = 200 #最大迭代次数
    problem = ProblemModel(bounds=[[-10, 10], [-10, 10]]) #上下界
    abcSolution = ABCAlgor(problem, employedNum, onlookerNum, maxIteration) #生成ABC
    abcSolution.solve() #解决问题
    abcSolution.showResult() #展示结果