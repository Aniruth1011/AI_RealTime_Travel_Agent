from langgraph.graph import MessagesState,StateGraph, END, START 
from tools.arithmetic import add , multiply , calculate_total_cost , calculate_daily_budget 
from tools.money import get_exchange_rate , convert_currency  
from tools.planner import create_itenary  
from tools.search_additional_info import reddit_search , tavily_search 
from tools.tourist import search_restaurent , search_places_and_tourist_spots , search_local_events_news , search_google_flights 
from tools.weather import get_current_weather , get_weather_forecast 

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

tools = [add  , multiply , calculate_total_cost , calculate_daily_budget , get_exchange_rate , convert_currency , create_itenary , reddit_search , tavily_search ,
         search_restaurent , search_places_and_tourist_spots , search_local_events_news , search_google_flights , get_current_weather , get_weather_forecast ]

def INIT_LLM(state:MessagesState):
    
    user_question=state["messages"]
    
    response = ""
    return {
        "messages":[response]
    }
    
    

def create_react_agent():
    builder=StateGraph(MessagesState) 

    builder.add_edge(START,"INIT_LLM")

    builder.add_node("INIT_LLM",INIT_LLM) 

    builder.add_node("TOOLS",ToolNode(tools))

    builder.add_conditional_edges(
        "llm_decision_step",
        tools_condition,
    )

    builder.add_edge("TOOLS","INIT_LLM") 

    react_graph=builder.compile() 

    return react_graph 





 
