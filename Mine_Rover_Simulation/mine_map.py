import math
import numpy as np
import matplotlib.pyplot as plt

UNKNOWN = -1
FREE = 0
OBSTACLE = 1


class MineMap:

    def __init__(self, width=60, height=60):

        self.width = width
        self.height = height

        self.grid = np.full(
            (height, width),
            UNKNOWN,
            dtype=np.int8
        )

        self.fig = None
        self.ax = None


    def mark(self, x, y, value):

        gx = int(round(x))
        gy = int(round(y))

        if 0 <= gx < self.width and 0 <= gy < self.height:

            current_value = self.grid[gy, gx]

            if current_value == OBSTACLE and value == FREE:
                return

            self.grid[gy, gx] = value


    def update_from_tof(self, rover, readings, step=0.5):

        self.mark(
            rover.x,
            rover.y,
            FREE
        )

        for reading in readings:

            world_angle = (
                rover.theta
                +
                reading["angle"]
            )

            radians = math.radians(
                world_angle
            )

            distance = reading[
                "distance"
            ]

            d = 0

            while d < distance:

                x = (
                    rover.x
                    +
                    d * math.cos(radians)
                )

                y = (
                    rover.y
                    +
                    d * math.sin(radians)
                )

                self.mark(
                    x,
                    y,
                    FREE
                )

                d += step

            if reading["hit_wall"]:

                x = (
                    rover.x
                    +
                    distance * math.cos(radians)
                )

                y = (
                    rover.y
                    +
                    distance * math.sin(radians)
                )

                self.mark(
                    x,
                    y,
                    OBSTACLE
                )


    def show(
        self,
        rover,
        path=None,
        goal=None,
        cost_map=None,
        semantic_map=None
    ):

        if self.fig is None or self.ax is None:

            plt.ion()

            self.fig, self.ax = plt.subplots(
                figsize=(8, 8)
            )

            plt.show(
                block=False
            )

        self.ax.clear()

        self.ax.imshow(
            self.grid,
            origin="lower",
            interpolation="nearest",
            cmap="viridis",
            vmin=-1,
            vmax=1
        )

        if cost_map is not None:

            hazard_overlay = np.ma.masked_where(
                cost_map <= 0,
                cost_map
            )

            self.ax.imshow(
                hazard_overlay,
                origin="lower",
                interpolation="nearest",
                cmap="hot",
                alpha=0.35
            )

        if path is not None and len(path) > 0:

            path_x = [
                point[0]
                for point in path
            ]

            path_y = [
                point[1]
                for point in path
            ]

            self.ax.plot(
                path_x,
                path_y,
                linewidth=2,
                label="Planned Path"
            )

        if goal is not None:

            goal_x, goal_y = goal

            self.ax.scatter(
                goal_x,
                goal_y,
                marker="X",
                s=100,
                label="Exploration Goal"
            )

        if semantic_map is not None:

            for obj in semantic_map.get_objects():

                obj_type = obj["type"]

                x = obj["x"]

                y = obj["y"]

                if obj_type == "WATER":

                    self.ax.scatter(
                        x,
                        y,
                        marker="o",
                        s=180,
                        edgecolors="black",
                        linewidths=1,
                        label="WATER"
                    )

                elif obj_type == "DEBRIS":

                    self.ax.scatter(
                        x,
                        y,
                        marker="D",
                        s=160,
                        edgecolors="black",
                        linewidths=1,
                        label="DEBRIS"
                    )

                elif obj_type == "CRACK":

                    self.ax.scatter(
                        x,
                        y,
                        marker="^",
                        s=180,
                        edgecolors="black",
                        linewidths=1,
                        label="CRACK"
                    )

                elif obj_type == "GAS":

                    self.ax.scatter(
                        x,
                        y,
                        marker="s",
                        s=160,
                        edgecolors="black",
                        linewidths=1,
                        label="GAS"
                    )

                elif obj_type == "SURVIVOR":

                    self.ax.scatter(
                        x,
                        y,
                        marker="*",
                        s=220,
                        edgecolors="black",
                        linewidths=1,
                        label="SURVIVOR"
                    )

        self.ax.scatter(
            rover.x,
            rover.y,
            marker="o",
            s=100,
            edgecolors="black",
            linewidths=1,
            label="Rover"
        )

        handles, labels = (
            self.ax.get_legend_handles_labels()
        )

        unique = dict(
            zip(labels, handles)
        )

        if unique:

            self.ax.legend(
                unique.values(),
                unique.keys(),
                loc="upper right"
            )

        self.ax.set_xlim(
            0,
            self.width
        )

        self.ax.set_ylim(
            0,
            self.height
        )

        self.ax.set_xlabel(
            "X"
        )

        self.ax.set_ylabel(
            "Y"
        )

        self.ax.set_title(
            "Autonomous Mine Rover - Semantic Map"
        )

        self.fig.canvas.draw()

        self.fig.canvas.flush_events()

        plt.pause(0.05)