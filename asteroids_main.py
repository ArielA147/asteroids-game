##############################################################################
# FILE: asteroids_main.py
#
# DESCRIPTION: in this file there is one class - GameRunner .
# The class represents the Asteroids game. the class is responsible on the
# objects movement in game and displaying appropriate messages to the user.
##############################################################################

############################################################
# Imports
############################################################
from screen import Screen
import sys

from math import sqrt
from random import randint
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo

############################################################
# Class definition
############################################################

X_AXIS = 0
Y_AXIS = 1

START_SPEED = 0
LEFT_TURN = 7
RIGHT_TURN = -7
DEFAULT_ASTEROIDS_NUM = 3
NO_ASTEROIDS_LEFT = 0

ASTEROIDS_MIN_SPEED = 1
ASTEROIDS_MAX_SPEED = 3

DELTA_X_AXIS = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
DELTA_Y_AXIS = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y

TWENTY_POINTS = 20
FIFTY_POINTS = 50
HUNDRED_POINTS = 100

ENDED_LIFE = 0
MAX_TORPEDO_NUM = 15  # the max number of asteroids that can be on the screen
OPPOSITE_DIRECTION = -1

SUM_POINTS = 0

TITLE_HIT_BY_ASTEROID = "Ship Hit!"
MSG_HIT_BY_ASTEROID = "Oh no! Be careful! " \
                      "There was a collision with the spacecraft. " \
                      "The amount of life decreased "

TITLE_WIN = "Congratulations!"
MSG_WIN = "You destroyed all asteroids and won the game!"

TITLE_LOSE = "Ship Destroyed!"
MSG_LOSE = "Too bad... All of the ship lifes are gone and " \
           "it is destroyed. You Lost."

TITLE_QUIT = "Goodbye!"
MSG_QUIT = "The 'Quit' button was pressed, therefore the game will end."


class GameRunner:

    def __init__(self, asteroids_amnt=DEFAULT_ASTEROIDS_NUM):
        """
        A constructor for asteroids game object.
        :param asteroids_amnt: the starting number of asteroids on the board.
        if there was no input the value will be DEFAULT_ASTEROIDS_NUM .
        """
        self._screen = Screen()
        # the borders of the screen. The maximum and minimum points
        # possible for movement on the screen.
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship()  # create a ship object.
        self.__asteroid_amount = asteroids_amnt
        # the starting amount of asteroids in the game.
        self.__asteroids = self._add_asteroids_to_game()
        # list of all the asteroids that are in the game.
        self.__torpedos = list()
        # a list of all the torpedo objects. starts empty.
        self.__sum_points = SUM_POINTS
        # the sum of the points for destroying asteroids.

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def _keyboard_pressing(self):
        """
        the function checks if the user pressed a key and moves the ship or
        creates a new torpedo accordingly.
        :return: None.
        """
        if self._screen.is_left_pressed():
            self.__ship.ship_turn(LEFT_TURN)
        elif self._screen.is_right_pressed():
            self.__ship.ship_turn(RIGHT_TURN)
        elif self._screen.is_up_pressed():
            self.__ship.ship_acceleration()
        elif self._screen.is_space_pressed():
            self._add_torpedo()

    def _create_asteroid_position(self):
        """
        the function raffles a new asteroid position (x,y) then insures that
        it's not set in the ship's starting location.
        :return: asteroid_pos: (x_location, y_location).
        """
        # check if the x value is not the same as the ship x value.
        x_location = randint(self.screen_min_x, self.screen_max_x)
        while x_location == self.__ship.get_position()[X_AXIS]:
            x_location = randint(self.screen_min_x, self.screen_max_x)
        # check if the y value is not the same as the ship y value.
        y_location = randint(self.screen_min_y, self.screen_max_y)
        while y_location == self.__ship.get_position()[Y_AXIS]:
            y_location = randint(self.screen_min_y, self.screen_max_y)
        asteroid_pos = (x_location, y_location)
        return asteroid_pos

    def _add_asteroids_to_game(self):
        """
        this method creates a list of Asteroid objects. each asteroid will be
        given a random position (that is not ship's position) and a random
        speed between the speed limits. the asteroids will then be registered.
        :return: asteroids_lst: a list of Asteroid objects.
        """
        asteroids_lst = list()
        for i in range(self.__asteroid_amount):
            # create position for the asteroid
            asteroid_pos = self._create_asteroid_position()
            new_speed = (randint(ASTEROIDS_MIN_SPEED, ASTEROIDS_MAX_SPEED),
                         randint(ASTEROIDS_MIN_SPEED, ASTEROIDS_MAX_SPEED))
            asteroids_lst.append(Asteroid(asteroid_pos, new_speed))
        for asteroid in asteroids_lst:  # register all of the asteroids.
            self._screen.register_asteroid(asteroid, asteroid.get_size())
        return asteroids_lst

    def _add_torpedo(self):
        """
        this function adds one torpedo object if there are less than
        15 torpedos in the game board. it will add it to the torpedo list and
        register it to the screen.
        :return: None.
        """
        if len(self.__torpedos) < MAX_TORPEDO_NUM:
            # if there are less than 15 torpedos at once, add a torpedo.
            torpedo = Torpedo(self.__ship.get_position(),
                              self.__ship.get_direction(),
                              self.__ship.get_speed())
            self._screen.register_torpedo(torpedo)
            self.__torpedos.append(torpedo)

    def _move_object_on_board(self, game_obj):
        """
        this function receives an object (torpedo, ship, asteroid) and moves
        it according to a formula.
        :param game_obj: game object (torpedo, ship, asteroid).
        :return: None.
        """
        new_x_coordinate = (game_obj.get_speed()[X_AXIS] +
                            game_obj.get_position()[X_AXIS] - abs(
            Screen.SCREEN_MIN_X)) % DELTA_X_AXIS + Screen.SCREEN_MIN_X
        new_y_coordinate = (game_obj.get_speed()[Y_AXIS] +
                            game_obj.get_position()[Y_AXIS] - abs(
            Screen.SCREEN_MIN_Y)) % DELTA_Y_AXIS + Screen.SCREEN_MIN_Y
        # update the value of the position for the game object
        game_obj.set_pos(new_x_coordinate, new_y_coordinate)

    def _torpedos_action(self):
        """
        the function moves all the torpedoes on the board and updates
        their life. if torpedo has no lives left, it will be deleted
        from the game.
        :return: None.
        """
        for torpedo in self.__torpedos:
            self._move_object_on_board(torpedo)
            x_torpedo, y_torpedo = torpedo.get_position()
            self._screen.draw_torpedo(torpedo, x_torpedo, y_torpedo,
                                      torpedo.get_direction())
            torpedo.update_life_time()
            if torpedo.get_life_time() == ENDED_LIFE:
                self._delete_torpedo(torpedo)

    def _ship_action(self):
        """
        this function moves the ship on game board.
        :return: None.
        """
        self._move_object_on_board(self.__ship)
        x_ship, y_ship = self.__ship.get_position()
        self._screen.draw_ship(x_ship, y_ship, self.__ship.get_direction())

    def _asteroids_action(self):
        """
        this function moves all of the asteroids in the game and checks if it
        had an intersection with a torpedo or the ship, and acts accordingly.
        :return: None.
        """
        for asteroid in self.__asteroids:
            self._move_object_on_board(asteroid)
            x_asteroid, y_asteroid = asteroid.get_position()
            self._screen.draw_asteroid(asteroid, x_asteroid, y_asteroid)
            self._asteroid_crash()

    def _asteroid_crash(self):
        """
        the function checks if the asteroid crashed with another object:
        ship or torpedo, and behaves accordingly.
        if the asteroid hit a ship - it will be deleted and the ship will
        be damaged. the number of life for the ship will decrease.
        if a torpedo hit the asteroid - the method will call the
        torpedo_hit_asteroid method, and the asteroid will be updated
        according to his size.
        :return: None.
        """
        for asteroid in self.__asteroids:
            asteroid_hit_ship = False
            if asteroid.has_intersection(self.__ship):
                self._screen.show_message(TITLE_HIT_BY_ASTEROID,
                                          MSG_HIT_BY_ASTEROID)
                self._screen.remove_life()  # remove one icon of life.
                self.__ship.decrease_life()
                asteroid_hit_ship = True
            if asteroid_hit_ship is True:
                # call the method to delete the asteroid from game.
                self._delete_asteroid(asteroid)
            else:  # asteroid was not hit by ship.
                for torpedo in self.__torpedos:
                    if asteroid.has_intersection(torpedo):
                        self._torpedo_hit_asteroid(asteroid, torpedo)

    def _torpedo_hit_asteroid(self, asteroid, torpedo):
        """
        the function updates the asteroid new size, position and speed.
        If the asteroid size is medium or biggest - the asteroid splits into
        two new asteroids, and the points are added to the points sum.
        if the asteroid size is the minimum size - the points are added to
        the points sum. the function will then delete both asteroid and
        torpedo that collided, and display the scores.
        :param asteroid: asteroid object - the asteroid that got hit.
        :param torpedo: torpedo object - the torpedo that hit the asteroid.
        :return: None.
        """
        # the position that the new asteroids are going to start - the same
        # position that of the coalition
        new_asteroids_pos = asteroid.get_position()
        asteroid_hit_speed = asteroid.get_speed()
        torpedo_hit_speed = torpedo.get_speed()
        if asteroid.get_size() == Asteroid.BIGGEST_SIZE_ASTEROID:
            self._split_asteroid(asteroid, asteroid_hit_speed,
                                 new_asteroids_pos, torpedo_hit_speed)
            self.__sum_points += TWENTY_POINTS
        elif asteroid.get_size() == Asteroid.MEDIUM_SIZE_ASTEROID:
            self._split_asteroid(asteroid, asteroid_hit_speed,
                                 new_asteroids_pos, torpedo_hit_speed)
            self.__sum_points += FIFTY_POINTS
        else:  # if the asteroid size is 1.
            self.__sum_points += HUNDRED_POINTS
        self._screen.set_score(self.__sum_points)
        self._delete_asteroid(asteroid)
        self._delete_torpedo(torpedo)
        # in any case delete the torpedo and previous asteroid from game.

    def _asteroid_new_axis_speed(self, axis, asteroid_hit_speed,
                                 torpedo_speed):
        """
        the function calculates the new speed of the asteroid in the given
        axis.
        :param axis: the axis of the speed. get the constants X_AXIS / Y_AXIS.
        :param asteroid_hit_speed: the current speed of asteroid (tuple).
        :param torpedo_speed: the current speed of torpedo (tuple).
        :return: the speed of the asteroid in the given axis (float).
        """
        return (torpedo_speed[axis] + asteroid_hit_speed[axis]) / sqrt(
            asteroid_hit_speed[X_AXIS] ** 2 + asteroid_hit_speed[Y_AXIS] ** 2)

    def _split_asteroid(self, asteroid, asteroid_hit_speed, new_asteroids_pos,
                        torpedo_speed):
        """
        this function creates two asteroids from the one that got hit by a
        torpedo. the new speed will be calculated according to a formula, and
        in an opposite directions. the new position will be the old asteroid's
        position. the size of them will be reduced by one size from the old
        asteroid. the function will then add the asteroids to the game.
        :param asteroid: asteroid object that was hit by torpedo (asteroid).
        :param asteroid_hit_speed: the current speed of asteroid (tuple).
        :param new_asteroids_pos: the position of the new asteroids (tuple).
        :param torpedo_speed: the current speed of torpedo (tuple).
        :return: None.
        """
        new_x_speed = self._asteroid_new_axis_speed(X_AXIS,
                                                    asteroid_hit_speed,
                                                    torpedo_speed)
        new_y_speed = self._asteroid_new_axis_speed(Y_AXIS,
                                                    asteroid_hit_speed,
                                                    torpedo_speed)
        if asteroid.get_size() == Asteroid.BIGGEST_SIZE_ASTEROID:
            new_asteroids_size = Asteroid.MEDIUM_SIZE_ASTEROID
            # asteroid size is decreased to medium.
        else:  # if the size of the asteroid is medium.
            new_asteroids_size = Asteroid.SMALLEST_SIZE_ASTEROID
            # asteroid size is decreased to small.
        asteroid_1 = Asteroid(new_asteroids_pos, (new_x_speed, new_y_speed),
                              new_asteroids_size)
        asteroid_2 = Asteroid(new_asteroids_pos,
                              (OPPOSITE_DIRECTION * new_x_speed,
                               OPPOSITE_DIRECTION * new_y_speed),
                              new_asteroids_size)
        # create two asteroids with the new size, same position as the
        # old asteroid, and opposite speed. add them to the game.
        self.__asteroids.extend([asteroid_1, asteroid_2])
        self._screen.register_asteroid(asteroid_1, new_asteroids_size)
        self._screen.register_asteroid(asteroid_2, new_asteroids_size)

    def _delete_asteroid(self, asteroid):
        """
        the function unregisters the asteroid and deletes it from the
        asteroids list.
        :param asteroid: the asteroid that will be deleted (type asteroid).
        :return: None.
        """
        self._screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def _delete_torpedo(self, torpedo):
        """
        the function unregisters the torpedo and deletes it from the
        torpedo list.
        :param torpedo: the torpedo that will be deleted (type torpedo).
        :return: None.
        """
        self._screen.unregister_torpedo(torpedo)
        self.__torpedos.remove(torpedo)

    def _check_won_game(self):
        """
        the function checks if the user won the game. if he did -
        an appropriate message will be displayed on screen and then the
        game will be closed.
        :return: None.
        """
        if len(self.__asteroids) == NO_ASTEROIDS_LEFT:
            # if no asteroids left, the game is won.
            self._screen.show_message(TITLE_WIN, MSG_WIN)
            self._screen.end_game()
            sys.exit()

    def _check_lost_game(self):
        """
        the function checks if the user lost the game. if he did - an
        appropriate message will be displayed on screen.
        the game window will then be closed.
        :return: None.
        """
        if self.__ship.get_life() == ENDED_LIFE:  # no life left for ship.
            self._screen.show_message(TITLE_LOSE, MSG_LOSE)
            self._screen.end_game()
            sys.exit()

    def _check_quit_game(self):
        """
        the function checks if the user pressed the 'Quit' button. If he does
        a message of quiting the game will appear and the game will be over.
        the window will be closed.
        :return: None.
        """
        if self._screen.should_end() is True:  # "Quit" button was pressed.
            self._screen.show_message(TITLE_QUIT, MSG_QUIT)
            self._screen.end_game()
            sys.exit()

    def _game_loop(self):
        """
        the function does one loop of the game in the order of checking if the
        user pressed on key and making all of the object's actions in game.
        the function will also check the game status: if the user won the
        game, lost the game or chose to end the game.
        :return: None.
        """
        self._keyboard_pressing()
        self._ship_action()
        self._torpedos_action()
        self._asteroids_action()
        self._check_lost_game()
        self._check_won_game()
        self._check_quit_game()


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
