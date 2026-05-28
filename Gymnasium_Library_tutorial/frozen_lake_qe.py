# This file is almost same as frozen_lake_q.py except this uses the frozen_lake_enhanced.py environment.

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

gym.register(
    id = "FrozenLake-enhanced", # give it a unique id
    entry_point = "frozen_lake_enhanced:FrozenLakeEnv", # frozen_lake_enhanced = name of file 'frozen_lake_enhanced.py'
    kwargs={"map_name" : "8x8"},
    max_episode_steps=200,
    reward_threshold=0.85,
)


def run(episodes,isTraining = True,render=False):
    env = gym.make('FrozenLake-enhanced',map_name="8x8",is_slippery=True,render_mode='human' if render else None)

    if (isTraining):
      q = np.zeros((env.observation_space.n,env.action_space.n)) # init a 64x4 array
    else:
        f = open('frozen_lake8x8.pkl','rb')
        q = pickle.load(f)
        f.close()

    learning_rate_a = 0.1
    discount_factor_g = 0.99

    epsilon = 1 # 1= 100% random actions
    epsilon_decay_rate = 0.001 # epsilon decay rate

    rng = np.random.default_rng() # random number generator

    rewards_per_episodes = np.zeros(episodes)

    for i in range(episodes):

        state = env.reset()[0] # states 0 to 63, 0=top left corner, 63 = bottom right corner

        terminated = False # True when fall in hole or reached goal
        truncated = False # True when actions > 200

        steps = 0

        while(not terminated and not truncated):

            if isTraining and rng.random() < epsilon:
                action = env.action_space.sample() # 0=left 1=down 2=right 3=up
            else:
                action = rng.choice(
                    np.flatnonzero(q[state,:] == q[state,:].max())
                )

            new_state,reward,terminated,truncated,_ = env.step(action)

            if isTraining:

                target = reward

                if not terminated:
                    target += discount_factor_g * np.max(q[new_state,:])

                q[state,action] = q[state,action] + learning_rate_a * (
                    target - q[state,action]
                )

            state = new_state

            steps += 1

            if steps > 200:
                break

        epsilon = max(epsilon - epsilon_decay_rate, 0)

        if reward == 1:
            rewards_per_episodes[i] = 1

    env.close()
    plt.close()

    sum_rewards= np.zeros(episodes)

    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episodes[max(0,t-100):(t+1)])

    plt.plot(sum_rewards)
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.title('FrozenLake Q-Learning')
    plt.savefig('frozen_lake8x8_qe.png')
    plt.show()

    if isTraining:
        f=open("frozen_lake8x8.pkl","wb")
        pickle.dump(q,f)
        f.close()

if __name__ == '__main__':

    run(15000,isTraining=True,render=True)
    # run(1,isTraining=False,render=True)