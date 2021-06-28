import time
import csv
import random
import os
import sys


class Board(object):
	# オブジェクト内の関数の第一引数は必ずself！
	def __init__(self):
		self.board = [[ '_' for _ in range(8)] for _ in range(8) ]
		self.board[3][3] = self.board[4][4] = '◯'
		self.board[4][3] = self.board[3][4] = '×'
			# 1回これでやってみる？
		# https://uguisu.skr.jp/othello/5-1.html
		self.value = ([[30, -12, 0, -1, -1, 0, -12, 30],
					[-12, -15, -3, -3, -3, -3, -15, -12],
					[0, -3, 0, -1, -1, 0, -3, 0],
					[-1, -3, -1, -1, -1, -1, -3, -1],
					[-1, -3, -1, -1, -1, -1, -3, -1],
					[0, -3, 0, -1, -1, 0, -3, 0],
					[-12, -15, -3, -3, -3, -3, -15, -12],
					[30, -12, 0, -1, -1, 0, -12, 30]])

	def depict(self):
		print('          x        ')
		print ('    1 2 3 4 5 6 7 8')
		for i in range(8):
			if i == 4:
				print('y ', end='')
			else:
				print('  ', end='')
			print(i+1, end=' ')
#			print(self.board[i], sep=' ')
			for a in self.board[i]:
				print(a, end=' ')
			print()
	
	def check_canput(self, x, y):
		global which_turn
		x -= 1
		y -= 1
#		if x > 7 or x < 0 or y > 7 or y < 0:
#			print('enter correct number')
		opposite_turn = Second if which_turn == First else First
		direction = []
		# 端以外に置こうとしてるときの処理（同時に扱う方法ある？）
		if 0 < x < 7 and 0 < y < 7:
			if self.board[x][y] != '_':
				return
#			# 進める可能性のある方向、上から時計回りに1,2,3,4
			if self.board[x][y-1] == opposite_turn:
				direction.append(4)
			if self.board[x+1][y] == opposite_turn:
				direction.append(3)
			if self.board[x][y+1] == opposite_turn:
				direction.append(2)
			if self.board[x-1][y] == opposite_turn:
				direction.append(1)
			# 斜めの時は5,6,7,8
			if self.board[x-1][y+1] == opposite_turn:
				direction.append(5)
			if self.board[x+1][y+1] == opposite_turn:
				direction.append(6)
			if self.board[x+1][y-1] == opposite_turn:
				direction.append(7)
			if self.board[x-1][y-1] == opposite_turn:
				direction.append(8)
			if len(direction) == 0:
				return

		elif x == 0 and y != 0 and y != 7:
			if self.board[x][y] != '_':
				return
			if self.board[x][y-1] == opposite_turn:
				direction.append(4)
			if self.board[x+1][y] == opposite_turn:
				direction.append(3)
			if self.board[x][y+1] == opposite_turn:
				direction.append(2)
			if self.board[x+1][y+1] == opposite_turn:
				direction.append(6)
			if self.board[x+1][y-1] == opposite_turn:
				direction.append(7)
			if len(direction) == 0:
				return
		elif y == 0 and x != 0 and x != 7:
			if self.board[x][y] != '_':
				return
			if self.board[x+1][y] == opposite_turn:
				direction.append(3)
			if self.board[x][y+1] == opposite_turn:
				direction.append(2)
			if self.board[x-1][y] == opposite_turn:
				direction.append(1)
			if self.board[x-1][y+1] == opposite_turn:
				direction.append(5)
			if self.board[x+1][y+1] == opposite_turn:
				direction.append(6)
			if len(direction) == 0:
				return
		elif x == 7 and y != 0 and y != 7:
			if self.board[x][y] != '_':
				return
			if self.board[x][y-1] == opposite_turn:
				direction.append(4)
			if self.board[x][y+1] == opposite_turn:
				direction.append(2)
			if self.board[x-1][y] == opposite_turn:
				direction.append(1)
			if self.board[x-1][y+1] == opposite_turn:
				direction.append(5)
			if self.board[x-1][y-1] == opposite_turn:
				direction.append(8)
			if len(direction) == 0:
				return
		elif y == 7 and x != 0 and x != 7:
			if self.board[x][y] != '_':
				return
			if self.board[x][y-1] == opposite_turn:
				direction.append(4)
			if self.board[x+1][y] == opposite_turn:
				direction.append(3)
			if self.board[x-1][y] == opposite_turn:
				direction.append(1)
			if self.board[x+1][y-1] == opposite_turn:
				direction.append(7)
			if self.board[x-1][y-1] == opposite_turn:
				direction.append(8)
			if len(direction) == 0:
				return

		elif x == 0 and y == 0:
			if self.board[x][y] != '_':
				return
			if self.board[x+1][y] == opposite_turn:
				direction.append(3)
			if self.board[x][y+1] == opposite_turn:
				direction.append(2)
			if self.board[x+1][y+1] == opposite_turn:
				direction.append(6)
			if len(direction) == 0:
				return
		elif x == 0 and y == 7:
			if self.board[x][y] != '_':
				return
			if self.board[x][y-1] == opposite_turn:
				direction.append(4)
			if self.board[x+1][y] == opposite_turn:
				direction.append(3)
			if self.board[x+1][y-1] == opposite_turn:
				direction.append(7)
			if len(direction) == 0:
				return
		elif x == 7 and y == 0:
			if self.board[x][y] != '_':
				return
			if self.board[x][y+1] == opposite_turn:
				direction.append(2)
			if self.board[x-1][y] == opposite_turn:
				direction.append(1)
			if self.board[x-1][y+1] == opposite_turn:
				direction.append(5)
			if len(direction) == 0:
				return
		elif x == 7 and y == 7:
			if self.board[x][y] != '_':
				return
			if self.board[x][y-1] == opposite_turn:
				direction.append(4)
			if self.board[x-1][y] == opposite_turn:
				direction.append(1)
			if self.board[x-1][y-1] == opposite_turn:
				direction.append(8)
			if len(direction) == 0:
				return

#			print('can go direction:', direction)
		num_get_coins = []
		coordinate_x, coordinate_y = x, y
		for a in direction:
			if a == 4:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				y -= 1
				while 0 <= y <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break
					else:
						tmp += 1
					y -= 1
			elif a == 3:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x += 1
				while 0 <= x <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break
					else:
						tmp += 1
					x += 1
			elif a == 2:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				y += 1
				while 0 <= y <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break	
					else:
						tmp += 1
					y += 1				
			elif a == 1:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x -= 1
				while 0 <= x <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break
					else:
						tmp += 1
					x -= 1				
			elif a == 5:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x -= 1
				y += 1
				while 0 <= x <= 7 and 0 <= y <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break
					else:
						tmp += 1
					x -= 1				
					y += 1
			elif a == 6:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x += 1
				y += 1
				while 0 <= x <= 7 and 0 <= y <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break
					else:
						tmp += 1
					x += 1				
					y += 1
			elif a == 7:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x += 1
				y -= 1
				while 0 <= x <= 7 and 0 <= y <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break
					else:
						tmp += 1
					x += 1				
					y -= 1
			elif a == 8:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x -= 1
				y -= 1
				while 0 <= x <= 7 and 0 <= y <= 7:
					if self.board[x][y] == which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '_':
						break
					else:
						tmp += 1
					x -= 1	
					y -= 1	
		if len(num_get_coins) != 0:
			return num_get_coins

	def put(self, num_get_coins, x, y):
		x -= 1
		y -= 1
		global which_turn
		self.board[x][y] = which_turn
		for lis in num_get_coins:
			if lis[0] == 1:
				for i in range(lis[1]):
					self.board[x-1-i][y] = which_turn
			elif lis[0] == 2:
				for i in range(lis[1]):
					self.board[x][y+1+i] = which_turn
			elif lis[0] == 3:
				for i in range(lis[1]):
					self.board[x+1+i][y] = which_turn
			elif lis[0] == 4:
				for i in range(lis[1]):
					self.board[x][y-1-i] = which_turn
			elif lis[0] == 5:
				for i in range(lis[1]):
					self.board[x-1-i][y+1+i] = which_turn
			elif lis[0] == 6:
				for i in range(lis[1]):
					self.board[x+1+i][y+1+i] = which_turn
			elif lis[0] == 7:
				for i in range(lis[1]):
					self.board[x+1+i][y-1-i] = which_turn
			elif lis[0] == 8:
				for i in range(lis[1]):
					self.board[x-1-i][y-1-i] = which_turn

	def which_win(self):
		# ◯ is protagonist, if ◯ wins, the judge is win
		total_num = [0, 0]
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == '◯':
					total_num[0] += 1
				elif self.board[i][j] == '×':
					total_num[1] += 1
		self.depict()
		print(total_num)
		if total_num[0] > total_num[1]:
			if total_num[1] == 0:
				return 'all'
			return 'win'
		elif total_num[0] < total_num[1]:
			if total_num[0] == 0:
				return 'all'
			return 'lose'
		else:
			return 'draw'

def file_make(folder_name):
	# make folder after checking new file or not
	if os.path.isdir(folder_name) == False:
		os.makedirs('./' + folder_name) # if there is the file, it shows error?
		os.makedirs('./' + folder_name + '/all')
		os.makedirs('./' + folder_name + '/draw')
		os.makedirs('./' + folder_name + '/error')
		os.makedirs('./' + folder_name + '/lose')
		os.makedirs('./' + folder_name + '/win')
	else:
		print('Folder exists')
		sys.exit()


if __name__ == '__main__':
	# to make folder for recording
	whether_file_make = input('do u wanna record?(y/n):')
	if whether_file_make == 'y':
		folder_name = input('what folder name do u wanna record?:')
		file_make(folder_name)
	else:
		# TODO ここ消す
		folder_name = './secret'

	# loop for reversi of computer vs computer
	num = int(input('how many times do u wanna loop?:'))
	win = 0
	lose = 0
	draw = 0
	all = 0
	for k in range(num):
		which_turn = '◯'
		First, Second = '◯', '×'
		board = Board()
		record = []
		# 2次元配列を想定
		step = 0
		while(step < 77):

			check = {}
			for i in range(1, 9):
				for j in range(1, 9):
					if board.check_canput(i, j):
						check[(i, j)] = board.value[i-1][j-1]
						# print(j,i)


			if len(check) > 0: # when u can put somewhere
				# 先攻は表を元に行動
				if which_turn == '◯':
					l = max(check, key=check.get)
				else:
					t = []
					[t.append(i) for i in check]
					l = random.choice(t)
				x = l[1]  # x, yをここで取り換えた
				y = l[0]
				tmp = board.check_canput(y, x)
				if tmp:
					board.put(tmp, y, x)
					which_turn = First if which_turn == Second else Second
					record.append([x, y])
					# sentence = '{},{}\n'.format(x, y)
					# f.writelines(sentence)
			else:
				which_turn = First if which_turn == Second else Second
			step += 1

		
		# 書き込むフォルダとファイル名の指定
		result = board.which_win()
		print(result)
		if result == 'win':
			win += 1
			path = './' + folder_name + '/win/' + str(k) + '.txt'
		elif result == 'lose':
			lose += 1
			path = './' + folder_name + '/lose/' + str(k) + '.txt'
		elif result == 'draw':
			draw += 1
			path = './' + folder_name + '/draw/' + str(k) + '.txt'
		elif result == 'all':
			all += 1
			path = './' + folder_name + '/all/' + str(k) + '.txt'
		else:
			path = './1st/error/' +str(i) + '.txt'


		if whether_file_make == 'y':

			# ファイルに記録するためのデータの加工
			str_lis = []
			print(path)
			for a in record:
				tmp = []
				for i in range(2):
					tmp.append(str(a[i]))
				str_lis.append(tmp)
			with open(path, mode='w') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerows(str_lis)
	
	print('win:' + str(win) + ' lose:' + str(lose) + ' draw:' + str(draw) + ' all:' + str(all))

