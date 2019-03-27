#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the matrixRotation function below.
def matrixRotation(x, r):
    m = len(x)
    n = len(x[0])
    p = m
    q = n
    iSqr_num = 0
    rx = r
    r = 1

    while p >= 2 and q >= 2:
        full = (p-1)*2 + (q-1)*2
        rot_x = rx % full
        while rot_x > 0:
            #left column
            tbot = x[m-1-iSqr_num][iSqr_num:n-iSqr_num]
            tbot = [x[m-2-iSqr_num][iSqr_num]] + tbot[0:q-1]
            for i in range(1+iSqr_num,m-iSqr_num):
                x[-i][iSqr_num] = x[-i-1][iSqr_num]
            
            #top row
            x[iSqr_num][iSqr_num:n-iSqr_num] = x[iSqr_num][r+iSqr_num:n-iSqr_num] + x[iSqr_num][iSqr_num:r+iSqr_num]

            #right column
            for i in range(p-1):
                x[i+iSqr_num][n-1-iSqr_num] = x[i+1+iSqr_num][(n-1)-iSqr_num]

            #bottom row
            x[m-1-iSqr_num][iSqr_num:n-iSqr_num] = tbot

            rot_x -= 1

        iSqr_num += 1
        p -= 2
        q -= 2

    for i in x:
        print(*i)

if __name__ == '__main__':
    mnr = input().rstrip().split()

    m = int(mnr[0])

    n = int(mnr[1])

    r = int(mnr[2])

    matrix = []

    for _ in range(m):
        matrix.append(list(map(int, input().rstrip().split())))

    matrixRotation(matrix, r)
