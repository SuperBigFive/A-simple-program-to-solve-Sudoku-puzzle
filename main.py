import copy
from all_rules import *
from utils import *

import numpy as np

import os

N = 9

rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, \
         rule10, rule11, rule12, rule13]

# rules = [rule1, rule2, rule3, rule4, rule5, rule7, rule9]
# rules = [rule1, rule2, rule3, rule5, rule7]

# rules = [rule1, rule2]

def solve(a, msk):
  c = copy.deepcopy(a)
  cnt = np.array([0] * 14)
  while True:
    if set() in c:
      return False, cnt
    chk = False
    for i in range(len(rules)):
      d, nmsk = rules[i](c, msk)
      if not np.array_equal(d, c) or not np.array_equal(nmsk, msk):
        print('> rule', i + 1, 'works!')
        c = d; msk = nmsk
        chk = True
        cnt[i] += 1
        break
    if not chk:
      mn_siz = min(len(c[i, j]) for i in range(N) for j in range(N) if msk[i, j] == 0)
      for i in range(N):
        for j in range(N):
          if msk[i, j] == 0 and len(c[i, j]) == mn_siz:
            mem_cij = copy.deepcopy(c[i, j])
            for x in c[i, j]:
              c[i, j] = set([int(x)])
              nmsk = copy.deepcopy(msk)
              print('> Assume that the number in block [' + str(i + 1) + \
                    ', ' + str(j + 1) + '] is ' + str(x) + '...')
              d, ncnt = solve(c, nmsk)
              for k in range(14):
                cnt[k] += ncnt[k]
              cnt[-1] += 1
              if not isinstance(d, bool):
                return d, cnt
              else:
                print('> The number in block [' + str(i + 1) + ', ' + \
                      str(j + 1) + '] is not ' + str(x) + '!')
            return False, cnt
    elif is_complete(msk): break
  return c, cnt

if __name__ == '__main__':
  a = np.array([[set(list(range(1, 10))) for _ in range(N)] for _ in range(N)])
  msk = np.array([[0] * N for _ in range(N)])
  with open('data.txt', 'r') as f:
    for i in range(N):
      line = list(f.readline().strip().split())
      for j in range(N):
        if line[j] != '0':
          a[i, j] = set([int(line[j])])
  b, cnt = solve(a, msk)
  if isinstance(b, bool):
    print('No solution!')
  else:
    print(cnt)
    for i in range(N):
      for j in range(N):
        print(b[i, j], end = ' ' if j < N - 1 else '\n')
    D = cal_diff_coef(cnt)
    print(u'难度系数: ', D, end = ' ')
    if D >= 1 and D < 1.05:
      print(u'容易难度')
    elif D >= 1.05 and D < 4.5:
      print(u'较容易难度')
    elif D >= 4.5 and D < 6:
      print(u'适中难度')
    elif D >= 6 and D < 13:
      print(u'困难难度') 
    else:
      print(u'非常困难难度')
