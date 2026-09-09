UNKNOWN = -1
FREE = 0


# ---------------------------------
# Find FREE cells beside UNKNOWN
# ---------------------------------

def find_frontiers(
    grid
):

    height, width = grid.shape

    frontiers = []


    for y in range(height):


        for x in range(width):


            # Frontier must be known FREE

            if (
                grid[y, x]
                !=
                FREE
            ):

                continue


            neighbors = [

                (x + 1, y),

                (x - 1, y),

                (x, y + 1),

                (x, y - 1)

            ]


            for nx, ny in neighbors:


                if (

                    0 <= nx < width

                    and

                    0 <= ny < height

                ):


                    # FREE beside UNKNOWN

                    if (

                        grid[ny, nx]
                        ==
                        UNKNOWN

                    ):


                        frontiers.append(
                            (x, y)
                        )

                        break


    return frontiers


# ---------------------------------
# Calculate information gain
# ---------------------------------

def frontier_information_gain(
    grid,
    frontier
):

    x, y = frontier

    height, width = grid.shape

    unknown_count = 0


    for dy in range(
        -1,
        2
    ):


        for dx in range(
            -1,
            2
        ):


            nx = x + dx
            ny = y + dy


            if (

                0 <= nx < width

                and

                0 <= ny < height

            ):


                if (

                    grid[ny, nx]
                    ==
                    UNKNOWN

                ):

                    unknown_count += 1


    return unknown_count


# ---------------------------------
# Sort frontiers
# ---------------------------------

def sort_frontiers(
    frontiers,
    rover_position,
    grid
):


    rover_x, rover_y = rover_position


    def frontier_score(
        point
    ):


        distance = (

            (point[0] - rover_x) ** 2

            +

            (point[1] - rover_y) ** 2

        )


        information = (

            frontier_information_gain(

                grid,

                point

            )

        )


        # Lower score = better frontier

        return (

            distance

            -

            information * 2

        )


    return sorted(

        frontiers,

        key=frontier_score

    )