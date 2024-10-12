from app.datsteam.HttpClient import HttpClient


def main(): 
    client = HttpClient()
    
    while (True): 
        resp = client.postRequest()
        
        transports = resp.get("transports", [])
        bounties = resp.get("bounties", [])
        enemies = resp.get("enemies", [])
        
        