import numpy as np
import pickle # 辞書をファイルに保存するため、拡張子pickle

def pickle_dump(obj, path):
	with open(path, mode='wb') as f:
		pickle.dump(obj,f)
def pickle_load(path):
	with open(path, mode='rb') as f:
		data = pickle.load(f)
		return data

q_table = np.random.uniform(low=-2, high=0, size=(20))
tr = np.array(q_table, np.str)
print(tr)
np.save('check.npy', tr)
np.save('check_q.npy', q_table)
print(np.load('check.npy'))

print(pickle_load('./aggr_ep.pickle'))