import random
import sys
import numpy as np
import os


class Board(object):
     def __init__(self):
          self.board = [['_'for _ in range(3)] for _ in range(3)]

     def find_board_number(self):
          row_index = 0
          for i in range(3):
               for j in range(3):
                    if self.board[i][j] == '×':
                         coef = 1
                    elif self.board[i][j] == '◯':
                         coef = 2
                    else:
                         coef = 0
                    row_index += 3 ** (i + 3 * j) * coef 
          
          return row_index

     def print(self):
          print('     x ')
          print('   1 2 3')
          for i in range(3):
               if i == 1:
                    print('y', i+1, end='')
               else:
                    print(' ', i+1, end='')
               for b in self.board[i]:
                    print(b, end=' ')
               print('')

     def can_put(self):
          can_put_place = []
          for i in range(3):
               for j in range(3):
                    if self.board[i][j] == '_':
                         can_put_place.append([i, j])
          
          return can_put_place

     def judge(self, turn):
          for i in range(3):
               if self.board[i][0] == turn and\
                    self.board[i][1] == turn and\
                    self.board[i][2] == turn:
                    return True
               elif self.board[0][i] == turn and\
                    self.board[1][i] == turn and\
                    self.board[2][i] == turn:
                    return True

          if self.board[0][0] == turn and\
               self.board[1][1] == turn and\
               self.board[2][2] == turn:
               return True
          elif self.board[0][2] == turn and\
               self.board[1][1] == turn and\
               self.board[2][0] == turn:
               return True

          return False


class Player_random(object):
     def __init__(self, turn):
          self.turn = turn

     def random_put(self, canput: list, board: Board) -> list:
          l = random.choice(canput)
          x, y = l[0], l[1]
          board.board[x][y] = self.turn
          # print(board.find_board_number())


class Player_using_table(object):
     def __init__(self, turn, table=None):
          self.turn = turn
          # FILE_PATH = './q_table.npy'
          # FILE_PATH = input("Eneter q_table's file name:")
          FILE_PATH = './q_table.npy'
          if os.path.exists(FILE_PATH):
               q_table = np.load(FILE_PATH)
          else:
               q_table =  np.zeros((3 ** 9, 9))  # 実質のランダム
          self.q_table = q_table

     def q_table_put(self, canput: list, board: Board):
          row_index = board.find_board_number()
          while True:
               action = np.argmax(self.q_table[row_index])
               y = action // 3
               x = action % 3
               if [x, y] in canput:
                    break
               self.q_table[row_index][action] = MINUS_INF
          
          board.board[x][y] = self.turn


if __name__ == '__main__':
     MINUS_INF = -1000
     # 対戦用の初期設定
     # ランダムで先攻後攻を決める
     f, s = '◯', '×'
     FIRST = random.choice(['◯', '×'])
     SECOND = s if FIRST == f else f
     which_turn = FIRST

     player_using_table = Player_using_table('◯')

     board= Board()
     board.print()
     while board.can_put():
          if which_turn == f:
               player_using_table.q_table_put(board.can_put(), board)
               if board.judge(which_turn) is True:
                    print('you lost')
                    board.print()
                    break
          else:
               print('you are ×')
               print("Where do u wanna put?")
               place = False
               while not place:
                    x = int(input('x:'))
                    y = int(input('y:'))
                    if [y-1, x-1] in board.can_put():
                         place = True
                    else:
                         print('you cannot put here')
               board.board[y-1][x-1] = s
               if board.judge(which_turn) is True:
                    board.print()
                    print('you won')
                    break
          board.print()
          which_turn = SECOND if which_turn == FIRST else FIRST
