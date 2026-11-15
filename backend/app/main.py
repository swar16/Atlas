from langchain_core.messages import HumanMessage

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

        result = chatbot.invoke({"messages": conversation})
        conversation = result["messages"]

        print(f"Atlas: {conversation[-1].content}")


if __name__ == "__main__":
    main()