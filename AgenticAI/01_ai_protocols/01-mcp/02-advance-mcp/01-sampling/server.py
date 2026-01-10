from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Demo Server")


@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """
    # On the server, during a tool call, run the create_message() method,
    # passing in some messages that you wish to send to a language model.
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(role="user", content=TextContent(type="text", text=prompt))
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )

    # After the client has generated and returned some text, it will be sent to the server. 
    # You can do anything with this text:

    # Use it as part of a workflow in your tool
    # Decide to make another sampling call
    # Return the generated text

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")


if __name__ == "__main__":
    mcp.run(transport="stdio")
