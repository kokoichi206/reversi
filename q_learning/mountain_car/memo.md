vip install gym, matplotlib

### 図を表示するGUIがない。。。
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x = [0, 1, 2, 3, 4, 5]
y = [2, 5, 3, 0, 10, 9]

plt.plot(x, y)
plt.savefig('figure01.jpg')

