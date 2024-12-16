import sys
from random import randint
# def create_enviroment(x,y,obs):
    
#     '''
#     start an enviroment with y highet and x width
#     return: A matrix X * Y has random places of obsticles 
#         list of lists, if the cell is empty it will be 0 if ot has an obstcle it will be 1
        
#     '''
#     env = [[0 for _ in range(y)] for _ in range(x)]
    
#     env = addObsticle(obs, env)
    
#     return

# def addObsticle(obs,enviroment):
#     env = enviroment
#     while(obs):
#         x = randint(0,len(env[0]))
#         y = randint(0,len(env))
#         if env[x][y] == 1 :
#             pass
#         else:
#             env[x][y] = 1
#             obs-=1
            
#     return env

class enviroument:
    
    def __init__(self):
        self.env = None
        self.goal_flag = False
        self.goal_pos = None
        pass
    def create_environment(self, x, y, obs):
        """
        Create an environment with dimensions (x, y) and randomly place obstacles.

        Parameters:
        - x (int): Width of the environment.
        - y (int): Height of the environment.
        - obs (int): Number of obstacles to place.

        Returns:
        - list of lists: A matrix of size x * y, where 0 indicates an empty cell 
        and 1 indicates a cell with an obstacle.
        """
        if obs > x * y:
            raise ValueError("Number of obstacles cannot exceed the total number of cells in the environment.")
        if x <= 0 or y <= 0:
            raise ValueError("Environment dimensions must be positive.")
        
        # Initialize an empty environment
        environment = [[0 for _ in range(y)] for _ in range(x)]
        self.env = environment
        # Add obstacles
        self.add_obstacles(obs)
        

    def add_obstacles(self, obs):
        """
        Randomly place obstacles in the environment.

        Parameters:
        - obs (int): Number of obstacles to place.
        - environment (list of lists): The current environment matrix.

        Returns:
        - list of lists: Updated environment matrix with obstacles added.
        """
        while obs:
            x = randint(0, len(self.env) - 1)
            y = randint(0, len(self.env[0]) - 1)
            
            if self.env[x][y] == 0:  # Only place an obstacle in an empty cell
                self.env[x][y] = 1
                obs -= 1
        
        return self.env
    
    def place_goal(self, pos):
        if not self.goal_flag:
            self.goal_pos = pos
            self.env[pos[0]][pos[1]] = 2
            self.goal_flag = True
        else:
            print("There is a goal already but we will add new one")
            self.remove_goal()
            self.goal_pos = pos
            self.env[pos[0]][pos[1]] = 2
            self.goal_flag = True
    
    def remove_goal(self):
        if self.goal_flag:
            self.env[self.goal_pos[0]][self.goal_pos[1]] = 0
            self.goal_pos = None
            self.goal_flag = False

        
    # def start_wave(self):
    #     visited = ([self.goal_pos[0],self.goal_pos[1]])
    #     val = 3
    #     while(len(visited)<(len(self.env)*len(self.env[0]))):
    #         cell = visited.pop(0)
    #         neighbours = []
    #         neighbours.append([cell[0]-1, cell[1]]) #left
    #         neighbours.append([cell[0]+1, cell[1]]) #right
    #         neighbours.append([cell[0],cell[0]+1]) #up
    #         neighbours.append([cell[0], cell[0]-1]) #down
    #         neighbours.append([cell[0]+1, cell[1]+1]) #up right
    #         neighbours.append([cell[0]-1, cell[1]+1]) #up left
    #         neighbours.append([cell[0]-1, cell[1]-1]) #down left
    #         neighbours.append([cell[0]+1, cell[1]-1]) #down right
            
    #         for cell in neighbours:
    #             if cell in visited:
    #                 pass
    #             if self.env[cell[0]][cell[1]] == 1:
    #                 pass
    #             if self.env[cell[0]][cell[1]] == 0:
    #                 visited.append(cell)   
    #                 self.env[cell[0]][cell[1]] = val 
            
    #         val += 1 
    #     else:
    #         print("warning there is no gaol")
    
        # Ensure valid goal position
    
    def start_wave(self):
        
        if not self.goal_flag:
            print("Warning: No goal set.")
            return
        
        visited = set()
        visited.add(tuple(self.goal_pos))
        print(visited)
        val = 3
        
        self.env[self.goal_pos[0]][self.goal_pos[1]] = val
        
        directions = [
        (-1, 0),  # left
        (1, 0),   # right
        (0, -1),  # up
        (0, 1),   # down
        (-1, -1), # up-left
        (-1, 1),  # up-right
        (1, -1),  # down-left
        (1, 1)    # down-right
    ]
        
        while 0<len(visited) < (len(self.env) * len(self.env[0])):  # Until all cells are visited
            current_cell = visited.pop()  # Get the first visited cell
            x, y = current_cell  # Unpack the coordinates
            # Explore all 8 neighbours
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Check if the new position is within bounds and not already visited
                if 0 <= nx < len(self.env) and 0 <= ny < len(self.env[0]) and (nx, ny) not in visited:
                    if self.env[nx][ny] == 0:  # Only visit empty cells
                        visited.add((nx, ny))
                        self.env[nx][ny] = val  # Mark the cell with the current wave value

            val += 1  # Increase wave value after each iteration
            print(val)


        
    def print(self):
        for row in self.env:
            print(row)
    
     
        


if __name__ == "__main__":
    env = enviroument()
    env.create_environment(10, 10, 10)
    env.place_goal([3,5])
    env.print()
    env.start_wave()
    env.print()


