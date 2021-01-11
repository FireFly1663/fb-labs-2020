import random, sys, math


def Random_values(size):
    values=2**(size-1)
    for i in range(1,size-1,1):
        b=random.randint(0,1)
        values+=((2**i)*b)
    values=values+1
    return values


def Generate(size):
    arays_random=[]
    for i in range(0,2,1):
        ran=Random_values(size)
        while Test(ran)==False:
            ran=Random_values(size)
        arays_random.append(ran)
    return arays_random


def gcd(a, b):
  if b == 0: return a
  else: return gcd(b, a % b)

def evkl(a, b):
    if a == 0: return (b, 0, 1)
    else: 
        g, x, y = evkl(b % a, a)
        return (g, y - (b // a) * x, x)
 
def Reverse(b, n):
    g, x, y = evkl(b, n)
    if g == 1:
        return x % n


def Miller_Rabin(n):
    r=int(math.log(n,2))
    if n == 2:
        return(True)
    elif n == 3:
        return(True)
    elif n % 2 == 0:
        return(False)
    else:
        power=0
        t=n-1
        while t%2==0:
            t=t//2
            power+=1
        for k in range(r):
            a= random.randint(2, n-1)
            x=pow(a, t, n)
            i=0
            if x==1: continue
            elif x==n-1: continue
            while i<power-1:
                x=pow(x,2,n)
                if x==n-1: break
                i=i+1
            else: return(False)
        return(True)

def Test(ran):
    if ran%2==0 or ran%3==0 or ran%5==0 or ran%7==0 or ran%11==0: 
        return False
    if Miller_Rabin(ran)==False: 
        print('Value %s is not prime valuesber.'% hex(ran))
        return False
    return ran


def oiLera(n):
    i=3
    eul=n
    if n%2==0:
        while n%2==0:
            n=n//2
        eul=eul//2
    while (i*i)<=n:
        if n%i==0:
            while n%i==0:
                n=n//i
            eul=eul//i
            eul=eul*(i-1)
        i+=2
    if n>1:
        eul=eul//n
        eul=eul*(n-1)
    return eul

def GenerateKeyPair(pq):
    n=int(pq[0])*int(pq[1])
    e=0
    oiler=(pq[0]-1)*(pq[1]-1)
    while gcd(e,oiler)!=1:
        e=random.randint(2,oiler-1) 
    d=Reverse(e,oiler)
    open_key=[n,e]
    secret_key=[d,pq,n]
    return(open_key,secret_key)

def encrypt(mess, open_key):
    C=pow(mess,open_key[1],open_key[0])
    return C

def Decrypt(C, secret_key):
    M=pow(C,secret_key[0],secret_key[2])
    return M

def Sign(M, key, N):
    S=pow(M,key,N)
    return S

def Verify(S,M,open_key):
    print(open_key)
    if M==pow(S,open_key[1],open_key[0]):
        return True
    else: return False

def SendKey(a_key,B_open, M):
    print('\nАлиса отправляет ключ Бобу.\n\n\tОтправка ключа\n')
    k1=encrypt(M,B_open)
    print('\nСекретний текст розшифровано. K1=%s'% hex(k1))
    S=Sign(M,a_key[1][0],a_key[1][2])
    print('Сообщение подписано Алисой\'s секретний ключ. S=%s'% hex(S))
    S1=encrypt(S,B_open)
    print('Подпись Алисы\'s была введена Бобом\'s открытый ключ. S1=%s'% hex(S1))
    a_message=[k1,S1]
    return a_message

def ReceiveKey(mess,B_secret,a_open):
    print('Боб проверяет подпись Алисы\'s подпись.\n\n\tПолучение ключа\n')
    k=Decrypt(mess[0], B_secret)
    print('Value k is %s'% hex(k))
    S=Decrypt(mess[1],B_secret)
    print('Value S is %s'% hex(S))
    print('S^(e)mod(n)=',hex(pow(S,a_open[1],a_open[0])))
    return Verify(S,k,a_open)

#TaSK
print('\nПривет! Шифрование на языке Питон. Для продолжения нажмите 1')
choose=input()

if int(choose)==1:
    pairs=[]
    for i in range(0,2,1):
        if i==0: 
            print("\nСгенерирована a пара p и q для Алисы:\n")
            pair=Generate(256)
            pairs.append(pair)
            print("\nПара p и q для  Алисы:%s, %s"% (hex(pairs[0][0]),hex(pairs[0][1])))
            
        if i==1: 
            print("\nСгенерирована a пара p и q для Боба:\n")
            pair=Generate(256)
            pairs.append(pair)
            while pairs[0][0]*pairs[0][1]>=pairs[1][0]*pairs[1][1]: 
                pair=Generate(256)
                pairs.pop(1)
                pairs.append(pair)
            print("\nПара p и q для Боба:%s, %s"% (hex(pairs[1][0]),hex(pairs[1][1])))

    a_keys=GenerateKeyPair(pairs[0])
    B_keys=GenerateKeyPair(pairs[1])
    while B_keys[0][0]<a_keys[0][0]:
        a_keys=GenerateKeyPair(pairs[0])

    print('\nСгенерирован открытый ключ (n=%s, e=%s) и секретний ключ (d=%s, pq=%s, %s) для Алисы.'% (hex(a_keys[0][0]),hex(a_keys[0][1]),hex(a_keys[1][0]),hex(a_keys[1][1][0]),hex(a_keys[1][1][1])))
    print('nСгенерирован открытый ключ (n=%s, e=%s) и секретний ключ (d=%s, pq=%s, %s) для Боба.\n'% (hex(B_keys[0][0]),hex(B_keys[0][1]),hex(B_keys[1][0]),hex(B_keys[1][1][0]), hex(B_keys[1][1][0])))

    message=random.randint(0,a_keys[0][0]-1)
    print('Алиса сгенерировала  секретное сообщение  \'%s\'для Боба.'% hex(message))

    a_mess=SendKey(a_keys,B_keys[0],message)
    if ReceiveKey(a_mess,B_keys[1],a_keys[0])==True: print('\nRSA успешно')
    else: print('\nRSA безуспешно')
