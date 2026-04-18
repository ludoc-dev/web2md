"""
Task Classifier - Analyzes tasks and determines type, complexity, and expertise
"""

import re
from enum import Enum
from typing import Tuple, List, Optional
from dataclasses import dataclass


class TaskType(Enum):
    """Types of tasks that can be classified"""
    IMPLEMENTATION = "implementation"
    REFACTORING = "refactoring"
    DEBUGGING = "debugging"
    RESEARCH = "research"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    OPTIMIZATION = "optimization"


class Complexity(Enum):
    """Complexity levels for tasks"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Expertise(Enum):
    """Required expertise areas"""
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DEVOPS = "devops"
    DATA = "data"
    SECURITY = "security"
    GENERAL = "general"


@dataclass
class TaskClassification:
    """Result of task classification"""
    task_type: TaskType
    complexity: Complexity
    expertise: List[Expertise]
    confidence: float
    suggested_strategy: str  # parallel, sequential, hybrid
    estimated_tokens: int
    suggested_model: str  # sonnet, haiku, opus


class TaskClassifier:
    """Analyzes task descriptions and classifies them"""

    # Keywords for each task type
    TASK_KEYWORDS = {
        TaskType.IMPLEMENTATION: [
            "implement", "create", "build", "add", "develop", "write",
            "feature", "functionality", "endpoint", "api", "module"
        ],
        TaskType.REFACTORING: [
            "refactor", "restructure", "reorganize", "clean up", "improve",
            "simplify", "rework", "modernize", "optimize code"
        ],
        TaskType.DEBUGGING: [
            "debug", "fix", "error", "bug", "issue", "problem",
            "broken", "not working", "failure", "crash", "exception"
        ],
        TaskType.RESEARCH: [
            "research", "investigate", "explore", "find", "search",
            "look into", "analyze", "study", "investigation"
        ],
        TaskType.TESTING: [
            "test", "testing", "test case", "unit test", "integration test",
            "coverage", "mock", "spec", "verify", "validate"
        ],
        TaskType.DOCUMENTATION: [
            "document", "documentation", "readme", "guide", "tutorial",
            "comment", "explain", "docs", "api docs"
        ],
        TaskType.OPTIMIZATION: [
            "optimize", "performance", "speed", "faster", "efficient",
            "improve performance", "reduce", "minimize", "cache"
        ]
    }

    # Keywords for complexity detection
    COMPLEXITY_KEYWORDS = {
        Complexity.HIGH: [
            "complex", "advanced", "scalable", "distributed", "microservices",
            "architecture", "system", "multiple", "integration", "comprehensive"
        ],
        Complexity.MEDIUM: [
            "feature", "function", "module", "component", "service",
            "endpoint", "api", "interface", "implementation"
        ],
        Complexity.LOW: [
            "fix", "update", "change", "small", "simple", "minor",
            "tweak", "adjust", "refactor single", "one function"
        ]
    }

    # Keywords for expertise detection
    EXPERTISE_KEYWORDS = {
        Expertise.FRONTEND: [
            "frontend", "front-end", "ui", "ux", "interface", "component",
            "react", "vue", "angular", "svelte", "css", "html", "javascript",
            "typescript", "web", "browser", "responsive", "mobile"
        ],
        Expertise.BACKEND: [
            "backend", "back-end", "server", "api", "database", "sql",
            "nosql", "microservice", "service", "endpoint", "auth", "authentication",
            "authorization", "python", "node", "java", "go", "rust"
        ],
        Expertise.FULLSTACK: [
            "fullstack", "full-stack", "full stack", "mvp", "app", "application",
            "web app", "system", "platform"
        ],
        Expertise.DEVOPS: [
            "deploy", "deployment", "ci", "cd", "pipeline", "docker", "kubernetes",
            "infrastructure", "aws", "gcp", "azure", "terraform", "ansible"
        ],
        Expertise.DATA: [
            "data", "database", "etl", "pipeline", "analytics", "ml", "machine learning",
            "ai", "model", "training", "inference", "processing"
        ],
        Expertise.SECURITY: [
            "security", "auth", "authentication", "authorization", "encryption",
            "vulnerability", "penetration", "audit", "compliance", "oauth", "jwt"
        ]
    }

    def classify(self, task_description: str) -> TaskClassification:
        """
        Classify a task based on its description

        Args:
            task_description: The task description to classify

        Returns:
            TaskClassification with type, complexity, expertise, etc.
        """
        task_lower = task_description.lower()

        # Classify task type
        task_type = self._classify_task_type(task_lower)

        # Classify complexity
        complexity = self._classify_complexity(task_lower, task_type)

        # Classify expertise
        expertise = self._classify_expertise(task_lower)

        # Calculate confidence
        confidence = self._calculate_confidence(task_type, complexity, expertise, task_lower)

        # Suggest strategy
        strategy = self._suggest_strategy(task_type, complexity, expertise)

        # Estimate tokens
        estimated_tokens = self._estimate_tokens(complexity, task_type)

        # Suggest model
        suggested_model = self._suggest_model(complexity, task_type)

        return TaskClassification(
            task_type=task_type,
            complexity=complexity,
            expertise=expertise,
            confidence=confidence,
            suggested_strategy=strategy,
            estimated_tokens=estimated_tokens,
            suggested_model=suggested_model
        )

    def _classify_task_type(self, task_lower: str) -> TaskType:
        """Classify the type of task"""
        scores = {}

        for task_type, keywords in self.TASK_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            if score > 0:
                scores[task_type] = score

        if not scores:
            return TaskType.IMPLEMENTATION  # Default

        return max(scores, key=scores.get)

    def _classify_complexity(self, task_lower: str, task_type: TaskType) -> Complexity:
        """Classify the complexity of the task"""
        high_score = sum(1 for kw in self.COMPLEXITY_KEYWORDS[Complexity.HIGH] if kw in task_lower)
        medium_score = sum(1 for kw in self.COMPLEXITY_KEYWORDS[Complexity.MEDIUM] if kw in task_lower)
        low_score = sum(1 for kw in self.COMPLEXITY_KEYWORDS[Complexity.LOW] if kw in task_lower)

        # Adjust based on task type
        if task_type in [TaskType.DEBUGGING, TaskType.DOCUMENTATION]:
            return Complexity.MEDIUM

        if high_score > 0:
            return Complexity.HIGH
        elif low_score > 0:
            return Complexity.LOW
        else:
            return Complexity.MEDIUM

    def _classify_expertise(self, task_lower: str) -> List[Expertise]:
        """Classify required expertise areas"""
        expertise_scores = {}

        for expertise, keywords in self.EXPERTISE_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            if score > 0:
                expertise_scores[expertise] = score

        if not expertise_scores:
            return [Expertise.GENERAL]

        # Return top 2 expertise areas
        sorted_expertise = sorted(expertise_scores.items(), key=lambda x: x[1], reverse=True)
        return [exp for exp, _ in sorted_expertise[:2]]

    def _calculate_confidence(
        self,
        task_type: TaskType,
        complexity: Complexity,
        expertise: List[Expertise],
        task_lower: str
    ) -> float:
        """Calculate confidence score (0.0 to 1.0)"""
        # Count keyword matches
        type_keywords = self.TASK_KEYWORDS[task_type]
        type_matches = sum(1 for kw in type_keywords if kw in task_lower)

        complexity_keywords = self.COMPLEXITY_KEYWORDS[complexity]
        complexity_matches = sum(1 for kw in complexity_keywords if kw in task_lower)

        expertise_matches = sum(
            len([kw for kw in self.EXPERTISE_KEYWORDS[exp] if kw in task_lower])
            for exp in expertise
        )

        total_matches = type_matches + complexity_matches + expertise_matches

        # Base confidence on number of matches
        if total_matches >= 5:
            return 0.9
        elif total_matches >= 3:
            return 0.75
        elif total_matches >= 1:
            return 0.6
        else:
            return 0.5  # Low confidence for ambiguous tasks

    def _suggest_strategy(
        self,
        task_type: TaskType,
        complexity: Complexity,
        expertise: List[Expertise]
    ) -> str:
        """Suggest execution strategy"""
        # Debugging and research usually sequential
        if task_type in [TaskType.DEBUGGING, TaskType.RESEARCH]:
            return "sequential"

        # High complexity tasks benefit from parallel decomposition
        if complexity == Complexity.HIGH:
            return "parallel"

        # Fullstack tasks can be parallelized
        if Expertise.FULLSTACK in expertise:
            return "parallel"

        # Low complexity: sequential is fine
        if complexity == Complexity.LOW:
            return "sequential"

        # Default: hybrid
        return "hybrid"

    def _estimate_tokens(self, complexity: Complexity, task_type: TaskType) -> int:
        """Estimate token requirements for the task"""
        base_tokens = {
            Complexity.LOW: 1000,
            Complexity.MEDIUM: 2000,
            Complexity.HIGH: 4000
        }

        # Adjust by task type
        type_multiplier = {
            TaskType.RESEARCH: 1.5,  # Research needs more context
            TaskType.IMPLEMENTATION: 1.2,
            TaskType.REFACTORING: 1.3,
            TaskType.DEBUGGING: 1.1,
            TaskType.TESTING: 0.8,
            TaskType.DOCUMENTATION: 0.7,
            TaskType.OPTIMIZATION: 1.2
        }

        return int(base_tokens[complexity] * type_multiplier.get(task_type, 1.0))

    def _suggest_model(self, complexity: Complexity, task_type: TaskType) -> str:
        """Suggest appropriate Claude model"""
        # High complexity or research: sonnet
        if complexity == Complexity.HIGH or task_type == TaskType.RESEARCH:
            return "sonnet"

        # Low complexity: haiku is sufficient
        if complexity == Complexity.LOW:
            return "haiku"

        # Default: sonnet
        return "sonnet"
