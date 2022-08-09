import numpy as np
import cv2
def main():
    GRID_SIZE = 10
    OCCUPANCY = 50 #Percentage
    generator = obstacle_grid_generator(GRID_SIZE,OCCUPANCY)
    generator.place_obstacles()
    # print(generator.grid)
    print(f"Occupancy Verified: {generator.occupancy_check()}%")
    cv2.imshow("map", generator.grid*255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    

class obstacle_grid_generator:
    def __init__(self, grid_size, occupancy):
        self.grid_size = grid_size
        self.occupancy = occupancy
        self.desired_occupied = int((self.grid_size**2) * self.occupancy/100)
        self.currently_occupied = 0
        self.grid = np.ones([grid_size, grid_size], dtype=np.uint8)
        self.coords_covered = set()
        

    def place_obstacles(self):
        while not self.occupancy_reached():
            curr_obstacle = np.random.randint(0,4)
            orientation = np.random.randint(0,3)
            x = np.random.randint(0,self.grid_size) 
            y = np.random.randint(0,self.grid_size)
            position = tuple([x,y])
            
            obstacle = self.get_obstacle(curr_obstacle, orientation)
            if self.obstacle_inside(obstacle,position) and position not in self.coords_covered:
                self.place(obstacle,position)
            else: 
                continue
            self.currently_occupied +=1
            
    
    def occupancy_reached(self):
        flag = False
        if self.currently_occupied >= self.desired_occupied:
            flag = True
        return flag


    def place(self,obstacle,position):
        if position not in self.coords_covered:
            self.grid[position] = 0
        self.coords_covered.add(position)


        

    def obstacle_inside(self, obstacle, position):
        if 0<=position[0]< self.grid_size and 0<=position[1]< self.grid_size:
            return True
    
    def get_obstacle(self,current, orientation):
        return np.array([[0]])
        

    def occupancy_check(self):
        occupied = 0
        
        for row in self.grid:
            for elem in row:
                if elem == 0:
                    occupied+=1
        
        return (occupied/(self.grid_size**2))*100


        # if self.obstacle_outside():

        




if __name__ =='__main__':
    main()