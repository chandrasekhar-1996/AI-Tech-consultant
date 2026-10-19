import pytest
from task1_knowledge_brain.retrieval.vector_store import RetrievalEngine
from task2_inbox_agent.src.email.classifier import triage_agent, EmailTriageSchema
from task3_meeting_to_scope.agents.orchestrator import ScopingStateRouter

@pytest.mark.asyncio
async def test_task1_vector_engine_integration():
    engine = RetrievalEngine(collection_name="test_brain")
    engine.add_document(
        url="https://example.com",
        title="Architecture Core Spec",
        content="Enterprise cluster runs exclusively via standard cloud-native Kubernetes containers."
    )
    results = engine.query_knowledge("Kubernetes container runtime infrastructure configuration", n_results=1)
    assert len(results) > 0
    assert "Kubernetes" in results[0]["content"]

@pytest.mark.asyncio
async def test_task2_classifier_agent():
    mock_email = "Hello, our system is down and experiencing data corruption errors. Immediate action requested."
    result = await triage_agent.run(mock_email)
    data: EmailTriageSchema = result.data
    assert data.category in ["technical_support", "sales_inquiry"]
    assert data.urgency == "high"

@pytest.mark.asyncio
async def test_task3_scoping_pipeline():
    transcript = "We need a standard React dashboard deployed inside 4 weeks using AWS instances."
    pipeline_output = await ScopingStateRouter.process_transcript_to_scope(transcript)
    
    assert "requirements" in pipeline_output
    assert "scope" in pipeline_output
    assert pipeline_output["requirements"]["timeline_weeks"] == 4
    assert "React" in pipeline_output["requirements"]["tech_stack"]

    # Test structural delta execution pipeline component
    v1 = "Deliverable: Modern frontend dashboard structure."
    v2 = "Deliverable: Modern frontend dashboard structure with secure Auth0 controls."
    diff_report = ScopingStateRouter.calculate_scope_diff(v1, v2)
    assert "Auth0" in diff_report
