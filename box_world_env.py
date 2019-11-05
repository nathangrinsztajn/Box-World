import gym
from gym.utils import seeding
from gym.spaces.discrete import Discrete
from gym.spaces import Box

import numpy as np
import matplotlib.pyplot as plt

from boxworld_gen import *

class boxworld(gym.Env):
    """Boxworld representation
    Args:
      n: specify the size of the field (n x n)
      goal_length
      num_distractor
      distractor_length
      world: an existing world data. If this is given, use this data.
             If None, generate a new data by calling world_gen() function
    """

    def __init__(self, n, goal_length, num_distractor, distractor_length, max_steps=300, world=None):
        self.goal_length = goal_length
        self.num_distractor = num_distractor
        self.distractor_length = distractor_length
        self.n = n
        self.num_pairs = goal_length - 1 + distractor_length * num_distractor

        # Penalties and Rewards
        self.step_cost = 0.1
        self.reward_gem = 10
        self.reward_key = 0

        # Other Settings
        self.viewer = None
        self.max_steps = max_steps
        self.action_space = Discrete(len(ACTION_LOOKUP))
        self.observation_space = Box(low=0, high=255, shape=(n, n, 3), dtype=np.uint8)

        # Game initialization
        self.owned_key = [220, 220, 220]

        self.reset(world)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def save(self):
        np.save('box_world.npy', self.world)

    def step(self, action):

        change = CHANGE_COORDINATES[action]
        new_position = self.player_position + change
        current_position = self.player_position.copy()

        self.num_env_steps += 1

        reward = -self.step_cost
        done = self.num_env_steps == self.max_steps

        # Move player if the field in the moving direction is either

        if np.any(new_position < 0) or np.any(new_position >= self.n):
            possible_move = False

        elif np.array_equal(new_position, [0, 0]):
            possible_move = False

        elif is_empty(self.world[new_position[0], new_position[1]]):
            # No key, no lock
            possible_move = True

        elif new_position[1] == 0 or is_empty(self.world[new_position[0], new_position[1]-1]):
            # It is a key
            if is_empty(self.world[new_position[0], new_position[1]+1]):
                # Key is not locked
                possible_move = True
                self.owned_key = self.world[new_position[0], new_position[1]].copy()
                self.world[0, 0] = self.owned_key
                if np.array_equal(self.world[new_position[0], new_position[1]], goal_color):
                    # Goal reached
                    reward += self.reward_gem
                    done = True
                else:
                    reward += self.reward_key
            else:
                possible_move = False
        else:
            # It is a lock
            if np.array_equal(self.world[new_position[0], new_position[1]], self.owned_key):
                # The lock matches the key
                possible_move = True
            else:
                possible_move = False
                print("lock color is {}, but owned key is {}".format(
                    self.world[new_position[0], new_position[1]], self.owned_key))

        if possible_move:
            self.player_position = new_position
            update_color(self.world, previous_agent_loc=current_position, new_agent_loc=new_position)

        info = {
            "action.name": ACTION_LOOKUP[action],
            "action.moved_player": possible_move,
        }

        return self.world, reward, done, info

    def reset(self, world=None):
        if world is None:
           self.world, self.player_position = world_gen(n=self.n, goal_length=self.goal_length,
                                                         num_distractor=self.num_distractor,
                                                         distractor_length=self.distractor_length)
        else:
            self.world, self.player_position = world

        self.num_env_steps = 0

        return self.world

    def render(self):
        img = self.world.astype(np.uint32)
        plt.imshow(img, vmin=0, vmax=255, interpolation='none')
        plt.show()


    def get_action_lookup(self):
        return ACTION_LOOKUP


ACTION_LOOKUP = {
    0: 'move up',
    1: 'move down',
    2: 'move left',
    3: 'move right',
}
CHANGE_COORDINATES = {
    0: (-1, 0),
    1: (1, 0),
    2: (0, -1),
    3: (0, 1)
}


if __name__ == "__main__":
    # execute only if run as a script
    env = boxworld(12, 3, 2, 1)
    env.render()
