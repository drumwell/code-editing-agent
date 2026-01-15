from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Callable, List, Tuple

from anthropic import Anthropic

@dataclass
class ToolDefinition:
    name: str
    description: str
    input_schema: dict
    function: Callable[[dict], str]


GetUserMessage = Callable[[], Tuple[str, bool]]


@dataclass
class Agent:
    client: Anthropic
    get_user_message: GetUserMessage
    tools: List[ToolDefinition] = field(default_factory=list)
    
    def run(self) -> None:
        conversation: List[dict] = []
        print("Chat with Claude (use 'ctrl-c' to quit)")

        read_user_input = True
        while True:
            if read_user_input:
                print("\033[94mYou\033[0m: ", end="", flush=True)
                user_input, ok = self.get_user_message()
                if not ok:
                    break

                user_message = {
                    "role": "user",
                    "content": [{"type": "text", "text": user_input}],
                }
                conversation.append(user_message)

            message = self.run_inference(conversation)
            conversation.append(message)

            tool_results = []
            for content in message["content"]:
                if content["type"] == "text":
                    print(f"\033[93mClaude\033[0m: {content['text']}")
                elif content["type"] == "tool_use":
                    result = self.execute_tool(content["id"], content["name"], content["input"])
                    tool_results.append(result)

            if not tool_results:
                read_user_input = True
                continue

            read_user_input = False
            conversation.append({"role": "user", "content": tool_results})

    def execute_tool(self, tool_id: str, name: str, tool_input: dict) -> dict:
        tool_def = None
        for tool in self.tools:
            if tool.name == name:
                tool_def = tool
                break

        if tool_def is None:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": "tool not found",
                "is_error": True,
            }

        print(f"\033[92mtool\033[0m: {name}({tool_input})")
        try:
            response = tool_def.function(tool_input)
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": response,
            }
        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": str(e),
                "is_error": True,
            }

    def run_inference(self, conversation: List[dict]) -> dict:
        # Build anthropic tools list
        anthropic_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self.tools
        ]

        message = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=conversation,
            tools=anthropic_tools if anthropic_tools else None,
        )
        # Convert Message object to dict for conversation history
        return {
            "role": message.role,
            "content": [
                {"type": block.type, "text": block.text} if block.type == "text"
                else {"type": block.type, "id": block.id, "name": block.name, "input": block.input}
                for block in message.content
            ],
        }