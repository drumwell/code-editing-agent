# Code Editing Agent

A minimal AI coding agent built with Claude that can read, list, and edit files in your project.

## Setup

1. **Create a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install anthropic
```

2. **Set your API key:**

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

```bash
python main.py
```

Then chat with Claude. Ask it to explore and edit files:

```
You: what files are in this directory?
You: read main.py and explain what it does
You: create a file called hello.py that prints hello world
You: change hello.py to print goodbye instead
```

Use `Ctrl+C` to quit.

## Tools

The agent has three tools available:

| Tool | Description |
|------|-------------|
| `list_files` | Lists files and directories at a given path |
| `read_file` | Reads the contents of a file |
| `edit_file` | Edits a file by replacing text, or creates new files |

## Project Structure

```
├── main.py      # Entry point, sets up and runs the agent
├── agent.py     # Agent class with conversation loop and tool execution
└── tools.py     # Tool definitions (list_files, read_file, edit_file)
```

## Rate Limits

If you hit rate limits, check:
- The Anthropic console at [console.anthropic.com](https://console.anthropic.com) for usage stats
- That `list_files` isn't recursively listing large directories (it's configured to only list immediate children)

