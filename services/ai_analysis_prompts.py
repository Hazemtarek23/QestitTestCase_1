"""AI Analysis Prompts Service
Provides intelligent test case generation using the configured LLM"""

import logging
from typing import Dict, List, Any, Optional
from services.llama_client import LlamaClient


class IntelligentTestCaseGenerator:
    """Intelligent test case generator using the configured LLM"""

    def __init__(self, model_name: str = "gpt-4.1"):
        self.model_name = model_name
        self.azure_client = LlamaClient(model_name)
        self.logger = logging.getLogger(__name__)

        # Banking domain-specific prompts
        self.BANKING_SYSTEM_PROMPT = """You are an expert banking test case analyst with deep knowledge of:
        - Core banking operations and workflows
        - Digital banking platforms and mobile applications
        - Risk management and compliance requirements
        - Payment processing and settlement systems
        - Customer onboarding and KYC processes
        - Regulatory compliance and audit requirements
        - Integration testing with external systems

        Generate comprehensive, realistic test cases that cover all aspects of banking operations."""

        self.RISK_ANALYSIS_PROMPT = """Analyze the following banking system requirements for potential risks:

        Focus on:
        - Security vulnerabilities
        - Compliance gaps
        - Integration risks
        - Performance bottlenecks
        - Data integrity issues
        - Business continuity concerns"""

        self.EXPERT_REVIEW_PROMPT = """As a banking domain expert, review and enhance the following analysis:

        Provide insights on:
        - Industry best practices
        - Regulatory requirements
        - Technical implementation considerations
        - Risk mitigation strategies
        - Quality assurance recommendations"""

    async def generate_banking_test_cases(self, requirements: str, test_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate banking-specific test cases"""
        try:
            prompt = f"""
            Generate comprehensive banking test cases for the following requirements:

            {requirements}

            Test Type: {test_type}

            Include test cases for:
            1. Account management operations
            2. Transaction processing
            3. Customer authentication
            4. Compliance validation
            5. Integration scenarios
            6. Error handling
            7. Security testing
            8. Performance validation
            """

            result = await self.azure_client.generate_text(
                system_prompt=self.BANKING_SYSTEM_PROMPT,
                user_prompt=prompt
            )

            return {
                "success": True,
                "test_cases": result,
                "model_used": self.model_name
            }

        except Exception as e:
            self.logger.error(f"Error generating banking test cases: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "test_cases": ""
            }

    async def analyze_requirements_risk(self, requirements: str) -> Dict[str, Any]:
        """Analyze requirements for potential risks"""
        try:
            prompt = f"""
            {self.RISK_ANALYSIS_PROMPT}

            Requirements to analyze:
            {requirements}

            Provide a detailed risk assessment with:
            - Risk categories
            - Likelihood and impact
            - Mitigation strategies
            - Testing recommendations
            """

            result = await self.azure_client.generate_text(
                system_prompt="You are a banking risk analysis expert.",
                user_prompt=prompt
            )

            return {
                "success": True,
                "risk_analysis": result,
                "model_used": self.model_name
            }

        except Exception as e:
            self.logger.error(f"Error analyzing requirements risk: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "risk_analysis": ""
            }

    async def expert_review_analysis(self, analysis: str, risk_assessment: str) -> Dict[str, Any]:
        """Perform expert review of analysis and risk assessment"""
        try:
            prompt = f"""
            {self.EXPERT_REVIEW_PROMPT}

            Analysis to review:
            {analysis}

            Risk Assessment:
            {risk_assessment}

            Provide expert recommendations and enhancements.
            """

            result = await self.azure_client.generate_text(
                system_prompt="You are a senior banking systems expert with 20+ years of experience.",
                user_prompt=prompt
            )

            return {
                "success": True,
                "expert_review": result,
                "model_used": self.model_name
            }

        except Exception as e:
            self.logger.error(f"Error performing expert review: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "expert_review": ""
            }

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return self.azure_client.get_model_info()
