import random
import sys
import numpy as np


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
          for a in self.board:
               for b in a:
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

class Player_learning(object):
     def __init__(self, turn, table=None):
          self.turn = turn
          if table is None:
               self.q_table = self.make_q_table()
          else:
               self.q_table = table

     def random_put(self, canput: list, board: Board):
          l = random.choice(canput)
          x, y = l[0], l[1]
          board.board[x][y] = self.turn

     def make_q_table(self):
          n_colums = 9
          n_rows = 3 ** 9
          return np.zeros((n_rows, n_colums))


     def q_table_put(self, canput: list, board: Board):
          row_index = board.find_board_number()
          if np.random.random() > epsilon:  #左辺は0から1のランダム
               action = np.argmax(self.q_table[row_index])
               y = action // 3
               x = action % 3
          else:
               l = random.choice(canput)
               x, y = l[0], l[1]
               action = x + y * 3             
          board.board[x][y] = self.turn
          
          reward = REWARD if board.judge(self.turn) is True else 0

          new_row_index = board.find_board_number()
          max_future_q = np.max(self.q_table[new_row_index])
          current_q = self.q_table[row_index][action]
          new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
          # print(new_q)
          self.q_table[row_index][action] = new_q


if __name__ == '__main__':
     # 対戦用の初期設定
     # board= Board()
     FIRST, SECOND = '◯', '×'
     # player_1 = Player_random(FIRST)
     player_2 = Player_random(SECOND)
     player_3 = Player_learning(FIRST)
     

     # Q学習の初期設定
     LEARNING_RATE = 0.1
     REWARD = 3
     DISCOUNT = 0.95 # 0-1
     EPISODES = 250000
     SHOW_EVERY = 10000

     epsilon = 0.5
     START_EPSILON_DECAYING = 1
     END_EPSILON_DECAYING = EPISODES // 2
     epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

     # TODO 負けた時のrewardをマイナスにすると学習速い？
     for episode in range(EPISODES):
          board= Board()
          which_turn = FIRST
          while board.can_put():
               # board.print()
               # print('-----')
               if which_turn == FIRST:
                    # player_1.random_put(board.can_put(), board)
                    player_3.q_table_put(board.can_put(), board)
               else:
                    player_2.random_put(board.can_put(), board)

               if board.judge(which_turn) is True:
                    # board.print()
                    break
               which_turn = SECOND if which_turn == FIRST else FIRST
          
          if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
               epsilon -= epsilon_decay_value

          if episode % SHOW_EVERY == 0:
               board.print()
               print(player_3.q_table)

     num = 0
     for i in range(3**8):
          for j in range(9):
               if player_3.q_table[i][j] != 0:
                    # print('atta')
                    num += 1
     print(num)
     np.savetxt('./q_table.txt', player_3.q_table)