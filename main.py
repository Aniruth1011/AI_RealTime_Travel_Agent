from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState
from langchain_groq import ChatGroq 

from tools.arithmetic import add, multiply, calculate_total_cost, calculate_daily_budget
from tools.money import get_exchange_rate, convert_currency
from tools.planner import create_itenary
from tools.search_additional_info import reddit_search, tavily_search
from tools.tourist import search_restaurent,get_distances, search_local_events_news, search_google_flights ,  search_famous_places
from tools.weather import get_current_weather, get_weather_forecast


memory = MemorySaver()
model = init_chat_model("groq:qwen/qwen3-32b")
trimmer_model = ChatGroq(model = "llama-3.3-70b-versatile")

tools = [
    add, multiply, calculate_total_cost, calculate_daily_budget,
    get_exchange_rate, convert_currency, create_itenary,
    reddit_search, tavily_search, search_restaurent,
    get_distances, search_local_events_news,
    search_google_flights, get_current_weather, get_weather_forecast , search_famous_places 
]

agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}

messages = [
    {
        "role": "system",
        "content": (
            """
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
                """        )
    }
]

def trim_and_summarize_messages(model, state: MessagesState):
    system_prompt = (
        "You are a helpful assistant. "
        "Answer all questions to the best of your ability. "
        "The provided chat history includes a summary of the earlier conversation."
    )
    system_message = SystemMessage(content=system_prompt)
    message_history = state["messages"][:-1]  

    if len(message_history) >= 4:
        last_human_message = state["messages"][-1]
        summary_prompt = (
            "Distill the above chat messages into a single summary message. "
            "Include as many specific details as you can."
        )

        summary_message = model.invoke(
            message_history + [HumanMessage(content=summary_prompt)]
        )

        new_messages = [
            system_message,
            summary_message,
            HumanMessage(content=last_human_message.content),
        ]
        return {"messages": new_messages}
    else:
        return state  

# user_input = input("You: ")
# messages.append({"role": "user", "content": user_input})

# while True:
#     for step in agent_executor.stream({"messages": messages}, config, stream_mode="values"):
#         last = step["messages"][-1]
#         last.pretty_print()

#     user_input = input("You: ")
#     if user_input.lower() in {"exit", "quit"}:
#         print("Exiting chat. Have a great trip! ✈️")
#         break

#     messages.append({"role": "user", "content": user_input})

with open("chat.txt", "w" , encoding="utf-8") as log_file:
    log_file.write("=== Chat Session Started ===\n\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("Exiting chat. Have a great trip! ✈️")
        with open("chat.txt", "a") as log_file:
            log_file.write("\n=== Chat Session Ended ===\n")

        break

    messages.append({"role": "user", "content": user_input})

    state = {"messages": [HumanMessage(content=m["content"]) if m["role"] == "user" 
                          else SystemMessage(content=m["content"]) 
                          for m in messages]}

    trimmed_state = trim_and_summarize_messages(trimmer_model, state)

    for step in agent_executor.stream(trimmed_state, config, stream_mode="values"):
        last = step["messages"][-1]
        try:
            last.pretty_print()
        except UnicodeEncodeError:
            print(last.content)  

    with open("chat.txt", "a"  , encoding="utf-8") as log_file:
        log_file.write(f"User: {user_input}\n")
        log_file.write(f"Assistant: {last.content}\n\n")

    messages = [{"role": "user" if isinstance(m, HumanMessage) else "system", "content": m.content}
                for m in trimmed_state["messages"]]
    messages.append({"role": "assistant", "content": last.content})
