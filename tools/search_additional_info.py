import os
from langchain_core.tools import tool
from langchain_community.tools.reddit_search.tool import RedditSearchRun
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper
from langchain_community.tools.reddit_search.tool import RedditSearchSchema
from dotenv import load_dotenv 
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_tavily import TavilySearch


load_dotenv()
os.environ["REDDIT_PERSONAL_USE_SCRIPT"] = os.getenv("REDDIT_PERSONAL_USE_SCRIPT")
os.environ["REDDIT_SECRET_KEY"] = os.getenv("REDDIT_SECRET_KEY")

@tool
def reddit_search(query: str) -> dict:
    """
    Search Reddit for recommended and negatively-reviewed places based on a query.

    Parameters:
    -----------
    query : str
        Any travel-related search query to explore experiences and recommendations on Reddit.
        Examples:
            - "best hotels in Rome"
            - "must visit places in Chennai"
            - "bad airline experience Emirates"
            - "honeymoon spots in Bali"
            - "avoid areas in Paris"

    Returns:
    --------
    dict
        {
            "places_to_visit": [list of recommended places],
            "places_to_avoid": [list of places with bad reviews or user complaints]
        }

    """

    # 1. Perform Reddit search
    search = RedditSearchRun(
        api_wrapper=RedditSearchAPIWrapper(
            reddit_client_id=os.environ["REDDIT_PERSONAL_USE_SCRIPT"],
            reddit_client_secret=os.environ["REDDIT_SECRET_KEY"],
            reddit_user_agent="Travel Agent",
        )
    )

    search_params = RedditSearchSchema(query=query, sort="new", limit="25")
    raw_reddit_results = search.run(tool_input=search_params.model_dump())

    # 2. Use LLM to extract structured places info
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

    template = """
    You are an expert travel assistant.

    From the following Reddit posts, extract:
    1. A list of **places people recommend visiting** based on positive sentiment or popular suggestions.
    2. A list of **places to avoid**, either due to bad reviews, safety concerns, or disappointing experiences.

    Only extract **actual place names** (like beaches, parks, attractions, streets, or landmarks).

    Return the result as JSON with:
    - "places_to_visit": list of strings
    - "places_to_avoid": list of strings

    Reddit Posts:
    ----------------
    {reddit_content}
    """

    prompt = PromptTemplate(
        input_variables=["reddit_content"],
        template=template
    )

    parser = JsonOutputParser()
    chain = prompt | llm | parser

    result = chain.invoke({"reddit_content": raw_reddit_results})

    return result

@tool
def tavily_search(query: str) -> dict:
    """
    Use Tavily's web search and LLM to plan a travel itinerary by extracting recommended and avoidable places.

    Parameters:
    -----------
    query : str
        A destination-based search query to explore trip planning insights.
        Ideal for generating real-world travel itineraries.
        
        Examples:
            - "3-day itinerary in Bangkok"
            - "top attractions in Istanbul"
            - "places to avoid in downtown LA"
            - "best street food tour in Penang"
            - "must-visit temples in Kyoto"

    Returns:
    --------
    dict
        {
            "places_to_visit": [list of popular or highly-rated spots],
            "places_to_avoid": [list of poorly reviewed or potentially unsafe places]
        }

    Notes:
    ------
    - This tool helps build realistic, well-informed itineraries by using up-to-date web data.
    - Use it to plan:
        - Day-wise sightseeing schedules
        - Food and nightlife spots
        - Cultural experiences
        - Safety warnings or sketchy areas to avoid
    """

    # 1. Tavily Web Search
    tavily_search_tool = TavilySearch(
        max_results=5,
        topic="general"
    )

    search_results = tavily_search_tool.invoke(query)
    combined_content = "\n\n".join([doc.get("content", "") for doc in search_results if "content" in doc])

    # 2. Use LLM to extract structured itinerary insights
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

    prompt_template = """
    You are a helpful travel planner.

    Analyze the following web search content. Based on user feedback, reviews, or reports, extract:

    - A list of **places to visit**: positively mentioned or recommended spots.
    - A list of **places to avoid**: locations with safety concerns, negative reviews, or bad experiences.

    ONLY extract proper names (e.g. landmarks, hotels, areas, attractions). No generic terms.

    Return this as valid JSON:
    {
        "places_to_visit": [...],
        "places_to_avoid": [...]
    }

    Web Results:
    -------------
    {web_content}
    """

    prompt = PromptTemplate(
        input_variables=["web_content"],
        template=prompt_template
    )

    parser = JsonOutputParser()
    chain = prompt | llm | parser

    result = chain.invoke({"web_content": combined_content})

    return result

