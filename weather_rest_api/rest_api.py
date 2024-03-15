import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource
import mysql.connector 
import requests


load_dotenv()

app = Flask(__name__)
api = Api(app)

DB_USER = os.getenv('DB_USER', 'fallback-user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'fallback-password')
DB_HOST = os.getenv('DB_HOST', 'fallback-host')
DB_NAME = os.getenv('DB_NAME', 'fallback-db-name')
DB_AUTH_PLUGIN = os.getenv('DB_AUTH_PLUGIN', 'fallback-auth-plugin')
API_KEY = os.getenv('API_KEY', 'fallback-api-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

def get_connection_to_db():
    connection = mysql.connector.connect(
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        database = DB_NAME,
        auth_plugin = DB_AUTH_PLUGIN)
    return connection 

class Weather(Resource):
    
    def get(self):
        connection = get_connection_to_db()
        cursor = connection.cursor()
        query = 'SELECT * FROM weather;'

        cursor.execute(query)
        data_list = []
        for row in cursor:
            data_list.append(
                f"\nLocation: {row[1]}\n"
                f"Current temperature: {row[2]}\n"
                f"Max Temperature: {row[3]}\n"
                f"Min Temperature: {row[4]}\n"
                f"Feelslike: {row[5]}\n"
                f"Wind Speed(kph): {row[6]}\n"
                f"UV index: {row[7]}\n\n"
            )

        connection.close()
        return "".join(data_list)

    def post(self, location):
        api_key = API_KEY
        current_base_url = 'http://api.weatherapi.com/v1/current.json'
        current_params = {'key': api_key, 'q': location}

        forecast_base_url = 'http://api.weatherapi.com/v1/forecast.json'
        forecast_params = {'key': api_key, 'q': location, 'days': 1, 'aqi': 'no', 'alerts': 'no'}

        connection = get_connection_to_db()
        cursor = connection.cursor()

        check_query = 'SELECT location FROM weather WHERE location = %(location)s'
        cursor.execute(check_query, {'location': location})
        existing_location = cursor.fetchone()

        if existing_location:
            connection.close()
            return f'Location already exists in the database: {location}', 400

        current_response = requests.get(current_base_url, params=current_params)
        forecast_response = requests.get(forecast_base_url, params=forecast_params)

        if current_response.status_code == 200 and forecast_response.status_code == 200:
            current_weather_data = current_response.json()
            forecast_weather_data = forecast_response.json()
            current_temp = current_weather_data['current']['temp_c']
            current_feelslike = current_weather_data['current']['feelslike_c']
            current_wind = current_weather_data['current']['wind_kph']
            current_uv = current_weather_data['current']['uv']

            forecast_data_list = forecast_weather_data['forecast']['forecastday']
            max_temp = forecast_data_list[0]['day']['maxtemp_c']
            min_temp = forecast_data_list[0]['day']['mintemp_c']  

            data = {'location': location,
                    'current_temp': current_temp,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'current_feelslike': current_feelslike,
                    'current_wind': current_wind,
                    'current_uv': current_uv
                    }

            table_query = '''INSERT INTO weather (location, current_temp, max_temp, min_temp, current_feelslike, current_wind, current_uv) VALUES (%(location)s, %(current_temp)s, %(max_temp)s, %(min_temp)s, %(current_feelslike)s, %(current_wind)s, %(current_uv)s)'''

            cursor.execute(table_query, data)
            connection.commit()
            connection.close()
            return data, 201

        connection.close()
        return 'Error fetching weather data.', 500

    def delete(self, location):
        connection = get_connection_to_db()
        cursor = connection.cursor()

        check_query = 'SELECT location FROM weather WHERE location = %(location)s'
        cursor.execute(check_query, {'location': location})
        existing_location = cursor.fetchone()

        if existing_location:
            del_query = "DELETE FROM weather WHERE location = %(location)s"
            cursor.execute(del_query, {'location': location})

            connection.commit()
            connection.close()
            return f'Successfully deleted location: {location}', 200
        else:
            connection.close()
            return f'Location not found: {location}', 404
            
    def patch(self):
        connection = get_connection_to_db()
        cursor = connection.cursor()
        api_key = API_KEY
        current_base_url = 'https://api.weatherapi.com/v1/current.json'
        forecast_base_url = 'http://api.weatherapi.com/v1/forecast.json'

        location_query = 'SELECT * FROM weather'
        
        cursor.execute(location_query)

        location_list = []
        for column in cursor:
            location_list.append(column[1])

        for location in location_list:
            current_params = {'key': api_key, 'q': location}  
            forecast_params = {'key': api_key, 'q': location, 'days': 1, 'aqi': 'no', 'alerts': 'no'}

            current_response = requests.get(current_base_url, params=current_params)
            forecast_response = requests.get(forecast_base_url, params=forecast_params)
            if current_response.status_code == 200 and forecast_response.status_code == 200:
                current_weather_data = current_response.json()
                forecast_weather_data = forecast_response.json()
                current_temp = current_weather_data['current']['temp_c']
                current_feelslike = current_weather_data['current']['feelslike_c']
                current_wind = current_weather_data['current']['wind_kph']
                current_uv = current_weather_data['current']['uv']

                forecast_data_list = forecast_weather_data['forecast']['forecastday']
                max_temp = forecast_data_list[0]['day']['maxtemp_c']
                min_temp = forecast_data_list[0]['day']['mintemp_c']  

                data = {'location': location,
                        'current_temp': current_temp,
                        'max_temp': max_temp,
                        'min_temp': min_temp,
                        'current_feelslike': current_feelslike,
                        'current_wind': current_wind,
                        'current_uv': current_uv}

                patch_query = '''
                    UPDATE weather SET 
                    current_temp = %(current_temp)s, 
                    max_temp = %(max_temp)s, 
                    min_temp = %(min_temp)s, 
                    current_feelslike = %(current_feelslike)s, 
                    current_wind = %(current_wind)s, 
                    current_uv = %(current_uv)s WHERE location = %(location)s'''

                cursor.execute(patch_query, data)
            else:
                return f'Error updating the data, try again later', 500
        connection.commit()
        connection.close()
        return 'Updated data for all locations', 200

        


api.add_resource(Weather, "/weather/","/weather/<string:location>")       

app.run(debug = DEBUG) 