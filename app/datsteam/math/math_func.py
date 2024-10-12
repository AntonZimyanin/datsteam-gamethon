import math


def calculate_distance(transport, target):
    """Calculate the Euclidean distance between a transport and a target (bounty or enemy)."""
    return math.sqrt((transport['x'] - target['x']) ** 2 + (transport['y'] - target['y']) ** 2)


def calculate_direction(transport, target):
    """Calculate the direction vector to set the acceleration toward the target (bounty or enemy)."""
    dx = target['x'] - transport['x']
    dy = target['y'] - transport['y']
    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    
    # Normalize the direction and scale by a factor if desired (e.g., max acceleration)
    if magnitude != 0:
        return {"x": dx / magnitude, "y": dy / magnitude}
    else:
        return {"x": 0, "y": 0}