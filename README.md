# Code Editing Agent

A minimal AI coding agent built with Claude. ~200 lines of Python running in a loop with LLM tokens.

Inspired by [Geoffrey Huntley's workshop](https://ghuntley.com/agent/).

## Setup

1. **Create a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install anthropic
```

2. **Install ripgrep** (for code search):

```bash
brew install ripgrep      # macOS
apt install ripgrep       # Ubuntu/Debian
```

3. **Set your API key:**

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

```bash
python main.py
```

Then chat with Claude:

```
You: what files are in this directory?
You: search the code for "ToolDefinition"
You: read agent.py and explain how the loop works
You: create a fizzbuzz.py that prints fizzbuzz from 1 to 100
You: run python fizzbuzz.py
You: fix the bug in fizzbuzz.py
```

Use `Ctrl+C` to quit.

## Tools

| Tool | Description |
|------|-------------|
| `list_files` | List files and directories at a given path |
| `read_file` | Read the contents of a file |
| `edit_file` | Edit a file by replacing text, or create new files |
| `bash` | Execute shell commands (dangerous commands blocked) |
| `code_search` | Search code with ripgrep |

### Tool Details

**edit_file** — Uses string replacement. Pass `old_str=""` to create a new file.

**bash** — Blocks dangerous patterns: `rm -rf`, `sudo`, `> /dev`, `mkfs`, `dd if=`, `:{()`. Times out after 30 seconds.

**code_search** — Requires `ripgrep` (`rg`). Returns matching lines with file paths and line numbers.

## Project Structure

```
├── main.py      # Entry point, sets up and runs the agent
├── agent.py     # Agent loop and tool execution
└── tools.py     # Tool definitions
```

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                    Agent Loop                       │
├─────────────────────────────────────────────────────┤
│  1. Get user input                                  │
│  2. Send conversation to Claude                     │
│  3. If Claude returns text → print it               │
│  4. If Claude returns tool_use → execute tool       │
│  5. Add tool result to conversation                 │
│  6. Go to step 2 (until no more tool calls)         │
│  7. Go to step 1                                    │
└─────────────────────────────────────────────────────┘
```
