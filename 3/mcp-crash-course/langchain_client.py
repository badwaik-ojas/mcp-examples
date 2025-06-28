import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI()


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "C:/ojas_stuff/MCP/mcp-examples/3/mcp-crash-course/server/math_server.py"
                ],
                "transport": "stdio",
            },
            # Run: uv run .\server\weather_server.py
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }  # type: ignore
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    # result = await agent.ainvoke({"messages": "What is 2 + 2?"})
    result = await agent.ainvoke(
        {"messages": "What is the weather in San Francisco?"}
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
