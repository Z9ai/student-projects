import time
from math import pi
import logging

from ev3dev import ev3

from planet import Direction
from helpers import *

DISCOVER_MODE, TARGET_MODE = range(2)

class Robot:
    """The main class, containing all the modules of the robot"""
    def __init__(self, platform, planet, communication, odometry):
        logging.basicConfig(filename='/home/robot/robot.log', level = logging.DEBUG)
        self.LG = logging.getLogger()
        #roboter modules 
        self.platform = platform
        self.planet = planet
        self.communication = communication
        self.odometry = odometry
        #roboter state
        self.mode = DISCOVER_MODE                         # mode can be explore or search
        self.x = self.y = self.direction = self.target = self.planet_name = None
        self.target_path = []                           # shortest path from dijkstra, for example [((1,0),Direction.WEST),((2,0),Direction.NORTH),((3,0),Direction.NORTH)]
        self.last_position = self.current_position = None #   for example:  ((1,2),Direction.NORTH)
        self.statUnveiled = False                         # True for unveiled path from mothership in current iterrobot.        #TODO unused messages so far
        self.known_nodes = []
        self.entrance_direction = None
        #b.send_testPlanet("")
    
    def wait_for_message(self, min_wait=2, timeout=None):
        print("\tWaiting for a response. {}")
        wait_time = 0
        while True:
            print(".", end="")
            time.sleep(1)
            wait_time += 1
            if timeout and wait_time == timeout or self.communication.has_message() and wait_time >= min_wait:
                break
        if not self.communication.has_message():
            print("NO MESSAGE RECEIVED!!!")
        else:
            print("")
        
    def update_position(self, x, y, angle):
        """sets internal and odometry data as saving the last position
        x,y are given in discrete coordinates, the angle in [0, 90, 180, 270]"""
        self.x, self.y, self.direction = x, y, DIRECTION_MESSAGE_TO_ENUM[angle]
        self.odometry.clear_orientation_data() 
        self.odometry.x, self.odometry.y =  1.0*x*UNIT_SIZE, 1.0*y*UNIT_SIZE
        self.odometry.angle = angle/180.0*pi
        self.odometry.last_direction_enum = DIRECTION_MESSAGE_TO_ENUM[angle]
        self.last_position = self.current_position
        self.current_position = (x, y, DIRECTION_MESSAGE_TO_ENUM[angle])
        
    def finish_exploration(self, message):
        pass

    def initialize(self):
        """0.   start()   // extra function for actions at first node"""
        # walk the first line to the given coordinates
        self.communication.ready()
        self.platform.follow_isolated_line()                            
        self.wait_for_message()
        _, ready_message = self.communication.get_message()
        self.planet_name = ready_message["planetName"]
        # reset the orientation
        self.update_position(
            x=ready_message["startX"], 
            y=ready_message["startY"], 
            angle=ready_message["startOrientation"]
        )
        self.entrance_direction = DIRECTION_TO_OPPOSITE[ready_message["startOrientation"]]

        
    def explore_planet(self):
        """Do the Robolab :)"""
        #0. INIT
        self.initialize()
        #TODO third finsh condition target not reachable and fully explored
        #explore loop
        while True:
            ###########################
            #1. SELECT THE NEXT DIRECTION
            ###########################
            print("\n\n1. SELECT THE NEXT DIRECTION\n ")
            direction_selected = None
            print("IMPORTANT:------------------    current_position: {}, MODE: {}".format(self.current_position, self.mode))
            print("IMPORTANT:------------------    old planet.unexplored: {}".format(self.planet.unexplored))
            if len(self.target_path)!=0: #still a plan where to go next
                print("\narrived at ({}, {}) @ {}. ".format(self.x, self.y, self.direction))
            elif self.mode == DISCOVER_MODE:
                if (self.current_position[0], self.current_position[1]) not in self.known_nodes:
                    available_directions = self.platform.explore_base(self.direction)
                    available_directions.remove(self.entrance_direction)
                    print("???:------------------  {} was scanned!!!!!  the following directions are added: {}".format(self.current_position, available_directions))
                    self.planet.unexplored_add_scanned_directions(
                        current_position=(self.x, self.y), scanned_directions=available_directions
                    )
                    print("???:------------------  scanned directions were added to unexplored, new planet.unexplored: {} .".format(self.planet.unexplored))
                else:
                    self.known_nodes += [(self.current_position[0], self.current_position[1])]
                self.target_path = self.planet.exploration(current_position=(self.x, self.y))
                if not self.target_path:  #planet.unexplored is empty
                    return self.communication.exploration_completed("Planet fully explored")
            
            print("IMPORTANT:------------------    current target_path: {}".format(self.target_path))
            direction_selected = self.target_path.pop(0)[1]
            direction_selected_old = direction_selected
            print("IMPORTANT:------------------    I want to follow the direction_selected: {}".format(direction_selected))

            #################################################################################
            #2. SEND THE PATH SELECT MESSAGE AND CHECK IF CORRECTED PATH SELECT MESSAGE COMES IN
            #################################################################################
            print("\n\n2. SEND THE PATH SELECT MESSAGE AND CHECK IF CORRECTED PATH SELECT MESSAGE COMES IN{}\n")
            self.communication.path_select(
                start_x=self.x, start_y=self.y, 
                start_direction=DIRECTION_ENUM_TO_MESSAGE[direction_selected]
            )
            #self.planet.unexplored.remove((self.x,self.y),DIRECTION_ENUM_TO_MESSAGE[direction_selected])
            self.wait_for_message(timeout=10)
            if self.communication.has_message():
                message_type, message = self.communication.get_message()
                if message_type == "pathSelect":
                    #TODO recalculate path select?
                    direction_selected = message["startDirection"]
                    if self.mode == DISCOVER_MODE:
                        self.planet.unexplored.append(((self.x, self.y), direction_selected_old))
                        try:
                            self.planet.unexplored.remove(((self.x, self.y), direction_selected))
                        except ValueError:
                            pass
                    print("\tComputer says no... I have to follow {}".format( direction_selected))
                else:
                    print("\tUnexpected message {} after path select {}".format(message_type, message))

            ###########
            #3.FOLLOW_THE LINE
            ###########
            print("\n\n3.FOLLOW_THE LINE {}\n")
            # TODO make turn to DIRECTION function
            # robot should drive to directionSelected
            self.turn(direction_selected)
            free_or_blocked = self.platform.follow_isolated_line()


            ##################################################################
            #4. DO ODOMETRY; SEND PATH AND USE CORRECTED POSITION FROM RESPONSE
            ##################################################################
            print("\n\n4. DO ODOMETRY; SEND PATH AND USE CORRECTED POSITION FROM RESPONSE {}\n")
            x_new, y_new, direction_new = self.odometry.update_orientation()
            #print("\tI think I am at", (x_new, y_new, direction_new))
            self.communication.path(
                start_x=self.x, start_y=self.y, start_direction=self.direction, 
                end_x=x_new, end_y=y_new, end_direction=DIRECTION_TO_OPPOSITE[direction_new], path_status= free_or_blocked
            )
            #print("\tWaiting for path message acknowledge")
            self.wait_for_message(timeout=30)
            while self.communication.has_message():
                message_type, message = self.communication.get_message()
                if message_type == "path":
                    x1, y1, end_dir, x0, y0, start_dir, pathStatus, weight = [
                        message[e] for e in ["endX","endY","endDirection","startX","startY","startDirection", "pathStatus", "pathWeight"]
                    ]
                    print("\t!!ACTUAL POSITION BY MOTHERSHIP(CORRECTED)!! {}".format((x1, y1, end_dir)))
                    self.update_position(x1, y1, DIRECTION_TO_OPPOSITE[end_dir])
                    self.planet.add_path(
                        start=((x0, y0), start_dir), target=((x1,y1), end_dir), weight=weight
                    )
                    self.entrance_direction = end_dir
                    try:
                        self.planet.unexplored.remove(((x1,y1),DIRECTION_TO_OPPOSITE[end_dir]))
                    except ValueError:
                        pass
                else:
                    self.handle_messages(message_type, message)

            if self.target and not self.target_path:
                target_reachable = self.planet.shortest_path((self.current_position[0],self.current_position[1]), self.target)
                if target_reachable:
                    self.target_path = target_reachable
            #################################
            #5. AT TARGET?
            #################################
            print("\n\n5. AT TARGET? {}".format(self.target == (self.x, self.y)))
            if self.target == (self.x, self.y):
                return self.communication.target_reached("Target reached")

    def turn(self, direction_selected):
        while self.direction != direction_selected:
            print("to", direction_selected, "is", self.direction)
            self.platform.turn_ticks(FULL_ROTATION_TICKS // 8)
            self.platform.turn_to_color(color=ev3.ColorSensor.COLOR_BLACK)
            _, _, self.platform.direction = self.odometry.update_orientation_centric_turn()
            self.direction = self.platform.direction
        print("to", direction_selected, "is", self.direction)

    def update_target(self, x, y):
        target_reachable = self.planet.shortest_path((self.current_position[0],self.current_position[1]), self.target)
        if target_reachable:
            self.mode = TARGET_MODE
            self.target_path = target_reachable
        else: # explore till fully explored or found the target
            self.mode = DISCOVER_MODE
            self.target_path = []
        self.target = (x,y)

    def handle_messages(self, message_type, message):
        #print("\n\n\nMESSAGE RECEIVED:       ", message_type, message)
        if message_type == "pathUnveiled":
            x0, y0, start_dir = message["startX"], message["startY"], message["startDirection"]
            x1, y1, end_dir = message["endX"], message["endY"], message["endDirection"]
            weight = message["pathWeight"]
            self.planet.add_path(start=((x0, y0), start_dir), target=((x1,y1), end_dir), weight=weight)
            if self.target:
                self.update_target(self.target[0], self.target[1])
        elif message_type == "target":
            x, y = message["targetX"], message["targetY"]
            if (x,y) not in self.planet.map:
                self.planet.add_node(x,y)
            self.update_target(x, y)