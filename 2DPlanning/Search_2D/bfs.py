"""
Breadth-first Searching_2D (BFS)
@author: huiming zhou
"""

import os
import sys
from collections import deque
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                # "/../../")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../")

# from Grid_Gen.obstacle_grid1 import obstacle_grid_generator

from Search_2D import plotting
from Search_2D.Astar import AStar
import math
import heapq

class BFS(AStar):
    """BFS add the new visited node in the end of the openset
    """
    def searching(self):
        """
        Breadth-first Searching.
        :return: path, visited order
        """

        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN,
                       (0, self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)

            if s == self.s_goal:
                break

            for s_n in self.get_neighbor(s):
                new_cost = self.g[s] + self.cost(s, s_n)

                if s_n not in self.g:
                    self.g[s_n] = math.inf

                if new_cost < self.g[s_n]:  # conditions for updating Cost
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s

                    # bfs, add new node to the end of the openset
                    prior = self.OPEN[-1][0]+1 if len(self.OPEN)>0 else 0
                    heapq.heappush(self.OPEN, (prior, s_n))

        return self.extract_path(self.PARENT), self.CLOSED


def main():
    s_start = (2, 126)
    s_goal = (126, 2)

    bfs = BFS(s_start, s_goal, 'None')
    plot = plotting.Plotting(s_start, s_goal,bfs.Env)

    path, visited = bfs.searching()
    plot.animation(path, visited, "Breadth-first Searching (BFS)")


if __name__ == '__main__':
    main()
