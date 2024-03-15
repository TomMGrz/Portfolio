'''200 OK: Successful request, the response contains the requested data.
201 Created: Successful creation of a new resource.
400 Bad Request: The server cannot process the request due to malformed syntax or invalid data.
404 Not Found: The requested resource could not be found on the server.
500 Internal Server Error: Indicates a server-side error occurred while processing the request.
'''
import os
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = os.getenv('BASE_URL', 'fallback-base-url')

class WeatherApp():

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}

    def get(self):
            response = requests.get(BASE_URL + '/weather/')
            return response.json()
    
    def post(self, location):
            response = requests.post(BASE_URL + f'/weather/{location}', headers=self.headers)
            return response.json()
        
    def patch(self):
            response = requests.patch(BASE_URL + f'/weather', headers=self.headers)
            return response.json()
        
    def delete(self,location):
            response = requests.delete(BASE_URL + f'/weather/{location}')
            return response.json()

