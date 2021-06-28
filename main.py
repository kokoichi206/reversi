import time
import csv
class Board(object):
	# オブジェクト内の関数の第一引数は必ずself！
	def __init__(self):
		self.board = [[ '_' for _ in range(8)] for _ in range(8) ]
		self.board[3][3] = self.board[4][4] = '◯'
		self.board[4][3] = self.board[3][4] = '×'
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

if __name__ == '__main__':
	whether_record = input('do u wanna record?:(y/n)')	
	board = Board()
	which_turn = '◯'
	First, Second = '◯', '×'
	board.depict()
	if whether_record == 'y' or whether_record == 'yes' or whether_record == 'Y':
		record = []
		step = 0
		# 書き込むフォルダとファイル名の指定
		path = './data/' + str(int(time.time())) + '.txt'
		# 2次元配列を想定
		with open(path, mode='w') as f:
			ref = [[5,3],[6,5],[5,6],[4,3],[7,5],[7,6],[7,7],[8,5],[3,3],[4,2],[3,1],[2,3],[1,3],[4,1],[5,1],[5,2],[3,5],[3,2],[2,1],[3,4],[6,4],[7,4],[8,3],[8,4],[8,6],[7,8],[2,4],[5,7],[6,1],[7,3],[8,7],[2,5],[6,6],[4,6],[8,8],[6,7],[6,8],[3,6],[5,8],[4,8],[3,8],[2,6],[4,7],[2,2],[3,7],[2,8],[1,8],[2,7],[1,1],[1,7],[1,6],[1,2]]
			for ana in ref:
				check = 0
				for i in range(1, 9):
					for j in range(1, 9):
						if board.check_canput(i, j):
							check += 1
							print(j,i)
				if check > 0: # when u can put somewhere
					print("Now it's {}'s turn".format(which_turn))
					print('where do you wanna put?(x, y)')
					x = ana[0]
					y = ana[1]

					tmp = board.check_canput(y, x)	
					if tmp:
						board.put(tmp, y, x)
						which_turn = First if which_turn == Second else Second
						board.depict()
						record.append([x, y])
						sentence = '{},{}\n'.format(x, y)
						f.writelines(sentence)

					else:
						print('you cannot put here')
				else:
					print('You have to PASS!')	
					which_turn = First if which_turn == Second else Second
				print('---------------------------')
				step += 1
			# terminalでx,y入力
			while(step < 100):
				check = 0
				for i in range(1, 9):
					for j in range(1, 9):
						if board.check_canput(i, j):
							check += 1
							print(j,i)
				if check > 0: # when u can put somewhere
					print("Now it's {}'s turn".format(which_turn))
					print('where do you wanna put?(x, y)')
					x = input('x:')
					y = input('y:')
					if not str.isdecimal(x) or not str.isdecimal(y):
						break
					x = int(x)
					y = int(y)
					tmp = board.check_canput(y, x)	
					if tmp:
						board.put(tmp, y, x)
						which_turn = First if which_turn == Second else Second
						board.depict()
						record.append([x, y])
						sentence = '{},{}\n'.format(x, y)
						f.writelines(sentence)

					else:
						print('you cannot put here')
				else:
					print('You have to PASS!')	
					which_turn = First if which_turn == Second else Second
				print('---------------------------')
				step += 1
		# fileへの記録
		# fileに記録するために先づデータをstringに
		# str_lis = []
		# for a in record:
		# 	tmp = []
		# #	print(type(a))
		# 	for i in range(len(a)):
		# 		tmp.append(str(a[i]))
		# 	str_lis.append(tmp)
		# path = './' + str(int(time.time())) + '.txt'
		# # 2次元配列を想定
		# with open(path, mode='w') as f:
		# 	writer = csv.writer(f, lineterminator='\n')
		# 	writer.writerows(str_lis)
	else:
		step = 0
		while(step < 100):
			check = 0
			for i in range(1, 9):
				for j in range(1, 9):
					if board.check_canput(i, j):
						check += 1
						print(j,i)
			if check > 0: # when u can put somewhere
				print("Now it's {}'s turn".format(which_turn))
				print('where do you wanna put?(x, y)')
				x = int(input('x:'))
				y = int(input('y:'))
				tmp = board.check_canput(y, x)	
				if tmp:
					board.put(tmp, y, x)
					which_turn = First if which_turn == Second else Second
					board.depict()
				else:
					print('you cannot put here')
			else:
				print('{} have to PASS!'.format(which_turn))	
				which_turn = First if which_turn == Second else Second
			print('---------------------------')
