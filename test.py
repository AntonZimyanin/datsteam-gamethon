import requests
import math
import time

auth_token = '670516cb9d5a9670516cb9d5ae'
url = 'https://games-test.datsteam.dev/play/magcarp/player/move'

headers = {
    'X-Auth-Token': auth_token,
}


data = {
    "transports": [
    ]
}


def postRequest(jsonData = data): 
    
    headers = {
        'X-Auth-Token': auth_token,
    }

    return requests.post(url, json=jsonData, headers=headers)

def calculate_distance(transport, bounty):
    """Calculate the Euclidean distance between a transport and a bounty."""
    return math.sqrt((transport['x'] - bounty['x']) ** 2 + (transport['y'] - bounty['y']) ** 2)

def calculate_direction(transport, bounty):
    """Calculate the direction vector to set the acceleration toward the bounty."""
    dx = bounty['x'] - transport['x']
    dy = bounty['y'] - transport['y']
    magnitude = math.sqrt(dx**2 + dy**2)
    
    # Normalize the direction and scale by a factor if desired (e.g., max acceleration)
    if magnitude != 0:
        return {"x": dx / magnitude, "y": dy / magnitude}
    else:
        return {"x": 0, "y": 0}

# Run the code 100 times with a 0.4-second delay
for _ in range(100):

    response = postRequest()

    # Parse the JSON response
    response_data = response.json()

    # Extract "transports" and "bounties"
    transports = response_data.get("transports", [])
    bounties = response_data.get("bounties", [])

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
    # response = requests.post(url, json=updated_data, headers=headers)
    
    response = postRequest(updated_data)

    # Print the transport coordinates and the closest bounty
    for transport in transports:
        transport_id = transport['id']
        transport_x = transport['x']
        transport_y = transport['y']
        closest_bounty = closest_bounties[transport_id]
        acceleration = transport['acceleration']

        print(f"Transport ID: {transport_id} - Coordinates: ({transport_x}, {transport_y}) - Closest Bounty: {closest_bounty} - New Acceleration: {acceleration}")

    # Wait for 0.4 seconds before the next iteration
    time.sleep(0.4)



def activate_shield_if_needed(transport, enemies):
    for enemy in enemies:
        distance = calculate_distance(transport, enemy)
        transport_id = transport['id']
        print(f"Расстояние до врага: {distance}")
        
        if distance <= 200:
            postRequest(data={id: transport_id})
            transport["activateShield"] = True
            print("Щит активирован!")
            break  # Если расстояние меньше 200, щит активируется, и больше не проверяем