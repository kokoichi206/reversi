win_num = []

FILE_PATH = './progress_1000000.txt'
with open(FILE_PATH) as f:
     l = f.readlines()
     for i in range(1, len(l)):
          tmp = l[i].split('\t')
          win_num.append(int(tmp[1]))

MAX_WIN_NUM = max(win_num)
MIN_WIN_NUM = min(win_num)
INCREMENT = (MAX_WIN_NUM - MIN_WIN_NUM) // 20
hist = [0 for _ in range(20)]
for i in range(len(win_num)):
     for j in range(20):
          if MIN_WIN_NUM + INCREMENT * j <= win_num[i] <= MIN_WIN_NUM + INCREMENT * (j+1):
               hist[j] += 1

for i in range(20):
     print('■' * (hist[i]//5))