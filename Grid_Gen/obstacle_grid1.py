 
import numpy as np
import cv2
def main():
    GRID_SIZE = 128
    OCCUPANCY = 35 #Percentage
    generator = obstacle_grid_generator(GRID_SIZE,OCCUPANCY)
    generator.place_obstacles()
    # print(generator.grid)
    print(f"Occupancy Verified: {generator.occupancy_check()}%")
    img = generator.grid*255
    scale_percent = 500 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
  
# resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 
    cv2.imshow("map", resized)
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
        pi = np.pi
        self.orientations = np.array([0, pi/2, pi, 3*pi/2])
        

        self.obstacles = {
                            0: np.array( [[1, 0, 1, 1],
                                          [1, 0, 1, 1],
                                          [1, 0, 1, 1],
                                          [1, 0, 1, 1]],dtype=np.uint8),
                            1: np.array( [[1, 0, 0, 1],
                                          [1, 1, 0, 1],
                                          [1, 1, 0, 1],
                                          [1, 1, 1, 1]],dtype=np.uint8),
                            2: np.array( [[1, 0, 1, 1],
                                          [1, 0, 0, 1],
                                          [1, 1, 0, 1],
                                          [1, 1, 1, 1]],dtype=np.uint8),
                            3: np.array( [[1, 1, 0, 1],
                                          [1, 0, 0, 1],
                                          [1, 1, 0, 1],
                                          [1, 1, 1, 1]],dtype=np.uint8)
                            }
        
        
        
        
    

    def place_obstacles(self):
        print("...Suspensful music playing...")
        while not self.occupancy_reached():
            curr_obstacle = np.random.randint(0,4)
            orientation = np.random.randint(0,4)
            
            x = np.random.randint(0,self.grid_size) 
            y = np.random.randint(0,self.grid_size)
            position = tuple([x,y])
            
            # print(position)
            obstacle = self.get_obstacle(curr_obstacle, orientation)

            if self.obstacle_all_clear(obstacle, position):
                self.place(obstacle,position)
            else: 
                continue
            self.currently_occupied +=4
            
    
    def occupancy_reached(self):
        flag = False
        if self.currently_occupied >= self.desired_occupied:
            flag = True
        return flag


    def place(self,obstacle,position):
        x,y = position
        to_place = list()
        for i in range(4):
            for j in range(4):
                if obstacle[i][j] == 0:
                    to_place.append((i,j))
        
        for elem in to_place:
            self.grid[x+elem[0]][y+elem[1]] = 0
       

        


        
    def obstacle_all_clear(self, obstacle, position):
        flag = False
        if self.obstacle_inside(obstacle, position) and self.obstacle_not_coliding(obstacle, position):
            flag = True
        return flag

    def obstacle_inside(self, obstacle, position):
        flag = False
        x,y  = position
        indices = list()
        right_most_obstacle = 0
        bottom_most_obstacle = 0
        for i in range(4):
            for j in range(4):
                if obstacle[i][j] == 0:
                    if j>right_most_obstacle:
                        right_most_obstacle = j
                    if i>bottom_most_obstacle:
                        bottom_most_obstacle = i  
        # print("RM: ",right_most_obstacle + y," BM: ", bottom_most_obstacle + x)

        if (y + right_most_obstacle < self.grid_size) and (x + bottom_most_obstacle < self.grid_size):
            # print("I m here")
            flag = True
        # print(flag)
        return flag

    def obstacle_not_coliding(self, obstacle, position):
        x,y = position
        flag = False
        black_indices = set()
        for i in range(4):
            for j in range(4):
                if obstacle[i][j] == 0:
                    black_indices.add((i+x,j+y))
        
        
        intersection =  black_indices & self.coords_covered
        # print("intersection:" , intersection)
        if len(intersection)==0:
            flag = True
            self.coords_covered |=black_indices
        # print(flag)
        return flag
    
    def get_obstacle(self, current, orientation):
        orig_obstacle = self.obstacles[current]
        # print(f"Angle: {np.rad2deg(self.orientations[orientation])}")
            
        if self.orientations[orientation] !=0:
            R = self.get_rotation_matrix(self.orientations[orientation])
            obstacle = self.rotate_obstacle(orig_obstacle, R)

        else:
            obstacle = orig_obstacle
        
        # print(f"rotating by {np.rad2deg(self.orientations[orientation])} degrees, \n{orig_obstacle} becomes\n{obstacle}")
        # print(obstacle)
        return obstacle
         
        
    def rotate_obstacle(self,obstacle, R):
        indices_original = list()
        indices_rotated = list()
        for i in range (4): 
            for j in range(4):
                indices_original.append((i,j))
                rotated_index = np.matmul(R, np.array([i,j]))
                # print(f"R: {R}\nOriginal: {(i,j)} \nRotated: {(rotated_index[0], rotated_index[1])} \n")
                indices_rotated.append((rotated_index[0],rotated_index[1]))
        
        indices_original = np.array(indices_original)
        indices_rotated = np.array(indices_rotated)
        # print("orig: ",indices_rotated)
        # print(indices_rotated[:,0])
        
        if min(indices_rotated[:,0])<0:
            indices_rotated[:,0]-=min(indices_rotated[:,0])
        if min(indices_rotated[:,1])<0:
            indices_rotated[:,1]-=min(indices_rotated[:,1])
        # for i in range(len (indices_original)):
        #     print(f"{obstacle[tuple(indices_original[i])]}\t{obstacle[tuple(indices_rotated[i])]}")
        # print()
        # print("Modified: ", indices_rotated)
        rotated_obstacle = np.empty_like(obstacle)
        # print(rotated_obstacle)
        for i in range(len(indices_rotated)):
            rotated_obstacle[tuple(indices_original[i])] = obstacle[tuple(indices_rotated[i])]
        # print(rotated_obstacle)
        return rotated_obstacle




        

    def get_rotation_matrix(self, theta):
        R = np.array([[int(np.cos(theta)), -int(np.sin(theta))],
                      [int(np.sin(theta)), int(np.cos(theta))]])
        return R

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