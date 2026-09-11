import json
import os
import time
import uuid


STATE_FILE = "rover_state.json"


def save_rover_state(
    rover,
    mine_map,
    semantic_map,
    cost_map=None,
    path=None,
    goal=None,
    mission_status="EXPLORING"
):

    objects = semantic_map.get_objects()

    state = {

        "rover": {

            "x": float(rover.x),

            "y": float(rover.y),

            "theta": float(rover.theta)

        },

        "grid": mine_map.grid.tolist(),

        "cost_map": (

            cost_map.tolist()

            if cost_map is not None

            else None

        ),

        "path": (

            [

                [

                    float(x),

                    float(y)

                ]

                for x, y in path

            ]

            if path is not None

            else []

        ),

        "goal": (

            [

                float(goal[0]),

                float(goal[1])

            ]

            if goal is not None

            else None

        ),

        "semantic_objects": objects,

        "mission_status": mission_status

    }


    folder = os.path.dirname(

        os.path.abspath(
            STATE_FILE
        )

    )


    temp_file = os.path.join(

        folder,

        f"rover_state_{uuid.uuid4().hex}.json"

    )


    with open(

        temp_file,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            state,

            file

        )


    for _ in range(10):

        try:

            os.replace(

                temp_file,

                STATE_FILE

            )

            return

        except PermissionError:

            time.sleep(
                0.05
            )


    try:

        if os.path.exists(
            temp_file
        ):

            os.remove(
                temp_file
            )

    except OSError:

        pass