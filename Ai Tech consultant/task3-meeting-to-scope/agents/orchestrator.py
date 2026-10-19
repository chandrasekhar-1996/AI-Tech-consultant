from typing import Dict, Any
from pydantic import BaseModel, Field
from pydantic import Agent

# 1. Structured Schemas
class ExtractedRequirements(BaseModel):
    deliverables: list[str] = Field(description="List of core feature items identified.")
    timeline_weeks: int = Field(description="Estimated deployment execution window.")
    tech_stack: list[str] = Field(description="Identified target technologies.")

class RefinedScope(BaseModel):
    scope_document: str = Field(description="Markdown formatted statement of work blueprint.")
    risk_factors: list[str] = Field(description="Identified infrastructural risks or unknowns.")

# 2. Specialized Multi-Agent Framework
extraction_agent = Agent('openai:gpt-4o', result_type=ExtractedRequirements, system_prompt="Extract structural technical criteria out of meeting dialogue logs.")
refinement_agent = Agent('openai:gpt-4o', result_type=RefinedScope, system_prompt="Compile structured enterprise blueprints using raw scoping metadata profiles.")

# 3. Dynamic Execution Router Blueprint
class ScopingStateRouter:
    @staticmethod
    async def process_transcript_to_scope(transcript: str) -> Dict[str, Any]:
        # Step A: Perform Raw Extraction Execution
        extraction_res = await extraction_agent.run(transcript)
        reqs: ExtractedRequirements = extraction_res.data
        
        # Step B: Inject into Scope Generation Agent
        refinement_prompt = f"""
        Construct a master Statement of Work framework from these criteria:
        Deliverables: {', '.join(reqs.deliverables)}
        Timeline Requirement: {reqs.timeline_weeks} weeks
        Tech Stack Core: {', '.join(reqs.tech_stack)}
        """
        
        refinement_res = await refinement_agent.run(refinement_prompt)
        scope: RefinedScope = refinement_res.data
        
        return {
            "requirements": reqs.model_dump(),
            "scope": scope.model_dump()
        }

    @staticmethod
    def calculate_scope_diff(version_a: str, version_b: str) -> str:
        """Computes structural baseline changes between system updates."""
        import difflib
        diff = difflib.unified_diff(
            version_a.splitlines(keepends=True),
            version_b.splitlines(keepends=True),
            fromfile='Baseline Scope V1',
            tofile='Revised Scope V2'
        )
        return "".join(diff)
