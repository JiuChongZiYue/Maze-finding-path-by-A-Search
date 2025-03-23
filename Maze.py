import random as rd

# step of using this Maze Class

# maze = Maze(rows, cols)
# maze.create_maze()
# a = maze.get_maze()

# then we will have an maze with 0 and 1, where 0 means ok to walk, 1 means blocked 



# This is to out the maze

# maze.print_maze()



class Maze: 
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # here gives a n*n array of -1
        self.array = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(-1)
            self.array.append(row)
        
    
    def print_maze(self):
        for i in self.array:
            print (i)
            
    def get_neighbors(self, x, y):
        
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        for change_of_x, change_of_y in directions:
            new_x, new_y = x + change_of_x, y + change_of_y
            # get the for possible direction 
            
            if 0 <= new_x < self.height and 0 <= new_y < self.width:
                # check both not less then 0 or out of boundary 
                
                if self.array[new_x][new_y] == -1:
                    neighbors.append((new_x, new_y))
                    
        return neighbors
            
    
    def get_maze(self):
        return self.array
            
            
    def create_maze(self):
        stack = []
        total_cells = self.width * self.height
        num_already_visited = 0

        # use random to start from a random cell
        x = rd.randint(0, self.height - 1)
        y = rd.randint(0, self.width - 1)
        
        self.array[x][y] = 0
        # 0 means already visited, and empty as a path 
        num_already_visited += 1
        stack.append((x, y))



        while num_already_visited < total_cells:
            if stack:
                curr = stack[-1]
                # check the last thing becasue this is DFS, and we are using stack, FILO
                x = curr[0]
                y = curr[1]
                
                neighbors = self.get_neighbors(x, y)
                # neighbors is a list of tuples
                
                
                
                # print (curr, neighbors)
                
                if neighbors:
                    curr = rd.choice(neighbors)
                    # choose 1 things from the tuple list, call it curr
                    
                    # print (curr)
                    new_x = curr[0]
                    new_y = curr[1]
                    
                    a = rd.random()
                    if a < 0.3:
                        # 0.3 chance to be blocked
                        self.array[new_x][new_y] = 1
                    else:
                        self.array[new_x][new_y] = 0
                        stack.append((new_x, new_y))
                        
                    num_already_visited += 1
                else:
                    # there is no unvisited neighbor of this node, means we are at an dead end
                    # return to the last node and check again
                    stack.pop()
            else:
                # find all the unvistited cell, and choose a random one fromm them
                
                
                
                unvisited = []
                for i in range(self.height):
                    for j in range(self.width):
                        if self.array[i][j] == -1:
                            unvisited.append((i, j))
                                
                                
                if len(unvisited) > 0:
                    x, y = rd.choice(unvisited)
                    self.array[x][y] = 0
                    num_already_visited += 1
                    stack.append((x, y))












# maze = Maze(10, 10)
# maze.create_maze()
# maze.print_maze()

# a = maze.get_maze()

# print (type(a))