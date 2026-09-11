import numpy as np


WALL = 1
FREE = 0


class MineEnvironment:

    def __init__(
        self,
        width=60,
        height=60
    ):

        self.width = width
        self.height = height

        # Empty hidden mine
        self.grid = np.zeros(
            (height, width),
            dtype=np.int8
        )

        self.create_walls()


    def create_walls(self):

        # ---------------------------------
        # Outer mine boundaries
        # ---------------------------------

        self.grid[0, :] = WALL
        self.grid[-1, :] = WALL
        self.grid[:, 0] = WALL
        self.grid[:, -1] = WALL


        # ---------------------------------
        # Internal tunnel walls
        # ---------------------------------

        self.grid[15:45, 20] = WALL

        self.grid[
            15,
            20:40
        ] = WALL

        self.grid[
            30:50,
            40
        ] = WALL


        # ---------------------------------
        # Tunnel opening
        # ---------------------------------

        self.grid[
            30:35,
            20
        ] = FREE


    def is_wall(
        self,
        x,
        y
    ):

        gx = int(round(x))
        gy = int(round(y))

        # Outside environment = wall
        if (
            gx < 0
            or gx >= self.width
            or gy < 0
            or gy >= self.height
        ):

            return True

        return (
            self.grid[gy, gx]
            ==
            WALL
        )