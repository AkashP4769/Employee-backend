from agent.utils import EmployeeAgent


def process_prompt(db, agent: EmployeeAgent, prompt: str) -> dict[str:any]:
    content = agent.process_prompt(prompt)
    return {"content": content}
