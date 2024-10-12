from math_func import calculate_distance, calculate_acceleration
from http_client import HttpClient

client = HttpClient()


while True:
    closest_bounties = {}
    for transport in client.transports:
        closest_bounty = None
        min_distance = float('inf')

        for bounty in client.bounties:
            distance = calculate_distance(transport, bounty)
            if distance < min_distance:
                min_distance = distance
                closest_bounty = bounty

        transport['acceleration'] = calculate_acceleration(transport, closest_bounty, client.max_acceleration)

        closest_bounties[transport['id']] = closest_bounty

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
    print(client.transports[0]['id'])
    print(client.transports[0]['acceleration'])
