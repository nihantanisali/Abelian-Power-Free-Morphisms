#!/usr/bin/env python
# coding: utf-8

# In[6]:


############################################
# Theorem 5.1

import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


f = ['00001', '010101']
n=len(f)

# alphabet is \Sigma={str(0),...,str(n-1)}, and we use str(n) to stand for the empty word.

def parikh(s): #Parikh vector of string s 
    v=[]
    for i in range(n):
        v.append(0)
    p=numpy.array(v)
    for i in range(len(s)):
        p[int(s[i])]=p[int(s[i])]+1
    return(p)

def applyf(w): #apply morphism f to w
    u=''
    for i in range(len(w)):
        u=u+f[int(w[i])]
    return(u)



def splits(): #List a[i] contains tuples [A,p,s] such that f(A) = pis. The empty word is signified by n
    a=[]
    for i in range(n+1):
        a.append([])
    a[n].append([n,'',''])
    for A in range(n):
        w=f[A]
        for i in range(len(w)+1):
            a[n].append([A,w[:i],w[i:]])
        for i in range(len(w)):
            a[int(w[i])].append([A,w[:i],w[i+1:]])
    
    j=[]
    k=[]
    l=[]
    for i in a[0]:
        j.append(    [i[0] , parikh(i[1]) ,parikh(i[2])]   )
    for i in a[1]:
        k.append(    [i[0] , parikh(i[1]) ,parikh(i[2])]   )
    for i in a[2]:
        l.append(    [i[0] , parikh(i[1]) ,parikh(i[2])]   )
    S=[j,k,l]
    
    
    
    return(S)



S1=splits()

#Matrix multiplication ----> Con function


def Con( x,y ):
    """
    Solve  [7]·[z1,z2]ᵀ = [2  -1]·[x,y]ᵀ
           [-1  3 ]         (mod Z)
    Return (z1, z2) if they are both integers, else None.
    """
    num1 =  x - y
    num2 = -1*x + 4*y
    if num1 % 3 == 0 and num2 % 9 == 0:
        return [num1 // 3, num2 // 9]
    return None

        
    
def parents(t):  # Finds the parents of a template t
    par=[]
    for A in S1[t[0]]:
        for B in S1[t[1]]:
          
            for C in S1[t[2]]:
                s1p2 = A[2]+B[1]
                s2p3 = B[2]+C[1]
                v1 = np.array([t[6],t[7]])-s2p3+s1p2
                
                C1= Con(v1[0], v1[1])
                if C1 !=None :
                    for D in S1[t[3]]:
                        s3p4 = C[2]+D[1]
                        v2 =np.array([t[8],t[9]])-s3p4+s2p3
                        C2 = Con(v2[0], v2[1])
                        if C2 != None:
                            for E in S1[t[4]]:
                                s4p5 = D[2]+E[1]
                                v3 = np.array([t[10],t[11]])-s4p5+s3p4
                                C3= Con(v3[0], v3[1])
                                if C3 != None:
                                    for F in S1[t[5]]:
                                        s5p6 = E[2]+F[1]
                                        v4 = np.array([t[12],t[13]])-s5p6+s4p5
                                        C4= Con(v4[0], v4[1])
                                        
                                        if C4 != None:
                                            par.append(( [A[0],B[0],C[0],D[0],E[0],F[0],      C1[0],C1[1],    C2[0],C2[1],   C3[0],C3[1],     C4[0],C4[1]] ))
                                                                                                                                               
    par=set(map(tuple,par))
    par=list(par)
    return par



t=   [n,n,n,n,n,n,      0, 0,   0, 0,    0, 0,    0, 0]# The template for Abelian 8-powers

def ancestors1(T):  # closure of parents
    level = 0  # how many iterations of parents to get the closure
    V = set(map(tuple, T)) # current list of ancestors
    U = list(T)  # new ancestors
    
    while (len(U) > 0):
        newtem =  []
        newtem=set(map(tuple, newtem))
        for u in U:
            newtem=newtem.union(set(map(tuple, parents(u))))    
            
        newtem=newtem.difference(V)
        V = V.union(newtem)
        
        newtem=list(newtem)
        U = newtem

        
        if len(U) > 0: level = level + 1
        print('at level',level,'there are',len(U),'new templates.')
    return [V, level]

def ancestors(T, dtype = np.int8):  # closure of parents
    level = 0  # how many iterations of parents to get the closure
    V = set(map(tuple, T))  # current list of ancestors
    U = list(T)  # new ancestors
    while len(U) > 0:
        newtem = []
        newTemplates = []
        # Parallel processing of U
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            chunksize = max(1, len(U) // multiprocessing.cpu_count())
            results = executor.map(parents, U, chunksize=chunksize)
        for result in results:
            newtem.extend(result)
        newtem=set(map(tuple, newtem))
        newtem=newtem.difference(V)
        V = V.union(newtem)
        newtem=list(newtem)
        U = newtem
        if len(U) > 0: 
            level = level + 1
            print('at level',level,'there are',len(U),'new templates.')
    return [V, level]


def avoids_abelian_k_power(sequence: str, k: int) -> bool:
    n = len(sequence)
    for block_len in range(1, n // k + 1):
        for start in range(n - block_len * k + 1):
            blocks = [sequence[start + j * block_len : start + (j + 1) * block_len] for j in range(k)]
            if all(sorted(blocks[0]) == sorted(b) for b in blocks):
                return False
            
    return True

print('This ')
print('We compute the number of ancestors of T5:')

Q=ancestors([t])
word=applyf(applyf(applyf(applyf('0'))))
word_avoid_5_power= avoids_abelian_k_power(word,5)


print('The total number of ancestors is ',len(Q[0]),', found in',Q[1],'generations.')
print('Hence we can check whether h^4 is abelian 5-power free.')
if word_avoid_5_power:
    print('h^4(a), and hence h^omega(a), is abelian 5 power free')


# In[ ]:




