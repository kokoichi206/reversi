import time
import csv
import random


class Board(object):

	def __init__(self):
		self.board = [[ '' for _ in range(8)] for _ in range(8) ]
		self.board[3][3] = self.board[4][4] = '●'
		self.board[4][3] = self.board[3][4] = '◯'
		self.which_turn = '◯'

	def depict(self):
		print('          x        ')
		print ('    1 2 3 4 5 6 7 8')
		for i in range(8):
			if i == 4:
				print('y ', end='')
			else:
				print('  ', end='')
			print(i+1, end=' ')
			for a in self.board[i]:
				print(a, end=' ')
			print()
	
	def check_canput(self, x, y):
		opposite_turn = '●' if self.which_turn == '◯' else '◯'
		direction = []
		# 端以外に置こうとしてるときの処理（同時に扱う方法ある？）
		if 0 < x < 7 and 0 < y < 7:
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
			if self.board[x][y] != '':
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
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
						break
					else:
						tmp += 1
					y -= 1
			elif a == 3:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x += 1
				while 0 <= x <= 7:
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
						break
					else:
						tmp += 1
					x += 1
			elif a == 2:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				y += 1
				while 0 <= y <= 7:
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
						break	
					else:
						tmp += 1
					y += 1				
			elif a == 1:
				x, y = coordinate_x, coordinate_y
				tmp = 0
				x -= 1
				while 0 <= x <= 7:
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
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
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
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
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
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
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
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
					if self.board[x][y] == self.which_turn:
						num_get_coins.append([a, tmp])
						break
					elif self.board[x][y] == '':
						break
					else:
						tmp += 1
					x -= 1	
					y -= 1	
		if len(num_get_coins) != 0:
			return num_get_coins

	def put(self, num_get_coins, x, y):

		self.board[x][y] = self.which_turn
		for lis in num_get_coins:
			if lis[0] == 1:
				for i in range(lis[1]):
					self.board[x-1-i][y] = self.which_turn
			elif lis[0] == 2:
				for i in range(lis[1]):
					self.board[x][y+1+i] = self.which_turn
			elif lis[0] == 3:
				for i in range(lis[1]):
					self.board[x+1+i][y] = self.which_turn
			elif lis[0] == 4:
				for i in range(lis[1]):
					self.board[x][y-1-i] = self.which_turn
			elif lis[0] == 5:
				for i in range(lis[1]):
					self.board[x-1-i][y+1+i] = self.which_turn
			elif lis[0] == 6:
				for i in range(lis[1]):
					self.board[x+1+i][y+1+i] = self.which_turn
			elif lis[0] == 7:
				for i in range(lis[1]):
					self.board[x+1+i][y-1-i] = self.which_turn
			elif lis[0] == 8:
				for i in range(lis[1]):
					self.board[x-1-i][y-1-i] = self.which_turn

		# change which_turn after putting one board
		self.which_turn = '●' if self.which_turn == '◯' else '◯'

	# すべての場所を調べ、そのターンの人が置ける可能性があるかチェック
	def check_canput_all(self):
		check = []
		for i in range(8):
			for j in range(8):
				if self.check_canput(i, j):
					check.append([i, j])
		
		if check:
			return check
		else:
			return False

	# 場所を指定し、そこにおけるなら置く、おけないならFalse
	def put_mine(self, location):
		if self.check_canput_all():
			x = int(location[0])
			y = int(location[1])
			num_direction = self.check_canput(x, y)
			if num_direction:
				self.put(num_direction, x, y)
				return True
			else:
				return False
			
		else:
			# パスなら、手番を変えてから、
			return False

	def count(self):
		black_count = 0
		white_count = 0
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == '●':
					black_count += 1
				elif self.board[i][j] == '◯':
					white_count += 1

		return black_count, white_count

	def winner_judge(self):
		b, w = self.count()
		if b > w:
			return 'BLACK', b, w
		elif w > b:
			return 'WHITE', w, b
		else:
			return 'DRAW', b, w

	def put_cpu_random(self):
		check = self.check_canput_all()
		if check:
			x, y = random.choice(check)
			num_direction = self.check_canput(x, y)
			self.put(num_direction, x, y)
		else:
			return 'PASS'

	def change_turn(self):
		self.which_turn = '●' if self.which_turn == '◯' else '◯'


if __name__ == '__main__':
	pass
