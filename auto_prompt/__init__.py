"""
Auto Prompt Generation System

Sistema inteligente de geração de prompts para subagentic programming.
"""

__version__ = "0.1.0"
__author__ = "Auto Prompt System"

from .core import (
    TaskClassifier,
    TaskType,
    Complexity,
    Expertise,
    TemplateEngine,
    Template,
    AutoPromptGenerator,
    GeneratedPrompt,
)

from .utils import (
    MCPClient,
    AdvancedRAGClient,
    CodeGraphClient,
    Web2MDClient,
)

__all__ = [
    "TaskClassifier",
    "TaskType",
    "Complexity",
    "Expertise",
    "TemplateEngine",
    "Template",
    "AutoPromptGenerator",
    "GeneratedPrompt",
    "MCPClient",
    "AdvancedRAGClient",
    "CodeGraphClient",
    "Web2MDClient",
]
