def f(x,y):
    return x**2-4*x + y**2-y-x*y
while True:
    x, y = eval(input("x,y="))
    print(f(x, y))