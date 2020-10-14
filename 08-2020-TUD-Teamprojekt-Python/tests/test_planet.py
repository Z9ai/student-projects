#!/usr/bin/env python3

import unittest
import copy
from planet import Direction, Planet


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """
        # Initialize your data structure here
        self.planet = Planet()
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    @unittest.skip('Example test, should not count in final test results')
    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))











class TestRoboLabPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """

        # planetS
        self.planetS = Planet()
        self.planetS.add_path(((2, 0), Direction.NORTH), ((1, 1), Direction.EAST), 1) #5
        self.planetS.add_path(((2, 0), Direction.WEST), ((1, 0), Direction.EAST), 2)  #6
        self.planetS.add_path(((1, 0), Direction.NORTH), ((1, 1), Direction.SOUTH), 1) #7


        # planetGromit
        self.planetGromit = Planet()
        self.planetGromit.add_path(((-2, -1), Direction.EAST), ((-1, -1), Direction.WEST), 6)  #1
        self.planetGromit.add_path(((-1, -1), Direction.EAST), ((1, -1), Direction.WEST), 4)  #2
        self.planetGromit.add_path(((-2, 0), Direction.NORTH), ((-1, 1), Direction.WEST), 7)  #3
        self.planetGromit.add_path(((1, -1), Direction.EAST), ((2, 0), Direction.SOUTH), 1)  #4
        self.planetGromit.add_path(((2, 0), Direction.NORTH), ((1, 1), Direction.EAST), 0)  #5
        self.planetGromit.add_path(((1, 0), Direction.EAST), ((2, 0), Direction.WEST), 5)  #6
        self.planetGromit.add_path(((1, 0), Direction.NORTH), ((1, 1), Direction.SOUTH), 1) #7
        self.planetGromit.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 23)  #8
        self.planetGromit.add_path(((0, 0), Direction.NORTH), ((1, 1), Direction.WEST), 1) #9
        self.planetGromit.add_path(((-1, 0), Direction.EAST), ((0, 0), Direction.WEST), 1)  #10
        self.planetGromit.add_path(((-1, 0), Direction.NORTH), ((-1, 1), Direction.SOUTH), 7) #11
        self.planetGromit.add_path(((-2, 0), Direction.EAST), ((-1, 0), Direction.WEST), 2)  #12
        self.planetGromit.add_path(((-1, 1), Direction.NORTH), ((-1, 1), Direction.EAST), 3) #13


        # planetGromitOutside
        self.planetGromitOutside = Planet()
        self.planetGromitOutside.map = copy.deepcopy(self.planetGromit.map)        # map from planetGromit is copied
        self.planetGromitOutside.add_path(((-3, 0), Direction.NORTH), ((-3, 1), Direction.SOUTH), 3)  #14


        # planetGromitSameLength
        self.planetGromitSameLength = Planet()
        self.planetGromitSameLength.map = copy.deepcopy(self.planetGromit.map)       # map from planetGromit is copied
        self.planetGromitSameLength.add_path(((2, 0), Direction.NORTH), ((1, 1), Direction.EAST), 6)  #5     #Path #5 is replaced by a new Path #5


        # planetGromitLoop
        self.planetGromitLoop = Planet()
        self.planetGromitLoop.add_path(((-2, -1), Direction.EAST), ((-1, -1), Direction.WEST), 6)  # 1
        self.planetGromitLoop.add_path(((-1, -1), Direction.EAST), ((1, -1), Direction.WEST), 4)  # 2
        self.planetGromitLoop.add_path(((-2, 0), Direction.NORTH), ((-1, 1), Direction.WEST), 7)  # 3
        self.planetGromitLoop.add_path(((1, -1), Direction.EAST), ((2, 0), Direction.SOUTH), 1)  # 4
        self.planetGromitLoop.add_path(((2, 0), Direction.NORTH), ((1, 1), Direction.EAST), 0)  # 5
        self.planetGromitLoop.add_path(((1, 0), Direction.EAST), ((2, 0), Direction.WEST), 5)  # 6
        self.planetGromitLoop.add_path(((1, 0), Direction.NORTH), ((1, 1), Direction.SOUTH), 8)  # 7
        self.planetGromitLoop.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 0)  #8
        self.planetGromitLoop.add_path(((-1, 1), Direction.EAST), ((1, 1), Direction.WEST), 1)  #15
        self.planetGromitLoop.add_path(((-1, 0), Direction.EAST), ((0, 0), Direction.WEST), 0)  #10
        self.planetGromitLoop.add_path(((-1, 0), Direction.NORTH), ((-1, 1), Direction.SOUTH), 1)  #11
        self.planetGromitLoop.add_path(((-2, 0), Direction.EAST), ((-1, 0), Direction.WEST), 2)  # 12
        self.planetGromitLoop.add_path(((-1, 1), Direction.NORTH), ((-1, 1), Direction.EAST), 0)  #13


        # planetGromitOutsideLoop
        self.planetGromitOutsideLoop = Planet()
        self.planetGromitOutsideLoop.map = copy.deepcopy(self.planetGromitLoop.map)  # map from planetGromitLoop is copied
        self.planetGromitOutsideLoop.add_path(((-3, 0), Direction.NORTH), ((-3, 1), Direction.SOUTH), 3)  #14


    def test_integrity(self): # planetS
        """
        This test should check that the dictionary returned by "planet.get_paths()" matches the expected structure
        """

        print("\n\n1. test_integrity (planetS) ############################################################################")

        mapExpectedS = {
            (2, 0): {Direction.NORTH: ((1, 1), Direction.EAST,1), Direction.WEST: ((1, 0),Direction.EAST, 2)},
            (1, 0): {Direction.EAST: ((2, 0), Direction.WEST,2), Direction.NORTH: ((1, 1),Direction.SOUTH, 1)},
            (1, 1): {Direction.SOUTH: ((1, 0), Direction.NORTH,1), Direction.EAST: ((2, 0),Direction.NORTH,1)}
            }

        self.assertEqual(mapExpectedS, self.planetS.get_paths())

        print("\ntest_integrity finished ############################################################################\n\n")



    def test_empty_planet(self):
        """
        This test should check that an empty planet really is empty
        """

        print("\n\n2. test_empty_planet (empty Planet) ############################################################################")

        planetEmpty = Planet()
        mapExpected = {}

        self.assertEqual(mapExpected, planetEmpty.get_paths())

        print("\ntest_empty_planet finished ############################################################################\n\n")


    def test_target_two_nodes(self): # planetS

        """
        This test should check that the shortest-path algorithm implemented works.

        Requirement: Maximimum distance is two nodes (one paths in list returned)
        """

        print("\n\n3. test_target_two_nodes (planetS) ############################################################################")

        shortestPath = self.planetS.shortest_path((2,0),(1,1))
        pathExpectedS = [((2,0),Direction.NORTH)]

        self.assertEqual(pathExpectedS, shortestPath)

        print("\ntest_target_two_nodes finished ############################################################################\n\n")


    def test_target(self): # planetGromit

        """
        This test should check that the shortest-path algorithm implemented works.

        Requirement: Minimum distance is three nodes (two paths in list returned)
        """

        print("\n\n4. test_target (planetGromit) ############################################################################")

        shortestPath = self.planetGromit.shortest_path((-2, -1), (-2, 0))
        pathExpected = [
            ((-2, -1), Direction.EAST),((-1,-1),Direction.EAST),((1,-1),Direction.EAST),((2,0),Direction.NORTH),
            ((1,1),Direction.WEST),((0,0),Direction.WEST),((-1,0),Direction.WEST)
            ]

        self.assertEqual(pathExpected, shortestPath)

        print("\ntest_target finished ############################################################################\n\n")


    def test_target_not_reachable(self): # planetGromitOutside
        """
        This test should check that a target outside the map or at an unexplored node is not reachable
        """

        print("\n\n5. test_target_not_reachable (planetGromitOutside) ############################################################################")

        shortestPath = self.planetGromitOutside.shortest_path((-2, -1), (-3, 1))
        pathExpected = None

        self.assertEqual(pathExpected, shortestPath)

        print("\ntest_target_not_reachable finished ############################################################################")



    def test_same_length(self): # planetGromitSameLength
        """
        This test should check that the shortest-path algorithm implemented also can return alternative routes with the
        same cost (weight) to a specific target

        Requirement: Minimum of two paths with same cost exists, only one is returned by the logic implemented
        """

        print("\n\n6. test_same_length (planetGromitSameLength) ############################################################################")

        shortestPath = self.planetGromitSameLength.shortest_path((-2, -1), (-2, 0))
        pathExpected = [
            ((-2, -1), Direction.EAST), ((-1, -1), Direction.EAST), ((1, -1), Direction.EAST),
            ((2, 0), Direction.NORTH),
            ((1, 1), Direction.WEST), ((0, 0), Direction.WEST), ((-1, 0), Direction.WEST)
        ]

        self.assertEqual(pathExpected, shortestPath)
        print("\ntest_same_length finished ############################################################################\n\n")

    def test_target_with_loop(self):   # planetGromitLoop
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target nearby

        Result: Target is reachable
        """

        print("\n\n7. test_target_with_loop (planetGromitLoop) ############################################################################")

        shortestPath = self.planetGromitLoop.shortest_path((-2, -1), (-2, 0))
        pathExpected = [
            ((-2, -1), Direction.EAST), ((-1, -1), Direction.EAST), ((1, -1), Direction.EAST),
            ((2, 0), Direction.NORTH),
            ((1, 1), Direction.WEST), ((-1, 1), Direction.SOUTH), ((-1,0),Direction.WEST)
        ]

        self.assertEqual(pathExpected, shortestPath)

        print("\ntest_target_with_loop finished ############################################################################\n\n")





    def test_target_not_reachable_with_loop(self): # planetGromitOutsideLoop
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """

        print("\n\n8. test_target_not_reachable_with_loop (planetGromitOutsideLoop) ############################################################################")

        shortestPath = self.planetGromitOutsideLoop.shortest_path((-2, -1), (-3, 1))
        pathExpected = None

        self.assertEqual(pathExpected, shortestPath)

        print("\ntest_target_not_reachable_with_loop finished ############################################################################")



    def test_unexplored_add_scanned_directions(self):
        print("\n\n9. test_unexplored_add_scanned_directions ############################################################################")

        self.planetE = Planet()
        self.planetE.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 3)
        self.planetE.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 4)


        self.planetE.unexplored = [((1, 3), Direction.NORTH)]
        print("unexplored before function unexplored_add_scanned_directions:")
        print(self.planetE.unexplored)

        current_position = (0,0)
        scanned_directions = [Direction.NORTH, Direction.WEST, Direction.SOUTH]
        self.planetE.unexplored_add_scanned_directions(current_position, scanned_directions)
        print("unexplored after function unexplored_add_scanned_directions:")
        print(self.planetE.unexplored)


        unexplored_expected = [((1, 3), Direction.NORTH), ((0, 0), Direction.WEST), ((0, 0), Direction.SOUTH)]

        self.assertEqual(unexplored_expected, self.planetE.unexplored)
        print("\ntest_unexplored_add_scanned_directions finished ############################################################################")






    def test_exploration(self):

        print("\n\n10. test_exploration ############################################################################")

        self.planetEE = Planet()
        self.planetEE.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 3)
        self.planetEE.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 4)
        self.planetEE.unexplored = [((1, 3), Direction.NORTH), ((0, 0), Direction.WEST), ((0, 0), Direction.SOUTH)]

        current_position = (0,0)
        target_path = self.planetEE.exploration(current_position)
        print(target_path)

        target_path_expected = [((0,0),Direction.SOUTH)]



        self.assertEqual(target_path_expected, target_path)
        print("\ntest_exploration finished ############################################################################")





    def test_exploration_long_path(self):

        print("\n\n10. test_exploration ############################################################################")

        self.planetEEE = Planet()
        self.planetEEE.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 3)
        self.planetEEE.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 4)
        self.planetEEE.add_path(((1, 0), Direction.EAST), ((2, 0), Direction.WEST), 4)
        self.planetEEE.unexplored = [((2, 0), Direction.SOUTH)]

        target_path = self.planetEEE.exploration((0,0))

        target_path_expected = [((0,0),Direction.EAST),((1,0),Direction.EAST),((2,0),Direction.SOUTH)]

        self.assertEqual(target_path_expected, target_path)
        print("\ntest_exploration finished ############################################################################")



    def test_exploration_unexplored_empty(self):
        print("\n\n11. test_exploration_unexplored_empty ############################################################################")

        self.planetF = Planet()
        self.planetF.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 3)
        self.planetF.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 4)
        self.planetF.add_path(((1, 0), Direction.EAST), ((2, 0), Direction.WEST), 4)
        self.planetF.unexplored = []

        target_path = self.planetF.exploration((0, 0))

        self.assertEqual(None, target_path)

        print("\n\ntest_exploration_unexplored_empty finished############################################################################")




    def test_unexplored_add_scanned_directions_node_not_in_map(self):
        print("\n\n12. unexplored_add_scanned_directions_node_not_in_map ###########################")

        self.planetR = Planet()
        self.planetR.unexplored = []

        self.planetR.unexplored_add_scanned_directions((0, 0), (Direction.NORTH, Direction.WEST))

        map = self.planetR.map

        self.assertEqual({(0, 0): {}}, map)
        print(self.planetR.unexplored)

        print("\n\nunexplored_add_scanned_directions_node_not_in_map   finished   #########################################")




if __name__ == "__main__":
    unittest.main()
