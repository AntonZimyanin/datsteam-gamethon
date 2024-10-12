import requests
from config import url, headers 

class HttpClient:
    def __init__(self):
        self.post_request({})

    def post_request(self, json_data):
        response = requests.post(url, json=json_data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()

            self.transports = response_data.get("transports")
            self.bounties = response_data.get("bounties")
            self.max_speed = response_data.get("maxSpeed")  
            self.max_acceleration = response_data.get("maxAccel") 
            self.transport_radius = response_data.get("transportRadius")

