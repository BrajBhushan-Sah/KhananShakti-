import os
import json
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="Mine Rover Mission Control",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st_autorefresh(
    interval=500,
    limit=None,
    key="rover_dashboard_refresh"
)


STATE_FILE = "rover_state.json"


def load_rover_state():

    if not os.path.exists(
        STATE_FILE
    ):

        return None


    try:

        with open(
            STATE_FILE,
            "r"
        ) as file:

            return json.load(
                file
            )

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return None


def get_demo_state():

    grid = np.full(
        (60, 60),
        -1
    )

    grid[5:55, 5:55] = 0

    grid[5:55, 5] = 1
    grid[5:55, 54] = 1

    grid[5, 5:55] = 1
    grid[54, 5:55] = 1


    return {

        "rover": {

            "x": 18.0,

            "y": 15.0,

            "theta": 35.0

        },

        "grid": grid.tolist(),

        "cost_map": None,

        "path": [],

        "goal": None,

        "semantic_objects": [],

        "mission_status": "WAITING FOR SIMULATION"

    }


state = load_rover_state()


if state is None:

    state = get_demo_state()


rover = state["rover"]

grid = np.array(
    state["grid"]
)


cost_map = state.get(
    "cost_map"
)


if cost_map is not None:

    cost_map = np.array(
        cost_map
    )


path = state.get(
    "path",
    []
)


goal = state.get(
    "goal"
)


semantic_objects = state.get(
    "semantic_objects",
    []
)


mission_status = state.get(
    "mission_status",
    "EXPLORING"
)


height, width = grid.shape


st.markdown(
    """
    <style>

    .main {
        background-color: #0b1015;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    .dashboard-title {
        font-size: 34px;
        font-weight: 700;
        color: white;
        line-height: 1.3;
        padding-top: 8px;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        color: #9aa4ad;
        font-size: 15px;
        margin-top: 0;
    }

    .status-card {
        background-color: #141b22;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #26313b;
        margin-bottom: 12px;
    }

    .status-title {
        color: #9aa4ad;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .status-value {
        color: white;
        font-size: 26px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="dashboard-title">
    AUTONOMOUS MINE SAFETY ROVER
    </div>

    <div class="dashboard-subtitle">
    MISSION CONTROL • REAL-TIME SEMANTIC MONITORING
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()


map_column, panel_column = st.columns(
    [3.2, 1]
)


with map_column:

    fig = go.Figure()


    fig.add_trace(

        go.Heatmap(

            z=grid,

            colorscale=[

                [0.00, "#111820"],

                [0.32, "#111820"],

                [0.33, "#2f786e"],

                [0.65, "#2f786e"],

                [0.66, "#f1cd50"],

                [1.00, "#f1cd50"]

            ],

            zmin=-1,

            zmax=1,

            showscale=False,

            hoverinfo="skip"

        )

    )


    if cost_map is not None:

        hazard_overlay = np.where(

            cost_map > 0,

            cost_map,

            np.nan

        )


        maximum_cost = np.nanmax(
            hazard_overlay
        )


        if np.isnan(
            maximum_cost
        ):

            maximum_cost = 1


        fig.add_trace(

            go.Heatmap(

                z=hazard_overlay,

                colorscale=[

                    [
                        0,
                        "rgba(0,0,0,0)"
                    ],

                    [
                        0.25,
                        "rgba(255,230,0,0.25)"
                    ],

                    [
                        0.55,
                        "rgba(255,140,0,0.40)"
                    ],

                    [
                        1,
                        "rgba(255,0,0,0.60)"
                    ]

                ],

                zmin=0,

                zmax=maximum_cost,

                showscale=False,

                hoverinfo="skip"

            )

        )


    marker_settings = {

        "GAS": {

            "symbol": "square",

            "size": 15,

            "color": "#ff4b4b"

        },

        "WATER": {

            "symbol": "circle",

            "size": 15,

            "color": "#2196f3"

        },

        "CRACK": {

            "symbol": "triangle-up",

            "size": 16,

            "color": "#ff9800"

        },

        "DEBRIS": {

            "symbol": "diamond",

            "size": 14,

            "color": "#b0bec5"

        },

        "SURVIVOR": {

            "symbol": "star",

            "size": 20,

            "color": "#00e676"

        }

    }


    for obj in semantic_objects:

        obj_type = obj.get(
            "type"
        )


        if obj_type not in marker_settings:

            continue


        settings = marker_settings[
            obj_type
        ]


        fig.add_trace(

            go.Scatter(

                x=[
                    obj["x"]
                ],

                y=[
                    obj["y"]
                ],

                mode="markers",

                name=obj_type,

                marker=dict(

                    symbol=settings[
                        "symbol"
                    ],

                    size=settings[
                        "size"
                    ],

                    color=settings[
                        "color"
                    ],

                    line=dict(

                        color="white",

                        width=1

                    )

                ),

                hovertemplate=(

                    f"<b>{obj_type}</b>"

                    +

                    f"<br>X: {obj['x']:.1f}"

                    +

                    f"<br>Y: {obj['y']:.1f}"

                    +

                    "<extra></extra>"

                )

            )

        )


    if len(path) > 0:

        path_x = [

            point[0]

            for point in path

        ]


        path_y = [

            point[1]

            for point in path

        ]


        fig.add_trace(

            go.Scatter(

                x=path_x,

                y=path_y,

                mode="lines",

                name="ROVER PATH",

                line=dict(

                    color="#00d4ff",

                    width=2,

                    dash="dot"

                )

            )

        )


    if goal is not None:

        fig.add_trace(

            go.Scatter(

                x=[
                    goal[0]
                ],

                y=[
                    goal[1]
                ],

                mode="markers",

                name="GOAL",

                marker=dict(

                    symbol="x",

                    size=14,

                    color="#ffffff"

                )

            )

        )


    fig.add_trace(

        go.Scatter(

            x=[
                rover["x"]
            ],

            y=[
                rover["y"]
            ],

            mode="markers",

            name="ROVER",

            marker=dict(

                symbol="triangle-up",

                size=20,

                color="#ffffff",

                line=dict(

                    color="#00d4ff",

                    width=3

                )

            ),

            hovertemplate=(

                "<b>ROVER</b>"

                +

                f"<br>X: {rover['x']:.1f}"

                +

                f"<br>Y: {rover['y']:.1f}"

                +

                f"<br>Heading: {rover['theta']:.0f}°"

                +

                "<extra></extra>"

            )

        )

    )


    fig.update_layout(

        title=dict(

            text="LIVE SEMANTIC MINE MAP",

            font=dict(

                size=20,

                color="white"

            )

        ),

        paper_bgcolor="#141b22",

        plot_bgcolor="#101820",

        height=720,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=-0.16,

            xanchor="center",

            x=0.5,

            font=dict(

                color="white"

            )

        ),

        xaxis=dict(

            title="X POSITION",

            gridcolor="#26313b",

            zeroline=False,

            color="#9aa4ad",

            range=[0, width]

        ),

        yaxis=dict(

            title="Y POSITION",

            gridcolor="#26313b",

            zeroline=False,

            color="#9aa4ad",

            range=[0, height],

            scaleanchor="x",

            scaleratio=1

        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


with panel_column:

    st.markdown(

        f"""

        <div class="status-card">

        <div class="status-title">

        MISSION STATUS

        </div>

        <div class="status-value">

        {mission_status}

        </div>

        </div>

        """,

        unsafe_allow_html=True

    )


    st.markdown(

        """

        <div class="status-card">

        <div class="status-title">

        ROVER POSITION

        </div>

        """,

        unsafe_allow_html=True

    )


    position_1, position_2 = st.columns(
        2
    )


    position_1.metric(

        "X",

        f"{rover['x']:.1f}"

    )


    position_2.metric(

        "Y",

        f"{rover['y']:.1f}"

    )


    st.metric(

        "HEADING",

        f"{rover['theta']:.0f}°"

    )


    st.markdown(

        "</div>",

        unsafe_allow_html=True

    )


    gas_objects = [

        obj

        for obj in semantic_objects

        if obj.get("type") == "GAS"

    ]


    gas_value = 0


    if len(gas_objects) > 0:

        gas_value = gas_objects[0].get(
            "value",
            450
        )


    st.markdown(

        f"""

        <div class="status-card">

        <div class="status-title">

        GAS MONITOR

        </div>

        <div class="status-value">

        {gas_value} ppm

        </div>

        </div>

        """,

        unsafe_allow_html=True

    )


    if len(gas_objects) > 0:

        st.warning(
            "⚠ GAS DETECTED"
        )

    else:

        st.success(
            "● GAS LEVEL NORMAL"
        )


    st.markdown(

        """

        <div class="status-card">

        <div class="status-title">

        DETECTIONS

        </div>

        </div>

        """,

        unsafe_allow_html=True

    )


    object_types = [

        "SURVIVOR",

        "GAS",

        "WATER",

        "CRACK",

        "DEBRIS"

    ]


    detection_rows = []


    for object_type in object_types:

        count = sum(

            1

            for obj in semantic_objects

            if obj.get("type") == object_type

        )


        detection_rows.append(

            {

                "TYPE": object_type,

                "COUNT": count

            }

        )


    detection_data = pd.DataFrame(

        detection_rows

    )


    st.dataframe(

        detection_data,

        use_container_width=True,

        hide_index=True

    )


    st.subheader(

        "SENSOR STATUS"

    )


    if os.path.exists(
        STATE_FILE
    ):

        st.success(
            "● SIMULATION ONLINE"
        )

    else:

        st.warning(
            "● WAITING FOR SIMULATION"
        )


    st.success(
        "● ToF / LiDAR ONLINE"
    )


    st.success(
        "● GAS SENSOR ONLINE"
    )


    st.success(
        "● AI VISION ONLINE"
    )


    st.info(
        "● ESP32 CONNECTION READY"
    )


st.divider()


explored_cells = np.sum(
    grid == 0
)


known_cells = np.sum(
    grid != -1
)


if known_cells > 0:

    explored_percentage = (

        explored_cells

        /

        known_cells

        *

        100

    )

else:

    explored_percentage = 0


obstacle_count = np.sum(
    grid == 1
)


hazard_count = sum(

    1

    for obj in semantic_objects

    if obj.get("type")

    in [

        "GAS",

        "WATER",

        "CRACK"

    ]

)


survivor_count = sum(

    1

    for obj in semantic_objects

    if obj.get("type") == "SURVIVOR"

)


footer_1, footer_2, footer_3, footer_4 = st.columns(
    4
)


footer_1.metric(

    "EXPLORED AREA",

    f"{explored_percentage:.0f}%"

)


footer_2.metric(

    "OBSTACLES",

    int(obstacle_count)

)


footer_3.metric(

    "HAZARDS",

    hazard_count

)


footer_4.metric(

    "SURVIVORS",

    survivor_count

)


st.caption(

    "LIVE DATA • AUTONOMOUS MINE SAFETY ROVER MISSION CONTROL"

)