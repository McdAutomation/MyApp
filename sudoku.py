import numpy as np
T = int(input())
arr = []
N = 9
def recur_solution(arr,in_row,in_col,in_sq,num):
    if num==81:
        return arr
    for r in range(3):
        for s in range(3):
            for i in range(0,3):
                for j in range(0,3):
                    if arr[3*r+i][3*s+j] == 0 and (not in_row[i][arr[i][j]]) and (not in_col[i][arr[i][j]]) and (not in_sq[(r+1)*(s+1)][arr[i][j]]):
                        in_row[i][arr[i][j]] = True # true if this row contains element arr[i][j]
                        in_col[j][arr[i][j]] = True
                        in_sq[(r+1)*(s+1)-1][arr[i][j]] = True
                        num += 1
                        return recur_solution(arr,in_row,in_col,in_sq,num)

                    in_row[i][arr[i][j]] = False # backtrack
                    in_col[j][arr[i][j]] = False
                    in_sq[(r+1)*(s+1)-1][arr[i][j]] = False
                    num -= 1

    return False

def recur_solution_2(arr,in_row,in_col,in_sq,R):
    if R > 2:
        return True
    for r in range(R,3):
        for s in range(3):
            for i in range(0,3):
                for j in range(0,3):
                    if arr[3*r+i][3*s+j] == 0 and (not in_row[i][arr[i][j]]) and (not in_col[i][arr[i][j]]) and (not in_sq[(r+1)*(s+1)][arr[i][j]]):
                        in_row[i][arr[i][j]] = True # true if this row contains element arr[i][j]
                        in_col[j][arr[i][j]] = True
                        in_sq[(r+1)*(s+1)-1][arr[i][j]] = True
                        num += 1
                    if recur_solution_2(arr,in_row,in_col,in_sq,R+1):
                        return True

                    in_row[i][arr[i][j]] = False # backtrack
                    in_col[j][arr[i][j]] = False
                    in_sq[(r+1)*(s+1)-1][arr[i][j]] = False
                    num -= 1

    return False

def recur_solution_onlyij(arr,col):
    if col>8:
        return True
    for i in range(N):
        if arr[i][col] == 0 and (not in_row[i][arr[i][col]]) and (not in_col[i][arr[i][col]]) and (not in_sq[(i//3 +1)*(col//3 +1)][arr[i][col]]):
            in_row[i][arr[i][col]] = True # true if this row contains element arr[i][j]
            in_col[col][arr[i][col]] = True
            in_sq[(i//3 +1)*(col//3 +1)][arr[i][col]] = True
            if recur_solution_onlyij(arr,col+1):
                return True

            in_row[i][arr[i][col]] = False # backtrack
            in_col[col][arr[i][col]] = False
            in_sq[(i//3 +1)*(col//3 +1)][arr[i][col]] = False

        return False

for t in range(T):
    for i in range(N):
        arr.append(list(map(int,input().split())))

    in_row = np.zeros(shape=(N,10))
    in_col = np.zeros(shape=(N,10))
    in_sq = np.zeros(shape=(N+1,10)) # grids from 1-9 and values from 1-9, both ignoring 0 value
    num=0

    for i in range(N):
        for j in range(N):
            if arr[i][j] != 0:
                in_row[i][arr[i][j]] = True # true if this row contains element arr[i][j]
                in_col[j][arr[i][j]] = True
                index=(i//3 +1)*(j//3 +1)
                in_sq[index][arr[i][j]] = True

    if(recur_solution_onlyij(arr,0)):
        print('\n\n')
        print(arr)
    print('\n\n')
    for row in arr:
        print(row)



'''
    for r in range(3):
        for s in range(3):
            for i in range(0,3):
                for j in range(0,3):

                    if arr[3*r+i][3*s+j] != 0:
                        in_sq[(r+1)*(s+1)-1][arr[i][j]] = True

'''
