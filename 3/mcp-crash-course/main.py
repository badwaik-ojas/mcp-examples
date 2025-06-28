import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_core.messages import HumanMessage


load_dotenv()

llm = ChatOpenAI()

stdio_server_params = StdioServerParameters(
    command="python",
    args=["C:/ojas_stuff/MCP/mcp-examples/3/mcp-crash-course/server/math_server.py"],
)

async def main():
    async with stdio_client(stdio_server_params) as (read,write):    
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)
            # print(tools)

            agent = create_react_agent(llm,tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="explictly use the tools at disposal. What is does this expression evaluate to using tool at disposal and tell me if the tools are used and tell me which tool is used? 544455 + 445 * 564?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
