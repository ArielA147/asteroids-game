##############################################################################
# FILE: asteroid.py
#
# DESCRIPTION:
# in this file there is one class - Asteroid.
# asteroid object starts in a random position on the screen and with random
# speed within the speed limits. also, the starting size will be the
# maximum size for an asteroid.
# the asteroid object can move on the board, crash into the ship or a torpedo.
##############################################################################

############################################################
# Imports
############################################################
from screen import Screen
from math import sqrt

############################################################
# Class definition
############################################################

X_AXIS = 0
Y_AXIS = 1

MAX_ASTEROID_SIZE = 3
MIN_ASTEROID_SIZE = 1

SIZE_COEFFICIENT = 10
NORMALIZATION_FACTOR = -5


class Asteroid:

    BIGGEST_SIZE_ASTEROID = 3
    MEDIUM_SIZE_ASTEROID = 2
    SMALLEST_SIZE_ASTEROID = 1

    def __init__(self, position, speed, size=MAX_ASTEROID_SIZE):
        """
        A constructor for an asteroid object.
        :param position: a tuple of the asteroid position (x, y).
        :param speed: the speed of the asteroid (x speed, y speed) tuple.
        :param size: the size of an asteroid object (int between 1-3).
        """
        self.__pos = position
        self.__speed = speed
        self.__size = size

    def get_position(self):
        """
        this method returns the position of the asteroid.
        :return: position of the asteroid in the game board ((x, y) tuple).
        """
        return self.__pos

    def get_size(self):
        """
        this method returns the size of the asteroid.
        :return: size of asteroid (int between 1 and 3).
        """
        return self.__size

    def get_speed(self):
        """
        this method returns the speed of the asteroid.
        :return: speed of the asteroid in both axis (tuple).
        """
        return self.__speed

    def get_radius(self):
        """
        this function calculates the radius of the asteroid according to:
        asteroid size times the coefficient of size plus normalization
        coefficient.
        :return: the radius of the asteroid.
        """
        return self.__size * SIZE_COEFFICIENT + NORMALIZATION_FACTOR

    def has_intersection(self, obj):
        """
        this function checks if there was an intersection between the given
        object (ship or torpedo) and the asteroid.
        :param obj: the object that the asteroid intersected with.
        type - ship or torpedo.
        :return: True if there was a collision with the asteroid, else False.
        """
        distance = sqrt(
            (obj.get_position()[X_AXIS] - self.__pos[X_AXIS]) ** 2 +
            (obj.get_position()[Y_AXIS] - self.__pos[Y_AXIS]) ** 2)
        # calculate the distance between the asteroid and the given object.
        if distance <= self.get_radius() + obj.get_radius():
            # if there was a crash.
            return True
        else:
            return False

    def set_pos(self, new_x_coordinate, new_y_coordinate):
        """
        the function update the values of the asteroid position
        :param new_x_coordinate: the new x coordinate of the asteroid (float).
        :param new_y_coordinate: the new y coordinate of the asteroid (float).
        :return: None.
        """
        self.__pos = new_x_coordinate, new_y_coordinate
