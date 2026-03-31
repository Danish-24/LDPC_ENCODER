import numpy as np
import math
import matplotlib.pyplot as plt
 
def rref(H):
    m,n=H.shape
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

def pauli_to_binary(H):
    m=len(H)
    n=len(H[0])
    Hx=np.zeros((m,n),dtype=int)
    Hz=np.zeros((m,n),dtype=int)
    for i in range(m):
        for j in range(n):
            op=H[i][j]
            if op=='X':
                Hx[i][j]=1

            elif op=='Z':
                Hz[i][j]=1
                
            elif op=='Y':
                Hx[i][j]=1
                Hz[i][j]=1
    Hb=np.hstack([Hz,Hx])
    return Hb

def rank(m):
    if m.size==0:
        return 0
    else:
        _,pivots=rref(m)
        return len(pivots)
    
def solve(H,s):
    m,n=H.shape
    H_aug=np.column_stack([H,s.reshape(-1,1)])
    H_aug_rref,pivots=rref(H_aug)
    
    if n in pivots:
        return None
    
    x=np.zeros(n,dtype=int)
    for i in range(len(pivots)):
        x[pivots[i]]=H_aug_rref[i,-1]

    return x

def osd(s,H,belief):
    m,n=H.shape
    e=np.array([1 if val<0 else 0 for val in belief],dtype=int)

    blf_per=np.argsort(np.abs(belief))[::-1] 
    r_blf_per=np.argsort(blf_per)

    H_per=H[:,blf_per]
    e_per=e[blf_per]
    H_rref,pivots= rref(H_per)
    s_res=np.mod(s+np.mod(H_per@e_per,2),2)
    J=[]
    H_j=np.empty((m,0),dtype=int)

    for i in range(n):
        if H_j.shape[1]>0:
            H_j_aug=np.column_stack([H_j,s_res])
            if rank(H_j_aug)==rank(H_j):
                break

        col=H_rref[:,i]
        H_j1=np.column_stack([H_j,col.reshape(-1,1)])
        if rank(H_j1)>rank(H_j):
            J.append(i)
            H_j=H_j1
            s_res=np.mod(s_res+e_per[i]*col,2)
    if len(J)==0:
        x=np.array([])
    else:
        x=solve(H_j,s_res)
        if x is None:
            return e[r_blf_per]
    
    e_f_per=e_per.copy()
    for k in range(len(J)):
        e_f_per[J[k]]=x[k]
    
    e_f=e_f_per[r_blf_per]

    return e_f

    

def bp_decoder(s,H,p,iters):
    m,n=H.shape
    checks_of_vars = [[] for _ in range(n)]
    vars_of_checks = [[] for _ in range(m)]
    for r in range(m):
        for col in range(n):
            if H[r][col]==1:
                checks_of_vars[col].append(r)
                vars_of_checks[r].append(col)
    L0 = math.log((1-p)/p)
    LLR = np.full(n,L0)
    
    v_to_c = {}
    c_to_v = {}
    for i in range(m):
        for j in vars_of_checks[i]:
            v_to_c[(i,j)] = LLR[j]
            c_to_v[(i,j)] = 0.0
    for iter in range(iters):
        for i in range(m):
            for j in vars_of_checks[i]:
                prod = 1
                for k in vars_of_checks[i]:
                    if j!=k:
                        prod *= math.tanh(v_to_c[(i,k)]/2)
                       
                if s[i]==1:
                    prod*=-1
                prod = max(min(prod,0.99999),-0.99999)
                c_to_v[(i,j)] = 2*math.atanh(prod)
        f_llr=np.zeros(n)
        for i in range(n):
            for j in checks_of_vars[i]:
                total = LLR[i]
                for k in checks_of_vars[i]:
                    if j!=k:
                        total+=c_to_v[(k,i)]
                f_llr[i]=total+c_to_v[(j,i)]
                v_to_c[j,i] = total
        e=np.array([1 if val<0 else 0 for val in f_llr])
        if np.array_equal(np.mod(H@e,2),s):
            return e,f_llr
    return e,f_llr

def bp_osd(H,s,p,iters):
    Hb=pauli_to_binary(H)
    e,fbeliefs=bp_decoder(s,Hb,p,iters)
    c_s=np.mod(Hb@e,2)

    if np.array_equal(c_s,s):
        return e
    else:
        e_osd=osd(s,Hb,fbeliefs)
        return e_osd
def binary_to_pauli(b_v):
    n=len(b_v)//2
    s=""
    for i in range(n):
        x=b_v[i]
        z=b_v[i+n]
        if x==1 and z==1:
            s+='Y'
        elif x==1:
            s+='X'
        elif z==1:
            s+='Z'
        else:
            s+='I'
    return s


# def main():
#     m=int(input("Enter the no of stabilizers : "))
#     n=int(input("Enter the no of qubits : "))
#     print("Enter the Pauli operators(stabilizers)")
#     H_pauli=[]
#     for i in range(m):
#         row=input(f"{i+1}th stabilizer :").strip().replace('"','').upper()
#         H_pauli.append(row)
#     s_i=input("Enter the syndrome :").strip().replace('"','')
#     s=np.array([int(b) for b in s_i])
#     p=0.05
#     max_iter=50
#     e_dec=bp_osd(H_pauli,s,p,max_iter)
#     print(binary_to_pauli(e_dec))
def main_hlp(Hb,p,iters,is_osd=True):
    m,n=Hb.shape

    e=np.zeros(n,dtype=int)
    for i in range(n//2):
        r=np.random.rand()
        if r <p/3:
            e[i]=1
        elif r<2*p/3:
            e[i+n//2]=1
        elif r<p:
            e[i]=1
            e[i+n//2]=1

    s=np.mod(Hb@e,2)
    if np.all(s==0):
        return 1
    e_bp,f_llr=bp_decoder(s,Hb,p,iters)
    if np.array_equal(np.mod(Hb@e_bp,2),s):
        return 1
    if is_osd:
        e_osd=osd(s,Hb,f_llr)
        if np.array_equal(np.mod(Hb@e_osd,2),s):
            return 1

    return 0
def main(Hb,n_qubits):
    trials=200
    for iter in range(10,101,20):
        p_vals = []
        bp_wer = []
        bp_osd_wer=[]
        p = 0.02
        while p<0.5:
            p_vals.append(p)
            succ_bp=0
            succ_bp_osd=0
            for i in range(trials):
                succ_bp+=main_hlp(Hb,p,iter,is_osd=False)
                succ_bp_osd+=main_hlp(Hb,p,iter,is_osd=True)
            bp_wer.append(1-(succ_bp/trials))
            bp_osd_wer.append(1-(succ_bp_osd/trials))
            p+=0.02
    plt.plot(p_vals,bp_wer,'--',label=f"Pure BP ")
    plt.plot(p_vals,bp_osd_wer,'-',label=f"BP-OSD-0")

    # plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Physical error rate")
    plt.ylabel("WER")
    plt.title("BP-OSD vs BP")
    plt.grid(True)
    plt.legend()
    plt.show()
if __name__ == "__main__":
    m=int(input("Enter the no of stabilizers : "))
    n=int(input("Enter the no of qubits : "))
    print("Enter the Pauli operators(stabilizers)")
    H_pauli=[]
    for i in range(m):
        row=input(f"{i+1}th stabilizer :").strip().replace('"','').upper()
        H_pauli.append(row)
    Hb=pauli_to_binary(H_pauli)

    s_i=input("Enter the syndrome :").strip().replace('"','')
    s=np.array([int(b) for b in s_i])
    main(Hb,n)


   
    





