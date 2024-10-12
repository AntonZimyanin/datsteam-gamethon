from math_func import *
from http_client import HttpClient

client = HttpClient()


while True:
    closest_bounties = {}
    for transport in client.transports:
        best_bounty = None
        min_value = float('inf')

        for bounty in client.bounties:
            value_of_bounty = calculate_distance(transport, bounty)
            if value_of_bounty < min_value:
                min_value = value_of_bounty
                best_bounty = bounty

        transport['acceleration'] = calculate_acceleration(transport, best_bounty, client.max_acceleration)

        closest_bounties[transport['id']] = best_bounty
        print(f"{transport['id']} x: {transport['x']}, y: {transport['y']}, bounty x: {best_bounty['x']}, y: {best_bounty['y']}")
        print(f"Acceleration {transport['acceleration']} {transport['selfAcceleration']} Anomali {transport['anomalyAcceleration']}")

    updated_data = {
        "transports": [
            {
                "id": transport['id'],
                "acceleration": transport['acceleration'],
            }
            for transport in client.transports
        ]
    }
    client.post_request(updated_data)
    print("  ")
