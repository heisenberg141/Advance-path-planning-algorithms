"""
Env 2D
@author: huiming zhou
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../")
from Grid_Gen.obstacle_grid1 import obstacle_grid_generator

class Env:
    def __init__(self):
        self.x_range = 128  # size of background
        self.y_range = 128
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
        # self.motions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        occupancy = 39
        self.generator = obstacle_grid_generator(self.x_range, occupancy)
        self.generator.place_obstacles()
        
        self.obs = self.obs_map()

        

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """
        # self.generator.place_obstacles()
        x = self.x_range
        y = self.y_range
        obs = set()

        for i in range(x):
            obs.add((i, 0))
        for i in range(x):
            obs.add((i, y - 1))

        for i in range(y):
            obs.add((0, i))
        for i in range(y):
            obs.add((x - 1, i))

        # for i in range(10, 21):
        #     obs.add((i, 15))
        # for i in range(15):
        #     obs.add((20, i))

        # for i in range(15, 30):
        #     obs.add((30, i))
        # for i in range(16):
        #     obs.add((40, i))
        obs.update(self.generator.coords_covered)
        # obs = self.generator.coords_covered
        # # print(obs)
        

        return obs
