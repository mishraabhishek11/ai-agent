import asyncio

from mcp_tools.mcp_client import (
    connect,
    disconnect,
    discover_tools
)

from planner.planner import planner
from executor.executor import execute_action
from agent_loop.loop import run_agent_loop
from final_answer.answer import format_answer
from memory.db import create_database

async def main():
    create_database()
    mcp_client = await connect()

    mcp_tools = await discover_tools(
        mcp_client
    )

    print("\nAvailable MCP Tools")
    print("----------------")

    for tool in mcp_tools:
        print(tool.name)

    user_request = input(
        "\nUser : "
    )

    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        mcp_tools,
        mcp_client
    )

    print("\nFinal Answer")
    print("------------")

    print(
        state["final_answer"]
    )

    await disconnect(mcp_client)


if __name__ == "__main__":
    asyncio.run(main())



