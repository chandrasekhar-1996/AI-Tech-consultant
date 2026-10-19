import pytest
from task1_knowledge_brain.retrieval.vector_store import RetrievalEngine
from task2_inbox_agent.src.email.classifier import triage_agent, EmailTriageSchema
from task3_meeting_to_scope.agents.orchestrator import ScopingStateRouter

@pytest.mark.asyncio
async def test_task1_vector_engine_integration():
    engine = RetrievalEngine(collection_name="test_brain")
    engine.add_document(
        url="https://test-docs.internal",
        title="Infrastructure Guide",
        content="Our primary container orchestration environment operates exclusively on secure Amazon EKS engine clusters."
    )
    results = engine.query_knowledge("EKS container clusters info extraction", n_results=1)
    assert len(results) > 0
    assert "EKS" in results[0]["content"]

@pytest.mark.asyncio
async def test_task2_classifier_agent():
    mock_email = "Help! Our database server is down and throwing 500 error anomalies across user endpoints."
    result = await triage_agent.run(mock_email)
    data: EmailTriageSchema = result.data
    assert data.category in ["technical_support", "sales_inquiry"]
    assert data.urgency == "high"

@pytest.mark.asyncio
async def test_task3_scoping_pipeline():
    transcript = "We require building a FastAPI server profile using Python within a 6 week window."
    pipeline_output = await ScopingStateRouter.process_transcript_to_scope(transcript)
    
    assert "requirements" in pipeline_output
    assert "scope" in pipeline_output
    assert pipeline_output["requirements"]["timeline_weeks"] == 6
    assert "FastAPI" in pipeline_output["requirements"]["tech_stack"]

    diff_report = ScopingStateRouter.calculate_scope_diff(
        "Feature: Core Endpoint Auth setup",
        "Feature: Core Endpoint Auth setup with multi-region OAuth validation"
    )
    assert "OAuth" in diff_report
