
"""
main.py

Main entry point for the German Legal AI Agent.
"""

from src.agent import ask_legal_agent


def main():

    print("=" * 55)
    print("       GERMAN LEGAL AI ASSISTANT")
    print("=" * 55)

    print("Local AI | German legislation | RAG")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not question:
            continue

        try:

            answer = ask_legal_agent(question)

            print("\nAssistant:")
            print(answer)

        except Exception as error:

            print("\nAn error occurred:")
            print(error)


if __name__ == "__main__":
    main()
