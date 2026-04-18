"""
Template Engine - Manages prompt templates and renders them with context
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class Template:
    """Prompt template structure"""
    name: str
    task_type: str
    template: str
    context_sources: List[str]
    required_variables: List[str]
    metadata: Dict[str, Any]


class TemplateEngine:
    """Manages and renders prompt templates"""

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize template engine

        Args:
            template_dir: Directory containing template files
        """
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates"

        self.template_dir = Path(template_dir)
        self.prompts_file = self.template_dir / "prompts.json"
        self.agents_dir = self.template_dir / "agents"

        self.templates: Dict[str, Template] = {}
        self._load_templates()

    def _load_templates(self):
        """Load templates from prompts.json"""
        if not self.prompts_file.exists():
            # Create default templates
            self._create_default_templates()
            return

        with open(self.prompts_file, 'r') as f:
            templates_data = json.load(f)

        for task_type, config in templates_data.items():
            self.templates[task_type] = Template(
                name=task_type,
                task_type=task_type,
                template=config["template"],
                context_sources=config.get("context_sources", []),
                required_variables=config.get("required_variables", []),
                metadata=config.get("metadata", {})
            )

    def _create_default_templates(self):
        """Create default templates if prompts.json doesn't exist"""
        default_templates = {
            "implementation": {
                "template": """# Task: Implement {feature}

## Overview
Implement {feature} for {project_name}.

## Requirements
{requirements}

## Context

### Relevant Code
{semantic_results}

### Dependencies
{dependencies}

### Implementation Examples
{examples}

## Technical Specifications
- **Tech Stack:** {tech_stack}
- **Files to Modify:** {files}
- **Integration Points:** {integration_points}

## Quality Standards
- Follow existing code conventions
- Include error handling
- Add appropriate tests
- Document complex logic

## Deliverables
1. Implementation code
2. Unit tests
3. Integration notes
4. Documentation updates

Please implement this feature following best practices and maintaining consistency with the existing codebase.""",
                "context_sources": ["semantic_search", "code_graph", "dependencies"],
                "required_variables": ["feature", "project_name", "requirements"],
                "metadata": {
                    "complexity": "medium",
                    "estimated_tokens": 2500,
                    "suggested_model": "sonnet"
                }
            },
            "refactoring": {
                "template": """# Task: Refactor {target}

## Overview
Refactor {target} to {objective}.

## Current Implementation
```{language}
{current_code}
```

## Issues Identified
{issues}

## Refactoring Goals
{goals}

## Analysis

### Impact Analysis
{impact_analysis}

### Call Graph
{call_graph}

### Dependencies
{dependencies}

## Refactoring Approach
{approach}

## Testing Strategy
{testing_strategy}

Please refactor the code while:
- Preserving all existing functionality
- Improving code quality and maintainability
- Following best practices
- Ensuring all tests pass""",
                "context_sources": ["impact_analysis", "trace_calls", "current_code"],
                "required_variables": ["target", "objective"],
                "metadata": {
                    "complexity": "medium",
                    "estimated_tokens": 2000,
                    "suggested_model": "sonnet"
                }
            },
            "debugging": {
                "template": """# Task: Debug {issue}

## Problem Description
{problem_description}

## Error Details
```
{error}
```

## Stack Trace
```
{stack_trace}
```

## Context

### Relevant Code
```{language}
{code_context}
```

### Execution Flow
{execution_flow}

### Environment
{environment}

## Investigation Steps
1. Analyze the error and stack trace
2. Identify the root cause
3. Review related code and dependencies
4. Check for similar issues
5. Propose and implement fix

## Similar Issues
{similar_issues}

## Debugging Strategy
{debugging_strategy}

Please:
1. Identify the root cause
2. Explain the issue clearly
3. Propose a fix
4. Implement the solution
5. Add tests to prevent regression""",
                "context_sources": ["semantic_search", "code_context", "similar_issues"],
                "required_variables": ["issue", "error"],
                "metadata": {
                    "complexity": "medium",
                    "estimated_tokens": 2000,
                    "suggested_model": "sonnet"
                }
            },
            "research": {
                "template": """# Research Task: {topic}

## Research Objective
{objective}

## What We Know
{known_info}

## What to Find Out
{research_questions}

## Sources to Investigate
{sources}

## Research Strategy
1. Search codebase for relevant implementations
2. Review external documentation
3. Analyze similar patterns
4. Evaluate approaches
5. Document findings

## Deliverables
1. Summary of findings
2. Comparison of approaches
3. Code examples (if applicable)
4. Recommendations
5. Risks and considerations

## Research Context
{context}

Please conduct thorough research and provide comprehensive findings with actionable recommendations.""",
                "context_sources": ["web2md", "semantic_search", "online_search"],
                "required_variables": ["topic", "objective"],
                "metadata": {
                    "complexity": "medium",
                    "estimated_tokens": 3000,
                    "suggested_model": "sonnet"
                }
            }
        }

        # Save default templates
        self.prompts_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.prompts_file, 'w') as f:
            json.dump(default_templates, f, indent=2)

        # Load them
        self._load_templates()

    def get_template(self, task_type: str) -> Optional[Template]:
        """
        Get template by task type

        Args:
            task_type: Type of task (implementation, refactoring, etc.)

        Returns:
            Template if found, None otherwise
        """
        return self.templates.get(task_type)

    def render_template(
        self,
        task_type: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Render template with provided context

        Args:
            task_type: Type of task
            context: Context variables to inject

        Returns:
            Rendered prompt string
        """
        template = self.get_template(task_type)
        if not template:
            raise ValueError(f"No template found for task type: {task_type}")

        # Validate required variables
        missing_vars = [
            var for var in template.required_variables
            if var not in context
        ]
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")

        # Render template
        try:
            rendered = template.template.format(**context)
        except KeyError as e:
            raise ValueError(f"Missing context variable: {e}")

        return rendered

    def list_templates(self) -> List[str]:
        """List all available template types"""
        return list(self.templates.keys())

    def add_template(
        self,
        name: str,
        template: str,
        context_sources: List[str],
        required_variables: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add a new template

        Args:
            name: Template name
            template: Template string
            context_sources: List of context sources
            required_variables: List of required variable names
            metadata: Optional metadata
        """
        self.templates[name] = Template(
            name=name,
            task_type=name,
            template=template,
            context_sources=context_sources,
            required_variables=required_variables,
            metadata=metadata or {}
        )

        # Save to file
        self._save_templates()

    def _save_templates(self):
        """Save templates to prompts.json"""
        templates_data = {}
        for name, template in self.templates.items():
            templates_data[name] = {
                "template": template.template,
                "context_sources": template.context_sources,
                "required_variables": template.required_variables,
                "metadata": template.metadata
            }

        self.prompts_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.prompts_file, 'w') as f:
            json.dump(templates_data, f, indent=2)
