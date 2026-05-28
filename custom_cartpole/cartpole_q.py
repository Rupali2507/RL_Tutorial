import gymnasium as gym 
import numpy as np
import matplotlib.pyplot as plt
import pickle

gym.register(
    id="CartPole-v1-Rupali",
    entry_point = "cartpole_env:CartPoleEnv",
    max_episode_steps=200,
    reward_threshold=-110.0,
)

def run(is_training = True, render = False):
    env = gym.make('CartPole-v1-Rupali',render_mode='human' if render else None)
    
    pos_space = np.linspace(-2.4,2.4,20) 
    vel_space = np.linspace(-4,4,20) 
    ang_space = np.linspace(-.2095,.2095,20)
    ang_vel_space = np.linspace(-4,4,20)
    
    if is_training:
      q = np.zeros ((len(pos_space)+1,len(vel_space)+1,len(ang_space)+1,len(ang_vel_space)+1,env.action_space.n)) # init a 11x11x11x2
    else:
        f = open('cart_pole.pkl','rb')
        q=pickle.load(f)
        f.close();

    learning_rate_a = 0.1
    discount_factor_g = 0.99

    epsilon = 1 # 1= 100% random actions
    epsilon_decay_rate = 0.001 # epsilon decay rate

    rng = np.random.default_rng() # random number generator

    rewards_per_episodes = []
    
    i=0

    while(True):
    
        state = env.reset()[0]

        state_p = np.clip(
            np.digitize(state[0], pos_space),
            0,
            len(pos_space)
        )

        state_v = np.clip(
            np.digitize(state[1], vel_space),
            0,
            len(vel_space)
        )

        state_a = np.clip(
            np.digitize(state[2], ang_space),
            0,
            len(ang_space)
        )

        state_av = np.clip(
            np.digitize(state[3], ang_vel_space),
            0,
            len(ang_vel_space)
        )


    
        terminated = False

        rewards = 0

        while(not terminated ):
            if is_training and rng.random()<epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q[state_p,state_v,state_a,state_av,:])

            new_state,reward,terminated,_,_ = env.step(action)
            new_state_p = np.clip(
                np.digitize(new_state[0], pos_space),
                0,
                len(pos_space)
            )

            new_state_v = np.clip(
                np.digitize(new_state[1], vel_space),
                0,
                len(vel_space)
            )

            new_state_a = np.clip(
                np.digitize(new_state[2], ang_space),
                0,
                len(ang_space)
            )

            new_state_av = np.clip(
                np.digitize(new_state[3], ang_vel_space),
                0,
                len(ang_vel_space)
            )
            if is_training:
             q[state_p,state_v,state_a,state_av,action] = q[state_p,state_v,state_a,state_av,action] + learning_rate_a * (reward + discount_factor_g * np.max(q[new_state_p,new_state_v,new_state_a,new_state_av,:])-q[state_p,state_v,state_a,state_av,action])

            state =new_state
            state_p=new_state_p
            state_v=new_state_v
            state_a=new_state_a
            state_av=new_state_av

            rewards+=reward
        rewards_per_episodes.append(rewards)
        mean_rewards = np.mean(rewards_per_episodes[len(rewards_per_episodes)-100:])
        
        if is_training and i%100==0:
            print(
                f'Episode: {i} '
                f'Reward: {rewards} '
                f'Epsilon: {epsilon:0.2f} '
                f'Mean Rewards: {mean_rewards:0.1f}'
            )
        if mean_rewards>120:
            break    

        epsilon = max(epsilon-epsilon_decay_rate,0)

        i+=1
    env.close()
    
    # Save q table to file
    if is_training:
        f = open('cart_pole.pkl','wb')
        pickle.dump(q,f)
        f.close();

    mean_rewards = []
    for t in range(i):
        mean_rewards.append(np.mean(rewards_per_episodes[max(0,t-100):(t+1)]))
    plt.figure(figsize=(10,5))
    plt.plot(mean_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Mean Reward")
    plt.title("CartPole Q-Learning Performance")
    plt.grid(True)
    if is_training:
     plt.savefig("cart_pole.png")
    
    plt.close()


if __name__ == '__main__':

    # run(is_training=True,render=False)

    run(is_training=False,render=True)      

