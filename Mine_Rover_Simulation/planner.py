import heapq


FREE = 0


# ---------------------------------
# Manhattan distance heuristic
# ---------------------------------

def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------
# Get valid neighbours
# ---------------------------------

def get_neighbors(position, grid):

    x, y = position


    neighbors = [

        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)

    ]


    valid_neighbors = []


    height, width = grid.shape


    for nx, ny in neighbors:


        if (

            0 <= nx < width

            and

            0 <= ny < height

        ):


            cell = grid[ny, nx]


            # Rover can only move through
            # confirmed FREE cells

            if cell == FREE:

                valid_neighbors.append(

                    (nx, ny)

                )


    return valid_neighbors


# ---------------------------------
# A* with semantic hazard costs
# ---------------------------------

def astar(

    grid,

    start,

    goal,

    cost_map=None

):


    open_list = []


    heapq.heappush(

        open_list,

        (0, start)

    )


    came_from = {}


    g_score = {

        start: 0

    }


    while open_list:


        current_priority, current = heapq.heappop(

            open_list

        )


        # ---------------------------------
        # Goal reached
        # ---------------------------------

        if current == goal:


            path = []


            while current in came_from:


                path.append(

                    current

                )


                current = came_from[

                    current

                ]


            path.append(

                start

            )


            path.reverse()


            return path


        # ---------------------------------
        # Check neighbours
        # ---------------------------------

        for neighbor in get_neighbors(

            current,

            grid

        ):


            nx, ny = neighbor


            # Normal movement cost

            movement_cost = 1


            # ---------------------------------
            # Add semantic hazard cost
            # ---------------------------------

            if cost_map is not None:


                movement_cost += cost_map[

                    ny,

                    nx

                ]


            new_cost = (

                g_score[current]

                +

                movement_cost

            )


            if (

                neighbor not in g_score

                or

                new_cost < g_score[neighbor]

            ):


                g_score[neighbor] = (

                    new_cost

                )


                priority = (

                    new_cost

                    +

                    heuristic(

                        neighbor,

                        goal

                    )

                )


                heapq.heappush(

                    open_list,

                    (

                        priority,

                        neighbor

                    )

                )


                came_from[

                    neighbor

                ] = current


    # No path found

    return None