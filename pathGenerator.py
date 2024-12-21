import sys
from random import randint

class Environment:
    def __init__(self):
        self.env = None
        self.goal_flag = False
        self.goal_pos = None
        self.directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinal directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonals
        ]

    def create_environment(self, rows, cols, obs):
        """
        Initialize the environment with dimensions (rows x cols) and randomly place obstacles.
        """
        if obs > rows * cols:
            raise ValueError("Number of obstacles cannot exceed the total number of cells.")
        if rows <= 0 or cols <= 0:
            raise ValueError("Environment dimensions must be positive.")

        # Initialize empty environment
        self.env = [[0 for _ in range(cols)] for _ in range(rows)]
        self.add_boundaries()
        self.add_obstacles(obs)

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
        """
        while obs > 0:
            x, y = randint(1, len(self.env) - 2), randint(1, len(self.env[0]) - 2)
            if self.env[x][y] == 0:
                self.env[x][y] = 1
                obs -= 1

    def place_goal(self, pos):
        """
        Place a goal (2) in the environment. If a goal already exists, replace it.
        """
        if self.goal_flag:
            self.env[self.goal_pos[0]][self.goal_pos[1]] = 0  # Remove existing goal
        self.goal_pos = pos
        self.env[pos[0]][pos[1]] = 2
        self.goal_flag = True

    def start_wave(self):
        """
        Execute the wavefront algorithm to propagate values from the goal point.
        """
        if not self.goal_flag:
            raise ValueError("Goal not set.")

        wave_value = 2
        self.env[self.goal_pos[0]][self.goal_pos[1]] = wave_value
        queue = [self.goal_pos]

        while queue:
            next_queue = []
            for x, y in queue:
                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(self.env) and 0 <= ny < len(self.env[0]) and self.env[nx][ny] == 0:
                        self.env[nx][ny] = wave_value + 1
                        next_queue.append((nx, ny))
            wave_value += 1
            queue = next_queue

    def get_shortest_path(self, start):
        """
        Compute the shortest path from the start position to the goal.
        """
        if self.env[start[0]][start[1]] in {0, 1}:
            raise ValueError("Invalid start point.")

        path = [start]
        current = start

        while current != self.goal_pos:
            x, y = current
            min_value = float('inf')
            next_step = None

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.env) and 0 <= ny < len(self.env[0]) and self.env[nx][ny] > 1:
                    if self.env[nx][ny] < min_value:
                        min_value = self.env[nx][ny]
                        next_step = (nx, ny)

            if not next_step:
                raise ValueError("No valid path found.")
            path.append(next_step)
            current = next_step

        return path

    def print_environment(self):
        """
        Print the current state of the environment.
        """
        for row in self.env:
            print(" ".join(f"{cell:2}" for cell in row))

if __name__ == "__main__":
    # Create and test the environment
    env = Environment()
    env.create_environment(14, 21, 30)  # 14x21 environment with 30 obstacles
    env.place_goal((2, 18))
    print("Initial Environment:")
    env.print_environment()
    env.start_wave()
    print("\nEnvironment After Wave Propagation:")
    env.print_environment()
    path = env.get_shortest_path((12, 2))  # Example starting point
    print("\nShortest Path from (12, 2) to Goal:")
    print(path)
