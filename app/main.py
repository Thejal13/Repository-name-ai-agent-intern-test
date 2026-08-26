from dotenv import load_dotenv

from app.agent import SupportAgent


def main():
    load_dotenv()

    print("Aster & Row Support Agent")
    print("Type 'exit' to quit.\n")

    agent = SupportAgent()

    while True:
        try:
            message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if message.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not message:
            continue

        try:
            answer = agent.answer(message)
            print(f"\nAgent: {answer}\n")
        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
