import requests
from config import url, headers 

class HttpClient:
    def __init__(self):
        response_data = self.post_request({})
        
        self.transports = response_data.get("transports")
        self.bounties = response_data.get("bounties")
        self.max_speed = response_data.get("maxSpeed")  
        self.max_acceleration = response_data.get("maxAccel") 

    def post_request(self, json_data):
        response = requests.post(url, json=json_data, headers=headers)
        response_data = response.json()

        return response_data 

