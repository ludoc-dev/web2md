"""
Tests for Auto Prompt Generator
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from auto_prompt.core.generator import AutoPromptGenerator, GeneratedPrompt
from auto_prompt.core.classifier import TaskType


class TestAutoPromptGenerator:
    """Test suite for AutoPromptGenerator"""

    def setup_method(self):
        """Setup test fixtures"""
        self.generator = AutoPromptGenerator()

    @pytest.mark.asyncio
    async def test_generate_prompt_implementation(self):
        """Test prompt generation for implementation task"""
        task = "Implement user authentication with JWT"
        result = await self.generator.generate_prompt(task)

        assert isinstance(result, GeneratedPrompt)
        assert len(result.prompt) > 0
        assert result.quality_score >= 0.0
        assert result.metadata["task_type"] == "implementation"
        assert result.token_estimate > 0

    @pytest.mark.asyncio
    async def test_generate_prompt_with_complexity(self):
        """Test prompt generation with complexity constraint"""
        task = "Implement user authentication"
        result = await self.generator.generate_prompt(
            task,
            constraints={"complexity": "low"}
        )

        assert result.metadata["complexity"] == "low"

    @pytest.mark.asyncio
    async def test_generate_prompt_quality_score(self):
        """Test that generated prompts have acceptable quality"""
        task = "Implement user authentication with JWT tokens"
        result = await self.generator.generate_prompt(task)

        # Quality score should be reasonable
        assert result.quality_score >= 0.5

    @pytest.mark.asyncio
    async def test_generate_prompt_has_task_section(self):
        """Test that generated prompts have task section"""
        task = "Implement user authentication"
        result = await self.generator.generate_prompt(task)

        assert "# Task:" in result.prompt or "## Task" in result.prompt

    @pytest.mark.asyncio
    async def test_generate_prompt_has_context(self):
        """Test that generated prompts include context"""
        task = "Implement user authentication"
        result = await self.generator.generate_prompt(task)

        # Should have some context or instructions
        has_context = (
            "## Context" in result.prompt or
            "## Instructions" in result.prompt or
            "## Overview" in result.prompt
        )
        assert has_context

    @pytest.mark.asyncio
    async def test_generate_prompt_has_deliverables(self):
        """Test that generated prompts specify deliverables"""
        task = "Implement user authentication"
        result = await self.generator.generate_prompt(task)

        # Should have deliverables or requirements
        has_deliverables = (
            "## Deliverables" in result.prompt or
            "## Requirements" in result.prompt or
            "## Output" in result.prompt
        )
        assert has_deliverables

    @pytest.mark.asyncio
    async def test_generate_prompt_appropriate_length(self):
        """Test that generated prompts have appropriate length"""
        task = "Implement user authentication with JWT tokens"
        result = await self.generator.generate_prompt(task)

        # Prompt should be between 100 and 10000 characters
        assert 100 <= len(result.prompt) <= 10000

    @pytest.mark.asyncio
    async def test_generate_different_task_types(self):
        """Test prompt generation for different task types"""
        tasks = [
            ("Implement user authentication", "implementation"),
            ("Refactor auth module", "refactoring"),
            ("Debug authentication issue", "debugging"),
            ("Research auth best practices", "research"),
        ]

        for task_desc, expected_type in tasks:
            result = await self.generator.generate_prompt(task_desc)
            assert result.metadata["task_type"] == expected_type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
