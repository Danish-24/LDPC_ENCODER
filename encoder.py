from random import randint
import numpy as np
 
def msg_gen(k):
    msg = []
    for i in range(k):
        msg.append(randint(0,1))
    msg = np.array(msg)
    return msg

def generator_mat(n,k,H):
    return np.array([
[1,0,0,1,0,1],
[0,1,0,1,1,0],
[0,0,1,0,1,1]
])

def encoder(G,msg):
    return np.mod(msg @ G,2)

def bit_flip(C,n):
    prob = 0.1
    p = int(1/prob)
    for i in range(n):
        r = randint(1,p)
        if r==p:
            C[i] = (C[i]+1)%2
    return C

def decoder(H):
    pass
k = int(input("len of msg:"))
n = int(input("len of codeword:"))
H = []
for i in range(n-k):
    print(f"give {n} bits input for {i}th row")
    row = input().split()
    row = list(map(int,row))
    H.append(row)
H = np.array(H)
print(H)
message = msg_gen(k)
print(message)
G = generator_mat(n,k,H)
print(G)
Code_wrd = encoder(G,message)
print(Code_wrd)
flip_C_wrd = bit_flip(Code_wrd,n)
print(flip_C_wrd)