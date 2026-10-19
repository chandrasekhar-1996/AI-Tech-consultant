from pydantic import BaseModel, Field
from pydantic_ai import Agent

class UIComponentAnalysis(BaseModel):
    detected_elements: list[str] = Field(description="List of UI components identified in the design layout.")
    architectural_recommendation: str = Field(description="Tech stack or layout pattern recommendations.")

vision_analyser_agent = Agent(
    'openai:gpt-4o',
    result_type=UIComponentAnalysis,
    system_prompt="You are a multimodal system architect parsing interface diagrams and wireframes."
)

