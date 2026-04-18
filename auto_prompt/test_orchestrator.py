import asyncio
import unittest.mock as mock
import pytest

from auto_prompt.core.orchestrator import SubagentOrchestrator
from auto_prompt.core.task_decomposer import TaskDecomposer, ExecutionStrategy, Subtask
from auto_prompt.core.generator import AutoPromptGenerator, GeneratedPrompt
from auto_prompt.core.classifier import TaskClassifier, TaskType, Complexity
from auto_prompt.core.result_aggregator import ResultAggregator, AgentResult, AggregatedResult, AggregationStrategy


@pytest.mark.asyncio
async def test_orchestrator(mocker):
    """Test subagent orchestrator"""
    # Mock AutoPromptGenerator.generate_prompt
    mocker.patch(
        'auto_prompt.core.orchestrator.AutoPromptGenerator.generate_prompt',
        new_callable=mock.AsyncMock,
        return_value=GeneratedPrompt(
            prompt="Mocked prompt for subtask",
            quality_score=0.9,
            metadata={"mocked": True},
            context_sources_used=["mock_source_1"],
            token_estimate=500
        )
    )

    orchestrator = SubagentOrchestrator()

    test_tasks = [
        ("Implement user authentication with JWT", "parallel"),
        ("Debug memory leak in authentication service", "sequential"),
        ("Research JWT authentication best practices", "sequential"),
        ("Build comprehensive distributed authentication system", "parallel")
    ]

    for task, strategy in test_tasks:
        result = await orchestrator.execute_task(task, strategy=strategy)

        assert result.subtasks_completed > 0
        assert result.aggregated_result.average_confidence > 0.0
        # Add more assertions as needed for a proper test

        # Optional: print results for debugging, but not for a standard test
        print(f"\n📋 Task: {task}")
        print(f"🚀 Strategy: {strategy}")
        print(f"\n✅ Execution completed")
        print(f"   Strategy: {result.strategy_used}")
        print(f"   Subtasks: {result.subtasks_completed}/{result.subtasks_total}")
        print(f"   Failed: {result.subtasks_failed}")
        print(f"   Time: {result.execution_time:.2f}s")
        print(f"   Success Rate: {result.aggregated_result.success_rate:.2%}")
        print(f"   Avg Confidence: {result.aggregated_result.average_confidence:.2f}")

        print(f"\n📝 Subtasks:")
        for subtask in result.metadata["subtasks"]:
            print(f"   - {subtask['id']}: {subtask['description'][:60]}...")
            print(f"     Type: {subtask['type']}, Priority: {subtask['priority']}")


