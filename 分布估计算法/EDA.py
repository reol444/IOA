# coding:gbk
import random

global n, m, C;  # n个体数量， m物品数量 ,背包容量C
global bn, time;  # bn较优个体数量 time 迭代次数
global best;  # 记录全局最优
n = 100;
m = 10;
bn = int(n * 0.3);
time = 100;  # 控制迭代次数
p = [0.0] * m;
ans = [[0] * (m) for i in range(n)]  # 概率模型p   ans记录种群情况
F = [0.0] * n;
best_way = [0] * m;  # F个体适应值  best_way 记录全局最优解方案
weight = [95, 4, 60, 32, 23, 72, 80, 62, 65, 46];
value = [55, 10, 47, 5, 4, 50, 8, 61, 85, 87]


def cop(a, b, le):  # 复制函数 把b数组的值赋值a数组
    for i in range(le):
        a[i] = b[i]


def produce():  # 个体产生
    for i in range(n):
        for k in range(m):
            if (random.random() < p[k]):
                ans[i][k] = 1;
            else:
                ans[i][k] = 0;


def calc(x):  # 计算个体适应值
    global C
    vsum = 0;
    wsum = 0;
    for i in range(m):
        vsum += x[i] * value[i];
        wsum += x[i] * weight[i];
    if (C - wsum < 0):
        gg = C - wsum;  # 罚函数，若超重则会被无限放大
    else:
        gg = 0;
    return -vsum + 10000 * gg * gg;


def update():  # 更新概率模型
    mx = -1;
    ob = 0;
    for i in range(m): p[i] = 0;
    for i in range(bn):
        mx = -1;
        for k in range(n):
            if (-F[k] > mx): mx = -F[k]; ob = i;
        F[ob] = 10000;
        for j in range(m):
            if (ans[ob][j] == 1): p[j] += 1.0;
    for i in range(m):
        p[i] = p[i] / bn;


def init():  # 初始化函数
    global C, best;
    C = 269;
    best = -1;
    for i in range(m): p[i] = 0.5;  # 初始概率都为0.5


def slove():  # 迭代函数
    global best
    produce()  # 产生新个体
    for i in range(n):  # 计算适应度
        F[i] = calc(ans[i])
        if (-F[i] > best):
            best = -F[i];
            cop(best_way, ans[i], m);
    update();  # 更新概率模型


init();
isGood = 0;  # 标记是否找到最优解

for i in range(time):
    slove();
    if (best == 295):
        print('找到最优解:295,迭代次数', i + 1);
        isGood = 1;
        break;  # 达到最优解提前退出

if (isGood == 0):   print('只找到次优解:', best, '迭代次数', time);
print('方案为：', best_way);