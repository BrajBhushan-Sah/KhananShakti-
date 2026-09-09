import math


# ---------------------------------
# Semantic object types
# ---------------------------------

GAS = "GAS"
WATER = "WATER"
CRACK = "CRACK"
SURVIVOR = "SURVIVOR"
DEBRIS = "DEBRIS"


class SemanticMap:

    def __init__(self):

        # Stores semantic detections
        self.objects = []


    # ---------------------------------
    # Add a semantic detection
    # ---------------------------------

    def add_detection(
        self,
        object_type,
        x,
        y,
        confidence=1.0,
        value=None
    ):

        detection = {

            "type": object_type,

            "x": float(x),

            "y": float(y),

            "confidence": float(confidence),

            "value": value

        }


        self.objects.append(
            detection
        )


    # ---------------------------------
    # Get all objects
    # ---------------------------------

    def get_objects(self):

        return self.objects


    # ---------------------------------
    # Get objects of one type
    # ---------------------------------

    def get_by_type(
        self,
        object_type
    ):

        return [

            obj

            for obj in self.objects

            if obj["type"] == object_type

        ]


    # ---------------------------------
    # Prevent duplicate detections
    # ---------------------------------

    def add_or_update_detection(
        self,
        object_type,
        x,
        y,
        confidence=1.0,
        value=None,
        merge_distance=2.0
    ):

        for obj in self.objects:

            if obj["type"] != object_type:
                continue


            distance = math.sqrt(

                (obj["x"] - x) ** 2

                +

                (obj["y"] - y) ** 2

            )


            # Existing detection nearby
            if distance < merge_distance:


                # Keep higher confidence

                if confidence > obj["confidence"]:

                    obj["x"] = float(x)

                    obj["y"] = float(y)

                    obj["confidence"] = float(
                        confidence
                    )

                    obj["value"] = value


                return


        # No nearby detection found

        self.add_detection(

            object_type,

            x,

            y,

            confidence,

            value

        )