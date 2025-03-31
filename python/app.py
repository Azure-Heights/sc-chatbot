"""Define a Chainlit frontend to interact with the LangGraph agent."""


# +-- imports

import logging
logger = logging.getLogger("chainlit")

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langchain.schema.runnable.config import RunnableConfig
from langsmith import traceable

from agent import agent

import chainlit as cl

# --+


# +-- chainlit

@cl.on_chat_start
async def on_chat_start():
    """Prepare settings panel and construct agent with initial settings."""
    cl.user_session.set("agent", agent)


@traceable
@cl.on_message
async def on_message(message: cl.Message):
    """Pass along user messages to the agent and display the response.

    Arguments:
        message - the incoming user message.
    """

    logger.info("User query: %s", message.content)

    agent = cl.user_session.get("agent")
    user_input = { "message": message.content }
    config = RunnableConfig(configurable={ "thread_id": cl.user_session.get("id") })
    msg = cl.Message(content="")

    async for event in agent.astream_events(user_input, config=config, version="v2"):

        if event["event"] == "on_chat_model_stream":
            await msg.stream_token(event["data"]["chunk"].content)

    await msg.send()

# --+

