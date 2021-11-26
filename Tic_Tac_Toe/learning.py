import numpy as np
import main


if __name__ == '__main__':
    # 学習率の写真を作成するかどうか
    make_img = True

    # Q学習の初期設定
    MINUS_INF = -100_000  # q tableのなかで置けないところはこいつで実質つぶす
    LEARNING_RATE = 0.1
    REWARD = 3
    DISCOUNT = 0.95 # 0-1
    EPISODES = 200_000
    SHOW_EVERY = 1000

    epsilon = 0.5
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = EPISODES // 2
    epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

    # 写真等を保存するフォルダ
    OUTPUT_DIR = './'
    FILE_PATH = f'{OUTPUT_DIR}progress_{EPISODES}.txt'

    sentence = f'episode\twin\tlose\tdraw\tepsilon\trate\n'
    with open(FILE_PATH, mode='w') as f:
        f.write(sentence)

    win = 0
    lose = 0
    draw = 0

    # 対戦用の初期設定
    FIRST, SECOND = '◯', '×'
    player_radom = main.Player_random('×')
    player_learning = main.Player_learning(
        turn = '◯', 
        epsilon = epsilon,
        rate = LEARNING_RATE,
        discount = DISCOUNT,
        reward = REWARD,
        table = None
    )
    for episode in range(1, EPISODES):
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
                action, row_index, new_row_index, max_future_q, current_q\
                        = player_learning.q_table_put(board.can_put(), board)
                if board.judge(which_turn) is True:
                        # board.print()
                        win += 1
                        is_judge_draw = False
                        break
            else:
                player_radom.random_put(board.can_put(), board)
                if board.judge(which_turn) is True:
                        # board.print()
                        player_learning.leaning_enemy(row_index, action, new_row_index, max_future_q, current_q)
                        lose += 1
                        is_judge_draw = False
                        break
            which_turn = SECOND if which_turn == FIRST else FIRST
        if is_judge_draw:
            draw += 1

        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            if(player_learning.epsilon - epsilon_decay_value > 0):
                player_learning.set_epsilon(player_learning.epsilon - epsilon_decay_value)

        if episode % SHOW_EVERY == 0:
            board.print()
            # print(player_3.q_table)
            print('win:', win, ' lose:', lose, ' draw:', draw)
            sentence = str(episode) + '\t' + str(win) + '\t' + str(lose)\
                    + '\t' + str(draw) + '\t' + str(player_learning.epsilon)\
                    + '\t' + str(win/SHOW_EVERY) + '\n'
            print('win_rate:' + '{:.2f}'.format(100*win/(SHOW_EVERY)) +'   progress:'+'■'*(episode*10//EPISODES)+'_'*(10-episode*10//EPISODES))
            with open(FILE_PATH, mode='a') as f:
                f.write(sentence)
            win = 0
            lose = 0
            draw = 0

    np.save('./q_table_min.npy', player_learning.q_table)

    num = 0
    for i in range(3**8):
        for j in range(9):
            if player_learning.q_table[i][j] != 0:
                # print('atta')
                num += 1
    print(num)
    np.savetxt(f'{OUTPUT_DIR}q_table.txt', player_learning.q_table)

    if make_img:
        import make_png
        make_png.make_graph(
            csv_file = f"{FILE_PATH}",
            x_axis = "episode",
            y_axis = "rate",
            title = "Learning Curve",
            y_name = "Win Rate (vs Random computer)",
            x_range = [0, 300000],
            y_range = [0, 1],
            output_file = f"{OUTPUT_DIR}progress_{EPISODES}.png",
        )
