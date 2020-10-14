#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import List, Tuple, Dict, Union



@unique
class Direction(IntEnum):
    """ Directions in shortcut """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270



Weight = int
"""
Weight of a given path (received from the server)

Value:  -1 if blocked path
        >0 for all other paths
        never 0
"""


class Planet:
    """
    Contains the representation of the map and provides certain functions to manipulate or extend
    it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None    # data from mothership: robo should find this node
        self.map = {}
        # dictionary example: {(3,4) : {Direction.NORTH : ((1,5), Direction.WEST, 1), Direction.SOUTH : ((6,3), Direction.WEST, 3)}
        #                      (1,7) : {Direction.NORTH : ((4,5), Direction.WEST, 4), Direction.WEST : ((7,3), Direction.EAST, 1)}  }
        # contains information of the whole map
        self.unexplored = []
        # list example: [((0,1), Direction.SOUTH),((0,1),Direction.EAST),((0,1),Direction.NORTH),((2,0),Direction.EAST)]
        # contains information of not yet explored node and its directions
        self.next_unexplored_position = None
        # example: ((2,3), Direction.NORTH)

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it

        Example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """
        startNode = start[0]
        targetNode = target[0]

        startDirection = start[1]
        targetDirection = target[1]

        if startNode not in self.map:
            self.map[startNode] = {}

        if targetNode not in self.map:
            self.map[targetNode] = {}

        self.map[startNode][startDirection] = (targetNode, targetDirection, weight)
        self.map[targetNode][targetDirection] = (startNode, startDirection, weight)

        if (targetNode, targetDirection) in self.unexplored:
            print("removed unexplored", targetNode, targetDirection, self.unexplored)
            self.unexplored.remove((targetNode, targetDirection))
        if (startNode, startDirection) in self.unexplored:
            print("removed unexplored", targetNode, targetDirection, self.unexplored)
            self.unexplored.remove((startNode, startDirection))

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """
        Returns all paths

        Example:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2),
                    Direction.WEST: ((0, 3), Direction.NORTH, 1)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """
        return self.map

    # dijkstra
    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[None, List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes

        Examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: 2-Tuple[List, Direction]
        """


        # self.map
        # dictionary example: {(3,4) : {Direction.NORTH : ((1,5), Direction.WEST, 1), Direction.SOUTH : ((6,3), Direction.WEST, 3)}
        #                      (1,7) : {Direction.NORTH : ((4,5), Direction.WEST, 4), Direction.WEST : ((7,3), Direction.EAST, 1)}  }
        # contains information of the whole map


        # these 3 paths dictionary are data for dijkstra, additionally self.map is used, all 3 dicts share same structure

        pathsOptimized = {}             # example:      {(3,4) : ([(3,3),(5,5),(2,9)],5),   (1,1) : ([(3,3),(5,5)],1)}
                                        # format:       key: end of path,    value:(path without end of path, weight)
        pathsNeigh = {}
        pathsNeighCurrent = {}


        nodeCurrent = ()                 # current node, an optimal path is found for. at the end nodeCurrent should be target.

        # 0. Iteration. initialize

        pathsOptimized = {start: ([], 0)}
        nodeCurrent = start



        # 1. Iteration 2. Iteration 3. Iteration 4. Iteration 5. Iteration ..... until nodeCurrent == target

        while nodeCurrent != target:


            # 1. find and actualize pathsNeighCurrent

            headPathCurrent = pathsOptimized [nodeCurrent][0].copy()    # headPath to nodeCurrent
            weightCurrent = pathsOptimized [nodeCurrent][1]             # weight to nodeCurrent
            directions = self.map[nodeCurrent].copy()                   # directions from nodeCurrent
            headPathCurrent.append(nodeCurrent)  # HeadPath to neigh from nodeCurrent

            for d in directions:

                nodeNeigh = directions [d][0]
                weightNeigh = directions [d][2]

                if nodeNeigh not in pathsOptimized:

                    weightNew = weightCurrent + weightNeigh                             # weight to neigh from nodeCurrent
                    pathsNeighCurrent[nodeNeigh] = (headPathCurrent, weightNew)         # new potential pathNeighCurrent added

            # 2. actualize pathsNeigh

            for t in pathsNeighCurrent:

                headPath = pathsNeighCurrent[t][0].copy()
                weightCompNew = pathsNeighCurrent[t][1]

                if t in pathsNeigh:
                    weightCompOld = pathsNeigh[t][1]
                    if weightCompNew < weightCompOld:
                        pathsNeigh[t] = (headPath, weightCompNew)   # path from temp pathsNeighCurrent is more efficient, path is replaced
                else:
                    pathsNeigh[t] = (headPath, weightCompNew)       # path is added to pathsNeigh

            pathsNeighCurrent = {}

            if pathsNeigh == {}:              # Warning !!!!! Tests are needed !!!!!!! No testing yet!!!!
                return None                   # this return is needed when map is not contiguous

            # 3. best path from pathsNeigh is chosen. best path is path with lowest weight.

            weights = []
            for t in pathsNeigh:
                weights.append(pathsNeigh[t][1])

            nodeCurrent = t  # nodeCurrent for next iteration is chosen
            weightL = min(weights)

            for t in pathsNeigh:

                if pathsNeigh[t][1] == weightL:
                    nodeCurrent = t                          # nodeCurrent for next iteration is chosen
                    break



            # 4. add path with key nodeCurrent to pathsOptimized. delete path with key nodeCurrent from pathsNeigh

            pathsOptimized[nodeCurrent] = pathsNeigh[nodeCurrent]
            pathsNeigh.pop(nodeCurrent)


        print("\npathsOptimized:")
        print(pathsOptimized)
        return self.addDirectionsToPath(target, pathsOptimized)


    def addDirectionsToPath(self, target, pathsOptimized)  ->  List[Tuple[Tuple[int, int], Direction]]:
        """
        general: generate format for return of shortest_path

        for function shortest_path(self, start, target)  optimal dijkstra path is gathered from pathsOptimized with key
        target and Directions are added to this optimal dijkstra path.
        Directions are gathered from map.
        """

        pathOptimized = pathsOptimized[target][0]  # list of Nodes without end node. end node is target node.

        pathOptimized.append(target)                 # list of Nodes with end node.
        length = len(pathOptimized)                  # length of path with end node.

        pathD = []

        for i in range(length-1):                    # for i without target, direction is needed

            node = pathOptimized[i]
            nodeNext = pathOptimized[i+1]

            directions = self.map[node]            # directions is a value from map, each node can have 4 directions in total max
            for d in directions:
                nextNodeMaybe = directions[d][0]
                if nextNodeMaybe == nodeNext:
                    pathD.append((node, d))

        print("\npathD:")
        print(pathD)
        return pathD

    def exploration(self, current_position):
        # format of directionScanned example: [direction.NORTH, direction.SOUTH, direction.WEST]
        # format for current_position only (x,y)
        """
        gets explored directions as parameter and returns direction for future exploration
        manipulates list "unexplored" from self.planet
        """
        if self.unexplored == []:
            return []

        # get last position from unexplored and also delete it from unexplored!!!!!
        # example for next_unexplored_position: ((2,3), Direction.NORTH)
        # (if mothership corrects own position in PATHSELECT or PATH, next_unexplored_position must be put back into last slot of unexplored)
        # that is, why this variable is an object variable
        self.next_unexplored_position = self.unexplored.pop()

        # if no shortest_path needs to be calculated, because next_unexplored is just one step away
        if current_position == self.next_unexplored_position[0]:
            return [self.next_unexplored_position]
        # robot should drive to last next_unexplored_position + one further
        # for example drive from (0,0) to (5,5) + ((5,5),direction.NORTH)
        target_path = self.shortest_path(current_position, self.next_unexplored_position[0]) + [self.next_unexplored_position]
        return target_path

    def unexplored_add_scanned_directions(self, current_position, scanned_directions):

        for direction in scanned_directions:
            #  !!!! if current position is already in map, it must be checked, if direction is also already in map
            if current_position in self.map:
                if direction not in self.map[current_position]:
                    self.unexplored.append((current_position, direction))
                else:
                    pass
            # NEW:!!!!!  if current position is not already in map, current position and direction is put into unexplored
            else:
                self.add_node(current_position)
                self.unexplored.append((current_position, direction))

    def add_node(self, startNode):    # format for startNode:  (x,y)    WITHOUT direction!
        """
         startNode can be added to map
        """
        if startNode not in self.map:
            self.map[startNode] = {}
        else:
            pass
