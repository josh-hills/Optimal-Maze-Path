import math
import pandas as pd
import numpy as np
import operator

class node:
    def __init__(self, row, col, path_cost, f_value, parent, label):
        self.row = row
        self.col = col
        self.path_cost = path_cost
        self.f_value = f_value
        self.parent = parent
        self.label = label

    def __lt__(self, other):
        if self.f_value == other.f_value:
            return self.path_cost < other.path_cost
        return self.f_value < other.f_value

#input_filepath = './Examples/Example0/input.txt'
input_filepath = "./Examples/Example0/input.txt"
def pathfinding(input_filepath):
    with open(input_filepath) as f:
        maze = f.readlines()

    #turn maze into a 2 dimentional list in form maze[row][col]
    maze = [x.replace(',', '') for x in maze]
    maze = [x.strip() for x in maze]
    # get the dimensions of the maze
    rows = len(maze)
    cols = len(maze[0])
    for row in range(rows):
        str1 = list(maze[row])
        maze[row]=str1

    #replace nodes next to hazards into walls
    for i in range(cols):
        for j in range(rows):
            if maze[j][i] == "H":
                if j-1 >= 0:
                    maze[j-1][i] = "X"
                if j+1 < rows:
                    maze[j+1][i] = "X"
                if i-1 >= 0:
                    maze[j][i-1] = "X"
                if i+1 < cols:
                    maze[j][i+1] = "X"

    # get the start and end state
    for i in range(cols):
        for j in range(rows):
            if maze[j][i] == 'S':
                start_state = node(j, i, 0, 0, "none", "S")
            if maze[j][i] == 'G':
                goal_state = node(j, i, 0, 0, "none", "G")

    #define a heuristic function - finds distance from arbitrary node to goal node
    def heuristic(node):
        a = [node.row, node.col] 
        b= [goal_state.row, goal_state.col]
        node.f_value = 10*sum(abs(val1-val2) for val1, val2 in zip(a,b)) + node.path_cost
    heuristic(start_state)

    #function used to find adjacent nodes to a given node, returns in the form (row, col, label) ex. (1, 3, O)
    def find_adjacent_nodes(graph, node):
        nodes = []
        for i in range(cols):
            for j in range(rows):

                if (graph[j][i] != "X") and (graph[j][i] != "H"):
                    if ((j,i) == (node.row-1, node.col) or (j,i) == (node.row+1, node.col) or (j,i) == (node.row, node.col-1) or (j,i) == (node.row, node.col+1)) and node.label != "H":
                        nodes.append((j,i,graph[j][i]))
        return nodes

    #function used to see if a given node is located in an array, if its not it returns a temp "none" node
    def node_in_array(arr, input_node):
        temp_node = node(-1, -1, -1, -1, "none", "N")
        if not arr:
            return temp_node
        for n in arr:
            if n.row == input_node[0] and n.col == input_node[1]:
                return n
        return temp_node

    #takes the total explored list of nodes and turns into our three output files: explored_list.txt, optimal_path.txt and optimal_path_cost.txt
    def build_outputs(explored):
        explored_list = open("explored_list.txt", "w")
        optimal_path = open("optimal_path.txt", "w")
        optimal_path_cost = open("optimal_path_cost.txt", "w")
        optimal_path.write("[")
        explored_list.write("[")
        for node in explored:
            if node.label != "G":
                explored_list.write("("+str(node.row)+", "+str(node.col)+"), ")
            else:
                explored_list.write("("+str(node.row)+", "+str(node.col)+")]")
        
        path = []
        curr_node = explored[-1]
        curr_label = curr_node.label
        while curr_node != "none":
            path.append(curr_node)
            curr_node = curr_node.parent
        path.reverse()
        for node in path:
            if node.label != "G":
                optimal_path.write("("+str(node.row)+", "+str(node.col)+"), ")
            else:
                optimal_path.write("("+str(node.row)+", "+str(node.col)+")]")

        optimal_path_cost.write(str(len(path)-1))

    #our final a* function, combines previous functions to output the previously stated files
    def a_star(graph, start_state):
        frontier = [start_state]
        heuristic(frontier[0])
        explored = []
        while True:
            if not frontier:
                return False
            leaf = frontier.pop()
            explored.append(leaf)
            if (leaf.label == "G"):
                build_outputs(explored)
                return True
            for n in find_adjacent_nodes(graph, leaf):
                curr_path_cost = leaf.path_cost + 10
                matching_frontier = node_in_array(frontier, n)
                matching_explored = node_in_array(explored, n) 
                if(matching_explored.label == "N" and matching_frontier.label == "N") or (matching_frontier and curr_path_cost < matching_frontier.path_cost or curr_path_cost < matching_explored.path_cost):
                    new_node = node(n[0], n[1], curr_path_cost, 0, leaf, n[2])
                    heuristic(new_node)
                    frontier.append(new_node)
                    frontier.sort(reverse=True)
    if a_star(maze, start_state):
        print("Completed!")
    else:
        print("Failed")

pathfinding(input_filepath)    