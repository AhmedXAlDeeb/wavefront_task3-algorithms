import sys
from random import randint
import numpy as np
class Environment:
    """
    This class can be used to generate muliple test cases and multiple senarios of the path planning problem    
    """
    def __init__(self):
        self.rows= 14 #default value
        self.columns = 20
        self.env = None
        self.goal_flag = True
        self.goal_pos = (2,17) #default goal
        self.directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinal directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonals
        ] #For moving 
    def create_defualt_environment(self):
        """
        Initialize the environment with dimensions (rows x cols) and randomly place obstacles.
        """
        map_matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        # Initialize the default map environment
        self.env = map_matrix

    def create_environment(self, rows, cols, obs):
        """
        Initialize the environment with dimensions (rows x cols) and randomly place obstacles.
            Args:
                rows (int): number of rows in zero index
                cols (int): number of cols in zero index
                obss (int): number of obstcales that willl be added in the enviroment


        """
        if obs > rows * cols:
            raise ValueError("Number of obstacles cannot exceed the total number of cells.")
        if rows <= 0 or cols <= 0:
            raise ValueError("Environment dimensions must be positive.")

        # Initialize empty environment
        self.env = [[0 for _ in range(cols)] for _ in range(rows)]
        self.add_boundaries() #fill the boundries with 1
        if obs>0:
            self.add_obstacles(obs) #add the obstcales if needeed 
        
    def find_goal_pos(self):
        for i, row in enumerate(self.env):
            for j, cell in enumerate(row):
                if cell == 2:
                    self.goal_pos = (i, j)
                # Return the position as a tuple (row, column)
                
    def add_boundaries(self):
        """
        Add boundaries (1s) around the environment edges.
        """
        for col in range(len(self.env[0])):
            self.env[0][col] = self.env[-1][col] = 1  # Top and bottom boundaries
        for row in range(len(self.env)):
            self.env[row][0] = self.env[row][-1] = 1  # Left and right boundaries

    def add_obstacles(self, obs):
        """
        Randomly place obstacles (1s) in the environment.
        Args:
            obs (int): number of obstecls to be added in the current enviroment randomly
        """
        while obs > 0:
            x, y = randint(1, len(self.env) - 2), randint(1, len(self.env[0]) - 2) #choosing random position
            if self.env[x][y] == 0: #checking that the position is valid to add obstcle
                self.env[x][y] = 1
                obs -= 1

    def place_goal(self, pos):
        """
        Place a goal (2) in the environment. If a goal already exists, replace it.
            Args: 
            pos (tuple): tuple of two values x and y in the zero index form
        """
        if self.goal_flag: #
            self.env[self.goal_pos[0]][self.goal_pos[1]] = 0  # Remove existing goal
        self.goal_pos = pos
        self.env[pos[0]][pos[1]] = 2
        self.goal_flag = True

    def start_wave(self):
        """
        Execute the wavefront algorithm to propagate values from the goal point.
        """
        if not self.goal_flag:
            #check for the occurance of a goal
            raise ValueError("Goal not set.")

        wave_value = 2
        self.env[self.goal_pos[0]][self.goal_pos[1]] = wave_value #setting the goal position to the value of 2 (Not neccessary but for the convention)
        queue = [self.goal_pos] #start the queue of the cells that need to be visited

        while queue:
            #looping over all the cells until no cell in the Qqueue
            next_queue = [] #the current surrounding cells that need to be visited and not visited before
            for x, y in queue:
                #for each cell in the current queue check the values of the surrounding cells and increment them
                for dx, dy in self.directions:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < len(self.env) and 0 <= new_y < len(self.env[0]) and self.env[new_x][new_y] == 0:
                        self.env[new_x][new_y] = wave_value + 1
                        next_queue.append((new_x, new_y)) #add new cell to the next iteration
            wave_value += 1 #increment the wave value of the next iteration (further from our goal)
            queue = next_queue

    def get_shortest_path(self, start):
        """
        Compute the shortest path from the start position to the goal.
        Args:
            start (tuple): tuple of two values x and y in the zero index form

        """

        path = [start] #initialization of the path starting from the known point
        current = start

        while current != self.goal_pos: #looping till reaching the goal
            
            x, y = current
            min_value = float('inf') #Initializtion of the minmum surounding cell value
            next_step = None

            for dx, dy in self.directions:
                #checking the value of the surrounding cells in the 8 directions
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < len(self.env) and 0 <= new_y < len(self.env[0]) and self.env[new_x][new_y] > 1:
                    if self.env[new_x][new_y] < min_value:
                        #if we found new minimum
                        min_value = self.env[new_x][new_y]
                        next_step = (new_x, new_y)

            if not next_step:
                raise ValueError("No valid path found.")
            path.append(next_step) #add the minimum surrounding cell value to the the path
            current = next_step #moving to the next cell

        return path

    def set_enviroment(self, environment):
        """_summary_

        Args:
            environment (2darray): 2d array that has a goal value setteld and follow the enviroment sturcture
        """
        if isinstance(environment, np.ndarray):
            #if the sent array in nparray
            self.env = environment.tolist()
        else:
            self.env = environment
        self.find_goal_pos() #find the pos of the goal and save it
        
    def print_environment(self):
        """
        Print the current state of the environment.
        """
        for row in self.env:
            print(" ".join(f"{cell:2}" for cell in row))
    def print_path(self, path):
        """
        Print the points of the shortest path to the goal from the current position
        Args:
            path (1darray): 1d array of tuples for the position of each point
        """
        for i, (a, b) in enumerate(path):
            #print the path and increment the position +1 to overcome zero indexing and start from 1
            print(f"{a+1} {b+1}")

    
            
if __name__ == "__main__":
    def planner(map , start_row, start_column):
        new_enviroment = Environment()
        new_enviroment.set_enviroment(map)
        new_enviroment.start_wave()
        shortest_path = new_enviroment.get_shortest_path((start_row-1, start_column-1))
        new_enviroment.print_path(shortest_path)
        value_map = new_enviroment.env
        return [value_map, shortest_path]
        
        
    map_matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    
    planner(map_matrix, 13,2) # the test in the statement
           
    # Create and test the environment module using our class
    # Note that the dimensions are zero indexing
    env = Environment()
    env.create_defualt_environment()  # 14x21 environment with 30 obstacles
    print("Initial Environment:")
    env.print_environment()
    env.start_wave()
    print("\nEnvironment After Wave Propagation:")
    env.print_environment()
    path = env.get_shortest_path((12, 2))  # Example starting point
    print("\nShortest Path from (12, 2) to Goal:")
    env.print_path(path)
