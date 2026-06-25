import os
from langchain.agents import create_agent
from langchain_litellm import ChatLiteLLM
from langchain_core.messages import HumanMessage, SystemMessage

from agent.tools import (
    search_in_policy_documents,
    make_search_address_by_employee_id,
    make_search_employee_by_id,
)

SYSTEM_PROMPT = """You are a helpful assistant that can answer questions and perform tasks for employees.
Help the user with their queries and provide relevant information.
Format the response in a clear and concise manner. If you need to perform a task, use the appropriate tool and provide the output in your response.
Do not use any markup or formatting in your response.
"""

TOOLS_BY_NAME = {
    "search_in_policy_documents": search_in_policy_documents,
    "search_employee_by_id": make_search_employee_by_id(),
    "search_address_by_employee_id": make_search_address_by_employee_id(),
}

TOOLS = list(TOOLS_BY_NAME.values())


class EmployeeAgent:
    def __init__(self):
        self.API_KEY = os.environ["AGENT_API_KEY"]
        # self.API_BASE = os.environ['API_BASE']
        self.TOOLS_BY_NAME = TOOLS_BY_NAME

        self.llm = ChatLiteLLM(
            # api_base=self.API_BASE,
            api_key=self.API_KEY,
            model="groq/qwen/qwen3-32b",
        )
        self.messages = [
            SystemMessage(content=SYSTEM_PROMPT),
        ]

    # def call_tool(self, call):
    #     # raise ValueError("mocking error")
    #     return self.TOOLS_BY_NAME[call["name"]].invoke(call["args"])

    # def process_prompt(self, prompt):
    #     self.messages.append(HumanMessage(prompt))
    #     return self.run_loop()

    async def process_prompt(
        self,
        db,
        prompt: str,
    ):
        tools = [
            search_in_policy_documents,
            make_search_employee_by_id(db),
            make_search_address_by_employee_id(db),
        ]

        agent = create_agent(self.llm, tools)

        self.messages.append(HumanMessage(content=prompt))

        result = await agent.ainvoke({"messages": self.messages})

        return result["messages"][-1].content

    # def run_loop(self):
    #     MAX_ITERATION = 10
    #     TOKEN_BUDGET = 1000
    #     fails = 0
    #     token_used = 0

    #     for step in range(MAX_ITERATION):
    #         if token_used > TOKEN_BUDGET:
    #             return "Stopping: Token budget exceeded"

    #         ai = self.agent.ai({
    #             "messages": self.messages,
    #         })
    #         self.messages.append(ai)

    #         token_used += ai.usage_metadata["total_tokens"]

    #         if not ai.tool_calls:
    #             return ai.content

    #         for call in ai.tool_calls:
    #             try:
    #                 tool_output = self.call_tool(call)

    #             except Exception as e:
    #                 tool_output = f"Error: {str(e)}"
    #                 fails += 1
    #                 print(f"failed: {fails}: Error: {tool_output}")
    #                 time.sleep(0.5 * fails)

    #             if fails >= 3:
    #                 return tool_output

    #             self.messages.append(
    #                 ToolMessage(tool_output, tool_call_id=call["id"]),
    #             )


agent_map = {}


def get_agent(id) -> EmployeeAgent:
    if id not in agent_map.keys():
        agent_map[id] = EmployeeAgent()

    return agent_map.get(id)
