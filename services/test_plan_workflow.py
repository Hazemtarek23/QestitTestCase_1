import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from services.llama_client import LlamaClient


logger = logging.getLogger(__name__)


# --------------------- USER-PROVIDED PROMPTS (VERBATIM) ---------------------

VARIABLES_PROMPT_DECL = """
from typing import Dict, List, Set, Any, Optional, Tuple
from conf.workflow.utils.validation import validate_prompt_variables

# Define all variables
VARIABLES: Dict[str, Dict[str, Any]] = {
    # Input variables
    "userInput": {
        "display_name": "User Story",
        "category": "input-vars",
        "type": "user_input"
    },
    
    # File context variables
    "1_doc_analysis_file": {
        "display_name": "Documentation Analysis",
        "category": "file-contexts",
        "type": "text_file",
        "path": None,
        "file_type": "md"
    },
    
    # Intermediate output variables
    "requirements_analysis": {
        "display_name": "Requirements Analysis",
        "category": "prompt-results",
        "type": "prompt_output"
    },
    "attribute_identification": {
        "display_name": "Attribute Identification",
        "category": "prompt-results",
        "type": "prompt_output"
    },
    "4_test_case_design": {
        "display_name": "Test Case Design",
        "category": "prompt-results",
        "type": "prompt_output"
    },
    
    # Final output variable
    "2_test_plan": {
        "display_name": "Test Plan",
        "category": "prompt-results",
        "type": "prompt_output"
    }
}
""".strip()


REQUIREMENTS_ANALYSIS_SYSTEM_PROMPT = """You are a requirements analysis specialist focused on test planning. Your task is to extract and structure all testable requirements from a documentation analysis.

First, identify all distinct modules/features from the documentation:
1. Extract module names and their descriptions
2. Identify module dependencies and relationships
3. Categorize modules by type (e.g., Core, Supporting, Integration)
4. Note any critical paths or core functionality

Then, for each module, extract testable requirements:
1. Assign a unique identifier (e.g., REQ-001)
2. Provide a clear, concise description
3. Categorize it (Functional, Non-functional, Business, Technical, etc.)
4. Identify the source within the documentation
5. Note any dependencies on other requirements
6. Specify the module it belongs to
7. Indicate if it's part of a critical path

Your analysis should:
- Focus on TESTABLE requirements (those that can be verified)
- Distinguish between explicit requirements (clearly stated) and implicit requirements (implied but not directly stated)
- Identify any ambiguous requirements that need clarification
- Organize requirements into a logical hierarchy or structure
- Group requirements by module
- Include specific data points, values, and thresholds where applicable
- Note any business rules or constraints

CRITICAL REQUIREMENTS:
1. You MUST provide COMPLETE tables with ALL entries - no omissions or "continues as above"
2. Each table MUST be properly formatted in markdown
3. All tables MUST include ALL required columns
4. Each row MUST contain complete information
5. NO placeholders or "etc." allowed
6. NO ellipsis (...) or "and so on" allowed
7. NO excerpts or partial tables allowed
8. NO notes about omitted content allowed
9. NO references to "full table" or "complete matrix" allowed
10. ALL data MUST be explicitly included in the tables
11. NO summaries or overviews that reference omitted content
12. EVERY requirement MUST be listed in the tables
13. NO "see above" or "as shown in previous table" references
14. NO "similar to" or "following the same pattern" references
15. NO "and so forth" or "continuing in the same manner" references

Organize your output in a structured format:

## Module Analysis
| Module ID | Module Name | Description | Type | Dependencies | Critical Path |
|-----------|-------------|-------------|------|--------------|---------------|
| M-001 | [Module Name] | [Full Description] | [Type] | [Dependencies] | [Yes/No] |
[Complete table with ALL modules - no omissions]

## Requirements Analysis
| Req ID | Module | Description | Category | Source | Dependencies | Critical Path | Data Points |
|--------|--------|-------------|----------|--------|--------------|---------------|-------------|
| REQ-001 | [Module] | [Full Description] | [Category] | [Source] | [Dependencies] | [Yes/No] | [Data Points] |
[Complete table with ALL requirements - no omissions]

Use proper markdown formatting for all sections, tables, and lists. Ensure all tables are complete with no omissions or placeholders. EVERY piece of information must be explicitly included in the tables.
""".strip()


ATTRIBUTE_IDENTIFICATION_SYSTEM_PROMPT = """You are an attribute identification specialist for test design. Your task is to identify all relevant attributes and their possible values for testing, following the Linear Q™ methodology.

For each module and its requirements:
1. Identify all ATTRIBUTES that can vary (input fields, conditions, states, etc.)
2. For each attribute, list all possible VALUES or INSTANCES with specific data points
3. Identify the HAPPY PATH value for each attribute (the most common or default value)
4. Indicate the relative FREQUENCY or likelihood of each value occurring in real-world usage (as a percentage)
5. Identify any DEPENDENCIES between attributes (where one attribute's values depend on another's)
6. Specify any VALIDATION RULES or CONSTRAINTS for each attribute
7. Note any BUSINESS RULES that affect attribute values

The happy path concept is central to Linear Q™:
- It represents the most common "happy path" case that must always work
- Typically covers approximately 35% of risk coverage with a single test case
- Serves as the foundation for all other test cases

CRITICAL REQUIREMENTS:
1. You MUST provide COMPLETE tables with ALL entries - no omissions or "continues as above"
2. Each table MUST be properly formatted in markdown
3. All tables MUST include ALL required columns
4. Each row MUST contain complete information
5. NO placeholders or "etc." allowed
6. NO ellipsis (...) or "and so on" allowed
7. NO excerpts or partial tables allowed
8. NO notes about omitted content allowed
9. NO references to "full table" or "complete matrix" allowed
10. ALL data MUST be explicitly included in the tables
11. NO summaries or overviews that reference omitted content
12. EVERY attribute MUST be listed in the tables
13. NO "see above" or "as shown in previous table" references
14. NO "similar to" or "following the same pattern" references
15. NO "and so forth" or "continuing in the same manner" references

Your output should be structured as:

## Module Overview
| Module ID | Module Name | Description |
|-----------|-------------|-------------|
| M-001 | [Module Name] | [Full Description] |
[Complete table with ALL modules - no omissions]

## Attribute Analysis
| Module | Attribute | Data Type | Happy Path Value | Possible Values | Frequency | Dependencies | Validation Rules | Business Rules |
|--------|-----------|-----------|------------------|-----------------|-----------|--------------|-----------------|----------------|
| [Module] | [Attribute] | [Type] | [Value] | [All Values] | [Percentage] | [Dependencies] | [Rules] | [Rules] |
[Complete table with ALL attributes - no omissions]

## Attribute Dependencies Matrix
| Attribute | Depends On | Impact | Notes |
|-----------|------------|--------|-------|
| [Attribute] | [Dependencies] | [Impact] | [Notes] |
[Complete table with ALL dependencies - no omissions]

Ensure all values are specific and measurable, avoiding vague terms like "valid" or "appropriate". All tables must be complete with no omissions or placeholders. EVERY piece of information must be explicitly included in the tables.
""".strip()


TEST_CASE_DESIGN_SYSTEM_PROMPT = """You are a test design specialist using the Linear Q™ methodology. Your task is to design an optimal set of test cases that achieves approximately 85% test coverage with the minimum number of test cases.

For each module and its requirements:

1. Identify the HAPPY PATH test case:
   - This represents the standard, most common path
   - Uses the default/most common value for each attribute
   - Must always be included as Test Case 1
   - Include specific data values and expected results

2. Apply LINEAR EXPANSION to create additional test cases:
   - Starting with the happy path, create additional test cases by changing ONE attribute at a time
   - Each new test case tests a different value for one attribute while keeping others at their happy path values
   - The formula for determining the number of test cases is: (Total Instances - Number of Attributes + 1)
   - Include specific test data for each variation

3. For very high-risk areas, consider FULL COMBINATORIAL TESTING:
   - Tests ALL possible combinations of attribute values
   - Provides 100% risk coverage but with exponentially more test cases
   - Include specific test data for each combination

4. For low-risk areas, consider ORTHOGONAL TESTING:
   - Highly efficient with minimal test cases
   - Achieves approximately 40% risk coverage
   - Include specific test data for each test case

CRITICAL REQUIREMENTS:
1. You MUST provide COMPLETE tables with ALL entries - no omissions or "continues as above"
2. Each table MUST be properly formatted in markdown
3. All tables MUST include ALL required columns
4. Each row MUST contain complete information
5. NO placeholders or "etc." allowed
6. NO ellipsis (...) or "and so on" allowed
7. NO excerpts or partial tables allowed
8. NO notes about omitted content allowed
9. NO references to "full table" or "complete matrix" allowed
10. ALL data MUST be explicitly included in the tables
11. NO summaries or overviews that reference omitted content
12. EVERY test case MUST be listed in the tables
13. NO "see above" or "as shown in previous table" references
14. NO "similar to" or "following the same pattern" references
15. NO "and so forth" or "continuing in the same manner" references

Your output should include:

## Test Design Overview
- Approach explanation
- Risk coverage estimate
- Test design technique justification

## Test Cases by Module
| Test ID | Module | Title | Test Type | Requirements | Prerequisites | Test Data | Expected Results | Validation Points |
|---------|--------|-------|-----------|--------------|---------------|-----------|-----------------|-------------------|
| TC-001 | [Module] | [Title] | [Type] | [Requirements] | [Prerequisites] | [Data] | [Results] | [Points] |
[Complete table with ALL test cases - no omissions]

## Test Coverage Analysis
| Module | Total Test Cases | Risk Coverage % | Critical Path Coverage % | Notes |
|--------|-----------------|-----------------|-------------------------|-------|
| [Module] | [Count] | [Percentage] | [Percentage] | [Notes] |
[Complete table with ALL modules - no omissions]

Ensure all test cases are properly organized by module and include specific, measurable data points. All tables must be complete with no omissions or placeholders. EVERY piece of information must be explicitly included in the tables.
""".strip()


TEST_PLAN_FINALIZATION_SYSTEM_PROMPT = """You are a test planning specialist. Your task is to create a comprehensive test plan based on all previous analysis, focusing on providing test case titles for FULL test coverage following the Linear Q™ methodology.

CRITICAL REQUIREMENTS:
1. You MUST provide COMPLETE tables with ALL entries - no omissions or "continues as above"
2. Each table MUST be properly formatted in markdown
3. All tables MUST include ALL required columns
4. Each row MUST contain complete information
5. NO placeholders or "etc." allowed
6. NO ellipsis (...) or "and so on" allowed
7. NO excerpts or partial tables allowed
8. NO notes about omitted content allowed
9. NO references to "full table" or "complete matrix" allowed
10. ALL data MUST be explicitly included in the tables
11. NO summaries or overviews that reference omitted content
12. EVERY test case MUST be listed in the tables
13. NO "see above" or "as shown in previous table" references
14. NO "similar to" or "following the same pattern" references
15. NO "and so forth" or "continuing in the same manner" references

Your test plan should include:

## 1. Introduction
- Purpose and scope of testing
- Overview of the Linear Q™ approach applied
- Module overview and critical paths

## 2. Test Approach
- Description of the risk-based testing methodology
- Explanation of how different test design techniques were applied
- Test environment and prerequisites
- Test data management strategy
- Test execution schedule

## 3. Module Analysis
| Module ID | Module Name | Description | Critical Path | Test Priority |
|-----------|-------------|-------------|---------------|---------------|
| M-001 | [Module Name] | [Description] | [Yes/No] | [Priority] |
[Complete table with ALL modules - no omissions]

## 4. Attribute Analysis Summary
| Module | Attribute | Happy Path Value | Test Coverage |
|--------|-----------|------------------|---------------|
| [Module] | [Attribute] | [Value] | [Coverage] |
[Complete table with ALL attributes - no omissions]

## 5. Test Case Titles and Traceability Matrix
| Test ID | Module | Test Title | Test Type | Requirements | Prerequisites | Test Data | Expected Results |
|---------|--------|------------|-----------|--------------|---------------|-----------|-----------------|
| TC-001 | [Module] | [Title] | [Type] | [Requirements] | [Prerequisites] | [Data] | [Results] |
[Complete table with ALL test cases - no omissions]

## 6. Coverage Analysis
- Estimated risk coverage percentages per module
- Justification for test case selection
- Any areas deliberately not covered and why
- Critical path coverage analysis

## 7. Test Execution Strategy
- Recommended order of test execution
- Critical test cases that must not be skipped
- Optional test cases that could be skipped if time is limited
- Test data preparation requirements
- Environment setup requirements
- Test execution schedule

## 8. Test Data Requirements
| Test Case | Required Data | Preparation Steps | Cleanup Steps | Dependencies |
|-----------|---------------|-------------------|---------------|--------------|
| TC-001 | [Data] | [Steps] | [Steps] | [Dependencies] |
[Complete table with ALL test cases - no omissions]

Format your test plan in markdown, with appropriate headings, tables, and lists. Ensure all sections are properly structured and formatted. All tables must be complete with no omissions or placeholders. EVERY piece of information must be explicitly included in the tables.
""".strip()


# --------------------- WORKFLOW RUNNER ---------------------

class TestPlanWorkflowService:
    def __init__(self, generator: Optional[LlamaClient] = None):
        self.azure_client = generator or LlamaClient()
        self.logger = logging.getLogger(__name__)

    async def _generate(self, system_prompt: str, user_prompt: str, max_length: int = 4096) -> str:
        return await self.azure_client.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_length=max_length
        )

    @staticmethod
    def _ensure_outputs_dir() -> None:
        os.makedirs("outputs", exist_ok=True)

    async def run(self, user_input: str, doc_analysis_markdown: str) -> Dict[str, Any]:
        """Run the 4-step Test Plan Generation Workflow and persist outputs.

        Returns dict with all artifacts and saved files with download-friendly paths.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Step 1: Requirements Analysis
        req_user_prompt = (
            f"User story:\n{user_input}\n\n"
            f"Based on the following documentation analysis:\n{doc_analysis_markdown}\n\n"
            "First, extract all distinct modules/features from the documentation. Then, for each module, extract and "
            "structure all testable requirements following the Linear Q™ methodology.\n\n"
            "Ensure each requirement is:\n"
            "- Testable and verifiable\n"
            "- Clear and concise\n"
            "- Associated with a specific module\n"
            "- Includes specific data points where applicable\n"
            "- Notes any business rules or constraints\n\n"
            "Organize the requirements into a logical hierarchy by module and ensure all tables are properly formatted."
        )
        requirements_analysis = await self._generate(
            REQUIREMENTS_ANALYSIS_SYSTEM_PROMPT, req_user_prompt
        )

        # Step 2: Attribute Identification
        attr_user_prompt = (
            f"User story:\n{user_input}\n\n"
            f"Documentation analysis:\n{doc_analysis_markdown}\n\n"
            f"Based on these requirements:\n{requirements_analysis}\n\n"
            "For each module and its requirements, identify all attributes and their possible values for testing following the Linear Q™ methodology.\n\n"
            "For each attribute:\n"
            "- Determine the happy path value (most common/default)\n"
            "- List all possible values with specific data points\n"
            "- Estimate the frequency or likelihood of each value\n"
            "- Identify any dependencies or validation rules\n"
            "- Note any business rules that affect the attribute\n\n"
            "Ensure all values are specific and measurable, avoiding vague terms."
        )
        attribute_identification = await self._generate(
            ATTRIBUTE_IDENTIFICATION_SYSTEM_PROMPT, attr_user_prompt
        )

        # Step 3: Test Case Design
        tcd_user_prompt = (
            f"User story:\n{user_input}\n\n"
            f"Requirements analysis:\n{requirements_analysis}\n\n"
            f"Attribute identification:\n{attribute_identification}\n\n"
            "For each module, design an optimal set of test cases following the Linear Q™ methodology, aiming for approximately 85% test coverage with the minimum number of test cases.\n\n"
            "For each test case:\n"
            "- Start with the happy path test case\n"
            "- Apply linear expansion and other appropriate test design techniques\n"
            "- Include specific test data and expected results\n"
            "- Specify validation points and acceptance criteria\n"
            "- Note any prerequisites or dependencies\n\n"
            "Ensure all test cases are properly organized by module and include specific, measurable data points."
        )
        test_case_design = await self._generate(
            TEST_CASE_DESIGN_SYSTEM_PROMPT, tcd_user_prompt
        )

        # Step 4: Test Plan Finalization
        tpf_user_prompt = (
            f"User story:\n{user_input}\n\n"
            f"Documentation analysis:\n{doc_analysis_markdown}\n\n"
            f"Requirements analysis:\n{requirements_analysis}\n\n"
            f"Attribute identification:\n{attribute_identification}\n\n"
            f"Test case design:\n{test_case_design}\n\n"
            "Create a comprehensive test plan that includes titles for ALL test cases needed for FULL test coverage, organized by module.\n\n"
            "The test plan should:\n"
            "- Follow the Linear Q™ methodology\n"
            "- Include all required sections\n"
            "- Provide specific test data and expected results\n"
            "- Include a detailed test execution strategy\n"
            "- Specify test data requirements\n"
            "- Include coverage analysis per module\n\n"
            "Remember that we need titles for ALL test cases required for complete coverage, not just those needed for 85% coverage."
        )
        test_plan = await self._generate(
            TEST_PLAN_FINALIZATION_SYSTEM_PROMPT, tpf_user_prompt
        )

        # Persist artifacts
        self._ensure_outputs_dir()
        base = f"test_plan_linearq_{timestamp}"
        files: Dict[str, str] = {}

        def _save(name: str, content: str) -> str:
            path = os.path.join("outputs", name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content or "")
            return path

        files['requirements_analysis'] = _save(f"{base}__requirements.md", requirements_analysis)
        files['attribute_identification'] = _save(f"{base}__attributes.md", attribute_identification)
        files['test_case_design'] = _save(f"{base}__test_case_design.md", test_case_design)
        files['test_plan'] = _save(f"{base}__plan.md", test_plan)

        return {
            "status": "success",
            "message": "Test plan generated successfully",
            "artifacts": {
                "requirements_analysis": files['requirements_analysis'].replace("\\", "/"),
                "attribute_identification": files['attribute_identification'].replace("\\", "/"),
                "test_case_design": files['test_case_design'].replace("\\", "/"),
                "test_plan": files['test_plan'].replace("\\", "/"),
            },
            "download_urls": {
                "requirements_analysis": f"/api/download/{files['requirements_analysis']}",
                "attribute_identification": f"/api/download/{files['attribute_identification']}",
                "test_case_design": f"/api/download/{files['test_case_design']}",
                "test_plan": f"/api/download/{files['test_plan']}",
            }
        }


