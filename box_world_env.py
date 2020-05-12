import gym
from gym.spaces.discrete import Discrete
from gym.spaces import Box

import matplotlib.pyplot as plt
from collections import deque

from boxworld_gen import *

class BoxWorld(gym.Env):
    """Boxworld representation
    Args:
      n (int): Size of the field (n x n)
      goal_length (int): Number of keys to collect to solve the level
      num_distractor (int): Number of distractor trajectories
      distractor_length (int): Number of distractor keys in each distractor trajectory
      max_steps (int): Maximum number of env step for a given level
      collect_key (bool): If true, a key is collected immediately when its corresponding lock is opened
      world: an existing level. If None, generates a new level by calling the world_gen() function
    """

    def __init__(self, n, goal_length, num_distractor, distractor_length, max_steps=10**6, collect_key=True, world=None):
        self.goal_length = goal_length
        self.num_distractor = num_distractor
        self.distractor_length = distractor_length
        self.n = n
        self.num_pairs = goal_length - 1 + distractor_length * num_distractor
        self.collect_key = collect_key  # if True, keys are collected immediately when available

        # Penalties and Rewards
        self.step_cost = 0
        self.reward_gem = 10
        self.reward_key = 1
        self.reward_distractor = -1

        # Other Settings
        self.viewer = None
        self.max_steps = max_steps
        self.action_space = Discrete(len(ACTION_LOOKUP))
        self.observation_space = Box(low=0, high=255, shape=(n+2, n+2, 3), dtype=np.uint8)

        # Game initialization
        self.owned_key = [220, 220, 220]

        self.np_random_seed = None
        self.reset(world)

        self.num_env_steps = 0
        self.episode_reward = 0

        self.last_frames = deque(maxlen=3)

    def seed(self, seed=None):
        self.np_random_seed = seed
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
        solved = False

        # Move player if the field in the moving direction is either

        if np.any(new_position < 1) or np.any(new_position >= self.n + 1):
            possible_move = False

        elif is_empty(self.world[new_position[0], new_position[1]]):
            # No key, no lock
            possible_move = True

        elif new_position[1] == 1 or is_empty(self.world[new_position[0], new_position[1] - 1]):
            # It is a key
            if is_empty(self.world[new_position[0], new_position[1] + 1]):
                # Key is not locked
                possible_move = True
                self.owned_key = self.world[new_position[0], new_position[1]].copy()
                self.world[0, 0] = self.owned_key
                if np.array_equal(self.world[new_position[0], new_position[1]], goal_color):
                    # Goal reached
                    self.world[0, 0] = wall_color
                    reward += self.reward_gem
                    solved = True
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

                if self.collect_key:
                    # goal reached
                    if np.array_equal(self.world[new_position[0], new_position[1]-1], goal_color):
                        # Goal reached
                        self.world[new_position[0], new_position[1] - 1] = [220, 220, 220]
                        self.world[0, 0] = wall_color
                        reward += self.reward_gem
                        solved = True
                        done = True

                    else:
                        # loose old key and collect new one
                        self.owned_key = np.copy(self.world[new_position[0], new_position[1] - 1])
                        self.world[new_position[0], new_position[1] - 1] = [220, 220, 220]
                        self.world[0, 0] = self.owned_key
                        if self.world_dic[tuple(new_position)] == 0:
                            reward += self.reward_distractor
                            done = True
                        else:
                            reward += self.reward_key
                else:
                    self.owned_key = [220, 220, 220]
                    self.world[0, 0] = [0, 0, 0]
                    if self.world_dic[tuple(new_position)] == 0:
                        reward += self.reward_distractor
                        done = True
            else:
                possible_move = False
                # print("lock color is {}, but owned key is {}".format(
                #     self.world[new_position[0], new_position[1]], self.owned_key))

        if possible_move:
            self.player_position = new_position
            update_color(self.world, previous_agent_loc=current_position, new_agent_loc=new_position)

        self.episode_reward += reward

        info = {
            "action.name": ACTION_LOOKUP[action],
            "action.moved_player": possible_move,
            "bad_transition": self.max_steps == self.num_env_steps,
        }
        if done:
            info["episode"] = {"r": self.episode_reward,
                               "length": self.num_env_steps,
                               "solved": solved}
        self.last_frames.append(self.world)

        return (self.world - grid_color[0])/255 * 2, reward, done, info

    def reset(self, world=None):
        if world is None:
            self.world, self.player_position, self.world_dic = world_gen(n=self.n, goal_length=self.goal_length,
                                                         num_distractor=self.num_distractor,
                                                         distractor_length=self.distractor_length,
                                                     seed=self.np_random_seed)
        else:
            self.world, self.player_position, self.world_dic = world

        self.num_env_steps = 0
        self.episode_reward = 0
        self.owned_key = [220, 220, 220]

        return (self.world - grid_color[0])/255 * 2

    def render(self, mode="human"):
        img = self.world.astype(np.uint8)
        if mode == "rgb_array":
            return img

        else:
            # from gym.envs.classic_control import rendering
            # if self.viewer is None:
            #     self.viewer = rendering.SimpleImageViewer()
            # self.viewer.imshow(img)
            # return self.viewer.isopen
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
    # import pickle

    # execute only if run as a script
    env = BoxWorld(6, 2, 1, 1)
    env.seed(10)

    # with open('/home/nathan/PycharmProjects/relational_RL_graphs/images/ex_world.pkl', 'rb') as file:

    env.reset()
    env.render()

    env.reset()
    env.render()
    # with open('/home/nathan/PycharmProjects/relational_RL_graphs/images/ex_world.pkl', 'wb') as file:
    #     pickle.dump([env.world, env.player_position, env.world_dic], file)


# TO DO : impossible lvls ? (keys stacked right made inaccessible)
