from app.datsteam.http.http_client import HttpClient


def main(): 
    client = HttpClient()
    resp = client.post_request()        
        