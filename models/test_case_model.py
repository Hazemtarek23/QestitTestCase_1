from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Any, Union, Optional
import json


class TestData(BaseModel):
    """Flexible test data model that handles both strings and arrays"""
    input: str = Field(default="", description="Test input data")
    expected: str = Field(default="", description="Expected output")

    @validator('input', pre=True)
    def convert_input_to_string(cls, v):
        """Convert input arrays to comma-separated strings"""
        if isinstance(v, list):
            return ', '.join([str(item) for item in v])
        return str(v) if v is not None else ""

    @validator('expected', pre=True)
    def convert_expected_to_string(cls, v):
        """Convert expected arrays to comma-separated strings"""
        if isinstance(v, list):
            return ', '.join([str(item) for item in v])
        return str(v) if v is not None else ""

    class Config:
        extra = "allow"  # Allow additional fields


class TestCase(BaseModel):
    """Enhanced TestCase model with flexible data handling"""
    test_id: str = Field(default="TC_001", description="Unique test case identifier")
    title: str = Field(default="Test Case", description="Test case title")
    description: str = Field(default="", description="Test case description")
    category: str = Field(default="Functional", description="Test category")
    priority: str = Field(default="Medium", description="Test priority")
    test_type: str = Field(default="Manual", description="Test type")
    steps: str = Field(default="", description="Test execution steps")
    test_data: TestData = Field(default_factory=TestData, description="Test input and expected data")
    expected_result: str = Field(default="", description="Expected test result")
    preconditions: str = Field(default="", description="Test preconditions")
    tags: List[str] = Field(default_factory=list, description="Test tags")

    @validator('steps', pre=True)
    def convert_steps_to_string(cls, v):
        """Convert steps array to numbered string"""
        if isinstance(v, list):
            return '\n'.join([f"{i + 1}. {step}" for i, step in enumerate(v)])
        return str(v) if v is not None else ""

    @validator('expected_result', pre=True)
    def convert_expected_result_to_string(cls, v):
        """Convert expected result array to string"""
        if isinstance(v, list):
            return ', '.join([str(item) for item in v])
        return str(v) if v is not None else ""

    @validator('preconditions', pre=True)
    def convert_preconditions_to_string(cls, v):
        """Convert preconditions array to bullet points"""
        if isinstance(v, list):
            return '\n'.join([f"- {item}" for item in v])
        return str(v) if v is not None else ""

    @validator('tags', pre=True)
    def ensure_tags_list(cls, v):
        """Ensure tags is always a list"""
        if isinstance(v, str):
            return [v] if v else []
        elif isinstance(v, list):
            return [str(item) for item in v]
        return []

    @validator('test_data', pre=True)
    def handle_test_data(cls, v):
        """Handle various test_data formats"""
        if isinstance(v, dict):
            return v
        elif isinstance(v, str):
            try:
                # Try to parse as JSON
                parsed = json.loads(v)
                return parsed if isinstance(parsed, dict) else {"input": str(v), "expected": ""}
            except:
                return {"input": str(v), "expected": ""}
        else:
            return {"input": str(v) if v else "", "expected": ""}

    @root_validator(pre=True)
    def handle_flexible_input(cls, values):
        """Handle various input formats and missing fields"""
        # Ensure all required fields have defaults
        defaults = {
            'test_id': 'TC_001',
            'title': 'Test Case',
            'description': '',
            'category': 'Functional',
            'priority': 'Medium',
            'test_type': 'Manual',
            'steps': '',
            'expected_result': '',
            'preconditions': '',
            'tags': []
        }

        for key, default_value in defaults.items():
            if key not in values or values[key] is None:
                values[key] = default_value

        # Handle test_data specially
        if 'test_data' not in values or values['test_data'] is None:
            values['test_data'] = {"input": "", "expected": ""}

        return values

    class Config:
        extra = "ignore"  # Ignore additional fields not in model
        validate_assignment = True


# Alternative: Simple field-by-field converter
class TestCaseConverter:
    """Utility class to convert AI responses to TestCase objects"""

    @staticmethod
    def from_dict(data: Dict[str, Any], case_id: Optional[str] = None) -> TestCase:
        """Convert dictionary to TestCase with robust error handling"""
        try:
            # Handle test_data conversion
            test_data = data.get('test_data', {})
            if isinstance(test_data, dict):
                # Convert arrays to strings in test_data
                for key in ['input', 'expected']:
                    if key in test_data and isinstance(test_data[key], list):
                        test_data[key] = ', '.join([str(item) for item in test_data[key]])

            # Prepare clean data
            clean_data = {
                'test_id': str(data.get('test_id', data.get('id', case_id or 'TC_001'))),
                'title': str(data.get('title', data.get('name', 'Test Case'))),
                'description': str(data.get('description', data.get('desc', ''))),
                'category': str(data.get('category', 'Functional')),
                'priority': str(data.get('priority', 'Medium')),
                'test_type': str(data.get('test_type', data.get('type', 'Manual'))),
                'test_data': test_data,
                'expected_result': str(data.get('expected_result', data.get('expected', ''))),
                'preconditions': str(data.get('preconditions', data.get('prerequisites', ''))),
                'tags': data.get('tags', [])
            }

            # Handle steps
            steps = data.get('steps', data.get('test_steps', []))
            if isinstance(steps, list):
                clean_data['steps'] = '\n'.join([f"{i + 1}. {step}" for i, step in enumerate(steps)])
            else:
                clean_data['steps'] = str(steps)

            return TestCase(**clean_data)

        except Exception as e:
            # Return a basic test case if conversion fails
            return TestCase(
                test_id=case_id or 'TC_FALLBACK',
                title='Fallback Test Case',
                description=f'Generated due to parsing error: {str(e)}',
                steps='1. Execute test\n2. Verify results',
                test_data=TestData(input='Sample input', expected='Expected result')
            )

    @staticmethod
    def from_ai_response(response: str, target_count: int = 65) -> List[TestCase]:
        """Convert AI JSON response to list of TestCase objects"""
        try:
            # Clean the response
            cleaned = TestCaseConverter._clean_json(response)
            data = json.loads(cleaned)

            # Extract test cases
            if isinstance(data, dict) and 'test_cases' in data:
                test_cases_data = data['test_cases']
            elif isinstance(data, list):
                test_cases_data = data
            else:
                test_cases_data = [data]

            # Convert each test case
            test_cases = []
            for i, case_data in enumerate(test_cases_data):
                case_id = f"TC_{i + 1:03d}"
                test_case = TestCaseConverter.from_dict(case_data, case_id)
                test_cases.append(test_case)

            return test_cases[:target_count]

        except Exception as e:
            # Return basic test cases if parsing fails
            return [
                TestCase(
                    test_id=f"TC_{i:03d}",
                    title=f"Basic Test Case {i}",
                    description=f"Generated basic test case {i}",
                    steps=f"1. Execute test scenario {i}\n2. Verify results",
                    test_data=TestData(input=f'Test input {i}', expected=f'Expected result {i}')
                ) for i in range(1, min(target_count, 10) + 1)
            ]

    @staticmethod
    def _clean_json(response: str) -> str:
        """Clean AI response to extract valid JSON"""
        import re
        # Remove markdown code blocks
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*$', '', response, flags=re.MULTILINE)

        # Find JSON boundaries
        start = min(
            response.find('{') if response.find('{') != -1 else len(response),
            response.find('[') if response.find('[') != -1 else len(response)
        )

        if start < len(response):
            response = response[start:]
            end = max(response.rfind('}'), response.rfind(']'))
            if end != -1:
                response = response[:end + 1]

        return response.strip()