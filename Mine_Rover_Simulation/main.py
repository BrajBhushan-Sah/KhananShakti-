import math
import numpy as np
import matplotlib.pyplot as plt

from environment import MineEnvironment

from mine_map import (
    MineMap,
    OBSTACLE
)

from rover import Rover

from lidar import SimulatedServoToF

from planner import astar

from exploration import (
    find_frontiers,
    sort_frontiers
)

from semantic_map import (
    SemanticMap,
    GAS,
    WATER,
    CRACK,
    SURVIVOR,
    DEBRIS
)
from live_data import save_rover_state


def simulate_semantic_detections(
    rover,
    semantic_map,
    mine_map
):

    def detect_nearby(
        object_type,
        object_x,
        object_y,
        confidence=1.0,
        value=None,
        detection_range=8.0,
        blocks_navigation=False
    ):

        distance = math.sqrt(
            (rover.x - object_x) ** 2
            +
            (rover.y - object_y) ** 2
        )

        if distance <= detection_range:

            semantic_map.add_or_update_detection(
                object_type,
                object_x,
                object_y,
                confidence=confidence,
                value=value
            )

            if blocks_navigation:

                mine_map.mark(
                    object_x,
                    object_y,
                    OBSTACLE
                )


    detect_nearby(
        GAS,
        11,
        11,
        confidence=1.0,
        value=450,
        detection_range=8
    )

    detect_nearby(
        WATER,
        14,
        8,
        confidence=0.95,
        detection_range=8
    )

    detect_nearby(
        CRACK,
        9,
        17,
        confidence=0.82,
        detection_range=8
    )

    detect_nearby(
        SURVIVOR,
        16,
        40,
        confidence=0.91,
        detection_range=10
    )

    detect_nearby(
        DEBRIS,
        16,
        27,
        confidence=1.0,
        value="BLOCKING_DEBRIS",
        detection_range=10,
        blocks_navigation=True
    )


def build_cost_map(
    mine_map,
    semantic_map
):

    cost_map = np.zeros(
        mine_map.grid.shape,
        dtype=float
    )

    hazard_settings = {

        "GAS": {
            "cost": 20,
            "radius": 3
        },

        "WATER": {
            "cost": 40,
            "radius": 3
        },

        "CRACK": {
            "cost": 25,
            "radius": 2
        }
    }

    for obj in semantic_map.get_objects():

        object_type = obj["type"]

        if object_type not in hazard_settings:

            continue

        settings = hazard_settings[
            object_type
        ]

        hazard_cost = settings[
            "cost"
        ]

        radius = settings[
            "radius"
        ]

        center_x = int(
            round(obj["x"])
        )

        center_y = int(
            round(obj["y"])
        )

        for y in range(
            center_y - radius,
            center_y + radius + 1
        ):

            for x in range(
                center_x - radius,
                center_x + radius + 1
            ):

                if (
                    x < 0
                    or x >= mine_map.width
                    or y < 0
                    or y >= mine_map.height
                ):

                    continue

                distance = math.sqrt(
                    (x - center_x) ** 2
                    +
                    (y - center_y) ** 2
                )

                if distance <= radius:

                    distance_factor = (
                        1
                        -
                        distance / (radius + 1)
                    )

                    added_cost = (
                        hazard_cost
                        *
                        distance_factor
                    )

                    cost_map[y, x] = max(
                        cost_map[y, x],
                        added_cost
                    )

    return cost_map


environment = MineEnvironment()

mine_map = MineMap()

semantic_map = SemanticMap()

rover = Rover(
    x=5,
    y=5,
    theta=0
)

tof = SimulatedServoToF(
    environment
)

survivor_alerted = False

plt.ion()


for step in range(500):

    print("\n------------------")

    print(
        "STEP:",
        step
    )

    print(
        "ROVER POSE:",
        (
            round(rover.x, 1),
            round(rover.y, 1),
            round(rover.theta, 1)
        )
    )

    readings = tof.scan(
        rover
    )

    mine_map.update_from_tof(
        rover,
        readings
    )

    simulate_semantic_detections(
        rover,
        semantic_map,
        mine_map
    )

    cost_map = build_cost_map(
        mine_map,
        semantic_map
    )


    survivors = []

    for obj in semantic_map.get_objects():

        if obj["type"] == SURVIVOR:

            survivors.append(obj)


    if survivors and not survivor_alerted:

        survivor = survivors[0]

        print("\n================================")
        print("SURVIVOR DETECTED!")
        print("================================")

        print(
            "Survivor location:",
            (
                round(survivor["x"], 1),
                round(survivor["y"], 1)
            )
        )

        print(
            "Survivor location saved to semantic map."
        )

        print(
            "Continuing autonomous exploration."
        )

        survivor_alerted = True


    rover_position = (
        int(round(rover.x)),
        int(round(rover.y))
    )

    frontiers = find_frontiers(
        mine_map.grid
    )

    print(
        "Frontiers found:",
        len(frontiers)
    )

    if not frontiers:

        print(
            "No more unexplored areas!"
        )

        mine_map.show(
            rover,
            cost_map=cost_map,
            semantic_map=semantic_map
        )

        break


    frontiers = sort_frontiers(
        frontiers,
        rover_position,
        mine_map.grid
    )

    path = None

    goal = None


    for frontier in frontiers[:100]:

        test_path = astar(
            mine_map.grid,
            rover_position,
            frontier,
            cost_map
        )

        if test_path is not None:

            path = test_path

            goal = frontier

            break


    if path is None:

        print(
            "No reachable frontier."
        )

        print(
            "Turning to scan a new direction..."
        )

        rover.turn(
            45
        )

        mine_map.show(
            rover,
            cost_map=cost_map,
            semantic_map=semantic_map
        )

        continue


    print(
        "Exploration goal:",
        goal
    )

    print(
        "Path length:",
        len(path)
    )


    if len(path) > 1:

        next_x, next_y = path[1]

        dx = (
            next_x
            -
            rover.x
        )

        dy = (
            next_y
            -
            rover.y
        )

        angle = math.degrees(
            math.atan2(
                dy,
                dx
            )
        )

        rover.theta = (
            angle
            %
            360
        )


        if environment.is_wall(
            next_x,
            next_y
        ):

            print(
                "OBSTACLE DETECTED!"
            )

            print(
                "Movement blocked."
            )

            mine_map.mark(
                next_x,
                next_y,
                OBSTACLE
            )

            rover.turn(
                45
            )


        else:

            rover.x = next_x

            rover.y = next_y

            print(
                "Moving to:",
                (
                    next_x,
                    next_y
                )
            )


    else:

        print(
            "Already at frontier."
        )

        rover.turn(
            45
        )


    mine_map.show(
        rover,
        path=path,
        goal=goal,
        cost_map=cost_map,
        semantic_map=semantic_map
    )
    save_rover_state(
    rover=rover,
    mine_map=mine_map,
    semantic_map=semantic_map,
    cost_map=cost_map,
    path=path,
    goal=goal,
    mission_status="EXPLORING"
    )


plt.ioff()

plt.show()