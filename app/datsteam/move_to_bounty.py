from config import url, headers
import requests
import math


# Initialize data
response = requests.post(url, headers=headers)
response_data = response.json()
transports = response_data.get("transports", [])
bounties = response_data.get("bounties", [])


def calculate_distance(transport, bounty):
    return math.sqrt((transport['x'] - bounty['x']) ** 2 + (transport['y'] - bounty['y']) ** 2) # Edit for using bounty

def calculate_acceleration(transport, bounty):
    dx = bounty['x'] - transport['x']
    dy = bounty['y'] - transport['y']
    magnitude = math.sqrt(dx**2 + dy**2)
    
    if magnitude != 0:
        return {"x": dx / magnitude, "y": dy / magnitude}
    else:
        return {"x": 0, "y": 0}

while True:
    closest_bounties = {}
    for transport in transports:
        closest_bounty = None
        min_distance = float('inf')

        for bounty in bounties:
            distance = calculate_distance(transport, bounty)
            if distance < min_distance:
                min_distance = distance
                closest_bounty = bounty

        transport['acceleration'] = calculate_acceleration(transport, closest_bounty)

        closest_bounties[transport['id']] = closest_bounty

    updated_data = {
        "transports": [
            {
                "id": transport['id'],
                "acceleration": transport['acceleration'],
                "activateShield": False,
                "attack": transport['acceleration']
            }
            for transport in transports
        ]
    }
    response = requests.post(url, json=updated_data, headers=headers)