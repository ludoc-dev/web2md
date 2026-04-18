"""
Auto Prompt Generator - Generates optimized prompts based on context
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .classifier import TaskClassifier, TaskType, Complexity
from .template_engine import TemplateEngine
from ..utils.mcp_client import AdvancedRAGClient, CodeGraphClient, Web2MDClient


@dataclass
class GeneratedPrompt:
    """Result of prompt generation"""
    prompt: str
    quality_score: float
    metadata: Dict[str, Any]
    context_sources_used: List[str]
    token_estimate: int


class AutoPromptGenerator:
    """Generates optimized prompts automatically based on context"""

    def __init__(self):
        """Initialize auto prompt generator"""
        self.classifier = TaskClassifier()
        self.template_engine = TemplateEngine()
        self.rag_client = AdvancedRAGClient()
        self.code_graph = CodeGraphClient()
        self.web2md = Web2MDClient()

    async def generate_prompt(
        self,
        task_description: str,
        constraints: Optional[Dict[str, Any]] = None
    ) -> GeneratedPrompt:
        """
        Generate an optimized prompt for a task

        Args:
            task_description: Description of the task
            constraints: Optional constraints (complexity, model, etc.)

        Returns:
            GeneratedPrompt with prompt and metadata
        """
        # Step 1: Classify the task
        classification = self.classifier.classify(task_description)

        # Apply constraints if provided
        if constraints:
            if "complexity" in constraints:
                classification.complexity = Complexity(constraints["complexity"])
            if "model" in constraints:
                classification.suggested_model = constraints["model"]

        # Step 2: Gather context
        context = await self._gather_context(
            classification.task_type,
            task_description,
            classification
        )

        # Step 3: Generate prompt
        prompt = self._generate_prompt_from_template(
            classification.task_type,
            context
        )

        # Step 4: Optimize prompt
        optimized_prompt = self._optimize_prompt(
            prompt,
            classification,
            constraints
        )

        # Step 5: Validate prompt
        quality_score = self._validate_prompt(optimized_prompt, classification)

        # Step 6: Generate metadata
        metadata = {
            "task_type": classification.task_type.value,
            "complexity": classification.complexity.value,
            "expertise": [exp.value for exp in classification.expertise],
            "strategy": classification.suggested_strategy,
            "model": classification.suggested_model,
            "confidence": classification.confidence
        }

        return GeneratedPrompt(
            prompt=optimized_prompt,
            quality_score=quality_score,
            metadata=metadata,
            context_sources_used=context.get("sources_used", []),
            token_estimate=classification.estimated_tokens
        )

    async def _gather_context(
        self,
        task_type: TaskType,
        task_description: str,
        classification
    ) -> Dict[str, Any]:
        """
        Gather relevant context from multiple sources

        Args:
            task_type: Type of task
            task_description: Task description
            classification: Task classification result

        Returns:
            Context dictionary
        """
        context = {
            "sources_used": [],
            "task_description": task_description,
            "project_name": "web2md",  # Could be detected
            "tech_stack": "TypeScript, Python, Bun"  # Could be detected
        }

        # Semantic search (Advanced RAG)
        if task_type in [TaskType.IMPLEMENTATION, TaskType.REFACTORING, TaskType.DEBUGGING]:
            semantic_results = self.rag_client.semantic_search(
                task_description,
                top_k=5
            )
            context["semantic_results"] = self._format_semantic_results(semantic_results)
            context["sources_used"].append("semantic_search")

        # Code graph analysis
        if task_type in [TaskType.IMPLEMENTATION, TaskType.REFACTORING]:
            # Try to find relevant files
            relevant_files = self._extract_files_from_context(task_description)
            if relevant_files:
                context["dependencies"] = self._analyze_dependencies(relevant_files)
                context["sources_used"].append("code_graph")

        # Documentation (web2md)
        if task_type == TaskType.RESEARCH:
            docs = self._find_relevant_docs(task_description)
            context["docs"] = docs
            context["sources_used"].append("web2md")

        return context

    def _generate_prompt_from_template(
        self,
        task_type: TaskType,
        context: Dict[str, Any]
    ) -> str:
        """
        Generate prompt from template

        Args:
            task_type: Type of task
            context: Context dictionary

        Returns:
            Generated prompt
        """
        try:
            template = self.template_engine.get_template(task_type.value)
            if not template:
                # Fallback to generic template
                return self._generate_generic_prompt(context)

            rendered = self.template_engine.render_template(
                task_type.value,
                context
            )
            return rendered

        except Exception as e:
            # Fallback to generic prompt on error
            return self._generate_generic_prompt(context)

    def _generate_generic_prompt(self, context: Dict[str, Any]) -> str:
        """Generate a generic prompt as fallback"""
        task_desc = context.get("task_description", "Complete the task")

        prompt = f"""# Task: {task_desc}

## Context
{self._format_context(context)}

## Instructions
Please complete this task following best practices:
1. Understand the requirements thoroughly
2. Use the provided context effectively
3. Implement a clean, maintainable solution
4. Include appropriate error handling
5. Add tests if applicable

## Deliverables
1. Implementation
2. Tests (if applicable)
3. Documentation

Please proceed with the task."""

        return prompt

    def _optimize_prompt(
        self,
        prompt: str,
        classification,
        constraints: Optional[Dict[str, Any]]
    ) -> str:
        """
        Optimize prompt for constraints

        Args:
            prompt: Original prompt
            classification: Task classification
            constraints: Optional constraints

        Returns:
            Optimized prompt
        """
        # Token optimization would happen here
        # For now, just return the prompt as-is

        # Could add:
        # - Progressive context loading
        # - Token limit enforcement
        # - Model-specific optimizations

        return prompt

    def _validate_prompt(
        self,
        prompt: str,
        classification
    ) -> float:
        """
        Validate prompt quality

        Args:
            prompt: Prompt to validate
            classification: Task classification

        Returns:
            Quality score (0.0 to 1.0)
        """
        score = 0.0

        # Check for essential elements
        if "# Task:" in prompt or "## Task" in prompt:
            score += 0.2

        if "## Context" in prompt or "## Instructions" in prompt:
            score += 0.2

        if "## Deliverables" in prompt or "## Requirements" in prompt:
            score += 0.2

        # Check prompt length
        prompt_length = len(prompt)
        if 100 <= prompt_length <= 5000:
            score += 0.2
        elif prompt_length > 5000:
            score += 0.1  # Too long but still valid

        # Check for specificity
        if any(keyword in prompt.lower() for keyword in ["implement", "create", "build", "fix", "refactor"]):
            score += 0.2

        return min(score, 1.0)

    def _format_semantic_results(self, results: List[Dict[str, Any]]) -> str:
        """Format semantic search results"""
        if not results:
            return "No relevant code found."

        formatted = []
        for i, result in enumerate(results[:5], 1):
            content = result.get("content", "")
            metadata = result.get("metadata", {})
            file = metadata.get("file", "unknown")
            score = result.get("score", 0.0)

            formatted.append(f"### {i}. {file} (relevance: {score:.2f})")
            formatted.append(f"```\n{content}\n```")

        return "\n\n".join(formatted)

    def _extract_files_from_context(self, task_description: str) -> List[str]:
        """Extract file paths from task description"""
        import re

        # Look for file patterns
        file_patterns = re.findall(r'[\w-]+\.(py|ts|js|tsx|jsx|go|rs|java)', task_description)
        return file_patterns

    def _analyze_dependencies(self, files: List[str]) -> str:
        """Analyze dependencies for given files"""
        dependencies = []

        for file in files:
            try:
                deps = self.code_graph.dependency_graph(format="json")
                dependencies.append(f"Dependencies for {file}: {len(deps.get('nodes', []))} nodes")
            except Exception:
                pass

        return "\n".join(dependencies) if dependencies else "No dependency analysis available."

    def _find_relevant_docs(self, task_description: str) -> str:
        """Find relevant documentation"""
        # This would search for and extract relevant docs
        return "No external documentation available."

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary"""
        formatted = []

        for key, value in context.items():
            if key == "sources_used":
                continue
            if value and key != "task_description":
                formatted.append(f"### {key.replace('_', ' ').title()}")
                formatted.append(str(value))

        return "\n\n".join(formatted) if formatted else "No additional context available."
