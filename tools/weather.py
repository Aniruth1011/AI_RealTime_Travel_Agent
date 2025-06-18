from langchain_community.utilities import SerpAPIWrapper 
from langchain_core.tools import tool 
from typing import Union
from datetime import date, datetime
import os 

@tool 
def get_current_weather(target_location : str):

    """
    Retrieves the current weather conditions for a specified location using SerpAPI.

    This tool performs a real-time Google search to obtain up-to-date weather 
    information such as temperature, humidity, wind, and general conditions 
    (e.g., sunny, cloudy, raining) for any given city, region, or country. It is 
    particularly useful for users planning travel, outdoor activities, or simply 
    checking the weather in another location.

    Parameters:
    - target_location (str): The name of the city, town, region, or country 
    for which the current weather data is to be fetched.

    Returns:
    - str: A string containing the current weather information as returned 
    by the search result.
    """
    
    google_search = SerpAPIWrapper(serpapi_api_key=os.environ["SERP_API_KEY"])

    search_query = f"What is the current weather in {target_location}."

    current_weather = google_search.run(search_query)

    return current_weather 

@tool 
def get_weather_forecast(location : str , time : Union[str, date, datetime]) : 

    """
    Fetches the weather forecast for a given location and time using SerpAPI search results.

    Parameters:
        location (str): The name of the location for which the weather forecast is required.
        time (Union[str, date, datetime]): The time or date (as a string, date, or datetime object) for which the weather forecast is to be retrieved.

    Returns:
        str: The predicted weather conditions as retrieved from the search results.

    Note:
        This function constructs a natural language query and uses the SerpAPIWrapper to fetch weather predictions via a Google search.
    """


    search_query = (
        f"Detailed weather forecast for {location} on {time}, including temperature, chance of rain, "
        f"humidity, wind speed, UV index, sunrise and sunset times, and overall weather conditions"
    )

    google_search = SerpAPIWrapper(serpapi_api_key=os.environ["SERP_API_KEY"])


    predicted_weather = google_search.run(search_query)

    return predicted_weather 