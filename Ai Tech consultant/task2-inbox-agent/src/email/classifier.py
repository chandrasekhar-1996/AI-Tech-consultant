from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import Literal

class EmailTriageSchema(BaseModel):
    category: Literal["technical_support", "sales_inquiry", "scoping_meeting", "spam"] = Field(
        description="The primary classification categorization of the incoming email query"
    )
    urgency: Literal["high", "medium", "low"] = Field(
        description="Priority calculation based on sender intent signals"
    )
    summary: str = Field(description="A single sentence summary summarizing the communication")

triage_agent = Agent(
    'openai:gpt-4o',
    result_type=EmailTriageSchema,
    system_prompt="You are an elite triage automation engineer sorting incoming executive and software consultancy emails."
)
