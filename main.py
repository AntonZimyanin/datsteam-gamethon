import requests
import math
import time

url = 'https://games-test.datsteam.dev/play/magcarp/player/move'
auth_token = '670516cb9d5a9670516cb9d5ae'
headers = {
    'X-Auth-Token': auth_token,
}


data = {
    "transports": []
}


def postRequest(jsonData=data):
    """
    Send a POST request to the server with the provided JSON data.
    """
    headers = {
        'X-Auth-Token': auth_token,
    }

    return requests.post(url, json=jsonData, headers=headers)

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

# Function to handle weak enemy actions
def enemy_action(transport, enemies):
    for enemy in enemies:
        _is_enemy = is_enemy(transport, enemy)
        _is_weak_enemy = is_weak_enemy(transport, enemy)
        
        if _is_enemy:
            transport_id = transport['id']
            
            new_data = {
                "transports": [
                    {
                        "activateShield": True,
                        "id": transport_id
                    }
                ]
            }
            
            postRequest(new_data)
            
            print("Shield activated for transport ID:", transport_id)
            
        if _is_weak_enemy:
            # Calculate the direction toward the weak enemy and move the transport toward it
            direction = calculate_direction(transport, enemy)
            transport['acceleration'] = direction
            
            # Send updated movement with the acceleration towards the weak enemy (ramming)
            new_data = {
                "transports": [
                    {
                        "id": transport['id'],
                        "acceleration": transport['acceleration'],
                        "activateShield": False,  # Can decide to keep shield off or on
                        "attack": transport['acceleration']  # Attack in the direction of movement
                    }
                ]
            }
            
            postRequest(new_data)
            
            print(f"Ramming weak enemy with transport ID: {transport['id']}, moving in direction: {transport['acceleration']}")
        
        if False == _is_weak_enemy: 
            
            direction = calculate_direction(transport, enemy)
            
            
# Run the code 100 times with a 0.4-second delay
for _ in range(100):
    response = postRequest()

    # Parse the JSON response
    response_data = response.json()

    # Extract "transports", "bounties", and "enemies"
    transports = response_data.get("transports", [])
    bounties = response_data.get("bounties", [])
    enemies = response_data.get("enemies", [])

    closest_bounties = {}

    # Iterate over each transport to find the closest bounty and adjust their acceleration
    for transport in transports:
        closest_bounty = None
        min_distance = float('inf')  # Initialize with a large value

        for bounty in bounties:
            distance = calculate_distance(transport, bounty)
            if distance < min_distance:
                min_distance = distance
                closest_bounty = bounty

        # Calculate acceleration toward the closest bounty
        direction = calculate_direction(transport, closest_bounty)
        transport['acceleration'] = direction

        closest_bounties[transport['id']] = closest_bounty

    # Prepare the updated data for the transport move request
    updated_data = {
        "transports": [
            {
                "id": transport['id'],
                "acceleration": transport['acceleration'],
                "activateShield": False,  # Assuming you may want to deactivate the shield while moving
                "attack": transport['acceleration']  # Attack in the direction of movement, if desired
            }
            for transport in transports
        ]
    }

    # Make the updated move request
    response = postRequest(updated_data)

    # Print the transport coordinates and the closest bounty
    for transport in transports:
        transport_id = transport['id']
        transport_x = transport['x']
        transport_y = transport['y']
        closest_bounty = closest_bounties[transport_id]
        acceleration = transport['acceleration']

        print(f"Transport ID: {transport_id} - Coordinates: ({transport_x}, {transport_y}) - Closest Bounty: {closest_bounty} - New Acceleration: {acceleration}")

    # Handle enemy actions, including shield activation and ramming weak enemies
    for transport in transports:
        enemy_action(transport, enemies)

    # Wait for 0.4 seconds before the next iteration
    time.sleep(0.4)
