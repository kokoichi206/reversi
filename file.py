import time
import csv
lis = [[1, 4], [2, 5], [4, 6]]
str_lis = []
for a in lis:
	tmp = []
#	print(type(a))
	for i in range(len(a)):
		tmp.append(str(a[i]))
	str_lis.append(tmp)
path = './' + str(int(time.time())) + '.txt'
# 2次元配列を想定
with open(path, mode='w') as f:
	writer = csv.writer(f, lineterminator='\n')
	writer.writerows(str_lis)
#		f.write(','.join(e))
#		f.wite('\n')	
