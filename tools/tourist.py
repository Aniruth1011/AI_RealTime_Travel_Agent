from typing import Optional
from serpapi import GoogleSearch
from langchain_core.tools import tool 
import os 
from typing import List

@tool 
def search_restaurent(    
    q: str,
    check_in_date: str,
    check_out_date: str,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
    currency: Optional[str] = None,
    adults: Optional[int] = 2,
    children: Optional[int] = 0,
    children_ages: Optional[str] = None,
    sort_by: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    property_types: Optional[str] = None,
    amenities: Optional[str] = None,
    rating: Optional[int] = None,
    brands: Optional[str] = None,
    hotel_class: Optional[str] = None,
    free_cancellation: Optional[bool] = None,
    special_offers: Optional[bool] = None,
    eco_certified: Optional[bool] = None
):
    


    """
    Search for hotels and vacation rentals using the Google Hotels API through SerpAPI.

    This tool allows users to query Google Hotels results with various filters, including location,
    travel dates, occupancy, amenities, and advanced search criteria such as pricing, rating, and hotel class.

    Required Parameters:
    --------------------
    q : str
        The search query (e.g., "hotels in New York").
    check_in_date : str
        The check-in date in the format "YYYY-MM-DD" (e.g., "2025-06-18").
    check_out_date : str
        The check-out date in the format "YYYY-MM-DD" (e.g., "2025-06-20").

    Optional Parameters:
    --------------------
    gl : str, optional
        Country code for localization (e.g., "us" for the United States).
    hl : str, optional
        Language code for localization (e.g., "en" for English).
    currency : str, optional
        Currency code for returned prices (e.g., "USD", "EUR").
    adults : int, optional
        Number of adults staying. Default is 2.
    children : int, optional
        Number of children staying. Default is 0.
    children_ages : str, optional
        Comma-separated ages of children (e.g., "5,8").
    sort_by : int, optional
        Sorting preference:
            - 3: Lowest price
            - 8: Highest rating
            - 13: Most reviewed
    min_price : int, optional
        Minimum price filter.
    max_price : int, optional
        Maximum price filter.
    property_types : str, optional
        Comma-separated property type IDs (e.g., "17,12").
    amenities : str, optional
        Comma-separated amenity IDs (e.g., "35,9,19").
    rating : int, optional
        Minimum rating filter:
            - 7: 3.5+
            - 8: 4.0+
            - 9: 4.5+
    brands : str, optional
        Comma-separated brand IDs to filter specific hotel brands.
    hotel_class : str, optional
        Comma-separated hotel class values (2: 2-star, 3: 3-star, etc.).
    free_cancellation : bool, optional
        If True, only return hotels with free cancellation.
    special_offers : bool, optional
        If True, only return hotels with special offers.
    eco_certified : bool, optional
        If True, only return eco-certified hotels.

    Returns:
    --------
    dict
        A dictionary containing the results returned by the SerpAPI Google Hotels search query.
        This includes hotel listings, prices, ratings, and any other applicable metadata.

    Example:
    --------
    >>> search_restaurent(
            q="hotels in Paris",
            check_in_date="2025-06-18",
            check_out_date="2025-06-20",
            currency="EUR",
            rating=8,
            hotel_class="4,5",
            free_cancellation=True
        )
    """

    params = {
        "engine": "google_hotels",
        "api_key": os.environ["SERP_API_KEY"],
        "q": q,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "children": children
    }

    optional_params = {
        "gl": gl,
        "hl": hl,
        "currency": currency,
        "children_ages": children_ages,
        "sort_by": sort_by,
        "min_price": min_price,
        "max_price": max_price,
        "property_types": property_types,
        "amenities": amenities,
        "rating": rating,
        "brands": brands,
        "hotel_class": hotel_class,
        "free_cancellation": "true" if free_cancellation else None,
        "special_offers": "true" if special_offers else None,
        "eco_certified": "true" if eco_certified else None
    }

    for key, value in optional_params.items():
        if value is not None:
            params[key] = value
    
    search = GoogleSearch(params)

    results = search.get_dict()

    return results 

@tool 
def search_places_and_tourist_spots(
    type: str,
    api_key: Optional[str] = None,
    q: Optional[str] = None,
    ll: Optional[str] = None,
    google_domain: Optional[str] = None,
    hl: Optional[str] = None,
    gl: Optional[str] = None,
    data: Optional[str] = None,
    place_id: Optional[str] = None,
    start: Optional[int] = 0,
    no_cache: Optional[bool] = False,
    async_mode: Optional[bool] = False,
    zero_trace: Optional[bool] = False,
    output: Optional[str] = "json"
):
    """
    Searches Google Maps using SerpAPI to find places or specific locations (e.g., tourist spots).

    Parameters
    ----------
    type : str
        Required. Type of search: 'search' for a query-based search, or 'place' for a specific location using `data` or `place_id`.
    api_key : str, optional
        Your SerpAPI private key. If not provided, uses the SERP_API_KEY environment variable.
    q : str, optional
        Query string to search for (e.g., "tourist attractions in Rome"). Required if type is 'search'.
    ll : str, optional
        GPS coordinates of the location in format "@lat,long,zoom" (e.g., "@40.7455096,-74.0083012,14z"). Required if using pagination with 'search'.
    google_domain : str, optional
        Google domain to use (e.g., "google.co.uk"). Defaults to "google.com".
    hl : str, optional
        Language code (e.g., "en", "fr").
    gl : str, optional
        Country code (e.g., "us", "uk").
    data : str, optional
        Encoded place data string used when type is 'place'.
    place_id : str, optional
        Google Maps Place ID of the location to retrieve.
    start : int, optional
        Result offset for pagination (e.g., 0, 20, 40).
    no_cache : bool, optional
        Whether to force a fresh fetch instead of using cached results.
    async_mode : bool, optional
        Whether to perform an asynchronous search (not compatible with `no_cache`).
    zero_trace : bool, optional
        Enterprise only. Disables search logging and parameter storage.
    output : str, optional
        Output format: 'json' (default) or 'html'.

    Returns
    -------
    dict
        Parsed JSON result containing place listings and metadata.

    Example
    -------
    >>> search_google_maps_places(
            type="search",
            q="tourist attractions in Tokyo",
            ll="@35.6895,139.6917,13z",
            gl="jp",
            hl="en"
        )
    """
    api_key = api_key or os.environ["SERP_API_KEY"]

    params = {
        "engine": "google_maps",
        "type": type,
        "api_key": api_key,
        "output": output,
        "start": start,
    }

    if q: params["q"] = q
    if ll: params["ll"] = ll
    if google_domain: params["google_domain"] = google_domain
    if hl: params["hl"] = hl
    if gl: params["gl"] = gl
    if data: params["data"] = data
    if place_id: params["place_id"] = place_id
    if no_cache: params["no_cache"] = "true"
    if async_mode: params["async"] = "true"
    if zero_trace: params["zero_trace"] = "true"

    search = GoogleSearch(params)
    results = search.get_dict()

    return results

@tool 
def search_local_events_news(
    location: str,
    time_frame: str = "this weekend", 
    gl: Optional[str] = "in",
    hl: Optional[str] = "en",
    google_domain: Optional[str] = "google.com",
    device: Optional[str] = "desktop",
    num: Optional[int] = 10,
    no_cache: Optional[bool] = True
):
    """
    Search news articles about local events and activities using SerpApi's google_news_light engine.

    Parameters:
        location (str): Name of the city or region to search in.
        time_frame (str): When the activities/events occur (e.g., "today", "next weekend").
        gl (str): Country code (default: "in" for India).
        hl (str): Language code (default: "en").
        google_domain (str): Google domain to use (default: "google.com").
        device (str): Device type: "desktop", "mobile", or "tablet".
        num (int): Number of results to return (max 100).
        no_cache (bool): Whether to force a fresh search.

    Returns:
        dict: JSON results from SerpApi.
    """
    query = f"events and activities in {location} {time_frame}"

    params = {
        "engine": "google_news_light",
        "q": query,
        "gl": gl,
        "hl": hl,
        "google_domain": google_domain,
        "device": device,
        "num": num,
        "no_cache": str(no_cache).lower(),
        "api_key": os.environ["SERP_API_KEY"] 
    }

    search = GoogleSearch(params)
    return search.get_dict()

@tool 
def search_google_flights(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
    return_date: Optional[str] = None,
    trip_type: int = 1,
    travel_class: int = 1,
    adults: int = 1,
    children: int = 0,
    infants_in_seat: int = 0,
    infants_on_lap: int = 0,
    currency: str = "INR",
    gl: str = "in",
    hl: str = "en",
    sort_by: int = 1,  
    max_price: Optional[int] = None,
    stops: Optional[int] = None,
    outbound_times: Optional[str] = None,
    return_times: Optional[str] = None,
    exclude_airlines: Optional[List[str]] = None,
    include_airlines: Optional[List[str]] = None,
    deep_search: bool = True,
    max_duration: Optional[int] = None,
    layover_duration: Optional[str] = None,
    exclude_conns: Optional[List[str]] = None,
    show_hidden: bool = False,
    no_cache: bool = True,
    api_key: str = "YOUR_SERPAPI_KEY"
) -> dict:
    """
    Search flights using SerpApi's Google Flights engine.

    Returns a JSON dictionary of flight results.
    """

    if exclude_airlines and include_airlines:
        raise ValueError("You can't use both exclude_airlines and include_airlines.")

    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "type": trip_type,
        "travel_class": travel_class,
        "adults": adults,
        "children": children,
        "infants_in_seat": infants_in_seat,
        "infants_on_lap": infants_on_lap,
        "currency": currency,
        "gl": gl,
        "hl": hl,
        "sort_by": sort_by,
        "deep_search": str(deep_search).lower(),
        "show_hidden": str(show_hidden).lower(),
        "no_cache": str(no_cache).lower(),
        "api_key": api_key,
    }

    if return_date and trip_type == 1:
        params["return_date"] = return_date
    if outbound_times:
        params["outbound_times"] = outbound_times
    if return_times and trip_type == 1:
        params["return_times"] = return_times
    if max_price:
        params["max_price"] = max_price
    if stops:
        params["stops"] = stops
    if max_duration:
        params["max_duration"] = max_duration
    if layover_duration:
        params["layover_duration"] = layover_duration
    if exclude_airlines:
        params["exclude_airlines"] = ",".join(exclude_airlines)
    if include_airlines:
        params["include_airlines"] = ",".join(include_airlines)
    if exclude_conns:
        params["exclude_conns"] = ",".join(exclude_conns)

    search = GoogleSearch(params)
    return search.get_dict()
