"""
Task Decomposer - Decompose complex tasks into subtasks
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .classifier import TaskType, Complexity


class ExecutionStrategy(Enum):
    """Execution strategy for subtasks"""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    HYBRID = "hybrid"


@dataclass
class Subtask:
    """A subtask from decomposition"""
    id: int
    description: str
    task_type: TaskType
    dependencies: List[int]  # IDs of subtasks this depends on
    priority: str  # critical, high, medium, low
    estimated_tokens: int
    context_requirements: List[str]  # What context this subtask needs
    metadata: Dict[str, Any]


class TaskDecomposer:
    """Decompose complex tasks into independent subtasks"""

    def __init__(self):
        """Initialize task decomposer"""
        self.max_subtasks = 6  # Match autonomous-automation limit

    def decompose(
        self,
        task_description: str,
        task_type: TaskType,
        complexity: Complexity,
        strategy: Optional[str] = None
    ) -> List[Subtask]:
        """
        Decompose a task into subtasks

        Args:
            task_description: Original task description
            task_type: Type of the main task
            complexity: Complexity of the main task
            strategy: Execution strategy (auto-detect if None)

        Returns:
            List of subtasks
        """
        # Auto-detect strategy if not provided
        if strategy is None:
            strategy = self._detect_strategy(task_type, complexity)

        # Decompose based on task type
        if task_type == TaskType.IMPLEMENTATION:
            subtasks = self._decompose_implementation(task_description, complexity)
        elif task_type == TaskType.REFACTORING:
            subtasks = self._decompose_refactoring(task_description, complexity)
        elif task_type == TaskType.DEBUGGING:
            subtasks = self._decompose_debugging(task_description, complexity)
        elif task_type == TaskType.RESEARCH:
            subtasks = self._decompose_research(task_description, complexity)
        else:
            # Generic decomposition
            subtasks = self._decompose_generic(task_description, complexity)

        # Apply strategy
        subtasks = self._apply_strategy(subtasks, strategy)

        # Limit to max_subtasks
        if len(subtasks) > self.max_subtasks:
            subtasks = subtasks[:self.max_subtasks]

        return subtasks

    def _detect_strategy(self, task_type: TaskType, complexity: Complexity) -> str:
        """Detect appropriate execution strategy"""
        # Debugging and research are usually sequential
        if task_type in [TaskType.DEBUGGING, TaskType.RESEARCH]:
            return ExecutionStrategy.SEQUENTIAL.value

        # High complexity tasks benefit from parallel
        if complexity == Complexity.HIGH:
            return ExecutionStrategy.PARALLEL.value

        # Default: hybrid
        return ExecutionStrategy.HYBRID.value

    def _decompose_implementation(
        self,
        task_description: str,
        complexity: Complexity
    ) -> List[Subtask]:
        """Decompose implementation task"""
        subtasks = []

        # Subtask 1: Research & Analysis
        subtasks.append(Subtask(
            id=1,
            description=f"Research similar implementations and best practices for: {task_description}",
            task_type=TaskType.RESEARCH,
            dependencies=[],
            priority="high",
            estimated_tokens=1500,
            context_requirements=["semantic_search", "web2md"],
            metadata={"phase": "research"}
        ))

        # Subtask 2: Design
        subtasks.append(Subtask(
            id=2,
            description=f"Design architecture and implementation plan for: {task_description}",
            task_type=TaskType.IMPLEMENTATION,
            dependencies=[1],
            priority="high",
            estimated_tokens=2000,
            context_requirements=["code_graph", "dependencies"],
            metadata={"phase": "design"}
        ))

        # Subtask 3: Core Implementation
        subtasks.append(Subtask(
            id=3,
            description=f"Implement core functionality: {task_description}",
            task_type=TaskType.IMPLEMENTATION,
            dependencies=[2],
            priority="critical",
            estimated_tokens=3000,
            context_requirements=["semantic_search", "code_graph"],
            metadata={"phase": "implementation"}
        ))

        # Subtask 4: Testing
        if complexity in [Complexity.MEDIUM, Complexity.HIGH]:
            subtasks.append(Subtask(
                id=4,
                description=f"Create comprehensive tests for: {task_description}",
                task_type=TaskType.TESTING,
                dependencies=[3],
                priority="high",
                estimated_tokens=2000,
                context_requirements=["semantic_search"],
                metadata={"phase": "testing"}
            ))

        # Subtask 5: Documentation
        if complexity == Complexity.HIGH:
            subtasks.append(Subtask(
                id=5,
                description=f"Create documentation for: {task_description}",
                task_type=TaskType.DOCUMENTATION,
                dependencies=[3],
                priority="medium",
                estimated_tokens=1500,
                context_requirements=["web2md"],
                metadata={"phase": "documentation"}
            ))

        return subtasks

    def _decompose_refactoring(
        self,
        task_description: str,
        complexity: Complexity
    ) -> List[Subtask]:
        """Decompose refactoring task"""
        subtasks = []

        # Subtask 1: Analysis
        subtasks.append(Subtask(
            id=1,
            description=f"Analyze current implementation and identify issues: {task_description}",
            task_type=TaskType.DEBUGGING,
            dependencies=[],
            priority="critical",
            estimated_tokens=2000,
            context_requirements=["code_graph", "impact_analysis"],
            metadata={"phase": "analysis"}
        ))

        # Subtask 2: Design Refactoring
        subtasks.append(Subtask(
            id=2,
            description=f"Design refactoring approach: {task_description}",
            task_type=TaskType.REFACTORING,
            dependencies=[1],
            priority="high",
            estimated_tokens=1500,
            context_requirements=["trace_calls"],
            metadata={"phase": "design"}
        ))

        # Subtask 3: Implementation
        subtasks.append(Subtask(
            id=3,
            description=f"Implement refactoring: {task_description}",
            task_type=TaskType.REFACTORING,
            dependencies=[2],
            priority="critical",
            estimated_tokens=2500,
            context_requirements=["code_graph"],
            metadata={"phase": "implementation"}
        ))

        # Subtask 4: Validation
        subtasks.append(Subtask(
            id=4,
            description=f"Validate refactoring and run tests: {task_description}",
            task_type=TaskType.TESTING,
            dependencies=[3],
            priority="high",
            estimated_tokens=1500,
            context_requirements=["semantic_search"],
            metadata={"phase": "validation"}
        ))

        return subtasks

    def _decompose_debugging(
        self,
        task_description: str,
        complexity: Complexity
    ) -> List[Subtask]:
        """Decompose debugging task"""
        subtasks = []

        # Subtask 1: Investigation
        subtasks.append(Subtask(
            id=1,
            description=f"Investigate and identify root cause: {task_description}",
            task_type=TaskType.DEBUGGING,
            dependencies=[],
            priority="critical",
            estimated_tokens=2000,
            context_requirements=["semantic_search", "code_context"],
            metadata={"phase": "investigation"}
        ))

        # Subtask 2: Analysis
        subtasks.append(Subtask(
            id=2,
            description=f"Analyze similar issues and solutions: {task_description}",
            task_type=TaskType.RESEARCH,
            dependencies=[1],
            priority="high",
            estimated_tokens=1500,
            context_requirements=["semantic_search"],
            metadata={"phase": "analysis"}
        ))

        # Subtask 3: Fix Implementation
        subtasks.append(Subtask(
            id=3,
            description=f"Implement fix for: {task_description}",
            task_type=TaskType.DEBUGGING,
            dependencies=[2],
            priority="critical",
            estimated_tokens=2000,
            context_requirements=["code_graph"],
            metadata={"phase": "fix"}
        ))

        # Subtask 4: Testing
        subtasks.append(Subtask(
            id=4,
            description=f"Test fix and prevent regression: {task_description}",
            task_type=TaskType.TESTING,
            dependencies=[3],
            priority="high",
            estimated_tokens=1500,
            context_requirements=["semantic_search"],
            metadata={"phase": "testing"}
        ))

        return subtasks

    def _decompose_research(
        self,
        task_description: str,
        complexity: Complexity
    ) -> List[Subtask]:
        """Decompose research task"""
        subtasks = []

        # Subtask 1: Initial Research
        subtasks.append(Subtask(
            id=1,
            description=f"Conduct initial research: {task_description}",
            task_type=TaskType.RESEARCH,
            dependencies=[],
            priority="critical",
            estimated_tokens=2500,
            context_requirements=["semantic_search", "web2md"],
            metadata={"phase": "research"}
        ))

        # Subtask 2: Analysis
        subtasks.append(Subtask(
            id=2,
            description=f"Analyze findings and compare approaches: {task_description}",
            task_type=TaskType.RESEARCH,
            dependencies=[1],
            priority="high",
            estimated_tokens=2000,
            context_requirements=["semantic_search"],
            metadata={"phase": "analysis"}
        ))

        # Subtask 3: Documentation
        subtasks.append(Subtask(
            id=3,
            description=f"Document findings and recommendations: {task_description}",
            task_type=TaskType.DOCUMENTATION,
            dependencies=[2],
            priority="high",
            estimated_tokens=2000,
            context_requirements=["web2md"],
            metadata={"phase": "documentation"}
        ))

        return subtasks

    def _decompose_generic(
        self,
        task_description: str,
        complexity: Complexity
    ) -> List[Subtask]:
        """Generic task decomposition"""
        subtasks = []

        # Subtask 1: Analysis
        subtasks.append(Subtask(
            id=1,
            description=f"Analyze task requirements: {task_description}",
            task_type=TaskType.RESEARCH,
            dependencies=[],
            priority="high",
            estimated_tokens=1500,
            context_requirements=["semantic_search"],
            metadata={"phase": "analysis"}
        ))

        # Subtask 2: Execution
        subtasks.append(Subtask(
            id=2,
            description=f"Execute task: {task_description}",
            task_type=TaskType.IMPLEMENTATION,
            dependencies=[1],
            priority="critical",
            estimated_tokens=2500,
            context_requirements=["semantic_search", "code_graph"],
            metadata={"phase": "execution"}
        ))

        # Subtask 3: Validation
        subtasks.append(Subtask(
            id=3,
            description=f"Validate and test: {task_description}",
            task_type=TaskType.TESTING,
            dependencies=[2],
            priority="high",
            estimated_tokens=1500,
            context_requirements=["semantic_search"],
            metadata={"phase": "validation"}
        ))

        return subtasks

    def _apply_strategy(
        self,
        subtasks: List[Subtask],
        strategy: str
    ) -> List[Subtask]:
        """Apply execution strategy to subtasks"""
        if strategy == ExecutionStrategy.PARALLEL.value:
            # Make all subtasks independent (remove dependencies)
            for subtask in subtasks:
                subtask.dependencies = []

        elif strategy == ExecutionStrategy.SEQUENTIAL:
            # Ensure sequential dependencies
            for i in range(1, len(subtasks)):
                if subtasks[i].dependencies == []:
                    subtasks[i].dependencies = [i]

        # Hybrid keeps original dependencies

        return subtasks
