#!/usr/bin/env python3
"""
Auto Prompt CLI - Interface de linha de comando para testes
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for development
parent_dir = Path(__file__).parent.parent
if parent_dir.name == "web2md":
    sys.path.insert(0, str(parent_dir))

try:
    from auto_prompt.core import AutoPromptGenerator, TaskClassifier
    from auto_prompt.utils.validators import PromptValidator
except ImportError:
    # Fallback for development
    import importlib.util

    core_dir = Path(__file__).parent / "core"
    utils_dir = Path(__file__).parent / "utils"

    spec = importlib.util.spec_from_file_location("classifier", core_dir / "classifier.py")
    classifier_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(classifier_module)
    TaskClassifier = classifier_module.TaskClassifier


async def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [options]")
        print("\nCommands:")
        print("  generate <task>     Generate optimized prompt")
        print("  analyze <task>      Analyze task and classify")
        print("  validate <file>     Validate prompt quality")
        sys.exit(1)

    command = sys.argv[1]

    if command == "generate":
        await generate_command()
    elif command == "analyze":
        analyze_command()
    elif command == "validate":
        validate_command()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


async def generate_command():
    """Generate prompt for task"""
    if len(sys.argv) < 3:
        print("Usage: python cli.py generate <task> [--complexity low|medium|high] [--output file]")
        sys.exit(1)

    task = " ".join(sys.argv[2:])
    complexity = None
    output = None

    # Parse options
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == "--complexity" and i + 1 < len(sys.argv):
            complexity = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    # Generate prompt
    generator = AutoPromptGenerator()

    constraints = {}
    if complexity:
        constraints["complexity"] = complexity

    result = await generator.generate_prompt(task, constraints if constraints else None)

    # Output result
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.prompt)
        print(f"✅ Prompt saved to {output}")
    else:
        print("\n" + "="*60)
        print(result.prompt)
        print("="*60 + "\n")

    print(f"📊 Quality Score: {result.quality_score:.2f}")
    print(f"🔧 Model: {result.metadata['model']}")
    print(f"📏 Estimated Tokens: {result.token_estimate}")
    print(f"📋 Task Type: {result.metadata['task_type']}")
    print(f"📊 Complexity: {result.metadata['complexity']}")
    print(f"🎯 Strategy: {result.metadata['strategy']}")
    print(f"📚 Context Sources: {', '.join(result.context_sources_used)}")


def analyze_command():
    """Analyze task and classify"""
    if len(sys.argv) < 3:
        print("Usage: python cli.py analyze <task>")
        sys.exit(1)

    task = " ".join(sys.argv[2:])

    classifier = TaskClassifier()
    classification = classifier.classify(task)

    print(f"📋 Task Type: {classification.task_type.value}")
    print(f"📊 Complexity: {classification.complexity.value}")
    print(f"🎯 Expertise: {', '.join([exp.value for exp in classification.expertise])}")
    print(f"📈 Confidence: {classification.confidence:.2f}")
    print(f"🚀 Suggested Strategy: {classification.suggested_strategy}")
    print(f"🤖 Suggested Model: {classification.suggested_model}")
    print(f"📏 Estimated Tokens: {classification.estimated_tokens}")


def validate_command():
    """Validate prompt quality"""
    if len(sys.argv) < 3:
        print("Usage: python cli.py validate <file> [--threshold 0.8]")
        sys.exit(1)

    prompt_file = sys.argv[2]
    threshold = 0.8

    # Parse threshold
    if "--threshold" in sys.argv and len(sys.argv) > sys.argv.index("--threshold") + 1:
        threshold = float(sys.argv[sys.argv.index("--threshold") + 1])

    # Read prompt
    try:
        prompt = Path(prompt_file).read_text()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    # Validate
    validator = PromptValidator(min_quality_score=threshold)
    result = validator.validate(prompt)

    valid = result["valid"]
    score = result["score"]

    if valid:
        print(f"✅ Valid - Quality Score: {score:.2f}")
    else:
        print(f"❌ Invalid - Quality Score: {score:.2f} (threshold: {threshold:.2f})")

    if result["issues"]:
        print("\n⚠️  Issues:")
        for issue in result["issues"]:
            print(f"  - {issue}")

    if result["suggestions"]:
        print("\n💡 Suggestions:")
        for suggestion in result["suggestions"]:
            print(f"  - {suggestion}")

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    asyncio.run(main())
