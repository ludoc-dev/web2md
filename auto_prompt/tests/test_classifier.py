"""
Tests for Task Classifier
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from auto_prompt.core.classifier import (
    TaskClassifier,
    TaskType,
    Complexity,
    Expertise
)


class TestTaskClassifier:
    """Test suite for TaskClassifier"""

    def setup_method(self):
        """Setup test fixtures"""
        self.classifier = TaskClassifier()

    def test_classify_implementation_task(self):
        """Test classification of implementation tasks"""
        task = "Implement user authentication with JWT tokens"
        result = self.classifier.classify(task)

        assert result.task_type == TaskType.IMPLEMENTATION
        assert result.complexity in [Complexity.MEDIUM, Complexity.HIGH]
        assert Expertise.BACKEND in result.expertise
        assert result.confidence > 0.5

    def test_classify_refactoring_task(self):
        """Test classification of refactoring tasks"""
        task = "Refactor the authentication module to improve maintainability"
        result = self.classifier.classify(task)

        assert result.task_type == TaskType.REFACTORING
        assert result.complexity == Complexity.MEDIUM
        assert result.confidence > 0.5

    def test_classify_debugging_task(self):
        """Test classification of debugging tasks"""
        task = "Debug the memory leak in the authentication service"
        result = self.classifier.classify(task)

        assert result.task_type == TaskType.DEBUGGING
        assert result.complexity in [Complexity.MEDIUM, Complexity.HIGH]
        assert result.confidence > 0.5

    def test_classify_research_task(self):
        """Test classification of research tasks"""
        task = "Research best practices for JWT authentication"
        result = self.classifier.classify(task)

        assert result.task_type == TaskType.RESEARCH
        assert result.confidence > 0.5

    def test_classify_low_complexity(self):
        """Test classification of low complexity tasks"""
        task = "Fix typo in authentication function"
        result = self.classifier.classify(task)

        assert result.complexity == Complexity.LOW

    def test_classify_high_complexity(self):
        """Test classification of high complexity tasks"""
        task = "Build a comprehensive distributed authentication system with microservices architecture"
        result = self.classifier.classify(task)

        assert result.complexity == Complexity.HIGH

    def test_classify_frontend_expertise(self):
        """Test classification of frontend expertise"""
        task = "Implement React component for user login form"
        result = self.classifier.classify(task)

        assert Expertise.FRONTEND in result.expertise

    def test_classify_backend_expertise(self):
        """Test classification of backend expertise"""
        task = "Implement REST API endpoint for user authentication"
        result = self.classifier.classify(task)

        assert Expertise.BACKEND in result.expertise

    def test_classify_fullstack_expertise(self):
        """Test classification of fullstack expertise"""
        task = "Build fullstack authentication system with frontend and backend"
        result = self.classifier.classify(task)

        assert Expertise.FULLSTACK in result.expertise

    def test_suggest_strategy_parallel(self):
        """Test strategy suggestion for parallel execution"""
        task = "Build a comprehensive authentication system with multiple components"
        result = self.classifier.classify(task)

        assert result.suggested_strategy in ["parallel", "hybrid"]

    def test_suggest_strategy_sequential(self):
        """Test strategy suggestion for sequential execution"""
        task = "Debug authentication issue"
        result = self.classifier.classify(task)

        assert result.suggested_strategy == "sequential"

    def test_estimate_tokens(self):
        """Test token estimation"""
        task_low = "Fix simple bug"
        result_low = self.classifier.classify(task_low)

        task_high = "Build comprehensive distributed system"
        result_high = self.classifier.classify(task_high)

        assert result_high.estimated_tokens > result_low.estimated_tokens

    def test_suggest_model(self):
        """Test model suggestion"""
        task_simple = "Fix typo"
        result_simple = self.classifier.classify(task_simple)

        task_complex = "Build complex distributed system"
        result_complex = self.classifier.classify(task_complex)

        assert result_simple.suggested_model in ["haiku", "sonnet"]
        assert result_complex.suggested_model == "sonnet"

    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        # Specific task should have higher confidence
        task_specific = "Implement user authentication with JWT tokens in Python"
        result_specific = self.classifier.classify(task_specific)

        # Vague task should have lower confidence
        task_vague = "Do something with auth"
        result_vague = self.classifier.classify(task_vague)

        assert result_specific.confidence >= result_vague.confidence


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
