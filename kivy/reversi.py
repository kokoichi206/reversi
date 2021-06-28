import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

import play_reversi, play_reversi_hard

# Set the app size
# 640 + 240, 880
Window.size = (880, 880)

# Designate Our .kv design file
Builder.load_file('reversi.kv')


class MyLayout(Widget):
     global board

     def dipict_map(self):
          global board
          for i in range(8):
               for j in range(8):
                    self.ids[f'{i}{j}'].text = board.board[i][j]
                    
     def clear(self):
          # if there is no 'global board' here, it didn't work,
          # I don't know why
          global board, hardBoard, hardCpu
          self.ids.clear_button.color = 1, 1, 1, 1
          if self.ids.clear_button.text != 'CLEAR':
               self.ids.clear_button.text = 'CLEAR'
          else:
               board = play_reversi.Board()
               hardBoard = play_reversi_hard.Board()
               hardCpu = play_reversi_hard.GreedyPlayer()

          self.dipict_map()

          self.ids.black_num.text = ''
          self.change_display_turn()
          self.change_number()

     # change button color
     def cpu_button(self, side):
          blackOrWhite = side.split('_')[0]
          which = side[6:]
          side_list = ['human', 'cpu', 'cpu_hard']
          if which == 'human':
               side_list.remove('human')
          elif which == 'cpu':
               side_list.remove('cpu')
          elif which == 'cpu_hard':
               side_list.remove('cpu_hard')
          if self.ids[side].background_color == [157/255, 157/255, 1, 1]:
               pass
          else:
               self.ids[side].background_color = 157/255, 157/255, 1, 1
               for a in side_list:
                    aa = blackOrWhite + '_' + a
                    self.ids[aa].background_color = 204/255, 204/255, 204/255, 1

     def isCPU(self, side):
          # side means black or white
          side += '_cpu'
          if self.ids[side].background_color == [157/255, 157/255, 1, 1]:
               return True
          else:
               return False

     def isCPU_hard(self, side):
          # side means black or white
          side += '_cpu_hard'
          if self.ids[side].background_color == [157/255, 157/255, 1, 1]:
               return True
          else:
               return False

     def buttonClicked(self, location):
          global board
          # CPU vs CPU
          
          if self.isCPU('black') and self.isCPU('white'):
               i = 0
               while i < 70:
                    self.put_cpu()
                    print(board.board)
                    i += 1
          # CPU(black) vs person
          elif self.isCPU('black'):
               if self.put_human(location):
                    self.resetFont()
                    self.put_cpu()
          # CPU(white) vs person
          elif self.isCPU('white'):
               if board.which_turn == '◯':
                    self.put_cpu()
               else:
                    if self.put_human(location):
                         self.resetFont()
                         self.put_cpu()
          # elif (not self.isCPU('white')) and (not self.isCPU('black')):
          #      self.put_human(location)

          elif self.isCPU_hard('black'):
               # 指定した場所に置けた時のみ、置いてかつtrueを返す
               if self.put_human_vs_hard(location):
                    self.put_cpu_hard('black')


     def put_cpu_hard(self,side):
          global board, hardBoard, hardCpu
          # hardボードの処理
          place = hardCpu.go(hardBoard)
          hardBoard.move(place)
          print(board.board)
          print(board.which_turn)
          # print(place)
          y = place // 8
          x = place % 8
          # print(str(y) + str(x))
          # print(board.put_mine(str(y) + str(x)))
          board.put_mine(str(y) + str(x))
          self.dipict_map()
          self.dipictPossiblePlaces()


     def put_human_vs_hard(self, location):
          global board, hardBoard, hardCpu, hardPlayer
          # 人間が置けた時のみTrue -> CPUも動作
          if board.put_mine(location):
               move = int(location[0]) * 8 + int(location[1])
               self.dipict_map()
               self.change_number()
               # print(location)
               # print(move)
               # hardPlayer.go(hardBoard, str(move))
               hardBoard.move(move)
               # print(hardBoard)
               return True
          # 人間がおけない時、True
          if not self.can_put():
               return True

          return False


     def put_cpu(self):
          global board
          if board.put_cpu_random() == 'PASS':
               board.change_turn()
               self.dipict_map()
               self.change_display_turn()
          self.dipict_map()
          self.dipictPossiblePlaces()

     def put_human(self, location):
          global board
          # 人間が置けた時のみTrue -> CPUも動作
          if board.put_mine(location):
               self.dipict_map()
               self.change_number()
               return True
          # 人間がおけない時、True
          if not self.can_put():
               return True

          return False

     def can_put(self):
          if board.check_canput_all():
               if self.ids.clear_button.text == 'PASSED':
                    self.ids.clear_button.text = 'CLEAR'
                    self.ids.clear_button.color = 1, 1, 1, 1
                    self.change_display_turn()
               return True
          else:
               self.ids.clear_button.text = 'PASSED'
               self.ids.clear_button.color = 1, 0, 0, 1
               board.change_turn()
               if not board.check_canput_all():
                    self.ids.clear_button.color = 1, 0, 0, 1
                    winner, num1, num2 = board.winner_judge()
                    if winner == 'DRAW':
                         self.ids.clear_button.text = f'DRAW: {num1} - {num2}'
                    else:
                         self.ids.clear_button.text = f'{winner} win: {num1} - {num2}'
               self.change_display_turn()
               return False
               
     def dipictPossiblePlaces(self):
          self.resetFont()
          possiblePlaces = board.check_canput_all()
          if possiblePlaces:
               for place in possiblePlaces:
                    self.ids[f'{place[0]}{place[1]}'].font_size = 15
                    self.ids[f'{place[0]}{place[1]}'].color = [0, 1, 0, 1]
                    self.ids[f'{place[0]}{place[1]}'].text = '□'

     # FIXME
     def resetFont(self):
          for i in range(8):
               for j in range(8):
                    self.ids[f'{i}{j}'].font_size = 45
                    self.ids[f'{i}{j}'].color = [1, 1, 1, 1]

          # board.put_mine(location)
          # self.dipict_map()
          # # tmp = board.check_canput(int(row), int(col))
          # self.change_number()
          # if board.check_canput_all():
          #      if self.ids.clear_button.text == 'PASSED':
          #           self.ids.clear_button.text = 'CLEAR'
          #           self.ids.clear_button.color = 1, 1, 1, 1
          # else:
          #      self.ids.clear_button.text = 'PASSED'
          #      self.ids.clear_button.color = 1, 0, 0, 1
          #      board.which_turn = '●' if board.which_turn == '◯' else '◯'
          #      if not board.check_canput_all():
          #           self.ids.clear_button.color = 1, 0, 0, 1
          #           winner, num1, num2 = board.winner_judge()
          #           if winner == 'DRAW':
          #                self.ids.clear_button.text = f'DRAW: {num1} - {num2}'
          #           else:
          #                self.ids.clear_button.text = f'{winner} win: {num1} - {num2}'
          # self.change_display_turn()


     
     # Collect all
     def scan_board(self):
          maps = [['' for _ in range(8)] for _ in range(8)]
          for i in range(8):
               for j in range(8):
                    if self.ids[f'{i}{j}'].text != '':
                         maps[i][j] = self.ids[f'{i}{j}'].text
          
     def change_display_turn(self):
          global board
          self.ids.turn_display.text = f"Now, it's {board.which_turn} turn"

     def change_number(self):
          black_count, white_count = board.count()
          self.ids.black_num.text = f'BLACK num{black_count}'
          self.ids.white_num.text = f'WHITE num: {white_count}'

class ReversiApp(App):
     def build(self):
          return MyLayout()


if __name__ == '__main__':
     board = play_reversi.Board()
     hardBoard = play_reversi_hard.Board()
     hardCpu = play_reversi_hard.GreedyPlayer()
     hardPlayer = play_reversi_hard.HumanPlayer()
     ReversiApp().run()
