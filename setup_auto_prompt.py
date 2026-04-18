#!/usr/bin/env python3
"""
Setup script for Auto Prompt system
"""

import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Now import
from auto_prompt.core import TaskClassifier, AutoPromptGenerator
import asyncio


def main():
    """Test the auto prompt system"""
    print("="*60)
    print("Auto Prompt System - Test")
    print("="*60)

    # Test 1: Classifier
    print("\n1. Testing Task Classifier")
    print("-"*60)

    classifier = TaskClassifier()
    result = classifier.classify("Implement user authentication with JWT tokens")

    print(f"Task Type: {result.task_type.value}")
    print(f"Complexity: {result.complexity.value}")
    print(f"Expertise: {[exp.value for exp in result.expertise]}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Strategy: {result.suggested_strategy}")
    print(f"Model: {result.suggested_model}")
    print(f"Estimated Tokens: {result.estimated_tokens}")

    # Test 2: Generator
    print("\n2. Testing Prompt Generator")
    print("-"*60)

    async def test_gen():
        generator = AutoPromptGenerator()
        result = await generator.generate_prompt(
            "Implement user authentication with JWT tokens"
        )

        print(f"Quality Score: {result.quality_score:.2f}")
        print(f"Model: {result.metadata['model']}")
        print(f"Task Type: {result.metadata['task_type']}")
        print(f"Complexity: {result.metadata['complexity']}")
        print(f"Token Estimate: {result.token_estimate}")
        print(f"\nGenerated Prompt Preview:")
        print("-"*60)
        print(result.prompt[:500] + "...")
        print("-"*60)

    asyncio.run(test_gen())

    print("\n" + "="*60)
    print("✅ Auto Prompt System is working!")
    print("="*60)


if __name__ == "__main__":
    main()
