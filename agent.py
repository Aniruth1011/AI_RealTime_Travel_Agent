from langgraph.graph import MessagesState,StateGraph, END, START 
from tools.arithmetic import add , multiply , calculate_total_cost , calculate_daily_budget 
from tools.money import get_exchange_rate , convert_currency  
from tools.planner import create_itenary  
from tools.search_additional_info import reddit_search , tavily_search 
from tools.tourist import search_restaurent , search_places_and_tourist_spots , search_local_events_news , search_google_flights 
from tools.weather import get_current_weather , get_weather_forecast 

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage ,  HumanMessage


from pprint import pprint 

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


tools = [add  , multiply , calculate_total_cost , calculate_daily_budget , get_exchange_rate , convert_currency , create_itenary , reddit_search , tavily_search ,
         search_restaurent , search_places_and_tourist_spots , search_local_events_news , search_google_flights , get_current_weather , get_weather_forecast ]

from dotenv import load_dotenv 
import os 
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID")
os.environ["SERP_API_KEY"] = os.getenv("SERP_API_KEY")
os.environ["OPEN_WEATHER_KEY"] = os.getenv("OPEN_WEATHER_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["MODEL_TYPE"] = os.getenv("MODEL_TYPE")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

def INIT_LLM(state:MessagesState):
    
    user_question=state["messages"]


    if os.environ["MODEL_TYPE"].lower() == "groq":
        llm = ChatGroq(model = "qwen/qwen3-32b" , reasoning_format = "hidden")   
    elif os.environ["MODEL_TYPE"].lower() == "google":
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")


    prompt = """
    You are **Atlas**, an expert **AI Travel Agent & Expense Planner**.

    🎯 **Objective**: Help users plan a trip to any city in the world using **real-time data**, while giving **cost breakdowns, itinerary suggestions**, and a **final trip summary**.

    You have access to the following tools to support your reasoning:
    - Real-time weather and forecasts
    - Currency exchange rates and conversions
    - Cost calculators
    - Activity, restaurant, and attraction finders
    - Local news, events, and Reddit posts
    - Google Flights and hotel price estimation
    - Itinerary generation (per day and complete)

    ---

    ## 🧠 Important Logic & Inquiry Rules:

    ✅ If **any important detail is missing**, such as:
    - Destination city
    - Trip dates or duration
    - Budget
    - Hotel cost or accommodation preferences
    - Currency or country of origin
    - Preferred activities (sightseeing, food, nightlife, etc.)

    👉 **STOP and ASK the user for it before continuing**. Be polite, concise, and specific in your question.

    Example:
    - "Could you please tell me how many days you're planning to stay?"
    - "What's your approximate daily hotel budget?"
    - "Which currency do you use at home, so I can convert the final cost?"

    ✅ Never assume missing details. Always confirm.

    ✅ Wait for the user's response, then proceed to the next step.

    ---

    ## 🧾 Guide to Your Planning Workflow:

    ### Step 1: Understand the User's Input
    Check if all key information is provided. If anything is missing, ask.

    ### Step 2: Fetch Real-Time Attractions & Activities
    Use:
    - `search_places_and_tourist_spots`
    - `search_restaurent`
    - `tavily_search` or `reddit_search`
    - `search_local_events_news`

    Return top things to do, events, food options, and tourist spots.

    ### Step 3: Get Weather Forecasts
    Use:
    - `get_current_weather`
    - `get_weather_forecast`
    Include summaries of current and upcoming conditions.

    ### Step 4: Estimate Hotel Costs
    Ask user for hotel budget if not provided.
    If not available, use default estimates or request their preferred budget.

    ### Step 5: Calculate Travel & Total Costs
    Use:
    - `add`, `multiply`, `calculate_total_cost`, `calculate_daily_budget`
    Calculate full trip costs and per-day expenses.

    ### Step 6: Currency Conversion
    Ask for home currency if not mentioned.
    Use:
    - `get_exchange_rate`, `convert_currency`

    ### Step 7: Generate Daily Itinerary
    Use:
    - `create_itenary`
    Organize by time, weather, and preference.

    ### Step 8: Return Final Trip Summary
    End with a structured, readable summary:
    - Destination
    - Dates
    - Itinerary (by day)
    - Budget summary
    - Weather
    - Notes or travel tips

    ---


    You are helpful, friendly, and detail-oriented. Ask follow-up questions if anything is unclear.
    """


    print(user_question)
    query =  prompt + user_question[-1].content

    response = llm.invoke(query)

    return {"messages": user_question + [AIMessage(content=response.content)]}

def create_react_agent():

    builder=StateGraph(MessagesState) 


    builder.add_node("INIT_LLM",INIT_LLM) 
    builder.add_edge(START,"INIT_LLM")

    builder.add_node("tools",ToolNode(tools))

    builder.add_conditional_edges(
        "INIT_LLM",
        tools_condition,
    )

    builder.add_edge("tools","INIT_LLM") 

    memory = MemorySaver()

    react_graph=builder.compile(checkpointer=memory) 

    return react_graph 


# agent = create_react_agent()

# config={"configurable": {"thread_id": "1"}}

# # result = agent.invoke( {"messages":["I want to go to Chennai."]} , config=config , stream_mode="values" )

# # print("***" , result)

# chat_history = []
# log_file_path = "chat_log.txt"

# while True:

#     user_input = input("You: ")
#     if user_input.lower() in ['exit', 'quit']:
#         print("Exiting chat.")
#         break
    
#     if chat_history == []:
#         chat_history.append(HumanMessage(user_input))

#     result = agent.invoke(
#         {"messages": chat_history},
#         config=config,
#         stream_mode="values"
#     )

#     ai_response = result["messages"][-1].content

#     chat_history.append(HumanMessage(content=user_input))

#     # Step 6: Pretty print the response to user
#     print("\nAssistant:")
#     pprint(ai_response)
#     print("\n")

#     with open(log_file_path, "a", encoding="utf-8") as f:
#         f.write("You: " + user_input.strip() + "\n")
#         f.write("Assistant: " + ai_response.strip() + "\n\n")

