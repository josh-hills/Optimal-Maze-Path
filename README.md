## Table of contents
* [Optimal maze path finder](#optimal-maze-path-finder)
* [Types of nodes](#types-of-nodes)
* [Technologies](#technologies)
* [Setup](#setup)


## Optimal maze path finder
Using A* search find the optimal path from start state S to goal state G, avoid walls and obstacles. Takes in a m x n csv file, see Examples.

## Types of nodes
* S: The start node
* G: The goal node
* O: Empty, traversable nodes
* X: A wall
* H: A hazard, the hazard and any node beside the hazard shouldn't be traversed.

## Technologies
* Python 3.9.9

## Setup
To run this project change the path of input_file to a maze, or leave as is. Then run "Astar Search.py".
