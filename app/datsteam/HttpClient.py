import requests


class HttpClient: 
    __headers = { 'X-Auth-Token': "" }
    __base_url = "" 
    

    def __init__(self, uri = ''):
        self.uri = uri
    
    
    def postRequest(self, jsonData): 
        
        return requests.post(self.__base_url + self.uri, json=jsonData, headers=self.__headers)