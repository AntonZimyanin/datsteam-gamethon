import math
from typing import Callable, Dict, Any


def calculate_distance(transport: Dict[str, Any], to_object: Dict[str, Any]) -> float:
    return math.sqrt((transport['x'] - to_object['x']) ** 2 + (transport['y'] - to_object['y']) ** 2)


def calculate_object_priority(transport: Dict[str, Any], to_object: Dict[str, Any], distance_callback: Callable[[Dict[str, Any], Dict[str, Any]], float]) -> float:
    distance = distance_callback(transport, to_object)
    points = to_object['points']

    return distance / points


def calculate_acceleration(transport: Dict[str, Any], bounty: Dict[str, Any], max_acceleration: float) -> Dict[str, float]:
    dx = bounty['x'] - transport['x']
    dy = bounty['y'] - transport['y']
    adx = transport['anomalyAcceleration']['x']
    ady = transport['anomalyAcceleration']['y']

    magnitude = math.sqrt(dx**2 + dy**2)

    if magnitude != 0:
        return {"x": dx / magnitude * max_acceleration - adx, "y": dy / magnitude * max_acceleration - ady}
    else:
        return {"x": 0, "y": 0}
