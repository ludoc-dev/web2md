"""
Subagent Orchestrator - Orchestrate multiple subagents with generated prompts
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .task_decomposer import TaskDecomposer, Subtask, ExecutionStrategy
from .generator import AutoPromptGenerator, GeneratedPrompt
from .classifier import TaskClassifier, TaskType, Complexity
from .result_aggregator import ResultAggregator, AgentResult, AggregatedResult, AggregationStrategy


@dataclass
class OrchestrationResult:
    """Result from orchestrating a task"""
    task_description: str
    strategy_used: str
    subtasks_total: int
    subtasks_completed: int
    subtasks_failed: int
    results: List[AgentResult]
    aggregated_result: AggregatedResult
    execution_time: float
    metadata: Dict[str, Any]


class SubagentOrchestrator:
    """Orchestrate multiple subagents with generated prompts"""

    def __init__(self):
        """Initialize subagent orchestrator"""
        self.task_classifier = TaskClassifier()
        self.task_decomposer = TaskDecomposer()
        self.prompt_generator = AutoPromptGenerator()
        self.result_aggregator = ResultAggregator()
        self.max_parallel = 6  # autonomous-automation limit

    async def execute_task(
        self,
        task_description: str,
        strategy: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None
    ) -> OrchestrationResult:
        """
        Execute a task with subagent orchestration

        Args:
            task_description: Description of the task to execute
            strategy: Execution strategy (auto-detect if None)
            constraints: Optional constraints (complexity, model, etc.)

        Returns:
            OrchestrationResult with all results
        """
        start_time = time.time()

        # Step 1: Classify task
        classification = self.task_classifier.classify(task_description)

        # Apply constraints if provided
        if constraints and "complexity" in constraints:
            classification.complexity = Complexity(constraints["complexity"])

        # Step 2: Determine strategy
        if strategy is None:
            strategy = classification.suggested_strategy

        # Step 3: Decompose task
        subtasks = self.task_decomposer.decompose(
            task_description,
            classification.task_type,
            classification.complexity,
            strategy
        )

        # Step 4: Generate prompts for each subtask
        prompts = await self._generate_prompts(subtasks, constraints)

        # Step 5: Execute subtasks
        results = await self._execute_subtasks(subtasks, prompts, strategy)

        # Step 6: Aggregate results
        aggregated = self.result_aggregator.aggregate(
            results,
            strategy=self._select_aggregation_strategy(strategy)
        )

        execution_time = time.time() - start_time

        return OrchestrationResult(
            task_description=task_description,
            strategy_used=strategy,
            subtasks_total=len(subtasks),
            subtasks_completed=len([r for r in results if r.success]),
            subtasks_failed=len([r for r in results if not r.success]),
            results=results,
            aggregated_result=aggregated,
            execution_time=execution_time,
            metadata={
                "classification": {
                    "type": classification.task_type.value,
                    "complexity": classification.complexity.value,
                    "confidence": classification.confidence
                },
                "subtasks": [
                    {
                        "id": s.id,
                        "description": s.description,
                        "type": s.task_type.value,
                        "priority": s.priority
                    }
                    for s in subtasks
                ]
            }
        )

    async def _generate_prompts(
        self,
        subtasks: List[Subtask],
        constraints: Optional[Dict[str, Any]]
    ) -> Dict[int, GeneratedPrompt]:
        """Generate prompts for each subtask"""
        prompts = {}

        for subtask in subtasks:
            try:
                prompt_result = await self.prompt_generator.generate_prompt(
                    subtask.description,
                    constraints
                )
                prompts[subtask.id] = prompt_result
            except Exception as e:
                # Create fallback prompt
                prompts[subtask.id] = GeneratedPrompt(
                    prompt=f"Complete this task: {subtask.description}",
                    quality_score=0.5,
                    metadata={"fallback": True, "error": str(e)},
                    context_sources_used=[],
                    token_estimate=1000
                )

        return prompts

    async def _execute_subtasks(
        self,
        subtasks: List[Subtask],
        prompts: Dict[int, GeneratedPrompt],
        strategy: str
    ) -> List[AgentResult]:
        """Execute subtasks with appropriate strategy"""
        if strategy == ExecutionStrategy.PARALLEL.value:
            return await self._execute_parallel(subtasks, prompts)
        elif strategy == ExecutionStrategy.SEQUENTIAL.value:
            return await self._execute_sequential(subtasks, prompts)
        else:  # HYBRID
            return await self._execute_hybrid(subtasks, prompts)

    async def _execute_parallel(
        self,
        subtasks: List[Subtask],
        prompts: Dict[int, GeneratedPrompt]
    ) -> List[AgentResult]:
        """Execute subtasks in parallel"""
        # Limit to max_parallel
        batch_size = min(len(subtasks), self.max_parallel)

        # Create batches
        batches = [
            subtasks[i:i + batch_size]
            for i in range(0, len(subtasks), batch_size)
        ]

        all_results = []

        for batch in batches:
            # Execute batch in parallel
            batch_tasks = [
                self._execute_single_subtask(subtask, prompts[subtask.id])
                for subtask in batch
            ]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            # Process results
            for result in batch_results:
                if isinstance(result, Exception):
                    # Create failed result
                    all_results.append(AgentResult(
                        subtask_id=0,
                        output="",
                        metadata={"error": str(result)},
                        confidence=0.0,
                        execution_time=0.0,
                        success=False,
                        error_message=str(result)
                    ))
                else:
                    all_results.append(result)

        return all_results

    async def _execute_sequential(
        self,
        subtasks: List[Subtask],
        prompts: Dict[int, GeneratedPrompt]
    ) -> List[AgentResult]:
        """Execute subtasks sequentially"""
        results = []

        for subtask in subtasks:
            result = await self._execute_single_subtask(subtask, prompts[subtask.id])
            results.append(result)

            # Stop if critical subtask failed
            if not result.success and subtask.priority == "critical":
                # Mark remaining as failed
                for remaining_subtask in subtasks[subtasks.index(subtask) + 1:]:
                    results.append(AgentResult(
                        subtask_id=remaining_subtask.id,
                        output="",
                        metadata={"skipped": True},
                        confidence=0.0,
                        execution_time=0.0,
                        success=False,
                        error_message="Skipped due to critical failure"
                    ))
                break

        return results

    async def _execute_hybrid(
        self,
        subtasks: List[Subtask],
        prompts: Dict[int, GeneratedPrompt]
    ) -> List[AgentResult]:
        """Execute subtasks with hybrid strategy"""
        # Separate independent and dependent subtasks
        independent = [s for s in subtasks if not s.dependencies]
        dependent = [s for s in subtasks if s.dependencies]

        results = []

        # Execute independent in parallel
        if independent:
            independent_results = await self._execute_parallel(independent, prompts)
            results.extend(independent_results)

        # Execute dependent sequentially
        if dependent:
            # Sort by dependencies
            dependent.sort(key=lambda s: len(s.dependencies))
            dependent_results = await self._execute_sequential(dependent, prompts)
            results.extend(dependent_results)

        return results

    async def _execute_single_subtask(
        self,
        subtask: Subtask,
        prompt: GeneratedPrompt
    ) -> AgentResult:
        """Execute a single subtask (mock implementation)"""
        start_time = time.time()

        # In real implementation, this would:
        # 1. Spawn a subagent (using Agent tool)
        # 2. Provide the generated prompt
        # 3. Wait for completion
        # 4. Return the result

        # Mock implementation for now
        await asyncio.sleep(0.1)  # Simulate work

        execution_time = time.time() - start_time

        # Mock result
        return AgentResult(
            subtask_id=subtask.id,
            output=f"Mock output for subtask {subtask.id}: {subtask.description}",
            metadata={
                "prompt_quality": prompt.quality_score,
                "tokens_used": prompt.token_estimate,
                "strategy": "mock"
            },
            confidence=0.8,
            execution_time=execution_time,
            success=True
        )

    def _select_aggregation_strategy(self, execution_strategy: str) -> str:
        """Select appropriate aggregation strategy"""
        if execution_strategy == ExecutionStrategy.PARALLEL.value:
            return AggregationStrategy.MERGE.value
        elif execution_strategy == ExecutionStrategy.SEQUENTIAL.value:
            return AggregationStrategy.APPEND.value
        else:
            return AggregationStrategy.CONSENSUS.value
