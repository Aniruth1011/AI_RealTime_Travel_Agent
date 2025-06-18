from langchain_core.tools import tool 
from typing import Union  , List , Optional , Dict 
from datetime import date, datetime
from langchain_groq import ChatGroq 
from langchain.prompts import PromptTemplate
from langchain_community.output_parsers import JsonOutputParser 
import json 

@tool 
def create_itenary(
    start_date: Union[str, date, datetime],
    end_date: Union[str, date, datetime],
    location: str,
    hotel_chosen_name: str,
    hotel_chosen_pricing_details: Dict[str, float],
    places_to_visit: List[str],
    flight_airlines_available: str,
    flight_airlines_pricing: float,
    flight_airlines_details: str,
    number_of_people: int = 1,
    preferences: Optional[Dict[str, Union[str, List[str]]]] = None,
    local_transport_options: Optional[List[str]] = None,
    daily_budget: Optional[float] = None,
    meal_plan_included: bool = True,
    special_occasions: Optional[str] = None,
    children_ages: Optional[List[int]] = None,
    weather_constraints: bool = True,
    timezone: Optional[str] = "Europe/Rome",
    activity_durations: Optional[Dict[str, int]] = None,
    local_events: Optional[List[Dict[str, Union[str, datetime]]]] = None,
) -> Dict:
    """
    Generate a complete travel itinerary with personalized daily plans, cost estimates,
    event-based scheduling, and travel logistics.

    Parameters:
    ----------
    start_date : Union[str, date, datetime]
        Trip start date.

    end_date : Union[str, date, datetime]
        Trip end date.

    location : str
        Destination city or region.

    hotel_chosen_name : str
        Hotel name where the guests will stay.

    hotel_chosen_pricing_details : Dict[str, float]
        Pricing info with keys like 'per_night', 'total', 'taxes'.

    places_to_visit : List[str]
        Key tourist spots or destinations to include in the itinerary.

    flight_airlines_available : str
        Selected airline or available carrier for the route.

    flight_airlines_pricing : float
        Cost of flights per person.

    flight_airlines_details : str
        Additional flight info such as flight number, time, and baggage.

    number_of_people : int, optional
        Total travelers. Used to compute total cost. Default is 1.

    preferences : Optional[Dict[str, Union[str, List[str]]]], optional
        Traveler preferences. Keys may include:
            - "diet": str
            - "pace": str ("relaxed", "packed", "balanced")
            - "interests": List[str] like ["art", "food", "history"]

    local_transport_options : Optional[List[str]], optional
        Modes of travel preferred locally, e.g., ["metro", "taxi", "walk"]

    daily_budget : Optional[float], optional
        Per person per day budget (not including flights and hotel)

    meal_plan_included : bool, optional
        Whether hotel includes meals (affects cost planning)

    special_occasions : Optional[str], optional
        e.g., "honeymoon", "birthday", "anniversary" for personalized touch

    children_ages : Optional[List[int]], optional
        Include if traveling with kids (for age-appropriate planning)

    weather_constraints : bool, optional
        If True, avoid outdoor activities during forecasted bad weather

    timezone : Optional[str], optional
        Destination timezone, used for daily plan alignment

    activity_durations : Optional[Dict[str, int]], optional
        Estimated time to spend at each activity (in minutes)

    local_events : Optional[List[Dict[str, Union[str, datetime]]]], optional
        List of events at the destination. Each event dict should contain:
            - "name": str
            - "location": str
            - "datetime": datetime
            - "description": str (optional)

    Returns:
    -------
    itinerary : Dict
        A dictionary containing:
            - 'daily_schedule': List[Dict[str, Any]]
            - 'total_cost_estimate': Dict[str, float]
            - 'notes': List[str]
            - 'timezone': str

    Example:
    -------
    create_itenary(
         start_date="2025-07-01",
         end_date="2025-07-03",
         location="Rome",
         hotel_chosen_name="Hotel Roma Lux",
         hotel_chosen_pricing_details={"per_night": 120.0, "total": 360.0, "taxes": 36.0},
         places_to_visit=["Colosseum", "Pantheon", "Trevi Fountain"],
         flight_airlines_available="ITA Airways",
         flight_airlines_pricing=250.0,
         flight_airlines_details="Direct flight, economy, includes 1 bag",
         number_of_people=2,
         preferences={"pace": "balanced", "interests": ["history", "food"]},
         local_events=[
             {"name": "Opera in the Park", "location": "Villa Borghese", "datetime": datetime(2025, 7, 2, 20, 0)}
         ]
     )
    {
        'daily_schedule': [
            {
                'date': '2025-07-01',
                'plan': [
                    {'time': '09:00 - 10:30', 'activity': 'Visit Colosseum'},
                    {'time': '11:00 - 12:00', 'activity': 'Pantheon'},
                    {'time': '12:00 - 13:00', 'activity': 'Lunch (local cuisine)'},
                    {'time': '14:00 - 15:00', 'activity': 'Trevi Fountain'},
                    {'time': '15:30 - 17:00', 'activity': 'Relax at hotel or explore nearby cafes'}
                ]
            },
            {
                'date': '2025-07-02',
                'plan': [
                    {'time': '09:30 - 12:00', 'activity': 'Visit Vatican Museums'},
                    {'time': '14:00 - 15:00', 'activity': 'Local market exploration'},
                    {'time': '20:00 - 22:00', 'activity': 'Attend: Opera in the Park at Villa Borghese'}
                ]
            },
            ...
        ],
        'total_cost_estimate': {
            'flights': 500.0,
            'hotel': 396.0,
            'activities': 100.0,
            'meals': 120.0,
            'transport': 60.0,
            'total': 1176.0
        },
        'notes': [
            'Pack light summer clothing',
            'Pre-book Vatican Museum tickets',
            'Opera in the Park is outdoors, check weather forecast'
        ],
        'timezone': 'Europe/Rome'
    }
    """

    parser = JsonOutputParser()

    llm = ChatGroq(model = "qwen-qwq-32b" ,  temperature=0)

    template = """ 
    You are a highly knowledgeable and detail-oriented travel planner. Based on the user's input parameters, your task is to generate a complete travel itinerary including:

    1. A personalized **daily schedule** of activities between the provided start and end dates, considering user preferences (pace, interests, children, special occasions, local events, weather constraints).
    2. An accurate **cost estimate** that includes:
        - Flights (price per person × number of travelers)
        - Hotel cost (including taxes, multiplied by number of nights)
        - Meals (if not included in hotel pricing)
        - Local transport (estimate based on options given)
        - Activity costs (optional, can be based on a heuristic if actual prices not provided)
    3. A set of **notes or tips** based on the location, events, and provided constraints (e.g., what to pack, booking tips, warnings).
    4. Return the **timezone** used for all scheduling.

    You must take into account:
    - The weather (skip outdoor events if `weather_constraints` is True and the forecast is bad)
    - Children's ages (to avoid adult-only or unsuitable activities)
    - Any special occasions (like honeymoon or birthday for enhancements)
    - Activity durations (if provided, plan based on these)
    - Local events (fit them into the schedule if timing and location allow)
    - Preferences (can be any specific place, or theme they want to do, or any dietary preferences if they have any, such as Vegetarian, etc)

    All output must be returned in **JSON format** with the following top-level keys:
    - `"daily_schedule"`: List of day-wise schedules with time blocks and activities
    - `"total_cost_estimate"`: Detailed cost breakdown with subcategories and total
    - `"notes"`: List of travel advice, considerations, and alerts
    - `"timezone"`: The timezone string used

    Use natural time slots (e.g., morning, lunch, afternoon, evening), and make the daily plan realistic—not overly packed unless user prefers a "packed" pace. Include meal breaks and downtime.

    Here is the input data for you to use:
    ```json
    {user_input}
    """
    
    user_input = {
    "start_date": start_date,
    "end_date": end_date,
    "location": location,
    "hotel_chosen_name": hotel_chosen_name,
    "hotel_chosen_pricing_details": hotel_chosen_pricing_details,
    "places_to_visit": places_to_visit,
    "flight_airlines_available": flight_airlines_available,
    "flight_airlines_pricing": flight_airlines_pricing,
    "flight_airlines_details": flight_airlines_details,
    "number_of_people": number_of_people
}

    if preferences is not None:
        user_input["preferences"] = preferences

    if local_transport_options is not None:
        user_input["local_transport_options"] = local_transport_options

    if daily_budget is not None:
        user_input["daily_budget"] = daily_budget

    user_input["meal_plan_included"] = meal_plan_included

    if special_occasions is not None:
        user_input["special_occasions"] = special_occasions

    if children_ages is not None:
        user_input["children_ages"] = children_ages

    user_input["weather_constraints"] = weather_constraints

    if timezone is not None:
        user_input["timezone"] = timezone

    if activity_durations is not None:
        user_input["activity_durations"] = activity_durations

    if local_events is not None:
        user_input["local_events"] = local_events
 
    prompt= PromptTemplate( 
        template=template,
        input_variable=["user_input"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain= prompt | llm | parser 

    response = chain.invoke({"user_input": json.dumps(user_input)})

    return response  