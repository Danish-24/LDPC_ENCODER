from random import randint
import numpy as np
 
def msg_gen(k):
    msg = []
    for i in range(k):
        msg.append(randint(0,1))
def generator_mat(n,k,H):
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