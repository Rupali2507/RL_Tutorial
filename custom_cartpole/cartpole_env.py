from typing import Optional
import numpy as np
import gymnasium as gym
import pygame 
from gymnasium import spaces
from enum import Enum



class Actions(Enum):
    LEFT = 0
    RIGHT = 1

class CartPoleEnv(gym.Env):
    metadata = {"render_modes":["human","rgb_array"],"render_fps":30}
    def __init__(self, render_mode=None):
        self.render_mode = render_mode
        self.window = None
        self.clock = None
        self.window_size = 512
        # Observation Space of cartpole
        # Cart Position (min= -4.8 and max =4.8)
        # Cart Velocity (min -inf and max = inf)
        # Pole angle (min : ~-0.418 rad(-24) max ~0.418 rad(24))
        # Pole angular velocity (min: -inf , max: inf)

        self.observation_space = gym.spaces.Box(
            low = np.array([-4.8,-np.inf,-0.418,-np.inf],dtype=np.float32),
            high= np.array([4.8, np.inf,0.418,np.inf],dtype=np.float32),
            dtype = np.float32
        )

        # action space
        # 0 : Push Cart to the left
        # 1 : Push Cart to the right
        self.action_space = gym.spaces.Discrete(2)

        ## initial state
        self.state = np.zeros(4,dtype=np.float32)
        

        ## Physical conastant
        self.gravity = 9.8
        self.masscart =1.0
        self.masspole = 0.1

        self.total_mass = self.masscart + self.masspole

        self.length=0.5
        self.force_mag = 10.0 # push stength
        self.tau = 0.02 # simulation timestep
        
        # POle falls if angle exceeds this
        self.theta_threshold_radians = 12* 2 * np.pi/360
        # Cart goes out if position exceeds this
        self.x_threshold = 2.4

    def _get_obs(self):
        """
        Convert internal state to obs format

        Returns : dict : Observation with agent and target posiiton

        """
        return np.array (
            [
                self.cart_position,
                self.cart_velocity,
                self.pole_angle,
                self.pole_angular_velocity,
            ],
            dtype = np.float32,
        )
    
    def _get_info(self):
        """
        Returns:
            dict: Extra information about current state
        """

        return {
            "pole_angle_degrees": np.degrees(self.pole_angle),

            "distance_from_center": abs(self.cart_position),

            "is_pole_balanced":
                abs(self.pole_angle) < 0.05
        }
    
    def reset(self,seed:Optional[int]=None,options=None):
        """
        Starts a new episode

        Args:
            seed: Random seed for reproducible episodes

        Returns:
            tuple: (observation, info) for thr initial state    
        """
        super().reset(seed = seed)

        self.cart_position = self.np_random.uniform(-0.05, 0.05)
        self.cart_velocity = self.np_random.uniform(-0.05, 0.05)
        self.pole_angle = self.np_random.uniform(-0.05, 0.05)
        self.pole_angular_velocity=self.np_random.uniform(-0.05, 0.05)
        observation = self._get_obs()
        info = self._get_info()
        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    def step(self,action):
        """
         Args : The action to take (0-1)
          0 : Push Cart to the left
          1 : Push Cart to the right

         Returns: tuple (observation, reward, terminated,truncated,info)
        """

        force = self.force_mag if action==1 else -self.force_mag

        x = self.cart_position
        x_val = self.cart_velocity

        theta = self.pole_angle
        ang_val = self.pole_angular_velocity

        costheta = np.cos(theta)
        sintheta = np.sin(theta)

        temp = (
            force + self.masspole * self.length * ang_val**2 * sintheta
        )/self.total_mass

        theta_acc = (
            self.gravity * sintheta - costheta * temp
        )/ ( self.length * (
            4.0 / 3.0
            - self.masspole * costheta**2 /self.total_mass
        ))

        x_acc = temp - (
            self.masspole * self.length * theta_acc * costheta
        ) / self.total_mass

        x = x + self.tau * x_val
        x_val = x_val + self.tau * x_acc

        theta = theta + self.tau * ang_val
        ang_val = ang_val + self.tau * theta_acc


        self.cart_position = x
        self.cart_velocity = x_val
        self.pole_angle = theta
        self.pole_angular_velocity=ang_val

        terminated = (
            abs(x)>self.x_threshold
            or
            abs(theta)>self.theta_threshold_radians
        )

        reward = 0 if terminated else 1

        observation = self._get_obs()
        info = self._get_info()

        truncated = False
        if self.render_mode == "human":
            self._render_frame()

        return observation, reward,terminated,truncated,info
    
    def render(self):
        if self.render_mode in ["human", "rgb_array"]:
            return self._render_frame()
        
    def _render_frame(self):

        # Initialize pygame window
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size,self.window_size)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        
        # Crete canvas
        canvas = pygame.Surface((self.window_size,self.window_size))
        canvas.fill((255,255,255))

        # Draw track
        pygame.draw.line(
            canvas,(0,0,0),
            (0,self.window_size//2),
            (self.window_size,self.window_size//2),
            2,
        )

        # Cart Position

        scale = self.window_size / (2* self.x_threshold)

        cart_x = int(
            self.window_size // 2 + self.cart_position * scale
        )
        cart_y = self.window_size // 2

        # Draw cart

        cart_width = 50
        cart_height = 30

        pygame.draw.rect(
            canvas,
            (0,0,255),
            pygame.Rect(
                cart_x - cart_width // 2,
                cart_y - cart_height // 2,
                cart_width,
                cart_height,
            ),
        )

        # Draw Pole

        pole_length = 120

        pole_x = cart_x + pole_length * np.sin(self.pole_angle)
        pole_y = cart_y - pole_length * np.cos(self.pole_angle)

        pygame.draw.line(
            canvas,
            (255,0,0),
            (cart_x,cart_y),
            (pole_x,pole_y),
            6,
        )
        # human rendering
        if self.render_mode == "human":
            # The following line copies our drawings from canvas to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            ) 


    def close(self):
        if self.window is not None:
             pygame.display.quit()
             pygame.quit()


        