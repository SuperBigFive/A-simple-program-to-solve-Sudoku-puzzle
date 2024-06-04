from utils import *
import copy
import numpy as np

N = 9

def rule1(a, msk):
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)
  for i in range(N):
    for j in range(N):
      if nmsk[i, j] == 0 and len(na[i, j]) == 1:
        nmsk[i, j] = 1
        na[i, j] = int(list(na[i, j])[0])
        print('> Fill the block [' + str(i + 1) + ', ' + str(j + 1) + '] with ' + str(na[i, j]))
        clear_cddt_for_row(i, na, nmsk[i, :], [na[i, j]])
        clear_cddt_for_col(j, na, nmsk[:, j], [na[i, j]])
        clear_cddt_for_block(get_block_idx(i, j), na, nmsk, [na[i, j]])
        return na, nmsk
  return na, nmsk

def rule2(a, msk):
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)
  bel = get_bel(na, nmsk)

  for i in range(1, 10):
    if len(bel[i]) == 1: 
      x, y = bel[i][0]
      nmsk[x, y] = 1
      na[x, y] = int(i)
      print('> Fill the block [' + str(x + 1) + ', ' + str(y + 1) + '] with ' + str(i))
      return na, nmsk
  return na, nmsk

def rule3(a, msk):
  return rule7(a, msk, 2)

def rule4(a, msk):
  return rule8(a, msk, 2)

def rule5(a, msk):
  return rule7(a, msk, 3)

def rule6(a, msk):
  return rule8(a, msk, 3)

def rule7(a, msk, cnt = 4):
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)

  for i in range(N):
    vis = dict()
    for j in range(N):
      if nmsk[i, j] == 0 and len(na[i, j]) == cnt:
        key = tuple(list(na[i, j]))
        vis[key] = vis.get(key, []) + [j]
        if len(vis[key]) >= cnt:
          tmp_msk = copy.deepcopy(nmsk[i, :])
          for col in vis[key]:
            tmp_msk[col] = 1
          print('> clear cddt for row', cnt, i, key, vis[key])
          na = clear_cddt_for_row(i, na, tmp_msk, list(na[i, j]))
          if not np.array_equal(na, a): return na, nmsk

  for j in range(N):
    vis = dict()
    for i in range(N):
      if nmsk[i, j] == 0 and len(na[i, j]) == cnt:
        key = tuple(list(na[i, j]))
        vis[key] = vis.get(key, []) + [i]
        if len(vis[key]) >= cnt:
          tmp_msk = copy.deepcopy(nmsk[:, j])
          for row in vis[key]:
            tmp_msk[row] = 1
          print('> clear cddt for col', cnt, j, key, vis[key])
          na = clear_cddt_for_col(j, na, tmp_msk, list(na[i, j]))
          if not np.array_equal(na, a): return na, nmsk
  
  for blo_idx in range(N):
    px, py = get_block_pos(blo_idx)
    vis = dict()
    for i in range(px, px + 3):
      for j in range(py, py + 3):
        if nmsk[i, j] == 0 and len(na[i, j]) == cnt:
          key = tuple(list(na[i, j]))
          vis[key] = vis.get(key, []) + [(i, j)]
          if len(vis[key]) >= cnt:
            tmp_msk = copy.deepcopy(nmsk)
            for row, col in vis[key]:
              tmp_msk[row, col] = 1
            print('> clear cddt for block', cnt, blo_idx, key, vis[key])
            na = clear_cddt_for_block(blo_idx, na, tmp_msk, list(na[i, j]))
            if not np.array_equal(na, a): return na, nmsk

  return na, nmsk

def rule8(a, msk, cnt = 4):
  print('> using rule8...', cnt)
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)
  
  combinations = get_all_combinations(cnt)
  for combination in combinations:
    for row in range(N):
      l = []
      for col in range(N):
        if nmsk[row, col] == 0:
          chk1 = True; chk2 = False
          for x in combination:
            if x not in na[row, col]:
              chk1 = False
            else:
              chk2 = True
          if chk1 and chk2:
            l.append(col)
          elif not chk1 and chk2:
            l = []; break
      if len(l) == cnt:
        for col in l:
          na[row, col] = set(combination)
      if not np.array_equal(na, a): return na, nmsk

    for col in range(N):
      l = []
      for row in range(N):
        if nmsk[row, col] == 0:
          chk1 = True; chk2 = False
          for x in combination:
            if x not in na[row, col]:
              chk1 = False
            else:
              chk2 = True
          if chk1 and chk2:
            l.append(row)
          elif not chk1 and chk2:
            l = []; break
      if len(l) == cnt:
        for row in l:
          na[row, col] = set(combination)
      if not np.array_equal(na, a): return na, nmsk
    
    for blo_idx in range(N):
      px, py = get_block_pos(blo_idx)
      l = []; chk1 = True; chk2 = False
      for row in range(px, px + 3):
        for col in range(py, py + 3):
          if nmsk[row, col] == 0:
            for x in combination:
              if x not in na[row, col]:
                chk1 = False
              else:
                chk2 = True
            if chk1 and chk2:
              l.append((row, col))
            elif not chk1 and chk2:
              l = [-1, -1, -1, -1, -1]; break
      if len(l) == cnt:
        for row, col in l:
          na[row, col] = set(combination)
      if not np.array_equal(na, a): return na, nmsk

  return na, nmsk
        
def rule9(a, msk):
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)

  for blo_idx in range(N):
    px, py = get_block_pos(blo_idx)
    bel = [[] for _ in range(10)]
    for row in range(px, px + 3):
      for col in range(py, py + 3):
        if nmsk[row, col] == 0:
          for x in na[row, col]:
            bel[x].append((row, col))
    for i in range(1, 10):
      row_set, col_set = set(), set()
      for r, c in bel[i]:
        row_set.add(r); col_set.add(c)
      if len(row_set) == 1:
        row = list(row_set)[0]
        for c in range(N):
          if nmsk[row, c] == 0 and get_block_idx(row, c) != blo_idx \
          and i in na[row, c]: na[row, c].discard(i)
        print('> clear cddt using rule9, blo for row', row, ',', blo_idx, i)
        if not np.array_equal(na, a): return na, nmsk
      if len(col_set) == 1:
        col = list(col_set)[0]
        for r in range(N):
          if nmsk[r, col] == 0 and get_block_idx(r, col) != blo_idx \
          and i in na[r, col]: na[r, col].discard(i)
        print('> clear cddt using rule9, blo for col', col, ',', blo_idx, i)
        if not np.array_equal(na, a): return na, nmsk

  for row in range(N):
    bel = [[] for _ in range(10)]
    for col in range(N):
      if nmsk[row, col] == 0:
        for x in na[row, col]:
          bel[x].append((row, col))
    for i in range(1, 10):
      blo_set = set()
      for r, c in bel[i]:
        blo_set.add(get_block_idx(r, c))
      if len(blo_set) == 1:
        blo_idx = list(blo_set)[0]
        px, py = get_block_pos(blo_idx)
        for x in range(px, px + 3):
          for y in range(py, py + 3):
            if x != row and nmsk[x, y] == 0 and i in na[x, y]:
              na[x, y].discard(i)
        print('> clear cddt using rule9, row for blo', row, ',', blo_idx, i)
        if not np.array_equal(na, a): return na, nmsk

  for col in range(N):
    bel = [[] for _ in range(10)]
    for row in range(N):
      if nmsk[row, col] == 0:
        for x in na[row, col]:
          bel[x].append((row, col))
    for i in range(1, 10):
      blo_set = set()
      for r, c in bel[i]:
        blo_set.add(get_block_idx(r, c))
      if len(blo_set) == 1:
        blo_idx = list(blo_set)[0]
        px, py = get_block_pos(blo_idx)
        for x in range(px, px + 3):
          for y in range(py, py + 3):
            if y != col and nmsk[x, y] == 0 and i in na[x, y]:
              na[x, y].discard(i)
        print('> clear cddt using rule9, col for blo', col, ',', blo_idx, i)
        if not np.array_equal(na, a): return na, nmsk

  return na, nmsk

def rule10(a, msk):
  return rule11(a, msk, 2)

@same_for_col
def rule11(a, msk, cnt = 3):
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)

  for num in range(1, 10):
    combinations = get_all_combinations(cnt, 0, 9)
    for row_list in combinations:
      col_bels = []
      for row in row_list:
        col_bel = []
        for col in range(N):
          if nmsk[row, col] == 0 and num in na[row, col]:
            col_bel.append(col)
        col_bels.append(col_bel)
      chk = True
      for col_bel in col_bels:
        if len(col_bel) != cnt or col_bel != col_bels[0]: chk = False; break
      if not chk: continue
      else:
        for col in col_bels[0]:
          for row in range(N):
            if row not in row_list and nmsk[row, col] == 0 \
            and num in na[row, col]: na[row, col].discard(num)

        if not np.array_equal(na, a): return na, nmsk
    
  return na, nmsk

@same_for_col
def rule12(a, msk):
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)
  cell_with_size2 = []
  
  for i in range(N):
    for j in range(N):
      if nmsk[i, j] == 0 and len(na[i, j]) == 2:
        cell_with_size2.append((i, j))
  n = len(cell_with_size2)
  for i in range(n):
    cell1 = cell_with_size2[i]
    for j in range(n):
      if i == j: continue
      cell2 = cell_with_size2[j]
      if get_block_idx(*cell1) != get_block_idx(*cell2) or cell1[0] == cell2[0] : continue
      for k in range(n):
        if i == k or j == k: continue
        cell3 = cell_with_size2[k]
        if get_block_idx(*cell1) == get_block_idx(*cell3) or cell1[0] != cell3[0]: continue
        if na[cell1] == na[cell2] or na[cell2] == na[cell3] or \
          na[cell1] == na[cell3]: continue
        s = set()
        for x in na[cell1]: s.add(x)
        for x in na[cell2]: s.add(x)
        for x in na[cell3]: s.add(x)
        if len(s) == 3:
          row1 = cell1[0]; row2 = cell2[0]
          x, y = list(na[cell1]); z = -1
          for num in na[cell2]:
            if num != x and num != y:
              z = num; break
          assert z > -1
          for col in range(N):
            if get_block_idx(row1, col) == get_block_idx(*cell1) and col != cell1[1] \
            and nmsk[row1, col] == 0 and z in na[row1, col]: na[row1, col].discard(z)
            if get_block_idx(row2, col) == get_block_idx(*cell3) \
            and nmsk[row2, col] == 0 and z in na[row2, col]: na[row2, col].discard(z)
          if not np.array_equal(na, a): return na, nmsk
  
  return na, nmsk

@same_for_col
def rule13(a, msk):
  na = copy.deepcopy(a)
  nmsk = copy.deepcopy(msk)
  cell_with_size2, cell_with_size3 = [], []
  
  for i in range(N):
    for j in range(N):
      if nmsk[i, j] == 0 and len(na[i, j]) == 2:
        cell_with_size2.append((i, j))
      if nmsk[i, j] == 0 and len(na[i, j]) == 3:
        cell_with_size3.append((i, j))

  n = len(cell_with_size2)
  m = len(cell_with_size3)
  for i in range(m):
    cell1 = cell_with_size3[i]
    for j in range(n):
      cell2 = cell_with_size2[j]
      if get_block_idx(*cell1) != get_block_idx(*cell2) or cell1[0] == cell2[0] : continue
      for k in range(n):
        if j == k: continue
        cell3 = cell_with_size2[k]
        if get_block_idx(*cell1) == get_block_idx(*cell3) or cell1[0] != cell3[0]: continue
        if na[cell2] == na[cell3]: continue
        s = set()
        for x in na[cell1]: s.add(x)
        for x in na[cell2]: s.add(x)
        for x in na[cell3]: s.add(x)
        if len(s) == 3:
          row = cell1[0]; z = -1
          for num in na[*cell1]:
            if num in na[*cell2] and num in na[*cell3]:
              z = num; break
          assert z > -1
          for col in range(N):
            if get_block_idx(row, col) == get_block_idx(*cell1) and col != cell1[1] \
            and nmsk[row, col] == 0 and z in na[row, col]: na[row, col].discard(z)
          if not np.array_equal(na, a): return na, nmsk
  
  return na, nmsk
