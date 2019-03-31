import sys
import tkinter
import tkinter.messagebox

from turtle import *


class ShapesMaster:
    ASTEROID_BASE_SHAPE = "asteroid%d"
    SHIP_SHAPE = "ship"
    TORPEDO_SHAPE = "torpedo"

    ASTEROIDS_TYPES = 3

    ASTEROID_3_LAYOUT = ((-20, -16), (-21, 0), (-20, 18), (0, 27), (17, 15),
                         (25, 0), (16, -15), (0, -21))

    ASTEROID_2_LAYOUT = ((-15, -10), (-16, 0), (-13, 12), (0, 19), (12, 10),
                         (20, 0), (12, -10), (0, -13))

    ASTEROID_1_LAYOUT = (
        (-10, -5), (-12, 0), (-8, 8), (0, 13), (8, 6), (14, 0), (12, 0),
        (8, -6),
        (0, -7))

    ASTEROIDS_LAYOUTS = [ASTEROID_1_LAYOUT, ASTEROID_2_LAYOUT,
                         ASTEROID_3_LAYOUT]

    SHIP_LAYOUT = ((-10, -10), (0, -5), (10, -10), (0, 10))

    TORPEDO_LAYOUT = ((-2, -4), (-2, 4), (2, 4), (2, -4))

    def __init__(self, screen):
        """
        This initializes the shapes controller, the screen passed is the screen
        controling the game, you should not call this method anywhere in your
        code.
        """
        self.screen = screen
        self._shapes = {}
        self._updated = False
        self._add_base_shapes()

    def add_shape(self, name, cords, override=False):
        if override or name not in self._shapes:
            self._shapes[name] = cords
            self.screen.register_shape(name, cords)

    def _add_base_shapes(self):
        for i in range(ShapesMaster.ASTEROIDS_TYPES):
            self.add_shape(ShapesMaster.ASTEROID_BASE_SHAPE % (i + 1),
                           ShapesMaster.ASTEROIDS_LAYOUTS[i])

        self.add_shape(ShapesMaster.SHIP_SHAPE, ShapesMaster.SHIP_LAYOUT)
        self.add_shape(ShapesMaster.TORPEDO_SHAPE, ShapesMaster.TORPEDO_LAYOUT)

    def get_shapes_dict(self):
        """
        Returns a dictionary of all the shapes in the game in the format of
        (name, coordinates).
        You have no reason of calling this method anywhere in your code...
        """
        return self._shapes


class Screen:
    SCREEN_MIN_X = -500
    SCREEN_MIN_Y = -500
    SCREEN_MAX_X = 500
    SCREEN_MAX_Y = 500

    def __init__(self):
        """
        This inits our graphics class.
        """

        self._boundKeys = []
        self._init_keys_values()
        self._init_graphics()
        self._bind_keys()
        self._screen.listen()

        self._ship = self._get_ship_obj(self._cv)

    def _init_keys_values(self):
        self._specialTorpedFired = 0
        self._rightClicks = 0
        self._leftClicks = 0
        self._upClicks = 0
        self._fireClicks = 0
        self._endGame = False
        self._lives = []
        self._asteroids = {}
        self._torpedos = {}

    def _init_graphics(self):
        self._root = tkinter.Tk()
        self._root.title("Asteroids!")
        self._cv = ScrolledCanvas(self._root, 600, 600, 600, 600)
        self._cv.pack(side=tkinter.LEFT)
        self._t = RawTurtle(self._cv)

        self._screen = self._t.getscreen()
        self._screen.setworldcoordinates(
            Screen.SCREEN_MIN_X,
            Screen.SCREEN_MIN_Y,
            Screen.SCREEN_MAX_X,
            Screen.SCREEN_MAX_X
        )
        self._shapeMaster = ShapesMaster(self._screen)
        shapes = self._shapeMaster.get_shapes_dict()

        frame = tkinter.Frame(self._root)
        frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

        # add scores frame
        self._score_val = tkinter.StringVar()
        self._score_val.set("0")
        scoreTitle = tkinter.Label(frame, text="Score")
        scoreTitle.pack()
        scoreFrame = tkinter.Frame(frame, height=2, bd=1,
                                   relief=tkinter.SUNKEN)
        scoreFrame.pack()
        score = tkinter.Label(scoreFrame, height=2, width=20,
                              textvariable=self._score_val, fg="Yellow",
                              bg="black")

        ################

        score.pack()

        # Add Lives Frame
        # livesTitle = tkinter.Label(frame, \
        #    text="Extra Lives Remaining")
        # livesTitle.pack()

        # livesFrame = tkinter.Frame(frame, \
        #     height=30,width=60,relief=tkinter.SUNKEN)
        # livesFrame.pack()
        # self._lives_canvas = ScrolledCanvas(livesFrame,150,40,150,40)
        # self._lives_canvas.pack()
        # livesTurtle = RawTurtle(self._lives_canvas)
        # livesTurtle.ht()
        # livesScreen = livesTurtle.getscreen()
        # livesScreen.register_shape(ShapesMaster.SHIP_SHAPE,
        # shapes[ShapesMaster.SHIP_SHAPE])

        # Add Lives Frame
        livesTitle = tkinter.Label(frame, text="Extra Lives Remaining")
        livesTitle.pack()

        livesFrame = tkinter.Frame(frame, height=30, width=60,
                                   relief=tkinter.SUNKEN)
        livesFrame.pack()
        livesCanvas = ScrolledCanvas(livesFrame, 150, 40, 150, 40)
        livesCanvas.pack()
        livesTurtle = RawTurtle(livesCanvas)
        livesTurtle.ht()
        livesScreen = livesTurtle.getscreen()
        livesScreen.register_shape(ShapesMaster.SHIP_SHAPE,
                                   shapes[ShapesMaster.SHIP_SHAPE])

        life1 = self._get_ship_obj(
            livesCanvas)  # SpaceShip(livesCanvas,-35,0,0,0)
        life2 = self._get_ship_obj(
            livesCanvas)  # SpaceShip(livesCanvas,0,0,0,0)
        life3 = self._get_ship_obj(
            livesCanvas)  # SpaceShip(livesCanvas,35,0,0,0)

        self._draw_object(life1, -35, 0)
        self._draw_object(life2, 0, 0)
        self._draw_object(life3, 35, 0)

        self._lives = [life1, life2, life3]

        self._t.ht()

        quitButton = tkinter.Button(frame, text="Quit",
                                    command=self._handle_exit)
        quitButton.pack()

        self._screen.tracer(0)

    def ontimer(self, func, milli):
        """
        This method is used to create a repeating action in your game.

        .. warning::

            **You don't need to call this method, it was already called for
            you at the end of the main game loop.**

        :param func: The function to repeat after **milli** milliseconds
        have passed
        :type func: function
        :param milli: The amount of milliseconds to wait before starting
        the given
            function
        :type milli: int
        """
        self._screen.ontimer(func, milli)

    def _bind_key(self, key, func):
        """
        This method is to allow you to add some functionality of your own,
        it allows you to bind the provided function to the desired input key.

        If there is already a function bound to this key it will do nothing.

        :param key: A key to bind.
        :type key: str
        :param func: The function to bind
        :type func: function
        """

        if key not in self._boundKeys:
            self._screen.onkeypress(func, key)
            self._boundKeys.append(key)

    def _bind_keys(self):
        self._bind_key("Left", self._handle_left)
        self._bind_key("Right", self._handle_right)
        self._bind_key("Up", self._handle_up)
        self._bind_key("space", self._handle_space)
        self._bind_key("q", self._handle_exit)
        self._bind_key("s", self._handle_special_torpedo)

    def _handle_special_torpedo(self):
        self._specialTorpedFired += 1

    def _handle_exit(self):
        self._endGame = True

    def _handle_left(self):
        self._leftClicks += 1

    def _handle_right(self):
        self._rightClicks += 1

    def _handle_up(self):
        self._upClicks += 1

    def _handle_space(self):
        self._fireClicks += 1

    def start_screen(self):
        """
        This is called to start our game (grphaics-wise).

        .. warning::

            **This method should not be called by you**
        """
        tkinter.mainloop()

    def update(self):
        """
        This is called to update our game (grphaics-wise).

        .. warning::

            **This method should not be called by you**
        """
        self._screen.update()

    def set_score(self, val):
        """
        Sets the current game score

        :param val: The game score
        :type val: int
        """
        self._score_val.set(str(val))

    def _get_ship_obj(self, canvas):
        ship = RawTurtle(canvas)
        ship.shape(ShapesMaster.SHIP_SHAPE)
        ship.color("purple")
        return ship

    def _get_asteroid_object(self, size):
        asteroid = RawTurtle(self._cv)
        asteroid.shape(ShapesMaster.ASTEROID_BASE_SHAPE % size)
        return asteroid

    def _get_torpedo_object(self):
        torpedo = RawTurtle(self._cv)
        torpedo.shape(ShapesMaster.TORPEDO_SHAPE)
        torpedo.color("blue")
        return torpedo

    def _draw_object(self, obj, x, y, heading=None):
        obj.penup()
        obj.goto(x, y)
        if heading:
            obj.setheading(heading)
        obj.pendown()

    def remove_life(self):
        """
        Remove one icon of life (starts with 3 lives)
        """
        deadship = self._lives.pop()
        deadship.ht()

    def register_asteroid(self, asteroid, size):
        """
        This is called to register a new asteroid in our system

        :param asteroid: This is your asteroid object
        :type asteroid: Asteroid

        :param size: The size of the asteroid (this should be in [1,2,3])
        :type size: int
        """
        if size not in [1, 2, 3]:
            print("Error: Wrong asteroid size: %d" % size)
            sys.exit(0)
        elif id(asteroid) in self._asteroids:
            print("Error: Asteroid id (%d) already exists" % asteroid_id)
            sys.exit(0)
        asteroid_obj = self._get_asteroid_object(size)
        self._asteroids[id(asteroid)] = asteroid_obj

    def register_torpedo(self, torpedo):
        """
        This is called to register a new torpedo in our system

        :param asteroid: This is your torpedo object
        :type asteroid: Torpedo
        """
        if id(torpedo) in self._torpedos:
            print("Error: Torpedo id (%d) already exists" % torpedo_id)
            sys.exit(0)
        torpedo_obj = self._get_torpedo_object()
        self._torpedos[id(torpedo)] = torpedo_obj

    def draw_ship(self, x, y, heading):
        """
        Draw the ship at the given coordinates with the given heading

        :param x: This is the X coordinate of the ship
        :type x: int
        :param y: This is the Y coordinate of the ship
        :type y: int
        :param heading: This is the heading of the ship (in degrees)
        :type heading: float

        """
        self._draw_object(self._ship, x, y, heading)

    def draw_asteroid(self, asteroid, x, y):
        """
        Draw the given asteroid on the specified (x,y) coordinates

        :param asteroid: This is your asteroid object (remember to
        register it before)
        :type asteroid: Asteroid
        :param x: This is the X coordinate of the asteroid
        :type x: int
        :param y: This is the Y coordinate of the asteroid
        :type y: int

        """
        asteroid_id = id(asteroid)
        if asteroid_id not in self._asteroids:
            print("Error: Asteroid id (%d) not found. " % asteroid_id +
                  "Are you sure there is such an asteroid?")
            sys.exit(0)

        self._draw_object(self._asteroids[asteroid_id], x, y)

    def draw_torpedo(self, torpedo, x, y, heading):
        """
        Draw the given torpedo on the specified (x,y) coordinates with the
        given heading

        :param asteroid: This is your torpedo object (remember to register
        it before)
        :type asteroid: Torpedo
        :param x: This is the X coordinate of the torpedo
        :type x: int
        :param y: This is the Y coordinate of the torpedo
        :type y: int
        :param heading: This is the heading of the torpedo
        :type heading: float
        """
        torpedo_id = id(torpedo)
        if torpedo_id not in self._torpedos:
            print("Torpedo id (%d) not found. " % torpedo_id +
                  "Are you sure there is such a torpedo?")
            sys.exit(0)

        self._draw_object(self._torpedos[torpedo_id], x, y, heading)

    def _remove_object(self, obj):
        obj.penup()
        obj.ht()
        obj.goto(Screen.SCREEN_MAX_X, Screen.SCREEN_MAX_Y * 2)

    def unregister_torpedo(self, torpedo):
        """
        This is called to un-register an existing torpedo in our system

        :param asteroid: This is your torpedo object
        :type asteroid: Torpedo
        """
        torpedo_id = id(torpedo)
        if torpedo_id not in self._torpedos:
            print("Torpedo id (%d) not found. " % torpedo_id +
                  "Are you sure there is such a torpedo?")
            sys.exit(0)
        torpedo_obj = self._torpedos[torpedo_id]
        self._remove_object(torpedo_obj)
        self._torpedos.pop(torpedo_id)

    def unregister_asteroid(self, asteroid):
        """
        This is called to un-register an existing asteroid in our system

        :param asteroid: This is your asteroid object
        :type asteroid: Asteroid
        """
        asteroid_id = id(asteroid)
        if asteroid_id not in self._asteroids:
            print("Asteroid id (%d) not found. " % asteroid_id +
                  "Are you sure there is such an asteroid?")
            sys.exit(0)
        asteroid_obj = self._asteroids[asteroid_id]
        self._remove_object(asteroid_obj)
        self._asteroids.pop(asteroid_id)

    def _clear_screen(self):
        self._cv.delete('all')

    def should_end(self):
        """
        :returns: True if the game should end or not (if "q" was pressed or
        not)
        """
        return self._endGame

    def is_left_pressed(self):
        """
        :returns: True if the left key was pressed, else False
        """
        res = self._leftClicks > 0
        self._leftClicks -= 1 if res else 0
        return res

    def is_up_pressed(self):
        """
        :returns: True if the up key was pressed, else False
        """
        res = self._upClicks > 0
        self._upClicks -= 1 if res else 0
        return res

    def is_right_pressed(self):
        """
        :returns: True if the right key was pressed, else False
        """
        res = self._rightClicks > 0
        self._rightClicks -= 1 if res else 0
        return res

    def is_space_pressed(self):
        """
        :returns: True if the fire key was pressed, else False
        """
        res = self._fireClicks > 0
        self._fireClicks -= 1 if res else 0
        return res

    def is_special_pressed(self):
        """
        :returns: True if the fire key was pressed, else False
        """
        res = self._specialTorpedFired > 0
        self._specialTorpedFired -= 1 if res else 0
        return res

    def show_message(self, title, msg):
        """
        This is a method used to show messages in the game.

        :param title: The title of the message box.
        :type title: str
        :param msg: The message to show in the message box.
        :type msg: str
        """
        tkinter.messagebox.showinfo(str(title), str(msg))

    def end_game(self):
        """
        This ends the current game.
        """
        self._root.destroy()
        self._root.quit()
