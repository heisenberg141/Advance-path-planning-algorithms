"""
Dijkstra 2D
@author: huiming zhou
"""

import os
import sys
import math
import heapq

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../")

from Grid_Gen.obstacle_grid1 import obstacle_grid_generator
from Search_2D import plotting, env

from Search_2D.Astar import AStar


class Dijkstra(AStar):
    """Dijkstra set the cost as the priority 
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

                    # best first set the heuristics as the priority 
                    heapq.heappush(self.OPEN, (new_cost, s_n))

        return self.extract_path(self.PARENT), self.CLOSED


def main():
    counter  = 0
    while(1):
        try:
            s_start = (1, 126)
            s_goal = (126, 1)

            dijkstra = Dijkstra(s_start, s_goal, "euclidean")
            plot = plotting.Plotting(s_start, s_goal,dijkstra.Env)
            path, visited = dijkstra.searching()

            print("PATH FOUND!!!")
            plot.animation(path, visited, "Dijkstra's")  # animation generate
            
            break  
        except: 
            print(f"Path Not Possible... \nTrying Again(try no. {counter}).\n") 
            counter += 1
            if(counter>100):
                print("I couldn't Find a Path. Too Many Obstacles!!!!")
                break
            continue   
    
if __name__ == '__main__':
    main()
