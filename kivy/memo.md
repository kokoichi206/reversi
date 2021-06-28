Kivyアプリケーションの作成は、ルートとしてWidgetインスタンスを1つ持つAppクラスを定義することで行います。その際に、ルートWidgetのcanvasプロパティに描画命令を登録することで、好きなグラフィックスを描画することができます。

Canvasへの描画命令の登録は、addメソッドやwithコマンドで行います。

## こんなファイル関係でやることが多いぽい
├── main.py
├── my.kv

・AnchorLayout : ウィジェットを上下左右と中央に配置。
・BoxLayout : 同サイズのウィジェットを垂直・水平方向に配置。
・FloatLayout : ウィジェットを絶対座標で配置。
・RelativeLayout : ウィジェットを相対座標で配置。
・GridLayout : ウィジェットをグリッド状に配置。
・PageLayout : ウィジェットをページ状に配置。
・ScatterLayout : ウィジェットをRelativeLayoutと同様に配置。マウスによるサイズ変更も可能。
・StackLayout : 個別サイズのウィジェットを垂直・水平方向に配置。

