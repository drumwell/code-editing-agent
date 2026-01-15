# main.py
import sys
from anthropic import Anthropic

from agent import Agent
from tools import ReadFileDefinition, ListFilesDefinition, EditFileDefinition


def main() -> None:
    client = Anthropic()

    # Equivalent to bufio.Scanner + getUserMessage closure
    def get_user_message() -> tuple[str, bool]:
        line = sys.stdin.readline()
        if line == "":  # EOF
            return "", False
        return line.rstrip("\n"), True

    tools = [ReadFileDefinition, ListFilesDefinition, EditFileDefinition]
    agent = NewAgent(client, get_user_message, tools)

    try:
        agent.run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


def NewAgent(client: Anthropic, get_user_message, tools: list) -> Agent:
    return Agent(
        client=client,
        get_user_message=get_user_message,
        tools=tools
    )


if __name__ == "__main__":
    main()
