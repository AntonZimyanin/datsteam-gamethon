import math

def calculate_distance(transport, bounty):
    distance = math.sqrt((transport['x'] - bounty['x']) ** 2 + (transport['y'] - bounty['y']) ** 2)
    points = bounty['points']
    return distance / points 

def calculate_acceleration(transport, bounty, max_acceleration):
    dx = bounty['x'] - transport['x']
    dy = bounty['y'] - transport['y']
    adx = transport['anomalyAcceleration']['x']
    ady = transport['anomalyAcceleration']['y']
    
    magnitude = math.sqrt(dx**2 + dy**2) 

    
    if magnitude != 0:
        return {"x": dx / magnitude * max_acceleration - adx, "y": dy / magnitude * max_acceleration - ady}
    else:
        return {"x": 0, "y": 0}
    