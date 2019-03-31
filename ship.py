##############################################################################
# FILE: ship.py
#
# DESCRIPTION: in this file there is one class - Ship.
# the class represents the object of ship in the game.
# the ship starting position will be chosen randomly, and it's starting
# speed will be 0 in both axis.
#
##############################################################################

############################################################
# Imports
############################################################
from screen import Screen
from math import sin, cos, radians
from random import randint

############################################################
# Class definition
############################################################
X_AXIS = 0
Y_AXIS = 1

START_DIRECTION = 0
X_START_SPEED = 0
Y_START_SPEED = 0

START_LIFE = 3
MIN_LIFE = 1
NUM_DECREASE_LIFE = 1  # The amount of decrease life

SHIP_RADIUS = 1


class Ship:
    def __init__(self):
        """
        A constructor for a ship object.
        """
        self.__pos = (randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X),
                      randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y))
        # a starting random position in the screen borders.
        self.__speed = (X_START_SPEED, Y_START_SPEED)  # starting speed (0).
        self.__direction = START_DIRECTION  # the direction angle of the ship.
        self.__life = START_LIFE  # life points of a ship (int between 0-3).
        self.__radius = SHIP_RADIUS

    def get_direction(self):
        """
        this method returns the heading direction of the ship.
        :return: direction angle of the ship (int).
        """
        return self.__direction

    def get_radius(self):
        """
        this method returns the radius of a ship.
        :return: radius of a ship object (int).
        """
        return self.__radius

    def get_life(self):
        """
        this method returns the life points left for the ship.
        :return: life points of ship (int).
        """
        return self.__life

    def get_speed(self):
        """
        this method returns the speed of the ship in both axis.
        :return: speed of ship (tuple).
        """
        return self.__speed

    def get_position(self):
        """
        this method returns the position of the ship.
        :return: position of the ship in the game board ((x, y) tuple).
        """
        return self.__pos

    def decrease_life(self):
        """
        the function updates the life
        :return:
        """
        self.__life -= NUM_DECREASE_LIFE
        return self.__life

    def check_if_no_more_life(self):
        """
        this function checks if the ship has no more life left.
        :return: True - if the ship have no life left, else return False.
        """
        if self.get_life() < MIN_LIFE:
            return True
        else:
            return False

    def ship_acceleration(self):
        """
        the function calculates the acceleration of the ship in each axis,
        and updates the speed of the ship accordingly.
        :return: None.
        """
        new_x_speed = self.__speed[X_AXIS] + cos(radians(self.__direction))
        new_y_speed = self.__speed[Y_AXIS] + sin(radians(self.__direction))
        self.__speed = (new_x_speed, new_y_speed)

    def ship_turn(self, angle):
        """
        this function turns the ship a given angle.
        :param angle: the angle of the turn (int).
        :return: None.
        """
        self.__direction += angle

    def set_pos(self, new_x, new_y):
        """
        the function updates the values of the ship position.
        :param new_x: the new x coordinate of the ship on the board (float).
        :param new_y: the new y coordinate of the ship on the board (float).
        :return: None.
        """
        self.__pos = new_x, new_y
