from mcp.server.fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP(name="Demo Server")

# Tool function recieves context argument
# ---------------------------------------
# Tool functions automatically receive 'Context' as their last argument. 
# This object has methods for logging and reporting progress to the client.
@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    # Create logs and progress with context
    # -------------------------------------
    # Throughout your tool function, call the info(), warning(), debug(), or error() 
    # methods to log different types of messages for the client. Also call the report_progress()
    # method to estimate the amount of remaining work for the tool call.
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info("OK, adding...")
    await ctx.report_progress(80, 100)

    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")
