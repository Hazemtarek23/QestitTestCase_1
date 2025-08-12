from typing import Dict, List, Set, Any

# ----------------------------
# Step 1: Variables Definition
# ----------------------------

VARIABLES: Dict[str, Dict[str, Any]] = {
    "userInput": {
        "display_name": "User Story",
        "category": "input-vars",
        "type": "user_input"
    }
}

# Add documentation chunks
for i in range(1, 7):
    VARIABLES[f"full_documentation_chunk_{i}"] = {
        "display_name": f"Full Documentation Chunk {i}",
        "category": "file-contexts",
        "type": "text_file",
        "path": None,
        "file_type": "md"
    }
    VARIABLES[f"tech_analysis_chunk_{i}"] = {
        "display_name": f"Technical Analysis of Chunk {i}",
        "category": "prompt-results",
        "type": "prompt_output"
    }

# ----------------------------
# Step 2: Prompt Template
# ----------------------------

TECHNICAL_ANALYSIS_SYSTEM_PROMPT = """You are a technical documentation analysis assistant. Your task is to provide a comprehensive overview of ALL relevant technical information from this documentation chunk.

Use this markdown structure for your analysis:

## Summary
A summary of all technical information found in the chunk.

## Overview
Technical overview of the system described in the chunk.

## Document Content Overview
| Section Title | Content Summary | Extraction Depth | System Relevancy |
|---------------|-----------------|------------------|------------------|
| Title 1 | Summary of content | High/Medium/Low | High/Medium/Low |
| Title 2 | Summary of content | High/Medium/Low | High/Medium/Low |

## Important Attributes and Data
| Attribute/Field Name | Description | Data Type | Validation Rules | Required | Technical Notes |
|----------------------|-------------|-----------|------------------|----------|----------------|
| Field 1 | Description | String/Number/etc | Rules | Yes/No | Notes |

## Business Process Tables
| Process Name | Process Description | Process Steps | Input Requirements | Output Results | Technical Implementation Details |
|--------------|---------------------|---------------|-------------------|---------------|----------------------------------|
| Process 1 | Description | Steps | Inputs | Outputs | Implementation |

## System Requirements Tables
| Requirement ID | Requirement Description | Requirement Type | Priority | Implementation Status | Technical Constraints |
|----------------|-------------------------|------------------|----------|------------------------|------------------------|
| REQ-1 | Description | Functional/Non-functional | High/Medium/Low | Status | Constraints |

Use 'N/A' where information is missing. Only include sections relevant to the chunk. Format properly in markdown.
"""

# ----------------------------
# Step 3: Prompts Definition
# ----------------------------

PROMPTS: Dict[str, Dict[str, Any]] = {}

for i in range(1, 7):
    PROMPTS[f"tech_analysisChunk{i}Prompt"] = {
        "description": f"Analyzes documentation chunk {i} for technical details",
        "required_variables": ["userInput", f"full_documentation_chunk_{i}"],
        "systemPrompt": TECHNICAL_ANALYSIS_SYSTEM_PROMPT,
        "userPrompt": f"""Analyze the following documentation chunk for technical details:
{{full_documentation_chunk_{i}}}

Focus on extracting technical information that would be essential for understanding system behavior and creating test cases.""",
        "output": f"tech_analysis_chunk_{i}"
    }

PROMPT_KEYS: Set[str] = set(PROMPTS.keys())

# ----------------------------
# Step 4: Workflow Configuration
# ----------------------------

WORKFLOW_CONFIG: Dict[str, Any] = {
    "version": "0.7",
    "id": "1_Documentation_analysis",
    "description": "Analyze documentation to create technical understanding foundation for test cases",
    "defaultPrompt": """Analyze the following documentation chunk and extract all technically relevant information using 
    a structured markdown format. Focus on summarizing, categorizing, and detailing all available data, processes, 
    and system elements. Apply the appropriate sections only if relevant data is found. Use 'N/A' where data is missing. 
    Format output according to the specified markdown structure.""",
    "name_field": "feature_title",
    "variables": VARIABLES,
    "steps": []
}

# Add 6 prompt steps dynamically
for i in range(1, 7):
    WORKFLOW_CONFIG["steps"].append({
        "step_id": f"analyze_documentation_chunk_{i}_tech",
        "type": "prompt",
        "prompt": f"tech_analysisChunk{i}Prompt",
        "output": f"tech_analysis_chunk_{i}",
        "description": f"Analyze documentation chunk {i} for technical details",
        "step_number": i
    })

# ----------------------------
# Step 5: Export All
# ----------------------------

__all__ = ["PROMPTS", "PROMPT_KEYS", "WORKFLOW_CONFIG", "VARIABLES"]
