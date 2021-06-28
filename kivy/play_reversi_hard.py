import gym
import creversi.gym_reversi
from creversi import *

import os
import datetime
import math
import random
import numpy as np
from collections import namedtuple
from itertools import count
from tqdm import tqdm_notebook as tqdm
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

env = gym.make('Reversi-v0').unwrapped

# if gpu is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

######################################################################
# Replay Memory

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'next_actions', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


######################################################################
# DQN

k = 192
fcl_units = 256
class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(2, k, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(k)
        self.conv2 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(k)
        self.conv3 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(k)
        self.conv4 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(k)
        self.conv5 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm2d(k)
        self.conv6 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn6 = nn.BatchNorm2d(k)
        self.conv7 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn7 = nn.BatchNorm2d(k)
        self.conv8 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn8 = nn.BatchNorm2d(k)
        self.conv9 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn9 = nn.BatchNorm2d(k)
        self.conv10 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn10 = nn.BatchNorm2d(k)
        self.fcl1 = nn.Linear(k * 64, fcl_units)
        self.fcl2 = nn.Linear(fcl_units, 65)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = F.relu(self.bn5(self.conv5(x)))
        x = F.relu(self.bn6(self.conv6(x)))
        x = F.relu(self.bn7(self.conv7(x)))
        x = F.relu(self.bn8(self.conv8(x)))
        x = F.relu(self.bn9(self.conv9(x)))
        x = F.relu(self.bn10(self.conv10(x)))
        x = F.relu(self.fcl1(x.view(-1, k * 64)))
        x = self.fcl2(x)
        return x.tanh() 


def get_state(board):
    features = np.empty((1, 2, 8, 8), dtype=np.float32)
    board.piece_planes(features[0])
    state = torch.from_numpy(features[:1]).to(device)
    return state



#############################################
#############################################

class GreedyPlayer:
    def __init__(self, model_path='model.pt', device=device):
        self.device = device
        self.model = DQN().to(device)
        checkpoint = torch.load(model_path)
        self.model.load_state_dict(checkpoint['state_dict'])
        self.model.eval()
        self.features = np.empty((1, 2, 8, 8), np.float32)

    def go(self, board):
        with torch.no_grad():
            board.piece_planes(self.features[0])
            state = torch.from_numpy(self.features).to(self.device)
            q = self.model(state)
            # 合法手に絞る
            legal_moves = list(board.legal_moves)
            next_actions = torch.tensor([legal_moves], device=self.device, dtype=torch.long)
            legal_q = q.gather(1, next_actions)
            # print(legal_q)
            # print(legal_q.argmax(dim=1).item())
            return legal_moves[legal_q.argmax(dim=1).item()]


class RandomPlayer:
    def go(self, board):
        legal_moves = board.legal_moves
        if len(legal_moves) == 0:
            return PASS
        else:
            return random.choice(list(legal_moves))



RESIGN = -1
QUIT = -2

class HumanPlayer:
    def go(self, board, move_str):
        legal_moves = board.legal_moves
        if len(legal_moves) == 0:
            return PASS
        else:
            while True:
                if move_str == 'resign':
                    return RESIGN
                elif move_str == 'quit':
                    return QUIT
                try:
                    move = move_from_str(move_str)
                except:
                    print('invalid string')
                    continue
                if board.is_legal(move):
                    return move


def main(player1, player2, model1='model.pt', model2=None, games=1, is_display=True):
    if is_display:
        try:
            is_jupyter = get_ipython().__class__.__name__ != 'TerminalInteractiveShell'
            if is_jupyter:
                from IPython.display import SVG, display
        except NameError:
            is_jupyter = False

    players = []
    for player, model in zip([player1, player2], [model1, model2]):
        if player == 'random':
            players.append(RandomPlayer())
        elif player == 'greedy':
            players.append(GreedyPlayer(model, device))
        elif player == 'human':
            players.append(HumanPlayer())
        else:
            raise RuntimeError(f'{player} not found')

    black_won_count = 0
    white_won_count = 0
    draw_count = 0
    board = Board()
    for n in range(games):
        print(f'game {n}')
        board.reset()
        move = None

        i = 0
        while not board.is_game_over():
            i += 1

            # if is_display:
            #     print(f'{i}: ' + ('black' if board.turn == BLACK_TURN else 'white'))
            #     if is_jupyter:
            #         display(SVG(board.to_svg(move)))
            #     else:
            #         print(board)

            if board.puttable_num() == 0:
                move = PASS
            else:
                player = players[(i - 1) % 2]
                move = player.go(board)
                if isinstance(player, HumanPlayer):
                    if move == RESIGN:
                        break
                    elif move == QUIT:
                        return
                assert board.is_legal(move)

            # if is_display:
                # move is a number
                # print(move_to_str(move))
                # print(move)

            board.move(move)


        # if isinstance(player, HumanPlayer) and move == RESIGN:
        #     if board.turn == BLACK_TURN:
        #         print('white won')
        #         white_won_count += 1
        #     else:
        #         print('black won')
        #         black_won_count += 1
        #     continue


        # if is_display:
        #     if is_jupyter:
        #         display(SVG(board.to_svg(move)))
        #     else:
        #         print(board)

        if board.turn == BLACK_TURN:
            piece_nums = [board.piece_num(), board.opponent_piece_num()]
        else:
            piece_nums = [board.opponent_piece_num(), board.piece_num()]

        # print(f'result black={piece_nums[0]} white={piece_nums[1]}')
        # if piece_nums[0] > piece_nums[1]:
        #     print('black won')
        #     black_won_count += 1
        # elif piece_nums[1] > piece_nums[0]:
        #     print('white won')
        #     white_won_count += 1
        # else:
        #     print('draw')
        #     draw_count += 1

    # print(f'black:{black_won_count} white:{white_won_count} draw:{draw_count}')


if __name__ == '__main__':
    main('greedy', 'random', model1='model.pt', games=100)
    # main('greedy', 'human', model1='model.pt')
