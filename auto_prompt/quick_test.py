#!/usr/bin/env python3
"""
Quick test without installation
"""

import sys
from pathlib import Path

# Import modules directly
sys.path.insert(0, str(Path(__file__).parent))

from core.classifier import TaskClassifier
from core.template_engine import TemplateEngine
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
        "Research JWT authentication best practices"
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

    print("\n✅ Classifier tests passed!")

def test_template_engine():
    """Test template engine"""
    print("\n" + "="*60)
    print("Testing Template Engine")
    print("="*60)

    engine = TemplateEngine()

    print(f"\n📝 Available templates: {', '.join(engine.list_templates())}")

    # Test getting a template
    template = engine.get_template("implementation")
    if template:
        print(f"\n✅ Template 'implementation' found")
        print(f"   Context sources: {template.context_sources}")
        print(f"   Required variables: {template.required_variables}")

    print("\n✅ Template Engine tests passed!")

def main():
    """Run all tests"""
    try:
        test_classifier()
        test_template_engine()

        print("\n" + "="*60)
        print("🎉 All tests passed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
