class Sudoku:
    
    def __init__(self,sudoku):
        self.sudoku = sudoku
        self.n = len(self.sudoku)
        self.b = int(self.n**(1/2))
        self.setupDLX()
        self.obs = []
        self.sudokus = []
        
    def setupDLX(self):
        self.m = [[[4*self.n**2,1]]]
        for i in range(self.n**2):
            self.m[0].append([i,i+2,0,0,0,0,i+1,0])
        for i in range(self.n**2):
            self.m[0].append([i+self.n**2,i+self.n**2+2,0,0,0,0,i+self.n**2+1,0])
        for i in range(self.n**2):
            self.m[0].append([i+2*self.n**2,i+2*self.n**2+2,0,0,0,0,i+2*self.n**2+1,0])
        for i in range(self.n**2):
            self.m[0].append([i+3*self.n**2,(i+3*self.n**2+2)%(4*self.n**2+1),0,0,0,0,i+3*self.n**2+1,0])

        r = 0
        for i in range(self.n):
            for j in range(self.n):
                e = self.sudoku[i][j]
                if e>0:
                    ind = [e-1]
                else:
                    ind = range(self.n)
                for k in ind:
                    r+=1
                    v = [[3,1,0,0,0,0,1+i*self.n+j,i*self.n**2+j*self.n+k]]
                    v.append([0,2,0,0,0,0,1+self.n**2+i*self.n+k,i*self.n**2+j*self.n+k])
                    v.append([1,3,0,0,0,0,1+2*self.n**2+j*self.n+k,i*self.n**2+j*self.n+k])
                    v.append([2,0,0,0,0,0,1+3*self.n**2+(self.b*(i//self.b)+j//self.b)*self.n+k,i*self.n**2+j*self.n+k])
                    for l in range(4):
                        idx = v[l][6]
                        if self.m[0][idx][2] == 0:
                            v[l][2] = 0
                            v[l][3] = idx
                        else:
                            v[l][2] = self.m[0][idx][2]            
                            v[l][3] = self.m[0][idx][3]
                        v[l][5] = idx
                        if v[l][2] != 0:
                            self.m[v[l][2]][v[l][3]][4] = r
                            self.m[v[l][2]][v[l][3]][5] = l
                        self.m[0][idx][2] = r
                        self.m[0][idx][3] = l
                        self.m[0][idx][7] += 1
                        if self.m[0][idx][4] == 0:
                            self.m[0][idx][4] = r
                            self.m[0][idx][5] = l
                    self.m.append(v)

    def cover_col(self,c):
        self.m[0][self.m[0][c][1]][0] = self.m[0][c][0]
        self.m[0][self.m[0][c][0]][1] = self.m[0][c][1]
        dr, dc = self.m[0][c][4], self.m[0][c][5]
        while dr != 0:
            rdc = self.m[dr][dc][1]
            while rdc != dc:
                self.m[self.m[dr][rdc][4]][self.m[dr][rdc][5]][2] = self.m[dr][rdc][2]
                self.m[self.m[dr][rdc][4]][self.m[dr][rdc][5]][3] = self.m[dr][rdc][3]
                self.m[self.m[dr][rdc][2]][self.m[dr][rdc][3]][4] = self.m[dr][rdc][4]
                self.m[self.m[dr][rdc][2]][self.m[dr][rdc][3]][5] = self.m[dr][rdc][5]
                self.m[0][self.m[dr][rdc][6]][7] -= 1
                rdc = self.m[dr][rdc][1]
            dr, dc = self.m[dr][rdc][4], self.m[dr][rdc][5]
        
    def uncover_col(self,c):
        ur, uc = self.m[0][c][2], self.m[0][c][3]
        while ur != 0:
            luc = self.m[ur][uc][0]
            while luc != uc:
                self.m[0][self.m[ur][luc][6]][7] += 1
                self.m[self.m[ur][luc][4]][self.m[ur][luc][5]][2] = ur
                self.m[self.m[ur][luc][4]][self.m[ur][luc][5]][3] = luc
                self.m[self.m[ur][luc][2]][self.m[ur][luc][3]][4] = ur
                self.m[self.m[ur][luc][2]][self.m[ur][luc][3]][5] = luc
                luc = self.m[ur][luc][0]
            ur, uc = self.m[ur][luc][2], self.m[ur][luc][3]
        self.m[0][self.m[0][c][1]][0] = c
        self.m[0][self.m[0][c][0]][1] = c
    
    def search(self):
        if self.m[0][0][0] == 0:
            s = []
            for i in range(self.n):
                zero = [0 for j in range(self.n)]
                s.append(zero)
            for l in range(len(self.obs)):
                d = self.obs[l][7]
                no = d%self.n + 1
                d //= self.n
                co = d%self.n
                d //= self.n
                ro = d
                s[ro][co] = no
            self.sudokus.append(s)
        else:
            s = self.n**3
            i = self.m[0][0][1]
            c = 0
            while i != 0:
                if self.m[0][i][7] < s:
                    c = i
                    s = self.m[0][i][7]
                i = self.m[0][i][1]
            self.cover_col(c)
            dr, dc = self.m[0][c][4], self.m[0][c][5]
            while dr != 0:
                self.obs.append(self.m[dr][dc])
                rdc = self.m[dr][dc][1]
                while rdc != dc:
                    self.cover_col(self.m[dr][rdc][6])
                    rdc = self.m[dr][rdc][1]
                self.search()
                ob = self.obs.pop()
                uc = ob[6]
                lc = ob[0]
                while self.m[dr][lc][6] != uc:
                    self.uncover_col(self.m[dr][lc][6])
                    lc = self.m[dr][lc][0]
                dr, dc = self.m[dr][rdc][4], self.m[dr][rdc][5] 
            self.uncover_col(c)
        
    def solve(self):
        self.search()
        return self.sudokus