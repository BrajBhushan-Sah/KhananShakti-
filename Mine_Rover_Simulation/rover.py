import math


class Rover:


    def __init__(
        self,
        x=5.0,
        y=5.0,
        theta=0
    ):


        self.x = x
        self.y = y
        self.theta = theta


    def move_forward(
        self,
        distance
    ):


        radians = math.radians(
            self.theta
        )


        self.x += (

            distance
            *
            math.cos(
                radians
            )

        )


        self.y += (

            distance
            *
            math.sin(
                radians
            )

        )


    def turn(
        self,
        angle
    ):


        self.theta += angle

        self.theta %= 360


    def pose(
        self
    ):


        return (

            self.x,

            self.y,

            self.theta

        )