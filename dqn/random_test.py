# このファイルをrandom.pyとするとだめだった！
import random


l = [0, 1, 2, 3, 4, 5]

print(random.sample(l, 3)) # 重複なし
print(tuple(random.sample(l, 3)))

print(''.join(random.sample('abcdef', 3)))
