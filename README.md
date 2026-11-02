# 🤖 AI Agent

A **Python AI agent** that breaks a user request into tasks, picks the right tool for each one through an MCP server, and returns a natural-language answer. It remembers useful facts about the user across sessions using embedding-based semantic memory stored in SQLite.

This project demonstrates an agent loop built from small, separate parts: task decomposition, planning, tool execution via MCP, long-term memory, and answer formatting.

---

## 🚀 Features

### 🧠 Planning

- Decomposes a request into ordered tasks
- Skips tool use for greetings, personal details, memory questions and general knowledge
- Chooses one pending task and the best tool for it at every step
- Reconsiders the task when a tool call fails

### 🔌 MCP Tools

- Tools are served by a FastMCP server and discovered at start-up
- Included tools:
  - `current_time` – current date and time
  - `roll_dice` – roll a six-sided dice
  - `generate_password` – generate a secure password of a given length

### 💾 Long-Term Memory

- Each conversation is saved with an embedding
- An LLM extracts durable facts (preferences, goals, skills, projects)
- Relevant memories are retrieved by cosine similarity and given to the planner and the final answer

### 🔄 Agent Loop

- Shared state tracks tasks, actions, observations and results
- Stops when all tasks are done, the planner returns `FINISH`, or the step limit (5) is reached

---

## 🛠 Tech Stack

### Core

- Python 3.14
- asyncio

### Libraries

- FastMCP (MCP server and client)
- OpenAI Python SDK (any OpenAI-compatible endpoint)
- NumPy (cosine similarity)
- python-dotenv

### Storage

- SQLite (`memory.db`)

---

## 📂 Project Structure

```
ai-agent/
├─ agent_loop
│  └─ loop.py              # Main agent loop and planner-decision parsing
├─ executor
│  └─ executor.py          # Runs the chosen MCP tool
├─ final_answer
│  └─ answer.py            # Turns the final state into the user-facing answer
├─ mcp_tools
│  ├─ mcp_client.py        # Connect, discover and call tools
│  └─ mcp_server.py        # FastMCP server exposing the tools
├─ memory
│  ├─ db.py                # SQLite access
│  ├─ memory.py            # Embeddings, saving and semantic search
│  └─ memory_extractor.py  # Extracts long-term facts from a conversation
├─ planner
│  ├─ planner.py           # Picks the next task and tool
│  └─ task_planner.py      # Splits the request into tasks
├─ state
│  └─ state.py             # Agent state helpers
├─ .env
├─ memory.db
└─ runner.py               # Entry point
```

---

## ⚙ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/mishraabhishek11/ai-agent.git
cd ai-agent
```

### 2️⃣ Create and activate a virtual environment

```
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```
pip install fastmcp openai numpy python-dotenv
```

`sqlite3` ships with Python, so it does not need to be installed.

### 4️⃣ Configure environment variables

Create a `.env` file in the project root:

```
BASE_URL=<OpenAI-compatible API base URL>
API_KEY=<your API key>
MODEL=<chat model name>
EMBEDDING_MODEL=<embedding model name>
```

### 5️⃣ Run the agent

```
python runner.py
```

The MCP server is started automatically by the client, so there is nothing else to launch.

---

## 🧑‍💻 Usage

```
Available MCP Tools
----------------
current_time
roll_dice
generate_password

User : roll a dice and tell me the time
```

1. Run `python runner.py`
2. Type a request at the `User :` prompt
3. Watch the task plan, planner decisions and observations
4. Read the final answer

---

## 🔁 How It Works

1. `runner.py` creates the database, connects to the MCP server and discovers its tools
2. Relevant memories are retrieved for the request
3. `task_planner.py` splits the request into tasks
4. For each step, `planner.py` returns a `TASK` and a `TOOL`, or `FINISH`
5. `executor.py` calls the tool and the observation is stored in state
6. `answer.py` writes the final answer
7. The conversation is saved, and any long-term fact is extracted into semantic memory

---

## 🎯 Learning Objectives

- Agent loop design (plan, act, observe)
- Model Context Protocol with FastMCP
- Task decomposition with an LLM
- Embedding-based semantic memory
- Async Python

---

## 🔮 Future Enhancements

- More MCP tools
- Tests for the loop, state and memory modules
- A `requirements.txt` to pin dependencies
- Smarter task matching than exact text
- Web or chat interface

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch  
   git checkout -b feature/your-feature

3. Commit changes  
   git commit -m "feat(scope): your message"

4. Push changes  
   git push origin feature/your-feature

5. Open Pull Request

---

## 👨‍💻 Author

Abhishek Mishra  
GitHub: https://github.com/mishraabhishek11

---

## ⭐ Support

Give a ⭐ if you like this project!
