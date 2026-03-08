from random import randint
import numpy as np
import math
import matplotlib.pyplot as plt
 
def msg_gen(k):
    msg = []
    for i in range(k):
        msg.append(randint(0,1))
    msg = np.array(msg)
    return msg

def rref(H,n,m):
    H = H.copy()
    rows = m
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
    H_rref,pivots = rref(H,n,n-k)
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
    return np.array(G),free_cols

def encoder(G,msg):
    return np.mod(msg @ G,2)

def bit_flip(C,n,prob):
    C = C.copy()
    p = int(1/prob)
    for i in range(n):
        r = randint(1,p)
        if r==p:
            C[i] = (C[i]+1)%2
    return C

def decoder(c,H,p,iterations,m,n):
    checks_of_vars = [[] for _ in range(n)]
    vars_of_checks = [[] for _ in range(m)]
    for r in range(m):
        for col in range(n):
            if H[r][col]==1:
                checks_of_vars[col].append(r)
                vars_of_checks[r].append(col)
    L0 = math.log((1-p)/p)
    LLR = np.zeros(n)
    for i in range(n):
        if c[i] == 1:
            LLR[i] = -L0
        else:
            LLR[i] = L0
    v_to_c = {}
    c_to_v = {}
    for i in range(m):
        for j in vars_of_checks[i]:
            v_to_c[(i,j)] = LLR[j]
            c_to_v[(i,j)] = 0.0
    for iter in range(iterations):
        for i in range(m):
            for j in vars_of_checks[i]:
                m_val = float("inf")
                sign = 1
                for k in vars_of_checks[i]:
                    if j!=k:
                        val = v_to_c[(i,k)]
                        m_val = min(m_val,abs(val))
                        sign *= np.sign(val)
                c_to_v[(i,j)] = sign*m_val
        decoded = np.zeros(n,dtype=int)
        for i in range(n):
            curr = LLR[i]
            for j in checks_of_vars[i]:
                total = LLR[i]
                for k in checks_of_vars[i]:
                    if j!=k:
                        total+=c_to_v[k,i]
                v_to_c[j,i] = total
                curr+=c_to_v[(j,i)]
            if curr<0:
                decoded[i] = 1
            else:
                decoded[i] = 0
        if np.all(np.mod(H@decoded.T,2)==0):
            return decoded
    print("max iterations reached")
    return decoded

def new_decoder(c,H,p,iterations,m,n):
    checks_of_vars = [[] for _ in range(n)]
    vars_of_checks = [[] for _ in range(m)]
    for r in range(m):
        for col in range(n):
            if H[r][col]==1:
                checks_of_vars[col].append(r)
                vars_of_checks[r].append(col)
    L0 = math.log((1-p)/p)
    LLR = np.zeros(n)
    for i in range(n):
        if c[i] == 1:
            LLR[i] = -L0
        else:
            LLR[i] = L0
    v_to_c = {}
    c_to_v = {}
    for i in range(m):
        for j in vars_of_checks[i]:
            v_to_c[(i,j)] = LLR[j]
            c_to_v[(i,j)] = 0.0
    for iter in range(iterations):
        for i in range(m):
            for j in vars_of_checks[i]:
                prod = 1
                for k in vars_of_checks[i]:
                    if j!=k:
                        prod *= math.tanh(v_to_c[(i,k)]/2)
                prod = max(min(prod,0.99999),-0.99999)
                c_to_v[(i,j)] = 2*math.atanh(prod)
        decoded = np.zeros(n,dtype=int)
        for i in range(n):
            curr = LLR[i]
            for j in checks_of_vars[i]:
                total = LLR[i]
                for k in checks_of_vars[i]:
                    if j!=k:
                        total+=c_to_v[k,i]
                v_to_c[j,i] = total
                curr+=c_to_v[(j,i)]
            if curr<0:
                decoded[i] = 1
            else:
                decoded[i] = 0
        if np.all(np.mod(H@decoded.T,2)==0):
            return decoded
    print("max iterations reached")
    return decoded

def find_msg(c,cols):
    return c[cols]

def main(prob,k,n,H,iter):
    message = msg_gen(k)
    G,free_cols = generator_mat(n,k,H)
    Code_wrd = encoder(G,message)
    flip_C_wrd = bit_flip(Code_wrd,n,prob)
    decoded = new_decoder(flip_C_wrd,H,prob,iter,n-k,n)
    final_msg = find_msg(decoded,free_cols)
    print(Code_wrd)
    print(flip_C_wrd)
    print(decoded)
    if np.array_equal(message,final_msg):
        return 1
    else:
        return 0
    # print(H)
    # print(message)
    # print(G)
    # print(Code_wrd)
    # print(flip_C_wrd)
    # print(decoded)
    # print(final_msg)


k = int(input("len of msg:"))
n = int(input("len of codeword:"))
H = []
for i in range(n-k):
    print(f"give {n} bits input for {i}th row")
    row = input().split()
    row = list(map(int,row))
    H.append(row)
H = np.array(H)
main(0.3,3,6,H,3)
print(rref(H,n,n-k))