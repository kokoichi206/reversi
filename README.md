# Reversi
- オセロの学習を通じて、いろいろなことを学ばせてもらった
  - オセロ実装
  - pythonにおけるGUI(kiviy)
  - 機械学習(dqnの実装)

## ファイル説明
- cpu_cpu.py
  - cpuとcpuがターミナルで戦うファイル
  - 記録するかと何回対戦するかが選べる
  - `python cpu_cpu.py`
  ![](img/cpu_cpu.png)

- random_main.py
  - ランダムに打ってくるCPUと戦える
  - `python random_main.py`
  ![](img/random_main.png)

- weight_1.py
  - [ある法則](https://uguisu.skr.jp/othello/5-1.html)に従って打ってくるCPUとの戦い
  - ターミナル上
  - `python weight_1.py`

- kivy/reversi.py
  - GUIでコンピュータと戦える
  - ランダム(EASY)かDQNで強くした敵(HARD)か選べる
  - `python ./kivy/reversi.py`
  ![](img/kivy_main.png)


## 強化学習やってみた

### やったこと
- /learning folder. にある
- 10000*4 試合戦わせて強くしてみてる

### ランダムなコンピュータとの戦い
|勝ち|負け|引き分け|
|---|---|---|
|261|36|3|

### 一定の法則に従って打つコンピュータとの比較
[簡単な法則](https://uguisu.skr.jp/othello/5-1.html)に従って打つコンピュータとランダムなものとの戦い

|勝ち|負け|引き分け|
|---|---|---|
|218|70|2|


## その他

### Tic_Tac_Toe
- 英語で三目並べって意味らしい
- 入門で、三目並べで`Q-learning`やってみた
- これくらいまでの状態数なら普通のQ-learningでいける
  - オセロぐらいになると状態数が爆発するので、もうひと工夫必要
    - DQNなど
