import copy, math

import numpy as np

w = [1, 5, 10, 15, 20, 25, 30, 35, 40, 500, 1000, 3000, 5000, 8000]

N = 9

def is_complete(msk):
  return msk.sum() >= N * N

def cal_diff_coef(cnt):
  score = 0
  for i in range(14):
    score += w[i] * cnt[i]
  return math.sqrt(score / sum(cnt))

def get_block_idx(x, y):
  return (x // 3) * 3 + (y // 3)

def get_block_pos(idx):
  return ((idx // 3) * 3, (idx % 3) * 3)

def clear_cddt_for_row(row, a, mask, nums):
  for j in range(N):
    if mask[j] == 0:
      for x in nums:
        if x in a[row][j] :
          a[row][j].discard(x)
  return a

def clear_cddt_for_col(col, a, mask, nums):
  for i in range(N):
    if mask[i] == 0:
      for x in nums:
        if x in a[i][col]:
          a[i][col].discard(x)
  return a

def clear_cddt_for_block(blo_idx, a, mask, nums):
  px, py = get_block_pos(blo_idx)
  for i in range(px, px + 3):
    for j in range(py, py + 3):
      if mask[i, j] == 0:
        for x in nums:
          if x in a[i, j]:
            a[i, j].discard(x)
  return a

def get_all_combinations(cnt, st = 1, en = 10):
  combinations = []
  for i in range(st, en):
    for j in range(i + 1, en):
      if cnt == 2: 
        if i < j : combinations.append((i, j))
      else:
        for k in range(j + 1, en):
          if cnt == 3:
            if i < j and j < k: combinations.append((i, j, k))
          else:
            for p in range(k + 1, en):
              if i < j and j < k and k < p: combinations.append((i, j, k, p))
  return combinations

def get_bel(a, msk):
  bel = [[] for _ in range(10)]
  for i in range(N):
    for j in range(N):
      if msk[i, j] == 0:
        for x in a[i, j]:
          bel[x].append((i, j))
  return bel

def same_for_col(rule):
  def fun(a, msk, cnt = -1):
    if cnt > -1:
      na, nmsk = rule(a, msk, cnt)
    else:
      na, nmsk = rule(a, msk)
    if np.array_equal(na, a) and np.array_equal(nmsk, msk):
      if cnt > -1:
        na, nmsk = rule(a.T, msk.T, cnt)
      else:
        na, nmsk = rule(a.T, msk.T)
      na = na.T; nmsk = nmsk.T
    return na, nmsk
  
  return fun
