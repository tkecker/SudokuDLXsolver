# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 15:36:12 2016

@author: TomKecker
"""
b = 3
n = b**2
sudoku = [[0,1,0,8,0,3,0,0,0],
          [0,0,9,0,0,7,0,6,0],
          [0,0,7,6,5,0,0,3,0],
          [0,0,0,0,6,0,0,4,9],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,9,1,6,5,0],
          [6,5,0,0,7,0,0,8,0],
          [2,0,8,0,0,5,1,9,0],
          [0,0,0,0,0,0,0,0,0]]

m = [[[4*n**2,1]]]
for i in range(n**2):
    m[0].append([i,i+2,0,0,0,0,i+1,0])
for i in range(n**2):
    m[0].append([i+n**2,i+n**2+2,0,0,0,0,i+n**2+1,0])
for i in range(n**2):
    m[0].append([i+2*n**2,i+2*n**2+2,0,0,0,0,i+2*n**2+1,0])
for i in range(n**2):
    m[0].append([i+3*n**2,(i+3*n**2+2)%(4*n**2+1),0,0,0,0,i+3*n**2+1,0])

r = 0
for i in range(n):
    for j in range(n):
        e = sudoku[i][j]
        if e>0:
            ind = [e-1]
        else:
            ind = range(n)
        for k in ind:
            r+=1
            v = [[3,1,0,0,0,0,1+i*n+j,i*n**2+j*n+k]]
            v.append([0,2,0,0,0,0,1+n**2+i*n+k,i*n**2+j*n+k])
            v.append([1,3,0,0,0,0,1+2*n**2+j*n+k,i*n**2+j*n+k])
            v.append([2,0,0,0,0,0,1+3*n**2+(b*(i//b)+j//b)*n+k,i*n**2+j*n+k])
            for l in range(4):
                idx = v[l][6]
                if m[0][idx][2] == 0:
                    v[l][2] = 0
                    v[l][3] = idx
                else:
                    v[l][2] = m[0][idx][2]            
                    v[l][3] = m[0][idx][3]
                v[l][5] = idx
                if v[l][2] != 0:
                     m[v[l][2]][v[l][3]][4] = r
                     m[v[l][2]][v[l][3]][5] = l
                m[0][idx][2] = r
                m[0][idx][3] = l
                m[0][idx][7] += 1
                if m[0][idx][4] == 0:
                    m[0][idx][4] = r
                    m[0][idx][5] = l
            m.append(v)

def cover_col(c):
    m[0][m[0][c][1]][0] = m[0][c][0]
    m[0][m[0][c][0]][1] = m[0][c][1]
    dr, dc = m[0][c][4], m[0][c][5]
    while dr != 0:
        rdc = m[dr][dc][1]
        while rdc != dc:
            m[m[dr][rdc][4]][m[dr][rdc][5]][2] = m[dr][rdc][2]
            m[m[dr][rdc][4]][m[dr][rdc][5]][3] = m[dr][rdc][3]
            m[m[dr][rdc][2]][m[dr][rdc][3]][4] = m[dr][rdc][4]
            m[m[dr][rdc][2]][m[dr][rdc][3]][5] = m[dr][rdc][5]
            m[0][m[dr][rdc][6]][7] -= 1
            rdc = m[dr][rdc][1]
        dr, dc = m[dr][rdc][4], m[dr][rdc][5]

def uncover_col(c):
    ur, uc = m[0][c][2], m[0][c][3]
    while ur != 0:
        luc = m[ur][uc][0]
        while luc != uc:
            m[0][m[ur][luc][6]][7] += 1
            m[m[ur][luc][4]][m[ur][luc][5]][2] = ur
            m[m[ur][luc][4]][m[ur][luc][5]][3] = luc
            m[m[ur][luc][2]][m[ur][luc][3]][4] = ur
            m[m[ur][luc][2]][m[ur][luc][3]][5] = luc
            luc = m[ur][luc][0]
        ur, uc = m[ur][luc][2], m[ur][luc][3]
    m[0][m[0][c][1]][0] = c
    m[0][m[0][c][0]][1] = c
    
sudokus = []
obs = []

def search():
    if m[0][0][0] == 0:
        s = []
        for i in range(n):
            zero = [0 for j in range(n)]
            s.append(zero)
        for l in range(len(obs)):
            d = obs[l][7]
            no = d%n + 1
            d //= n
            co = d%n
            d //= n
            ro = d
            s[ro][co] = no
        sudokus.append(s)
    else:
        s = n**3
        i = m[0][0][1]
        c = 0
        while i != 0:
            if m[0][i][7] < s:
                c = i
                s = m[0][i][7]
            i = m[0][i][1]
        cover_col(c)
        dr, dc = m[0][c][4], m[0][c][5]
        while dr != 0:
            obs.append(m[dr][dc])
            rdc = m[dr][dc][1]
            while rdc != dc:
                cover_col(m[dr][rdc][6])
                rdc = m[dr][rdc][1]
            search()
            ob = obs.pop()
            uc = ob[6]
            lc = ob[0]
            while m[dr][lc][6] != uc:
                uncover_col(m[dr][lc][6])
                lc = m[dr][lc][0]
            dr, dc = m[dr][rdc][4], m[dr][rdc][5] 
        uncover_col(c)
    
search()
print("Number of solutions: "+str(len(sudokus)))
for k in range(len(sudokus)):
    print("Solution no. "+str(k+1))
    print("*****************")
    for i in range(n):
        l = ""
        for j in range(n):
            l += str(sudokus[k][i][j])+" "
        print(l)
    print("*****************")