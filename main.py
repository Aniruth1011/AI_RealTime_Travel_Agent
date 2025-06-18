from agent import create_react_agent  
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

        state.messages.append({"role": "user", "content": user_input})

        try:
            state = agent.step(state)
            last_response = state.messages[-1]["content"]
            print(f"Agent: {last_response}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
