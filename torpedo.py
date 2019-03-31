##############################################################################
# FILE: torpedo.py
#
# DESCRIPTION: in this file there is one class - Torpedo.
# the class represents the object of torpedo in the game.
# the starting position and direction of the torpedo will be the same as
# the ship's.
# each torpedo will start with life time amount that represents it's stay
# in the game.
##############################################################################

############################################################
# Imports
############################################################
from screen import Screen

from math import cos, sin, radians

############################################################
# Class definition
############################################################
X_AXIS = 0
Y_AXIS = 1

ACCELERATION_FACTOR = 2

TORPEDO_RADIUS = 4
STARTING_LIFE_TIME = 200  # the life time of a new torpedo.
ONE_ROUND_LIFE = 1


class Torpedo:
    def __init__(self, position, direction, ship_speed):
        """
        A constructor for a torpedo object.
        :param position: position of the torpedo, received by ship (tuple).
        :param direction: direction of the torpedo, received by ship (float).
        :param ship_speed: tuple of the ship speed. will be used in order to
        calculate the speed of the torpedo.
        """
        self.__pos = position
        self.__direction = direction
        self.__speed = self.set_speed(ship_speed)
        # call the method to get the speed of the torpedo.
        self.__radius = TORPEDO_RADIUS
        self.__life_time = STARTING_LIFE_TIME

    def get_position(self):
        """
        this method returns the position of the torpedo.
        :return: position of the torpedo in the game board ((x, y) tuple).
        """
        return self.__pos

    def get_direction(self):
        """
        this method returns the direction of the torpedo.
        :return: direction of the torpedo in degrees (float).
        """
        return self.__direction

    def get_radius(self):
        """
        this method returns the radius of the torpedo.
        :return: radius of the torpedo (int).
        """
        return self.__radius

    def get_speed(self):
        """
        this method returns the speed of the torpedo in both axis.
        :return: speed of the torpedo (x speed, y speed).
        """
        return self.__speed

    def get_life_time(self):
        """
        this method returns the life time of the torpedo.
        :return: life time of the torpedo (int between 200 and 0).
        """
        return self.__life_time

    def set_speed(self, ship_speed):
        """
        this function receives the ship speed and calculates the torpedo
        speed in both axis (by a formula).
        :param ship_speed: a tuple of the ship speed (x speed, y speed).
        :return: new_torpedo_speed: the speed for the torpedo (tuple).
        """
        new_x_speed = ship_speed[X_AXIS] + ACCELERATION_FACTOR * cos(
            radians(self.__direction))
        new_y_speed = ship_speed[Y_AXIS] + ACCELERATION_FACTOR * sin(
            radians(self.__direction))
        new_torpedo_speed = new_x_speed, new_y_speed
        return new_torpedo_speed

    def set_pos(self, new_x, new_y):
        """
        the function updates the values of the torpedo position.
        :param new_x: the new x coordinate of the torpedo on the board (float)
        :param new_y: the new y coordinate of the torpedo on the board (float)
        :return: None.
        """
        self.__pos = new_x, new_y

    def update_life_time(self):
        """
        this method updates the life time of a torpedo each iteration of the
        game.
        :return: None.
        """
        self.__life_time -= ONE_ROUND_LIFE
