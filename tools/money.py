from langchain_community.utilities import SerpAPIWrapper 
from langchain_core.tools import tool 
import os 

@tool 
def get_exchange_rate(client_country: str, destination_country: str):
    """
    Retrieves the real-time currency exchange rate between the currency of the 
    client's country and the currency of the destination country.

    This tool leverages SerpAPI (Google Search API) to perform a search query 
    that fetches the most recent exchange rate information. It is useful in 
    scenarios where the user is planning to travel or send/receive money and 
    needs accurate conversion rates between two countries' currencies.

    Parameters:
    - client_country (str): The name of the country where the client resides or 
      holds the base currency.
    - destination_country (str): The name of the country the client is traveling to, 
      or the country whose currency they want to convert into.

    Returns:
    - str: A string representation of the exchange rate information retrieved 
      from the search results.
    """
    google_search = SerpAPIWrapper(serpapi_api_key=os.environ["SERP_API_KEY"])

    search_query = f"Currency exchange rate from {client_country} currency to {destination_country}"

    exchange_rate_result = google_search.run(search_query)

    return exchange_rate_result

@tool 
def convert_currency(amount_in_foreign_currency: float, exchange_rate: float):
    """
    Converts a given amount in foreign currency to the equivalent value 
    in the local (client's) currency using a specified exchange rate.

    This tool is intended to help users understand how much a specified 
    amount in the destination currency is worth in their local currency, 
    based on the most recent exchange rate.

    Parameters:
    - amount_in_foreign_currency (float): The amount of money expressed in the 
      foreign or destination currency.
    - exchange_rate (float): The exchange rate used for conversion. This should 
      reflect the value of 1 unit of the foreign currency in terms of the 
      local currency.

    Returns:
    - float: The equivalent amount in the local (client's) currency.
    """
    converted_amount = amount_in_foreign_currency * exchange_rate

    return converted_amount
