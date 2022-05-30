import numpy as np
from FindFactor import FindFactor

def inv_N(i,N):
    # 大衍求一术（辗转相除法）
    r_0,r_1 = N,i
    c_0,c_1 = 1,0
    d_0,d_1 = 0,1
    n = 0;
    while(1):
        n = n + 1;
        q_2 = r_0//r_1
        r_2= r_0%r_1
        if(r_2==0):
            break
        c_2 = q_2*c_1+c_0
        d_2 = q_2*d_1+d_0
        r_0,c_0,d_0 = r_1,c_1,d_1
        r_1,c_1,d_1 = r_2,c_2,d_2
        
    q = (-1)**(n-1)*d_1
    if(q<0): q = q + N 
    return q

def getRSA(p1,p2):
    # 利用质数p1,p2产生RSA 公钥和私钥
    N = p1*p2
    Euler_N = (p1-1)*(p2-1)
    while(1):
        e = np.random.randint(2,Euler_N-1)
        if(np.gcd(e,Euler_N)==1):
            break
    d = inv_N(e,Euler_N)
    return (N,e),(N,d)

def Send(p1,p2):
    # 随机产生密文并发送
    [a,b] = getRSA(3,19)
    N ,e,d = a[0],a[1],b[1]
    M = np.random.randint(2,N-1)
    print("明文是:",M,";密钥是",d)
    S = M**e%N
    return N,e,S

def Decode(N,e,S):
    # 利用公钥和密文获得私钥和明文
    Found = FindFactor(N)
    p1 = Found.find_factors()
    p1 = int(p1[0])
    p2 = int(N/p1)
    d = inv_N(e,(p1-1)*(p2-1))
    print("密钥是",d)
    M2 = S**d%N
    print("明文是",M2)
    return M2

#主函数,N=57
[N,e,S] = Send(3,19) #3*19=57
print("公钥N和e以及密文为：",N,e,S)
M = Decode(N,e,S)

#N=119
#[N,e,S] = Send(7,17) #7*17=119
#print("公钥N和e以及密文为：",N,e,S)
#M = Decode(N,e,S)
