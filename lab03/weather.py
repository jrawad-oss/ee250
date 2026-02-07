import requests
import json
# WeatherAPI key
WEATHER_API_KEY = 'c5de5e1f066c41e28cd53619260602'  # TODO: Replace with your own WeatherAPI key

def get_weather(city):
    # TODO: Build the API request URL using the base API endpoint, the API key, and the city name provided by the user.
    base_URL = "http://api.weatherapi.com/v1/current.json"
    parameters = {
        "key": WEATHER_API_KEY,
        "q": city,
    }   
    # TODO: Make the HTTP request to fetch weather data using the 'requests' library.
    response = requests.get(base_URL, params=parameters)

    # TODO: Handle HTTP status codes:
    # - Check if the status code is 200 (OK), meaning the request was successful.
    # - If not 200, handle common errors like 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), and any other relevant codes.
    
    if response.status_code == 200:
        # TODO: Parse the JSON data returned by the API. Extract and process the following information:
        # - Current temperature in Fahrenheit
        # - The "feels like" temperature
        # - Weather condition (e.g., sunny, cloudy, rainy)
        # - Humidity percentage
        # - Wind speed and direction
        # - Atmospheric pressure in mb
        # - UV Index value
        # - Cloud cover percentage
        # - Visibility in miles
        data = response.json()
        
        current = data.get("current", {})
        condition = current.get("condition", {})
        
        temp_f = current.get("temp_f")
        feelslike_f = current.get("feelslike_f")
        text = condition.get("text")
        humidity = current.get("humidity")
        wind_mph = current.get("wind_mph")
        wind_dir = current.get("wind_dir")
        pressure_mb = current.get("pressure_mb")
        uv = current.get("uv")
        cloud = current.get("cloud")
        vis_miles = current.get("vis_miles")
        # TODO: Display the extracted weather information in a well-formatted manner.
        print(f"Weather data for {city}...")
        print(f"The temperature is {temp_f} degrees farenheit")
        print(f"The weather feels like {feelslike_f} degrees farenheit")
        print(f"The weather condition is {text}")
        print(f"The humidity percentage is {humidity}")
        print(f"The wind speed is {wind_mph} mph, and the direction is {wind_dir}")
        print(f"The atmospheric pressure is {pressure_mb} mb")
        print(f"The UV index values is {uv}")
        print(f"The cloud cover percentage is {cloud}")
        print(f"The visibility is {vis_miles} miles")
    else:
        # TODO: Implement error handling for common status codes. Provide meaningful error messages based on the status code.
        print(f"Error: {response.status_code}. Something went wrong.")
        if response.status_code == 400:
            print("Error 400 (Bad Request): Parameter 'q' not provided/invalid or API request URL is invalid")
        elif response.status_code == 401:
            print("Error 401 (Unauthorized): API key not provided or invalid")
        elif response.status_code == 403:
            print("Error 403 (Forbidden): API key has been disabled or does not have access to resource due to subscription plan")
        elif response.status_code == 404:
            print("Error 404 (Not Found): Cannot find requested WeatherAPI or city")
if __name__ == '__main__':
    # TODO: Prompt the user to input a city name.
    city = input("Enter a city name: ")

    # TODO: Call the 'get_weather' function with the city name provided by the user.
    get_weather(city)
    pass
