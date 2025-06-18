from agent import create_react_agent  
from langchain_core.messages import HumanMessage 
from langgraph.graph import MessagesState  
import sys

def main():
    print("Starting ReAct Agent. Type 'exit' to quit.")
    agent = create_react_agent()
    state = MessagesState()

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        message=[HumanMessage(content=user_input)]

        state.messages.append({"messages" : message})

        try:
            state = agent.step(state)
            last_response = state.messages[-1]["content"]
            print(f"Agent: {last_response}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
