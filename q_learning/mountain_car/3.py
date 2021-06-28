import gym 
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle # 辞書をファイルに保存するため、拡張子pickle

def pickle_dump(obj, path):
	with open(path, mode='wb') as f:
		pickle.dump(obj,f)
def pickle_load(path):
	with open(path, mode='rb') as f:
		data = pickle.load(f)
		return data

env = gym.make("MountainCar-v0")
env.reset()


LEARNING_RATE = 0.1
DISCOUNT = 0.95 # 0-1
EPISODES = 250000

SHOW_EVERY = 500

# obsevation_sizeを、discreteなものにしてQテーブルをつくる
# あんまり値は重要ではない？ win はwindouw size
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE


epsilon = 0.5
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // 2
epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}


def get_discrete_state(state):
	discrete_state = (state - env.observation_space.low) / discrete_os_win_size
	return tuple(discrete_state.astype(np.int))

sentence = 'Episode\tavg\tmin\tmax\n'
with open('./episode.txt', mode='a') as f:
	f.write(sentence)

for episode in range(EPISODES):
	episode_reward = 0
	if episode % SHOW_EVERY == 0:
		render = True
	else:
		render = False

	discrete_state = get_discrete_state(env.reset())
	done = False
	while not done:
		# random.random は0ー1の乱数
		if np.random.random() > epsilon:
			action = np.argmax(q_table[discrete_state])
		else:
			action = np.random.randint(0, env.action_space.n)
		new_state, reward, done, _ = env.step(action)
		episode_reward += reward
		new_discrete_state = get_discrete_state(new_state)
		# print(reward, new_state)
		if render:
			env.render()  # What is this?
		if not done:
			max_future_q = np.max(q_table[new_discrete_state])
			current_q = q_table[discrete_state + (action, )]
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
			q_table[discrete_state+(action, )] = new_q
		elif new_state[0] >= env.goal_position:
			# print(f"We made it on episode {episode}")
			q_table[discrete_state + (action, )] = 0 # there is no punishment
	
		discrete_state = new_discrete_state
	
	if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
		epsilon -= epsilon_decay_value

	ep_rewards.append(episode_reward)

	if not episode % SHOW_EVERY:
		average_reward = sum(ep_rewards[-SHOW_EVERY:])/len(ep_rewards[-SHOW_EVERY:])
		aggr_ep_rewards['ep'].append(episode)
		aggr_ep_rewards['avg'].append(average_reward)
		aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
		aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))

		print(f"Episode: {episode} avg: {average_reward} min: {min(ep_rewards[-SHOW_EVERY:])} max: {max(ep_rewards[-SHOW_EVERY:])}")
		pickle_dump(aggr_ep_rewards, './aggr_ep.pickle')
		sentence = str(episode) + '\t' + str(average_reward) + '\t' + str(min(ep_rewards[-SHOW_EVERY:])) + '\t' + str(max(ep_rewards[-SHOW_EVERY:])) + '\n'
		with open('./episode.txt', mode='a') as f:
			f.write(sentence)

env.close()

np.save('q_table.npy', q_table)

plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], Label="avg")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], Label="min")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], Label="max")
plt.legend(loc=4)
# plt.show()
plt.savefig('figure01.pdf')
