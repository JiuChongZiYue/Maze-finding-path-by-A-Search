import heapq as hp
from Maze import Maze
import random as rd
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import time

node_explored_forward_large_G = 0
node_explored_backward_large_G = 0
node_explored_forward_small_G = 0
node_explored_Adaptive_large_G = 0

def count_total_explored_nodes(a,  b ,   c,  d  ):
    global node_explored_forward_large_G, node_explored_backward_large_G , node_explored_forward_small_G  ,node_explored_Adaptive_large_G
    node_explored_forward_large_G += a
    node_explored_backward_large_G += b
    node_explored_forward_small_G += c
    node_explored_Adaptive_large_G += d
    
    # print (node_explored_forward_large_G, node_explored_backward_large_G , node_explored_forward_small_G  ,node_explored_Adaptive_large_G)






class ANode: 
    
    # It will initialize h value by 
    # 1) if there is a hnew stored in matrix, then f = g + hnwe
    # 2) if there is no hnew stroed in matrix, then f = g + h (mahatton distance)
    # hnew_matrix will initialize all location to -1
    def __init__(self, location, destination, parent, g_cost_to_here, arr, hnew_matrix):
        
        # location is a list [a, b]
        self.location = location
        self.destination = destination
        self.parent = parent 
        self.g_cost_to_here = g_cost_to_here
        
        # the knowledge graph
        self.arr = arr
        
        
        a, b = location
        
        
        if hnew_matrix[a][b] == -1:
            # there is no stored hnew value for this location, we will use manhatton distacne to calculate h
            self.h_heuristic = abs( self.location[0] - self.destination[0]) + abs( self.location[1] - self.destination[1])
        else: 
            # the value of this location in hnew matrix is stored, we will use hnew to conpute f
            self.h_heuristic = hnew_matrix[a][b]
            
        # self.h_heuristic = abs( self.location[0] - self.destination[0]) + abs( self.location[1] - self.destination[1])
        
        
        self.f = self.h_heuristic + self.g_cost_to_here
        

        
    
    def __str__(self):
        return (f'================\nlocation: {self.location}\ndestination: {self.destination}\ng_cost: {self.g_cost_to_here}\nh_heur: {self.h_heuristic}\nf: {self.f}\n===============\n')
        # return (f'================\nlocation: {self.location}\ndestination: {self.destination}\nparent: {self.parent}\ng_cost: {self.g_cost_to_here}\nh_heur: {self.h_heuristic}\nf: {self.f}\n===============\n')

    def __lt__(self, other):
        # this is for compare f value between two nodes, in order to use the pirority queue
        if self.f < other.f:
            return True 
        elif self.f >= other.f:
            return False
        elif self.f == other.f:
            if self.g_cost_to_here > self.g_cost_to_here:
                return True
            elif self.g_cost_to_here <= self.g_cost_to_here:
                return False

    
    def __eq__(self, other):
        # this is for checking if a location is already in open or closed list
        
        return self.location == other.location
    
    def check_neighbors(self):
        list_of_neighboer = []
        
        if (self.location[0] - 1 < len(self.arr)   and self.location[0] - 1 >= 0):
            # south is in the boundary
            new_row = self.location[0] - 1
            new_col = self.location[1]
            if (self.arr[new_row][new_col] == 0):
                # south is a new way
                list_of_neighboer.append([new_row, new_col])
                
        
        if (self.location[0] + 1 < len(self.arr)   and self.location[0] + 1 >= 0):
            # north is in the boundary
            new_row = self.location[0] + 1
            new_col = self.location[1]
            if (self.arr[new_row][new_col] == 0):
                # north is a new way
                list_of_neighboer.append([new_row, new_col])
                
        
        if (self.location[1] - 1 < len(self.arr[self.location[0]])   and self.location[1] - 1 >= 0):
            # west is in the boundary
            new_row = self.location[0]
            new_col = self.location[1] - 1
            if (self.arr[new_row][new_col] == 0):
                # west is a new way
                list_of_neighboer.append([new_row, new_col])
                
        if (self.location[1] + 1 < len(self.arr[self.location[0]])   and self.location[0] + 1 >= 0):
            # east is in the boundary
            new_row = self.location[0]
            new_col = self.location[1] + 1
            if (self.arr[new_row][new_col] == 0):
                # east is a new way
                list_of_neighboer.append([new_row, new_col])
        
        return list_of_neighboer
    
    def return_parent_list(self):
        return self.parent
    
    def calculate_new_f(self):
        self.f = self.h_heuristic + self.g_cost_to_here
        
    def calculate_new_parent(self, new_parent_list):
        self.parent = new_parent_list
        






def print_list(lista): 
    for i in lista:
        print (i)
        






def A_star_search_in_Adaptive(arr, start, dest, hnew_matrix):
    
    Starting_Node = ANode(start,dest, [], 0, arr, hnew_matrix)
    
    
    # this two list are list of Node objects, open list is pirority queue
    open_list = []
    closed_list = []
    
    
    hp.heappush(open_list, Starting_Node)

    
    while open_list:
        
        curr = hp.heappop(open_list)
        closed_list.append (curr)
        
       
        if curr.location == dest:
            # we have found the dest, return the path
            # print('we have reach the dest')
            temp_list = curr.parent
            temp_list.append (curr.location)
            
            # print (f'Adaptive: there are {len (closed_list)} Node have been explored')   
            
            
            
            count_total_explored_nodes(  0, 0, 0, len (closed_list))
            
            t = []
            t.append (temp_list)
            t.append (closed_list)

            return t
        

        
        
        for neighbor in curr.check_neighbors():
            # we have found all the reachable neighbor, check if they are already in closed_list. 
            # which means this node is already explored, skip it. 
            

            
            skip_closed_node = False
            for closed_node in closed_list:
                if closed_node.location == neighbor:
                    # neighbor.location == closed_node.location, in other words curr is in the closed list
                    skip_closed_node = True
                    # print ('this neighbor is in closed_list, skip it')
                    break
            if skip_closed_node:
                continue
 
            # set a temp node for later uses

            parent_of_curr = curr.parent
            

            new_parent_list = parent_of_curr.copy()
            new_parent_list.append(curr.location)
            new_g_cost = curr.g_cost_to_here + 1
            temp = ANode(neighbor, dest, new_parent_list, new_g_cost, arr, hnew_matrix)
            
            
            # check if temp is in open list
            is_in_open_list = False
            for open_node in open_list:
                
                if open_node.location == temp.location:
                    is_in_open_list = True
                    # we found the open node in open list, check if the new path is better
                    if temp.f < open_node.f:
                        # change g to better g, and re-calculate f
                        open_node.g_cost_to_here = temp.g_cost_to_here
                        open_node.calculate_new_f()
                        
                        # change the parent path to this node
                        new_parent_list1 = temp.parent
                        open_node.calculate_new_parent(new_parent_list1)
                        
                        # resort the heap because we have change it
                        hp.heapify(open_list)
                        break
                    break
            
            if not is_in_open_list:
                # this neighbor is not in the open list yet, put it in the open list

                hp.heappush(open_list, temp)
                hp.heapify(open_list)
        
        if len(open_list) ==  0:
            # we do not have avilible node in the open list, means there is no path from start to dest
            print ('DOES NNOT exist such path! ')
            # print (curr.parent)
            return None
            
 






















def Adaptive_repeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name, folder_name, hnew_matrix, speed_mode):
    # it will take one more argument compare to repeated_forward
    # the hnew_matrix is the matrix contain hnew value from previous search 
    # the initial value in hnew_matrix is -1, if not than means we have updated before
    
    path_of_movement= []
    
    
    # num_of_expanded_cell = 0
    
    # initializre the known_graph
    known_graph = []
    rows, cols = num_of_grids, num_of_grids
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(0)
        known_graph.append(col)
    
    agent_current_location = start
    

    
    
    # explore the neighbor of the start location 
    
    x = agent_current_location[0]
    y = agent_current_location[1]
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        # the campass direction 
        newx, newy = x + dx, y + dy
        if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
            # Find new blocked area, update the known area
            known_graph [newx][newy] = 1
            
            
    # now do an A* search base on the knowledge for now
    t = A_star_search_in_Adaptive(known_graph, start, dest , hnew_matrix )
    
    if t != None:
        temp_parent_list = t[0]
        closed_list = t[1]
        # here we will check all the elements in the close_list, and use all of them to update the hnew_matrix 

        for close in closed_list:
            a, b = close.location
            
            # by the function: h(s) = g(S_goal) - g(s)
            # which means: hnew = the cost of the the total path - cost of start path to this node. 
            hnew = len(temp_parent_list) - close.g_cost_to_here
            hnew_matrix [a] [b] = hnew
    
    else:
        temp_parent_list = None


    

    if not speed_mode: 
        visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
    

    
    if temp_parent_list == None:
        # A* did not find a path in current known_graph
        print('Adaptive A* search: WE COULD NOT REACH THE TARGET!!!')
        # if folder_name != None:
        if not speed_mode: 
            visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
        return False
        


    while (agent_current_location != dest):
        # we have not yet get to the dest 

        
        # pop an element from the temp_parent_list, try to move to there 
        # if temp_parent_list is None, that means we fail to find a path
        if temp_parent_list == None:
            print('Adaptive A* search: WE COULD NOT REACH THE TARGET!!!')
            # if folder_name != None:
            if not speed_mode: 
                visualize_maze(known_graph, maze_name,  folder_name, temp_parent_list)
            return False
        
        new_location = temp_parent_list.pop(0)
        
        # print(temp_parent_list)
        
        
        
        nextx, nexty = new_location
        # check if the new_location in known_graph is block
        if known_graph[nextx][nexty] == 0: 
            # not blocked move to ther new place
            
            agent_current_location = [nextx, nexty]
            
   
            if path_of_movement == []:
                path_of_movement.append(agent_current_location)
            elif path_of_movement[-1] != agent_current_location:
                path_of_movement.append(agent_current_location)
            
            # explore the new location and update the known_graph
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # the campass direction 
                newx, newy = nextx + dx, nexty + dy
                if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
                    # Find new blocked area, update the known area
                    known_graph [newx][newy] = 1
            
            
            # visualize maze after moves alone the path
            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
                


            continue
        else: 
            # we have poped an blocked location, use A* at current place, which is agent_current_location
            # now do an A* search base on the knowledge for now
            
    
            t = A_star_search_in_Adaptive(known_graph, agent_current_location, dest , hnew_matrix )
            
            if t != None:
                temp_parent_list = t[0]
                closed_list = t[1]
                # here we will check all the elements in the close_list, and use all of them to update the hnew_matrix 

                for close in closed_list:
                    a, b = close.location
                    
                    # by the function: h(s) = g(S_goal) - g(s)
                    # which means: hnew = the cost of the the total path - cost of start path to this node. 
                    hnew = len(temp_parent_list) - close.g_cost_to_here
                    hnew_matrix [a] [b] = hnew
            else:
                temp_parent_list = None


    

            
            
            
            
            # t = A_star_search_in_Adaptive(known_graph, start, dest , hnew_matrix )
            # temp_parent_list = t[0]
            # closed_list = t[1]
            # here we will check all the elements in the close_list, and use all of them to update the hnew_matrix 

            # for close in closed_list:
            #     a, b = close.location
                
            #     # by the function: h(s) = g(S_goal) - g(s)
            #     # which means: hnew = the cost of the the total path - cost of start path to this node. 
            #     hnew = len(temp_parent_list) - close.g_cost_to_here
            #     hnew_matrix [a] [b] = hnew
            



                    
            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
    

    
    # we have got to the destination!
    # if folder_name != None:
    if not speed_mode: 
        visualize_maze(known_graph, maze_name,  folder_name, path_of_movement)
    print (f'have found a path by Adaptive A*!!! With {len(path_of_movement)}')
    return path_of_movement
        








































class GNode: 
    
    # this is same as Node, but prefer the smallest f value and smaller g value
    def __init__(self, location, destination, parent, g_cost_to_here, arr):
        # location is a list [a, b]
        self.location = location
        self.destination = destination
        self.parent = parent 
        self.g_cost_to_here = g_cost_to_here
        
        # the knowledge graph
        self.arr = arr
        
        self.h_heuristic = abs( self.location[0] - self.destination[0]) + abs( self.location[1] - self.destination[1])
        
        self.f = self.h_heuristic + self.g_cost_to_here
    
    def __str__(self):
        return (f'================\nlocation: {self.location}\ndestination: {self.destination}\ng_cost: {self.g_cost_to_here}\nh_heur: {self.h_heuristic}\nf: {self.f}\n===============\n')
        
    def __lt__(self, other):
        # this is for compare f value between two nodes, in order to use the pirority queue
        if self.f < other.f:
            return True 
        elif self.f >= other.f:
            return False
        elif self.f == other.f:
            # if the f value is same, we want to choose the one with smaller g
            # return true if g smaller
            
            if self.g_cost_to_here < self.g_cost_to_here:
                return True
            elif self.g_cost_to_here >= self.g_cost_to_here:
                return False
            

    def __eq__(self, other):
        # this is for checking if a location is already in open or closed list
        
        return self.location == other.location
    
    def check_neighbors(self):
        list_of_neighboer = []
        
        if (self.location[0] - 1 < len(self.arr)   and self.location[0] - 1 >= 0):
            # south is in the boundary
            new_row = self.location[0] - 1
            new_col = self.location[1]
            if (self.arr[new_row][new_col] == 0):
                # south is a new way
                list_of_neighboer.append([new_row, new_col])
                
        
        if (self.location[0] + 1 < len(self.arr)   and self.location[0] + 1 >= 0):
            # north is in the boundary
            new_row = self.location[0] + 1
            new_col = self.location[1]
            if (self.arr[new_row][new_col] == 0):
                # north is a new way
                list_of_neighboer.append([new_row, new_col])
                
        
        if (self.location[1] - 1 < len(self.arr[self.location[0]])   and self.location[1] - 1 >= 0):
            # west is in the boundary
            new_row = self.location[0]
            new_col = self.location[1] - 1
            if (self.arr[new_row][new_col] == 0):
                # west is a new way
                list_of_neighboer.append([new_row, new_col])
                
        if (self.location[1] + 1 < len(self.arr[self.location[0]])   and self.location[0] + 1 >= 0):
            # east is in the boundary
            new_row = self.location[0]
            new_col = self.location[1] + 1
            if (self.arr[new_row][new_col] == 0):
                # east is a new way
                list_of_neighboer.append([new_row, new_col])
        
        return list_of_neighboer
    
    def return_parent_list(self):
        return self.parent
    
    def calculate_new_f(self):
        self.f = self.h_heuristic + self.g_cost_to_here
        
    def calculate_new_parent(self, new_parent_list):
        self.parent = new_parent_list
        


def GA_star_search(arr, start, dest):
    Starting_Node = GNode(start,dest, [], 0, arr)
    
    
    # this two list are list of Node objects, open list is pirority queue
    open_list = []
    closed_list = []
    
    
    hp.heappush(open_list, Starting_Node)
    

    
    while open_list:
        
        curr = hp.heappop(open_list)
        closed_list.append (curr)
        
       
        if curr.location == dest:
            # we have found the dest, return the path

            temp_list = curr.parent
            temp_list.append (curr.location)
            
            # print (f'Small_G: there are {len (closed_list)} Node have been explored')  
            
            
            
            count_total_explored_nodes(0, 0, len (closed_list), 0)   

            return temp_list
        

        
        
        for neighbor in curr.check_neighbors():
            # we have found all the reachable neighbor, check if they are already in closed_list. 
            # which means this node is already explored, skip it. 
            

            
            skip_closed_node = False
            for closed_node in closed_list:
                if closed_node.location == neighbor:
                    # neighbor.location == closed_node.location, in other words curr is in the closed list
                    skip_closed_node = True

                    break
            if skip_closed_node:
                continue
 
            # set a temp node for later uses

            parent_of_curr = curr.parent
            

            new_parent_list = parent_of_curr.copy()
            new_parent_list.append(curr.location)
            new_g_cost = curr.g_cost_to_here + 1
            temp = GNode(neighbor, dest, new_parent_list, new_g_cost, arr)
            
            
            # check if temp is in open list
            is_in_open_list = False
            for open_node in open_list:
                
                if open_node.location == temp.location:
                    is_in_open_list = True
                    # we found the open node in open list, check if the new path is better
                    if temp.f < open_node.f:
                        # change g to better g, and re-calculate f
                        open_node.g_cost_to_here = temp.g_cost_to_here
                        open_node.calculate_new_f()
                        
                        # change the parent path to this node
                        new_parent_list1 = temp.parent
                        open_node.calculate_new_parent(new_parent_list1)
                        
                        # resort the heap because we have change it
                        hp.heapify(open_list)
                        break
                    break
            
            if not is_in_open_list:
                # this neighbor is not in the open list yet, put it in the open list

                hp.heappush(open_list, temp)
                hp.heapify(open_list)
        
        if len(open_list) ==  0:
            # we do not have avilible node in the open list, means there is no path from start to dest
            print ('DOES NNOT exist such path! ')
            # print (curr.parent)
            return None
        
        

def Grepeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name, folder_name, speed_mode):

    
    path_of_movement= []
    
    # initializre the known_graph
    known_graph = []
    rows, cols = num_of_grids, num_of_grids
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(0)
        known_graph.append(col)
    
    agent_current_location = start
    

    
    
    # explore the neighbor of the start location 
    
    x = agent_current_location[0]
    y = agent_current_location[1]
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        # the campass direction 
        newx, newy = x + dx, y + dy
        if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
            # Find new blocked area, update the known area
            known_graph [newx][newy] = 1
            
            
    # now do an A* search base on the knowledge for now
    temp_parent_list = GA_star_search(known_graph, start, dest)
    
    

    if not speed_mode: 
        visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
    

    

    
    if temp_parent_list == None:
        # A* did not find a path in current known_graph
        print('repeated_search: WE COULD NOT REACH THE TARGET!!!')
        if not speed_mode: 
            visualize_maze(known_graph, maze_name, folder_name,  temp_parent_list)
        return False
        


    while (agent_current_location != dest):
        # we have not yet get to the dest 

        
        # pop an element from the temp_parent_list, try to move to there 
        # if temp_parent_list is None, that means we fail to find a path
        if temp_parent_list == None:
            print('repeated_search: WE COULD NOT REACH THE TARGET!!!')
            if not speed_mode: 
                visualize_maze(known_graph, maze_name,  folder_name, temp_parent_list)
            return False
        
        new_location = temp_parent_list.pop(0)
        
        
        
        nextx, nexty = new_location
        # check if the new_location in known_graph is block
        if known_graph[nextx][nexty] == 0: 
            # not blocked move to ther new place
            
            agent_current_location = [nextx, nexty]
            
   
            if path_of_movement == []:
                path_of_movement.append(agent_current_location)
            elif path_of_movement[-1] != agent_current_location:
                path_of_movement.append(agent_current_location)
            
            # explore the new location and update the known_graph
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # the campass direction 
                newx, newy = nextx + dx, nexty + dy
                if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
                    # Find new blocked area, update the known area
                    known_graph [newx][newy] = 1
            
            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
    

            continue
        else: 
            # we have poped an blocked location, use A* at current place, which is agent_current_location
            
            temp_parent_list = GA_star_search(known_graph, agent_current_location, dest)
            
            
            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
    


    
    
     
    
    # we have got to the destination!
    if not speed_mode: 
        visualize_maze(known_graph, maze_name,  folder_name, path_of_movement)
    print (f'have found a path by repeated forward A*!!! With {len(path_of_movement)}')
    return path_of_movement
        

    

class Node: 
    def __init__(self, location, destination, parent, g_cost_to_here, arr):
        # location is a list [a, b]
        self.location = location
        self.destination = destination
        self.parent = parent 
        self.g_cost_to_here = g_cost_to_here
        
        # the knowledge graph
        self.arr = arr
        
        self.h_heuristic = abs( self.location[0] - self.destination[0]) + abs( self.location[1] - self.destination[1])
        
        self.f = self.h_heuristic + self.g_cost_to_here
    
    def __str__(self):
        return (f'================\nlocation: {self.location}\ndestination: {self.destination}\ng_cost: {self.g_cost_to_here}\nh_heur: {self.h_heuristic}\nf: {self.f}\n===============\n')
        # return (f'================\nlocation: {self.location}\ndestination: {self.destination}\nparent: {self.parent}\ng_cost: {self.g_cost_to_here}\nh_heur: {self.h_heuristic}\nf: {self.f}\n===============\n')

    def __lt__(self, other):
        # this is for compare f value between two nodes, in order to use the pirority queue
        if self.f < other.f:
            return True 
        elif self.f >= other.f:
            return False
        elif self.f == other.f:
            if self.g_cost_to_here > self.g_cost_to_here:
                return True
            elif self.g_cost_to_here <= self.g_cost_to_here:
                return False
            
            
            
            
            
            
            
        
        # return self.f < other.f 
    
    def __eq__(self, other):
        # this is for checking if a location is already in open or closed list
        
        return self.location == other.location
    
    def check_neighbors(self):
        list_of_neighboer = []
        
        if (self.location[0] - 1 < len(self.arr)   and self.location[0] - 1 >= 0):
            # south is in the boundary
            new_row = self.location[0] - 1
            new_col = self.location[1]
            if (self.arr[new_row][new_col] == 0):
                # south is a new way
                list_of_neighboer.append([new_row, new_col])
                
        
        if (self.location[0] + 1 < len(self.arr)   and self.location[0] + 1 >= 0):
            # north is in the boundary
            new_row = self.location[0] + 1
            new_col = self.location[1]
            if (self.arr[new_row][new_col] == 0):
                # north is a new way
                list_of_neighboer.append([new_row, new_col])
                
        
        if (self.location[1] - 1 < len(self.arr[self.location[0]])   and self.location[1] - 1 >= 0):
            # west is in the boundary
            new_row = self.location[0]
            new_col = self.location[1] - 1
            if (self.arr[new_row][new_col] == 0):
                # west is a new way
                list_of_neighboer.append([new_row, new_col])
                
        if (self.location[1] + 1 < len(self.arr[self.location[0]])   and self.location[0] + 1 >= 0):
            # east is in the boundary
            new_row = self.location[0]
            new_col = self.location[1] + 1
            if (self.arr[new_row][new_col] == 0):
                # east is a new way
                list_of_neighboer.append([new_row, new_col])
        
        return list_of_neighboer
    
    def return_parent_list(self):
        return self.parent
    
    def calculate_new_f(self):
        self.f = self.h_heuristic + self.g_cost_to_here
        
    def calculate_new_parent(self, new_parent_list):
        self.parent = new_parent_list
        


def A_star_search(arr, start, dest, Forward=True):
    Starting_Node = Node(start,dest, [], 0, arr)
    
    
    # this two list are list of Node objects, open list is pirority queue
    open_list = []
    closed_list = []
    
    
    hp.heappush(open_list, Starting_Node)

    
    while open_list:
        
        curr = hp.heappop(open_list)
        closed_list.append (curr)
        
       
        if curr.location == dest:
            # we have found the dest, return the path
            # print('we have reach the dest')
            temp_list = curr.parent
            temp_list.append (curr.location)
            
            
            if Forward == True:
                count_total_explored_nodes( len (closed_list), 0, 0, 0)
                # print (f'Forward: there are {len (closed_list)} Node have been explored')   
                
            else:
                count_total_explored_nodes(  0,len (closed_list),  0, 0)
                # print (f'Backword: there are {len (closed_list)} Node have been explored')  

            return temp_list
        

        
        
        for neighbor in curr.check_neighbors():
            # we have found all the reachable neighbor, check if they are already in closed_list. 
            # which means this node is already explored, skip it. 
            

            
            skip_closed_node = False
            for closed_node in closed_list:
                if closed_node.location == neighbor:
                    # neighbor.location == closed_node.location, in other words curr is in the closed list
                    skip_closed_node = True
                    # print ('this neighbor is in closed_list, skip it')
                    break
            if skip_closed_node:
                continue
 
            # set a temp node for later uses

            parent_of_curr = curr.parent
            

            new_parent_list = parent_of_curr.copy()
            new_parent_list.append(curr.location)
            new_g_cost = curr.g_cost_to_here + 1
            temp = Node(neighbor, dest, new_parent_list, new_g_cost, arr)
            
            
            # check if temp is in open list
            is_in_open_list = False
            for open_node in open_list:
                
                if open_node.location == temp.location:
                    is_in_open_list = True
                    # we found the open node in open list, check if the new path is better
                    if temp.f < open_node.f:
                        # change g to better g, and re-calculate f
                        open_node.g_cost_to_here = temp.g_cost_to_here
                        open_node.calculate_new_f()
                        
                        # change the parent path to this node
                        new_parent_list1 = temp.parent
                        open_node.calculate_new_parent(new_parent_list1)
                        
                        # resort the heap because we have change it
                        hp.heapify(open_list)
                        break
                    break
            
            if not is_in_open_list:
                # this neighbor is not in the open list yet, put it in the open list

                hp.heappush(open_list, temp)
                hp.heapify(open_list)
        
        if len(open_list) ==  0:
            # we do not have avilible node in the open list, means there is no path from start to dest
            print ('DOES NNOT exist such path! ')
            # print (curr.parent)
            return None
            
        


def repeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name, folder_name, speed_mode):

    
    path_of_movement= []
    
    # initializre the known_graph
    known_graph = []
    rows, cols = num_of_grids, num_of_grids
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(0)
        known_graph.append(col)
    
    agent_current_location = start
    

    
    
    # explore the neighbor of the start location 
    
    x = agent_current_location[0]
    y = agent_current_location[1]
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        # the campass direction 
        newx, newy = x + dx, y + dy
        if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
            # Find new blocked area, update the known area
            known_graph [newx][newy] = 1
            
            
    # now do an A* search base on the knowledge for now
    temp_parent_list = A_star_search(known_graph, start, dest, True )
    
    

    if not speed_mode: 
        visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
    

    
    if temp_parent_list == None:
        # A* did not find a path in current known_graph
        print('repeated_search: WE COULD NOT REACH THE TARGET!!!')
        if not speed_mode: 
            visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
        return False
        


    while (agent_current_location != dest):
        # we have not yet get to the dest 

        
        # pop an element from the temp_parent_list, try to move to there 
        # if temp_parent_list is None, that means we fail to find a path
        if temp_parent_list == None:
            print('repeated_search: WE COULD NOT REACH THE TARGET!!!')
            if not speed_mode: 
                visualize_maze(known_graph, maze_name,  folder_name, temp_parent_list)
            return False
        
        new_location = temp_parent_list.pop(0)
        
        
        
        nextx, nexty = new_location
        # check if the new_location in known_graph is block
        if known_graph[nextx][nexty] == 0: 
            # not blocked move to ther new place
            
            agent_current_location = [nextx, nexty]
            
   
            if path_of_movement == []:
                path_of_movement.append(agent_current_location)
            elif path_of_movement[-1] != agent_current_location:
                path_of_movement.append(agent_current_location)
            
            # explore the new location and update the known_graph
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # the campass direction 
                newx, newy = nextx + dx, nexty + dy
                if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
                    # Find new blocked area, update the known area
                    known_graph [newx][newy] = 1
                    
                    
            
            # visualize maze after moves alone the path
            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
                


            

            continue
        else: 
            # we have poped an blocked location, use A* at current place, which is agent_current_location
            
            temp_parent_list = A_star_search(known_graph, agent_current_location, dest , True)
            # temp_parent_list = A_star_search(known_graph, start, dest)
            
            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list)
    

    

    
    # we have got to the destination!
    if not speed_mode: 
        visualize_maze(known_graph, maze_name,  folder_name, path_of_movement)
    print (f'have found a path by repeated forward A*!!! With {len(path_of_movement)}')
    return path_of_movement
        


def repeated_backward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name, folder_name , speed_mode):

    
    path_of_movement= []
    
    # initializre the known_graph
    known_graph = []
    rows, cols = num_of_grids, num_of_grids
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(0)
        known_graph.append(col)
    
    agent_current_location = start
    

    
    
    # explore the neighbor of the start location 
    
    x = agent_current_location[0]
    y = agent_current_location[1]
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        # the campass direction 
        newx, newy = x + dx, y + dy
        if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
            # Find new blocked area, update the known area
            known_graph [newx][newy] = 1
            
            
    # now do an A* search base on the knowledge for now
    temp_parent_list_backward = A_star_search(known_graph, dest, start, False)
    
    
    

    if not speed_mode: 
        visualize_maze(known_graph, maze_name, folder_name, temp_parent_list_backward)
    

    
    
    if temp_parent_list_backward == None:
        # A* did not find a path in current known_graph
        print('repeated_search: WE COULD NOT REACH THE TARGET!!!')
        if not speed_mode: 
            visualize_maze(known_graph, maze_name,  folder_name, temp_parent_list_backward)
        return False
        


    while (agent_current_location != dest):
        # we have not yet get to the dest 

        
        # pop an element from the temp_parent_list_backward, try to move to there 
        # if temp_parent_list_backward is None, that means we fail to find a path
        if temp_parent_list_backward == None:
            print('repeated_search: WE COULD NOT REACH THE TARGET!!!')
            if not speed_mode:
                visualize_maze(known_graph, maze_name,  folder_name, temp_parent_list_backward)
            return False
        
        
        # pop (1) will pop the first elemnt in the list, but pop() will pop the last elemetn in the list, which is -1
        new_location = temp_parent_list_backward.pop()
        
        nextx, nexty = new_location
        # check if the new_location in known_graph is block
        if known_graph[nextx][nexty] == 0: 
            # not blocked move to ther new place
            
            agent_current_location = [nextx, nexty]
            
                
            if path_of_movement == []:
                path_of_movement.append(agent_current_location)
            elif path_of_movement[-1] != agent_current_location:
                path_of_movement.append(agent_current_location)
            
            # explore the new location and update the known_graph
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # the campass direction 
                newx, newy = nextx + dx, nexty + dy
                if 0 <= newx < num_of_grids and 0 <= newy < num_of_grids and array_of_maze [newx][newy] == 1:
                    # Find new blocked area, update the known area
                    known_graph [newx][newy] = 1
            
    

            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list_backward)
    


            continue
        else: 
            # we have poped an blocked location, use A* at current place, which is agent_current_location
            
            temp_parent_list_backward = A_star_search(known_graph, dest, agent_current_location, False )
            
                

            if not speed_mode: 
                visualize_maze(known_graph, maze_name, folder_name, temp_parent_list_backward)
        


     
    if not speed_mode:
        visualize_maze(known_graph, maze_name,  folder_name, path_of_movement)
    print (f'have found a path by repeated backward A*!!! With {len(path_of_movement)}')
    return path_of_movement
        
        





def direct_A_star_search(array_of_maze, start, dest, num_of_grids, f=None):

    final_parent_list = A_star_search(array_of_maze, start, dest)
    
    
    new_list = array_of_maze.copy()
    if final_parent_list is not None:
        print ('\ndirect A* search gives path: ')
        print( final_parent_list)
        print()
    else: 
        
        print ('\ndirect A* search gives path: ')
        print( 'DOES NOT EXIST SUCH PATH')
        print()
        
   
            




def visualize_maze(maze, maze_name,  folder_name, path=None):
    num_of_grids = len(maze)
    
    # print(path)
    
    plt.figure(figsize=(10, 10), dpi=80)
    plt.imshow(maze, cmap="gray_r", origin="upper")  # Black = walkable, White = blocked
    plt.xticks(range(num_of_grids))
    plt.yticks(range(num_of_grids))
    plt.grid(True, color='gray', linestyle='-', linewidth=0.1)  # Grid for clarity
    plt.title("Maze Visualization with Path")

    # If a path is provided, plot it in red
    if path:
        path = np.array(path)  # Convert to NumPy array for easier indexing
        plt.plot(path[:, 1], path[:, 0], marker='o', color='red', linewidth=2, markersize=6)


    if folder_name != None: 
        # Save the figure inside 'repeat_forward' folder
        
        save_folder = folder_name
        save_path = os.path.join(save_folder, maze_name)  # Construct the path
        plt.savefig(save_path, dpi=300)  # Save with high resolution
        plt.close()
    else:
        # show for 0.2 seconds, and clost 
        
        # # plt.show(block=False)

        # plt.show()
        # # plt.pause(3)
        # # plt.close()
        
        if maze_name ==  '1':
            # show for 0.2 seconds, and clost 
        
            plt.show(block=False)

           
            plt.pause(1)
            plt.close()
        else: 
            # mannully show it
            plt.show()
                

    
    
    
    
    
    

    
        
def setting_up_environment(num_of_grids):

 
    # num_of_grids

    maze = Maze(num_of_grids, num_of_grids)
    maze.create_maze()
    # maze.print_maze()
    
    array_of_maze = maze.get_maze()

    
    
    start = [rd.randint(0, num_of_grids - 1) for _ in range(2)]
    dest = [rd.randint(0, num_of_grids - 1) for _ in range(2)]
    
    stx, sty = start
    dtx, dty = dest
    
    # make sure the start and dest is not a blocked area
    while array_of_maze [stx][sty] == 1 or array_of_maze[dtx ][dty] == 1:
        
        start = [rd.randint(0, num_of_grids - 1) for _ in range(2)]
        dest = [rd.randint(0, num_of_grids - 1 ) for _ in range(2)]
        stx, sty = start
        dtx, dty = dest
    

    return (num_of_grids, start, dest, array_of_maze)
          



def main1    ():
    # result = setting_up_environment()
    
    # num_of_grids = result[0]
    # start = result[1]
    # dest = result [2]
    # array_of_maze = result[3]
    # maze_name = "luck"
    # folder_name = None
    # hnew_matrix = []
    
    array_of_maze = [
        [ 0, 0, 0, 0, 0],
        [ 0, 1, 1, 1, 0],
        [ 0, 1, 0, 0, 0],
        [ 0, 0, 1, 0, 1],
        [ 0, 0, 1, 0, 0 ],
    ]
    
    num_of_grids = 5
    start = [4,1]
    dest = [ 4,4 ]

    maze_name = "luck"
    folder_name = None
    hnew_matrix = []
    
    # Generate a 10x10 2D array filled with -1
    hnew_matrix = [[-1 for _ in range(num_of_grids)] for _ in range(num_of_grids)]

    t = A_star_search_in_Adaptive (array_of_maze, start, dest, hnew_matrix)

    print (t[0])
    print_list (t[1])
    
    
    a = direct_A_star_search(array_of_maze, start, dest, 5)
    
    # Adaptive_repeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name, hnew_matrix, speed_mode = False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

def main    (): 
    
    # generate 50 maze, store all of them in a result_list
    
    speed_mode = bool(int(input('Would you like to run in Speed_mode?  Anser with 1 or 0, 1 means Speedmode\n')))
    
    
    set_foulder_name = False
    
    
    # if not speed_mode:
    #     set_foulder_name = bool(int(input('Would you like to print output in files store in folders?  Anser with 1 or 0, 1 means \n')))
    
    # else: 
    #     set_foulder_name = False
        

    if speed_mode:
    
        
        result_list= []
        for i in range(50): 
            result = setting_up_environment(101)
            result_list.append(result)
            
            
            
        # 
        i = 0
        if set_foulder_name: 
            folder_name = 'repeated_forward'
        else: 
            folder_name = None
        start_time_1 = time.time()
        for result in result_list:
            # do 50 times repeated forward A and, store the image in a folder
            
            print (i)
            num_of_grids = result[0]
            start = result[1]
            dest = result [2]
            array_of_maze = result[3]
            maze_name = str (i)
            i+=1
            
            repeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name,speed_mode = True)
        end_time_1 = time.time() - start_time_1
            
            
            
            
            
        i = 0
        if set_foulder_name: 
            folder_name = 'repeated_backward'
        else: 
            folder_name = None
        start_time_2 = time.time()
        for result in result_list:
            # do 50 times repeated backward A and, store the image in a folder
            
            print (i)
            num_of_grids = result[0]
            start = result[1]
            dest = result [2]
            array_of_maze = result[3]
            maze_name = str (i)
            i+=1
            
                    
            
            repeated_backward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name, speed_mode = True)
            
        end_time_2 = time.time() - start_time_2

            
            
            
        i = 0
        if set_foulder_name: 
            folder_name = 'Grepeated_forward'
        else: 
            folder_name = None
        start_time_3 = time.time()
        for result in result_list:
            # do 50 times repeated backward A and, store the image in a folder
            # prefer smallest f and larger g
            
            print (i)
            num_of_grids = result[0]
            start = result[1]
            dest = result [2]
            array_of_maze = result[3]
            maze_name = str (i)
            i+=1
            
                    
            
            Grepeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name, speed_mode = True)
            
        end_time_3 = time.time() - start_time_3
        
        
        
        
        
        
        
                
            
        i = 0
        if set_foulder_name: 
            folder_name = 'Adaptive_A'
        else: 
            folder_name = None
        start_time_4 = time.time()
        for result in result_list:
            # do 50 times repeated backward A and, store the image in a folder
            # prefer smallest f and larger g
            
            print (i)
            num_of_grids = result[0]
            start = result[1]
            dest = result [2]
            array_of_maze = result[3]
            maze_name = str (i)
            i+=1
            
            hnew_matrix = []
        
            # Generate a 10x10 2D array filled with -1
            hnew_matrix = [[-1 for _ in range(num_of_grids)] for _ in range(num_of_grids)]

                
            Adaptive_repeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name, hnew_matrix, speed_mode = True)


            
        end_time_4 = time.time() - start_time_4
        
        
        
        
        
        
        
        print (f'repeated_forward: {end_time_1} s, explored {node_explored_forward_large_G} nodes')
        
        
        print (f'repeated_backward: {end_time_2} s, explored {node_explored_backward_large_G} nodes')
        
        print (f'repeated_forward_prefer_small _g: {end_time_3} s, explored {node_explored_forward_small_G} nodes')
        
        
        
        print (f'Adaptive_A* search: {end_time_4} s, explored {node_explored_Adaptive_large_G} nodes')
        
        
    else: 
        
        # generte 1 maze 
        
        num_of_grids = int( input('How large the domo maze need to be?\n')   )
        result = setting_up_environment( num_of_grids    )
        
        num_of_grids = result[0]
        start = result[1]
        dest = result [2]
        array_of_maze = result[3]
        # maze_name = str (i)
        
        mode = int    (  input(' Which serche you would like to demo? Input an int. \n1: repeated forward\n2: repeated backward\n3: prefer small g\n4: Adaptive\n'))
        
        maze_name = input('Do you want to run it Automatically? 1 means Auto, 0 means manual \n')
        
        
        folder_name = None
        
        match mode:
            case 1:
                repeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name,speed_mode = False)
            case 2:
                repeated_backward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name, speed_mode = False)
            case 3:
                Grepeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name, speed_mode = False)
            case 4:
                # Generate a 10x10 2D array filled with -1
                hnew_matrix = []
                hnew_matrix = [[-1 for _ in range(num_of_grids)] for _ in range(num_of_grids)]
                Adaptive_repeated_forward_A_star_search(num_of_grids, start, dest, array_of_maze, maze_name,folder_name, hnew_matrix, speed_mode = False)
            
            


    



if __name__=="__main__":
    main()