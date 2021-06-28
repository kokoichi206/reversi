## how to work on other settings?
create and go new directory
?? do on the virtual env ?? 
$pip install pyinstaller
$pip freeze <- what is this>
$pyinstaller cals.py -w 
-w is for windows
dist(file) -> calc -> calc.exe
maybe don't work
have to change calc.spec file
```add first line
from kivy_deps import sdl2, glew
```
```between pyz and exe, add something(path to kv file ..) 
a.datas += [('Code\calc.kv', 'C:\\kivygui\\calc\calc.kv', 'DATA')]
```
change
coll = COLLECT(exe, ....)
to
coll = COLLECT(exe, Tree('C:\\kivygui\\calc\\'),)
AND after a.datas,
a.datas,
*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],

SAVE and RECOMPILE
$pyinstaller calc.spec -y
dist->calc->calc.exe
When share this file, u have to include ALL files


### utils
color:  0,0,0,0 で灰色?
color:  0,0,0,1 で黒色?

r: 0,1,0,1
は、1つめからr,g,bっぽい。
4つめはなんだろう

同じディレクトリに2つ以上のkvファイルがあるとよくわからん動きしてた！
他のファイルのFloatLayoutを勝手に読んだりしてて、ずっと悩んでしも打てた

### はまっていること
idを数字で指定すると、そこがうまく数字で取り出せない
-> convert alphabet letters to number(a-1,b-2,...)
-> これはウソで、ids['00']とかで余裕で取り出せた
num = ord(char) - 97  # -97とすると、aと0が対応
char = chr(num+97)


### button
colorは、文字の色の指定、
ボタンの色は、background_color: [0, 0, 0, 1]などで指定
日本語フォントにするために、同じディレクトリ内にipag.ttfを追加し、
font_name: 'ipag.ttf'と記述


<RootWidget>:
    canvas.before:
        Color:
            rgb: [1, 1, 1]
        Rectangle:
            pos: self.pos
            size: self.size


### memo
    def buttonClicked(self, **args):
        print(self.ids.a.text)
        Clock.schedule_once(partial(self.update,'a'),0)
        
    def update(self, message, *a):
        self.ids.a.text = message
        # if self.ids.aa.text == '◯':
        #     text = '●'



check out the concept of Properties (StringProperty for example) in Kivy. It is more elegant most of the time...


