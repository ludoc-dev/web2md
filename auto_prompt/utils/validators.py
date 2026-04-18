"""
Validators - Quality validation for prompts and results
"""

from typing import Dict, Any, List
import re


class PromptValidator:
    """Validates prompt quality"""

    def __init__(self, min_quality_score: float = 0.8):
        """
        Initialize validator

        Args:
            min_quality_score: Minimum quality score threshold
        """
        self.min_quality_score = min_quality_score

    def validate(self, prompt: str) -> Dict[str, Any]:
        """
        Validate prompt quality

        Args:
            prompt: Prompt to validate

        Returns:
            Validation result with score and issues
        """
        issues = []
        score = 0.0

        # Check 1: Has clear task description
        if self._has_task_description(prompt):
            score += 0.25
        else:
            issues.append("Missing clear task description")

        # Check 2: Has context or instructions
        if self._has_context_or_instructions(prompt):
            score += 0.25
        else:
            issues.append("Missing context or instructions")

        # Check 3: Has deliverables or requirements
        if self._has_deliverables(prompt):
            score += 0.25
        else:
            issues.append("Missing deliverables or requirements")

        # Check 4: Appropriate length
        if self._has_appropriate_length(prompt):
            score += 0.25
        else:
            issues.append("Prompt length inappropriate (too short or too long)")

        # Check 5: Well structured (bonus)
        if self._is_well_structured(prompt):
            score += 0.1

        return {
            "valid": score >= self.min_quality_score,
            "score": min(score, 1.0),
            "issues": issues,
            "suggestions": self._generate_suggestions(issues)
        }

    def _has_task_description(self, prompt: str) -> bool:
        """Check if prompt has clear task description"""
        patterns = [
            r"# Task:",
            r"## Task",
            r"Task:",
            r"Objective:",
            r"## Objective"
        ]
        return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)

    def _has_context_or_instructions(self, prompt: str) -> bool:
        """Check if prompt has context or instructions"""
        patterns = [
            r"## Context",
            r"## Instructions",
            r"## Overview",
            r"## Background",
            r"## Description"
        ]
        return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)

    def _has_deliverables(self, prompt: str) -> bool:
        """Check if prompt has deliverables or requirements"""
        patterns = [
            r"## Deliverables",
            r"## Requirements",
            r"## Output",
            r"## Expected Result",
            r"## Success Criteria"
        ]
        return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)

    def _has_appropriate_length(self, prompt: str) -> bool:
        """Check if prompt has appropriate length"""
        length = len(prompt)
        return 100 <= length <= 10000

    def _is_well_structured(self, prompt: str) -> bool:
        """Check if prompt is well structured"""
        # Has proper markdown headers
        header_count = len(re.findall(r"^#+\s", prompt, re.MULTILINE))
        return header_count >= 3

    def _generate_suggestions(self, issues: List[str]) -> List[str]:
        """Generate suggestions based on issues"""
        suggestions = []

        if "Missing clear task description" in issues:
            suggestions.append("Add a clear task description at the beginning (e.g., '# Task: ...')")

        if "Missing context or instructions" in issues:
            suggestions.append("Add context or instructions section (e.g., '## Context' or '## Instructions')")

        if "Missing deliverables or requirements" in issues:
            suggestions.append("Add deliverables or requirements section (e.g., '## Deliverables')")

        if "Prompt length inappropriate" in issues:
            suggestions.append("Adjust prompt length (should be 100-10000 characters)")

        return suggestions


class ResultValidator:
    """Validates subagent results"""

    def __init__(self, min_confidence: float = 0.7):
        """
        Initialize result validator

        Args:
            min_confidence: Minimum confidence threshold
        """
        self.min_confidence = min_confidence

    def validate(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate subagent result

        Args:
            result: Result from subagent

        Returns:
            Validation result
        """
        issues = []
        score = 0.0

        # Check 1: Has output
        if "output" in result and result["output"]:
            score += 0.3
        else:
            issues.append("Missing output")

        # Check 2: Has metadata
        if "metadata" in result and result["metadata"]:
            score += 0.2
        else:
            issues.append("Missing metadata")

        # Check 3: Output is not empty
        if result.get("output") and len(result.get("output", "")) > 0:
            score += 0.3
        else:
            issues.append("Output is empty")

        # Check 4: Has confidence score
        if "confidence" in result:
            score += 0.2
        else:
            issues.append("Missing confidence score")

        return {
            "valid": score >= self.min_confidence,
            "score": min(score, 1.0),
            "issues": issues
        }


class ContextValidator:
    """Validates context quality"""

    def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate context quality

        Args:
            context: Context dictionary

        Returns:
            Validation result
        """
        issues = []
        score = 0.0

        # Check 1: Has task description
        if "task_description" in context and context["task_description"]:
            score += 0.3
        else:
            issues.append("Missing task_description")

        # Check 2: Has sources
        if "sources_used" in context and context["sources_used"]:
            score += 0.3
        else:
            issues.append("No sources used")

        # Check 3: Has relevant context data
        relevant_keys = ["semantic_results", "dependencies", "docs", "code_context"]
        if any(key in context for key in relevant_keys):
            score += 0.4
        else:
            issues.append("No relevant context data")

        return {
            "valid": score >= 0.7,
            "score": min(score, 1.0),
            "issues": issues
        }
