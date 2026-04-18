#!/usr/bin/env python3
"""
Simple test script for Auto Prompt system
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_prompt.core import TaskClassifier, AutoPromptGenerator
import asyncio


def test_classifier():
    """Test task classifier"""
    print("="*60)
    print("Testing Task Classifier")
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
        print(f"\nTask: {task}")
        result = classifier.classify(task)
        print(f"  Type: {result.task_type.value}")
        print(f"  Complexity: {result.complexity.value}")
        print(f"  Expertise: {[exp.value for exp in result.expertise]}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Strategy: {result.suggested_strategy}")
        print(f"  Model: {result.suggested_model}")
        print(f"  Tokens: {result.estimated_tokens}")


async def test_generator():
    """Test prompt generator"""
    print("\n" + "="*60)
    print("Testing Prompt Generator")
    print("="*60)

    generator = AutoPromptGenerator()

    test_task = "Implement user authentication with JWT tokens"

    print(f"\nTask: {test_task}")

    result = await generator.generate_prompt(test_task)

    print(f"\nQuality Score: {result.quality_score:.2f}")
    print(f"Model: {result.metadata['model']}")
    print(f"Task Type: {result.metadata['task_type']}")
    print(f"Complexity: {result.metadata['complexity']}")
    print(f"Strategy: {result.metadata['strategy']}")
    print(f"Token Estimate: {result.token_estimate}")
    print(f"Context Sources: {', '.join(result.context_sources_used)}")

    print("\n" + "-"*60)
    print("Generated Prompt:")
    print("-"*60)
    print(result.prompt)
    print("-"*60)


def test_template_engine():
    """Test template engine"""
    print("\n" + "="*60)
    print("Testing Template Engine")
    print("="*60)

    from auto_prompt.core import TemplateEngine

    engine = TemplateEngine()

    print(f"\nAvailable templates: {', '.join(engine.list_templates())}")

    # Test rendering implementation template
    context = {
        "feature": "user authentication",
        "project_name": "web2md",
        "requirements": "JWT-based authentication with access and refresh tokens",
        "tech_stack": "TypeScript, Node.js",
        "files": "auth.ts, jwt.ts",
        "integration_points": "API routes, middleware",
        "semantic_results": "No relevant code found.",
        "dependencies": "No dependency analysis available.",
        "examples": "See auth.ts in similar projects"
    }

    try:
        rendered = engine.render_template("implementation", context)
        print(f"\n✅ Template rendered successfully")
        print(f"Length: {len(rendered)} characters")
        print(f"Preview (first 200 chars):\n{rendered[:200]}...")
    except Exception as e:
        print(f"\n❌ Error rendering template: {e}")


def main():
    """Run all tests"""
    try:
        # Test 1: Classifier
        test_classifier()

        # Test 2: Template Engine
        test_template_engine()

        # Test 3: Generator (async)
        asyncio.run(test_generator())

        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
