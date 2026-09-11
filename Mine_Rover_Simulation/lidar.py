import math


class SimulatedServoToF:

    def __init__(
        self,
        environment,
        max_range=15,
        step=0.5
    ):

        self.environment = environment
        self.max_range = max_range
        self.step = step


        # Servo scan angles
        # Relative to rover front

        self.angles = [

            -60,
            -45,
            -30,
            -15,
            0,
            15,
            30,
            45,
            60

        ]


    def scan(
        self,
        rover
    ):

        readings = []


        for servo_angle in self.angles:


            # Servo direction in world coordinates

            world_angle = (

                rover.theta
                +
                servo_angle

            )


            radians = math.radians(
                world_angle
            )


            distance = 0

            hit_wall = False


            # Ray-cast sensor beam

            while (
                distance
                <
                self.max_range
            ):

                distance += self.step


                x = (

                    rover.x
                    +
                    distance
                    *
                    math.cos(radians)

                )


                y = (

                    rover.y
                    +
                    distance
                    *
                    math.sin(radians)

                )


                if self.environment.is_wall(
                    x,
                    y
                ):

                    hit_wall = True

                    break


            readings.append(

                {

                    "angle": servo_angle,

                    "distance": distance,

                    "hit_wall": hit_wall

                }

            )


        return readings