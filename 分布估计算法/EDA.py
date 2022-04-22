# coding:gbk
import random

global n, m, C;  # n���������� m��Ʒ���� ,��������C
global bn, time;  # bn���Ÿ������� time ��������
global best;  # ��¼ȫ������
n = 100;
m = 10;
bn = int(n * 0.3);
time = 100;  # ���Ƶ�������
p = [0.0] * m;
ans = [[0] * (m) for i in range(n)]  # ����ģ��p   ans��¼��Ⱥ���
F = [0.0] * n;
best_way = [0] * m;  # F������Ӧֵ  best_way ��¼ȫ�����Žⷽ��
weight = [95, 4, 60, 32, 23, 72, 80, 62, 65, 46];
value = [55, 10, 47, 5, 4, 50, 8, 61, 85, 87]


def cop(a, b, le):  # ���ƺ��� ��b�����ֵ��ֵa����
    for i in range(le):
        a[i] = b[i]


def produce():  # �������
    for i in range(n):
        for k in range(m):
            if (random.random() < p[k]):
                ans[i][k] = 1;
            else:
                ans[i][k] = 0;


def calc(x):  # ���������Ӧֵ
    global C
    vsum = 0;
    wsum = 0;
    for i in range(m):
        vsum += x[i] * value[i];
        wsum += x[i] * weight[i];
    if (C - wsum < 0):
        gg = C - wsum;  # ����������������ᱻ���޷Ŵ�
    else:
        gg = 0;
    return -vsum + 10000 * gg * gg;


def update():  # ���¸���ģ��
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


def init():  # ��ʼ������
    global C, best;
    C = 269;
    best = -1;
    for i in range(m): p[i] = 0.5;  # ��ʼ���ʶ�Ϊ0.5


def slove():  # ��������
    global best
    produce()  # �����¸���
    for i in range(n):  # ������Ӧ��
        F[i] = calc(ans[i])
        if (-F[i] > best):
            best = -F[i];
            cop(best_way, ans[i], m);
    update();  # ���¸���ģ��


init();
isGood = 0;  # ����Ƿ��ҵ����Ž�

for i in range(time):
    slove();
    if (best == 295):
        print('�ҵ����Ž�:295,��������', i + 1);
        isGood = 1;
        break;  # �ﵽ���Ž���ǰ�˳�

if (isGood == 0):   print('ֻ�ҵ����Ž�:', best, '��������', time);
print('����Ϊ��', best_way);