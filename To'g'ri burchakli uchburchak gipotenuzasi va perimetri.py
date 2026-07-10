import math
a,b=map(int,input().split());
c=math.sqrt(a*a+b*b);
P=a+b+c;
print(f"{c:.2f}",f"{P:.2f}")