import flappy_bird_gymnasium
import gymnasium as gym

env = gym.make("FlappyBird-v0",render_mode="human",use_lidar=False)

obs,_ = env.reset()

while True :
    action = env.action_space.sample()

    obs,reward,terminated,_,info = env.step(action)
    
    if terminated:
        break

env.close()    