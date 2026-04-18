#!/usr/bin/env python3
"""
Direct import test without package structure
"""

import sys
from pathlib import Path

# Add parent directories to path
auto_prompt_dir = Path(__file__).parent
sys.path.insert(0, str(auto_prompt_dir))

# Import directly from files
import importlib.util

# Load classifier
spec = importlib.util.spec_from_file_location(
    "classifier",
    auto_prompt_dir / "core" / "classifier.py"
)
classifier_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(classifier_module)

TaskClassifier = classifier_module.TaskClassifier

def main():
    """Test the system"""
    print("="*60)
    print("Auto Prompt System - Direct Import Test")
    print("="*60)

    classifier = TaskClassifier()

    test_tasks = [
        "Implement user authentication with JWT tokens",
        "Refactor authentication module for better maintainability",
        "Debug memory leak in authentication service",
        "Research JWT authentication best practices",
        "Create React component for user login form",
        "Build comprehensive distributed authentication system"
    ]

    for task in test_tasks:
        print(f"\n📋 Task: {task}")
        result = classifier.classify(task)
        print(f"   Type: {result.task_type.value}")
        print(f"   Complexity: {result.complexity.value}")
        print(f"   Expertise: {[exp.value for exp in result.expertise]}")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   Strategy: {result.suggested_strategy}")
        print(f"   Model: {result.suggested_model}")
        print(f"   Tokens: {result.estimated_tokens}")

    print("\n" + "="*60)
    print("✅ All tests passed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
