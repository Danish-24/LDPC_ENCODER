from random import randint
import numpy as np
 
def msg_gen(k):
    msg = []
    for i in range(k):
        msg.append(randint(0,1))
    msg = np.array(msg)
    return msg

def rref(H,n,k):
    H = H.copy()
    rows = n-k
    i = 0
    pivots = []
    for c in range(n):
        pivot = None
        for r in range(i,rows):
            if H[r][c] == 1:
                pivot = r
                break
        if pivot==None:
            continue
        H[[i,pivot]] = H[[pivot,i]]
        for r in range(rows):
            if r!=i and H[r][c] == 1:
                H[r] ^= H[i]
        pivots.append(c)
        i+=1
        if i>=rows:
            break
    return H,pivots

def generator_mat(n,k,H):
    H_rref,pivots = rref(H,n,k)
    G = []
    free_cols = []
    for c in range(n):
        if c not in pivots:
            free_cols.append(c)
    for f in free_cols:
        row = np.zeros(n,dtype=int)
        row[f] = 1
        for i,p_col in enumerate(pivots):
            if H_rref[i][f] == 1:
                row[p_col] = 1
        G.append(row)
    return np.array(G)

def encoder(G,msg):
    return np.mod(msg @ G,2)

def bit_flip(C,n):
    C = C.copy()
    prob = 0.05
    p = int(1/prob)
    for i in range(n):
        r = randint(1,p)
        if r==p:
            C[i] = (C[i]+1)%2
    return C

def decoder(H):
    

k = int(input("len of msg:"))
n = int(input("len of codeword:"))
H = []
for i in range(n-k):
    print(f"give {n} bits input for {i}th row")
    row = input().split()
    row = list(map(int,row))
    H.append(row)
H = np.array(H)
message = msg_gen(k)
G = generator_mat(n,k,H)
Code_wrd = encoder(G,message)
flip_C_wrd = bit_flip(Code_wrd,n)
print(H)
print(message)
print(G)
print(Code_wrd)
print(flip_C_wrd)