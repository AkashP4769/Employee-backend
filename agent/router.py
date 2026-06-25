from fastapi import APIRouter


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agent.utils import get_agent
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database.connection import get_db

import agent.service as service

from agent.schemas import AgentMessage, AgentResponse


router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("", response_model=AgentResponse)
async def get_all_department(
    body: AgentMessage,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
) -> AgentResponse:

    agent = get_agent(_current_user.id)
    return service.process_prompt(db, agent, body.prompt)
