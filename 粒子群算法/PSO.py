import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#pso类
class PSO():
    def __init__(self,dim,bound,maxiter,popsize):#构造函数
        self.w=0.6 #惯性权重
        self.c1=2.05 #个体认知函数
        self.c2=2.05 #社会经验函数
        self.popsize=popsize #种群大小
        self.dim=dim #解维数
        self.maxiter=maxiter #最大迭代次数
        self.bound=bound #上下界
        self.x=np.random.uniform(self.bound[0], self.bound[1],(self.popsize, self.dim)) #位置随机初始化
        self.v=np.random.rand(self.popsize, self.dim) #速度随机初始化
        self.pbest=self.x #个体最好位置
        self.gbest=self.x[np.argmin(self.fitness(self.x))] #全局最好位置
        self.pbest_fit=self.fitness(self.x) #个体最好适应值
        self.gbest_fit=np.min(self.fitness(self.x)) #全局最好适应值

    def fitness(self,x): #适应值函数
        return np.sum(np.square(x), axis=1) #x^2的和

    def draw(self,iter):#画图函数
        plt.clf() #清空缓存
        plt.scatter(self.x[:, 0], self.x[:, 1], s=30, color='b') #画出当前种群位置
        plt.xlim(self.bound[0], self.bound[1]) #限制x轴
        plt.ylim(self.bound[0], self.bound[1]) #限制y轴
        plt.title("iteration{}".format(iter)) #标题
        plt.pause(0.05) #停顿0.05秒

    def iteration(self): #迭代
        best_fit=[] #最好适应值列表
        mean_fit=[] #平均适应值列表
        for i in range(self.maxiter): #对每次迭代
            #生成rndreal
            rd1 = np.random.rand(self.popsize, self.dim) #rndreal1 随机01实数
            rd2 = np.random.rand(self.popsize, self.dim) #rndreal2 随机01实数
            #更新速度与位置
            self.v=self.w * self.v + self.c1 * rd1 * (self.pbest - self.x) + self.c2 * rd2 * (self.gbest - self.x) #更行速度，公式ppt上
            self.x=self.x+self.v #更新位置
            #画出当前图像
            self.draw(i+1)
            fit = self.fitness(self.x) #计算当前种群的适应值
            # 个体更新
            index= np.greater(self.pbest_fit, fit) #找出个体需要更新的下标
            self.pbest[index] = self.x[index] #更新位置
            self.pbest_fit[index] = fit[index] #更新适应值
            # 全局更新
            if np.min(fit) < self.gbest_fit: #当前最优优于之前
                self.gbest = self.x[np.argmin(fit)] #更新全局最优位置
                self.gbest_fit = np.min(fit) #更新全局最优适应值
            best_fit.append(self.gbest_fit) #加入列表
            mean_fit.append(np.mean(fit)) #加入列表
        plt.show() #展示
        dataframe = pd.DataFrame({'best_fit': best_fit, 'mean_fit': mean_fit})#保存在df中
        dataframe.to_csv("fit.csv",index=False,  sep=',') #保存在csv中
        return best_fit,mean_fit #返回结果



if __name__ == '__main__':
    pso = PSO(2, [-10, 10], 100, 100) #调用pso函数，初始化
    best_fit,mean_fit=pso.iteration() #进行迭代，返回结果
    iter=np.linspace(1,pso.maxiter,pso.maxiter) #迭代次数
    #画图操作
    plt.clf()
    plt.plot(iter,best_fit,label="best_fit",color='b')
    plt.title("best_fit—iter")
    plt.savefig("best_fit—iter.png")
    plt.clf()
    plt.plot(iter, mean_fit, label="aver_fit", color='b')
    plt.title("mean_fit—iter")
    plt.savefig("mean_fit—iter.png")
