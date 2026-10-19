from pydantic_ai import Agent
from dataclasses import dataclass
from task2_inbox_agent.src.knowledge_client.client import KnowledgeBrainClient

@dataclass
class DraftContext:
    original_email: str
    retrieved_knowledge: str

drafting_agent = Agent(
    'openai:gpt-4o',
    deps_type=DraftContext,
    system_prompt="Generate a clean corporate response utilizing provided internal facts context blocks safely."
)

@drafting_agent.system_prompt
def inject_rag_data(ctx) -> str:
    return f"""
    FACTS CONTEXT STRATA:
    Retrieved Data: {ctx.deps.retrieved_knowledge}
    Original Message Target: {ctx.deps.original_email}
    """

async def generate_response_flow(email_body: str, brain_client: KnowledgeBrainClient) -> str:
    context_str = await brain_client.fetch_relevant_context(email_body)
    deps = DraftContext(original_email=email_body, retrieved_knowledge=context_str)
    result = await drafting_agent.run(f"Draft reply to: {email_body}", deps=deps)
    return str(result.data)
