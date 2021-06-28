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
               while True:
                    action = np.argmax(self.q_table[row_index])
                    y = action // 3
                    x = action % 3
                    if [x, y] in canput:
                         break
                    self.q_table[row_index][action] = MINUS_INF
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
          return action, row_index, new_row_index, max_future_q, current_q

     def leaning_enemy(self, row_index, action, new_row_index, max_future_q, current_q):
          # 負けた時はここから負のrewardで学習させる
          reward = -3
          new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
          self.q_table[row_index][action] = new_q


class Player_using_table(object):
     def __init__(self, turn, table=None):
          self.turn = turn
          # FILE_PATH = './q_table.npy'
          FILE_PATH = input("Eneter q_table's file name:")
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
     # Q学習の初期設定
     MINUS_INF = -100_000  # q tableのなかで置けないところはこいつで実質つぶす
     LEARNING_RATE = 0.1
     REWARD = 3
     DISCOUNT = 0.95 # 0-1
     EPISODES = 3_000_000
     SHOW_EVERY = 1000

     epsilon = 0.5
     START_EPSILON_DECAYING = 1
     END_EPSILON_DECAYING = EPISODES // 2
     epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)


     win = 0
     lose = 0
     draw = 0

     # 対戦用の初期設定
     FIRST, SECOND = '◯', '×'
     player_radom = Player_random('×')
     player_using_table = Player_using_table('◯')
     # if input('do u wanna use q_table exsited?:(y/n)') == 'y':
     #      q_table = np.load('./q_table.npy')
     #      player_3 = Player_learning('◯', q_table)
     # else:
     #      player_3 = Player_learning('◯')
     player_3 = Player_random('◯')
     for episode in range(1, EPISODES):
          # episodeの偶奇で先攻後攻を変えている
          if episode % 2 == 0:
               which_turn = FIRST
          else:
               which_turn = SECOND

          board= Board()
          is_judge_draw = True
          while board.can_put():
               if which_turn == FIRST:
                    # player_1.random_put(board.can_put(), board)
                    player_3.random_put(board.can_put(), board)
                    if board.judge(which_turn) is True:
                         # board.print()
                         win += 1
                         is_judge_draw = False
                         break
               else:
                    player_radom.random_put(board.can_put(), board)
                    if board.judge(which_turn) is True:
                         # board.print()
                         lose += 1
                         is_judge_draw = False
                         break
               which_turn = SECOND if which_turn == FIRST else FIRST
          if is_judge_draw:
               draw += 1

          if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
               epsilon -= epsilon_decay_value

          if episode % SHOW_EVERY == 0:
               board.print()
               # print(player_3.q_table)
               print('win:', win, ' lose:', lose, ' draw:', draw)
               sentence = str(episode) + '\t' + str(win) + '\t' + str(lose)\
                     + '\t' + str(draw) + '\t' + str(epsilon) + '\n'
               print('win_rate:' + '{:.2f}'.format(100*win/(SHOW_EVERY)) +'   progress:'+'■'*(episode*10//EPISODES)+'_'*(10-episode*10//EPISODES))

               win = 0
               lose = 0
               draw = 0

     # q_tableの中で更新を受けたもの
     num = 0
     for i in range(3**8):
          for j in range(9):
               if player_3.q_table[i][j] != 0:
                    # print('atta')
                    num += 1
     print(num)
