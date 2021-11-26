import numpy as np
import main


if __name__ == '__main__':
    # 試合数
    GAMES = 10000

    # カウント用変数
    win = 0
    lose = 0
    draw = 0

    # 対戦用の初期設定
    FIRST, SECOND = '◯', '×'
    player_radom = main.Player_random('×')
    player_learned = main.Player_using_table(
        turn = '◯'
    )

    for episode in range(1, GAMES):
        # episodeの偶奇で先攻後攻を変えている
        if episode % 2 == 0:
            which_turn = FIRST
        else:
            which_turn = SECOND

        board= main.Board()
        is_judge_draw = True
        while board.can_put():
            if which_turn == FIRST:
                # player_1.random_put(board.can_put(), board)
                action, row_index = player_learned.q_table_put(board.can_put(), board)
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
    print(win, lose, draw)
