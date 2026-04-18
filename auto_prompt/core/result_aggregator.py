"""
Result Aggregator - Aggregate results from multiple subagents
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json


class AggregationStrategy(Enum):
    """Strategies for aggregating results"""
    APPEND = "append"  # Concatenate all results
    MERGE = "merge"    # Merge structured results
    VOTE = "vote"      # Majority voting
    CONSENSUS = "consensus"  # Weighted consensus


@dataclass
class AgentResult:
    """Result from a subagent"""
    subtask_id: int
    output: str
    metadata: Dict[str, Any]
    confidence: float
    execution_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class AggregatedResult:
    """Aggregated result from multiple subagents"""
    outputs: List[str]
    merged_output: str
    metadata: Dict[str, Any]
    confidence_scores: List[float]
    average_confidence: float
    execution_times: List[float]
    total_execution_time: float
    success_rate: float
    strategy_used: str


class ResultAggregator:
    """Aggregate results from multiple subagents"""

    def __init__(self):
        """Initialize result aggregator"""
        pass

    def aggregate(
        self,
        results: List[AgentResult],
        strategy: str = AggregationStrategy.MERGE.value
    ) -> AggregatedResult:
        """
        Aggregate results from multiple subagents

        Args:
            results: List of agent results
            strategy: Aggregation strategy to use

        Returns:
            Aggregated result
        """
        if not results:
            return self._empty_result()

        # Filter successful results
        successful_results = [r for r in results if r.success]

        if not successful_results:
            return self._failed_result(results)

        # Apply aggregation strategy
        if strategy == AggregationStrategy.APPEND.value:
            return self._append_aggregation(successful_results)
        elif strategy == AggregationStrategy.MERGE.value:
            return self._merge_aggregation(successful_results)
        elif strategy == AggregationStrategy.VOTE.value:
            return self._vote_aggregation(successful_results)
        elif strategy == AggregationStrategy.CONSENSUS.value:
            return self._consensus_aggregation(successful_results)
        else:
            return self._merge_aggregation(successful_results)  # Default

    def _append_aggregation(self, results: List[AgentResult]) -> AggregatedResult:
        """Append all results"""
        outputs = []
        for result in results:
            outputs.append(f"## Subtask {result.subtask_id}\n\n{result.output}")

        merged_output = "\n\n---\n\n".join(outputs)

        return AggregatedResult(
            outputs=[r.output for r in results],
            merged_output=merged_output,
            metadata=self._aggregate_metadata(results),
            confidence_scores=[r.confidence for r in results],
            average_confidence=sum(r.confidence for r in results) / len(results),
            execution_times=[r.execution_time for r in results],
            total_execution_time=sum(r.execution_time for r in results),
            success_rate=len(results) / len([r for r in results if r.success]),
            strategy_used=AggregationStrategy.APPEND.value
        )

    def _merge_aggregation(self, results: List[AgentResult]) -> AggregatedResult:
        """Merge structured results"""
        # Try to merge structured outputs
        structured_results = []
        text_results = []

        for result in results:
            if self._is_structured(result.output):
                structured_results.append(result)
            else:
                text_results.append(result)

        merged = {}
        metadata = {}

        # Merge structured results
        for result in structured_results:
            try:
                data = json.loads(result.output)
                if isinstance(data, dict):
                    merged.update(data)
            except:
                text_results.append(result)

        # Create merged output
        if merged:
            merged_output = json.dumps(merged, indent=2)
            if text_results:
                merged_output += "\n\n## Additional Results\n\n"
                merged_output += "\n\n---\n\n".join([
                    f"### Subtask {r.subtask_id}\n{r.output}"
                    for r in text_results
                ])
        else:
            # Fall back to append
            return self._append_aggregation(results)

        return AggregatedResult(
            outputs=[r.output for r in results],
            merged_output=merged_output,
            metadata=self._aggregate_metadata(results),
            confidence_scores=[r.confidence for r in results],
            average_confidence=sum(r.confidence for r in results) / len(results),
            execution_times=[r.execution_time for r in results],
            total_execution_time=sum(r.execution_time for r in results),
            success_rate=len(results) / len(results) if results else 0,
            strategy_used=AggregationStrategy.MERGE.value
        )

    def _vote_aggregation(self, results: List[AgentResult]) -> AggregatedResult:
        """Majority voting aggregation"""
        # Group similar outputs
        output_groups = {}
        for result in results:
            # Simple grouping by output hash (could be smarter)
            output_hash = hash(result.output)
            if output_hash not in output_groups:
                output_groups[output_hash] = []
            output_groups[output_hash].append(result)

        # Find majority
        if output_groups:
            majority_group = max(output_groups.values(), key=len)
            majority_result = majority_group[0]

            return AggregatedResult(
                outputs=[r.output for r in results],
                merged_output=majority_result.output,
                metadata=self._aggregate_metadata(results),
                confidence_scores=[r.confidence for r in results],
                average_confidence=sum(r.confidence for r in majority_group) / len(majority_group),
                execution_times=[r.execution_time for r in results],
                total_execution_time=sum(r.execution_time for r in results),
                success_rate=len(majority_group) / len(results),
                strategy_used=AggregationStrategy.VOTE.value
            )

        # Fall back to merge
        return self._merge_aggregation(results)

    def _consensus_aggregation(self, results: List[AgentResult]) -> AggregatedResult:
        """Weighted consensus aggregation"""
        # Weight by confidence
        weighted_outputs = []
        for result in results:
            weighted_outputs.append({
                "output": result.output,
                "weight": result.confidence,
                "subtask_id": result.subtask_id
            })

        # Sort by weight
        weighted_outputs.sort(key=lambda x: x["weight"], reverse=True)

        # Build consensus output
        consensus_parts = []
        for item in weighted_outputs:
            consensus_parts.append(
                f"### Subtask {item['subtask_id']} (confidence: {item['weight']:.2f})\n\n{item['output']}"
            )

        merged_output = "\n\n---\n\n".join(consensus_parts)

        return AggregatedResult(
            outputs=[r.output for r in results],
            merged_output=merged_output,
            metadata=self._aggregate_metadata(results),
            confidence_scores=[r.confidence for r in results],
            average_confidence=sum(r.confidence for r in results) / len(results),
            execution_times=[r.execution_time for r in results],
            total_execution_time=sum(r.execution_time for r in results),
            success_rate=len(results) / len(results) if results else 0,
            strategy_used=AggregationStrategy.CONSENSUS.value
        )

    def _is_structured(self, output: str) -> bool:
        """Check if output is structured (JSON)"""
        try:
            json.loads(output)
            return True
        except:
            return False

    def _aggregate_metadata(self, results: List[AgentResult]) -> Dict[str, Any]:
        """Aggregate metadata from results"""
        aggregated = {
            "total_results": len(results),
            "successful_results": len([r for r in results if r.success]),
            "failed_results": len([r for r in results if not r.success]),
            "subtask_ids": [r.subtask_id for r in results],
            "strategies_used": [r.metadata.get("strategy", "unknown") for r in results]
        }

        return aggregated

    def _empty_result(self) -> AggregatedResult:
        """Return empty result"""
        return AggregatedResult(
            outputs=[],
            merged_output="No results to aggregate",
            metadata={"total_results": 0},
            confidence_scores=[],
            average_confidence=0.0,
            execution_times=[],
            total_execution_time=0.0,
            success_rate=0.0,
            strategy_used="none"
        )

    def _failed_result(self, results: List[AgentResult]) -> AggregatedResult:
        """Return failed result"""
        errors = [r.error_message for r in results if r.error_message]

        return AggregatedResult(
            outputs=[],
            merged_output=f"All subtasks failed. Errors: {'; '.join(errors)}",
            metadata=self._aggregate_metadata(results),
            confidence_scores=[r.confidence for r in results],
            average_confidence=sum(r.confidence for r in results) / len(results) if results else 0.0,
            execution_times=[r.execution_time for r in results],
            total_execution_time=sum(r.execution_time for r in results),
            success_rate=0.0,
            strategy_used="failed"
        )
