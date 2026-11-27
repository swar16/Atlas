from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.agent.graph import chatbot


def main() -> None:
    conversation = []

    print("Atlas is ready. Type 'quit' to exit.")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        conversation.append(HumanMessage(content=question))

        for event in chatbot.stream(
            {"messages": conversation},
            stream_mode="updates"
        ):
            for node_name, update in event.items():
                print(f"\n[Node: {node_name}]")

                for message in update.get("messages", []):
                    conversation.append(message)

                    if isinstance(message, AIMessage):
                        if message.tool_calls:
                            for call in message.tool_calls:
                                print(f"Tool requested: {call['name']}")
                                print(f"Arguments: {call['args']}")
                        else:
                            print(f"Atlas: {message.content}")

                    elif isinstance(message, ToolMessage):
                        print(f"Tool result: {message.content}")

    return


if __name__ == "__main__":
    main()