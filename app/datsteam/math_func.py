import math

def calculate_distance(transport, bounty):
    return math.sqrt((transport['x'] - bounty['x']) ** 2 + (transport['y'] - bounty['y']) ** 2) # Edit for using bounty

def calculate_acceleration(transport, bounty, max_acceleration):
    dx = bounty['x'] - transport['x']
    dy = bounty['y'] - transport['y']
    magnitude = math.sqrt(dx**2 + dy**2) 
    
    if magnitude != 0:
        return {"x": dx / magnitude * max_acceleration, "y": dy / magnitude * max_acceleration}
    else:
        return {"x": 0, "y": 0}