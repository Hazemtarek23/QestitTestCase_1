from typing import Dict, List, Optional
from fastapi import HTTPException
import logging
from services.llama_client import LlamaClient
from services.ports import TextGenerator


class ExpertAnalysisRequest:
    """Request model for expert analysis"""

    def __init__(self, user_story: str, analysis_text: str, risk_assessment: str,
                 analysis_type: Optional[str] = "comprehensive", **kwargs):
        self.user_story = user_story
        self.analysis_text = analysis_text
        self.risk_assessment = risk_assessment
        self.analysis_type = analysis_type


class ExpertStepResult:
    def __init__(self, step_id: str, description: str, output_key: str, output_value: str):
        self.step_id = step_id
        self.description = description
        self.output_key = output_key
        self.output_value = output_value


class ExpertReviewResult:
    def __init__(self, run_id: str, user_input: str, chunk_data: Dict[str, str],
                 step_results: List[ExpertStepResult], expert_analysis: str = ""):
        self.run_id = run_id
        self.user_input = user_input
        self.chunk_data = chunk_data
        self.step_results = step_results
        self.expert_analysis = expert_analysis


class ExpertAnalysisService:
    def __init__(self, generator: Optional[TextGenerator] = None):
        self.azure_client = generator or LlamaClient()
        self.logger = logging.getLogger(__name__)

        # Domain analysis system prompt based on the expert workflow
        self.DOMAIN_ANALYSIS_SYSTEM_PROMPT = """You are a domain expert analysis assistant. Your task is to analyze this documentation chunk specifically for its relevance to the given user story.

Use this markdown structure for your analysis:

## Summary
Overview of domain-specific information found in this chunk that relates to the user story.

## Content Overview
| Section Title | Content Summary | Relevancy to User Story | Domain Context Notes |
|---------------|-----------------|-------------------------|----------------------|
| Title 1 | Summary of content | High/Medium/Low | Domain context |
| Title 2 | Summary of content | High/Medium/Low | Domain context |

*Relevancy to User Story: How important is this for implementing the user story*

## Domain-Specific Data
| Domain Term/Concept | Description | Business Context | Relationship to User Story | Domain-Specific Constraints |
|---------------------|-------------|------------------|----------------------------|------------------------------|
| Term 1 | Description | Context | Relationship | Constraints |
| Term 2 | Description | Context | Relationship | Constraints |

## Domain-Specific Abbreviations
| Abbreviation | Full Term | Domain Context | Relevance to User Story |
|--------------|-----------|---------------|-------------------------|
| ABB1 | Full term 1 | Context | Relevance |
| ABB2 | Full term 2 | Context | Relevance |

## Missing Information
| Missing Information Item | Why It's Needed | Potential Impact if Not Provided | Suggested Source |
|--------------------------|----------------|----------------------------------|------------------|
| Missing item 1 | Reason | Impact | Source |
| Missing item 2 | Reason | Impact | Source |

When information in a table cell is missing, use 'N/A' as value.
Create appropriate sections only for information found in the chunk.
Use proper markdown syntax for all tables and sections."""

    async def perform_expert_analysis(self, request: ExpertAnalysisRequest) -> ExpertReviewResult:
        """Perform comprehensive expert analysis combining document analysis and risk assessment"""
        try:
            # Create comprehensive expert analysis prompt
            expert_prompt = f"""
            As a domain expert, perform comprehensive analysis combining the following inputs:

            User Story: {request.user_story}

            Document Analysis: {request.analysis_text}

            Risk Assessment: {request.risk_assessment}

            Provide expert review that:
            1. Validates the document analysis findings
            2. Assesses the completeness of risk identification
            3. Identifies domain-specific considerations
            4. Provides expert recommendations
            5. Highlights critical success factors
            6. Suggests implementation approach
            """

            expert_analysis = await self.azure_client.generate_text(
                system_prompt=self.DOMAIN_ANALYSIS_SYSTEM_PROMPT,
                user_prompt=expert_prompt
            )

            # Create step results for workflow compatibility
            step_results = [
                ExpertStepResult(
                    step_id="domain_analysis_step_1",
                    description="Analyze documentation for domain-specific information",
                    output_key="domain_analysis_chunk_1",
                    output_value=expert_analysis[:500] + "..." if len(expert_analysis) > 500 else expert_analysis
                )
            ]

            return ExpertReviewResult(
                run_id=f"expert_analysis_{hash(request.user_story) % 10000}",
                user_input=request.user_story,
                chunk_data={"analysis": request.analysis_text, "risk": request.risk_assessment},
                step_results=step_results,
                expert_analysis=expert_analysis
            )

        except Exception as e:
            self.logger.error(f"Expert analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Expert analysis failed: {str(e)}")

    async def analyze_documentation_chunks(self, user_story: str, chunks: List[str]) -> Dict[str, str]:
        """Analyze multiple documentation chunks for domain expertise"""
        try:
            results = {}

            for i, chunk in enumerate(chunks, 1):
                chunk_key = f"domain_analysis_chunk_{i}"

                analysis_prompt = f"""
                Analyze the following documentation chunk for domain-specific information relevant to this user story:

                {chunk}

                User Story: {user_story}

                Focus on extracting domain-specific knowledge, abbreviations, and identifying information gaps that would be needed to fully address this user story.
                """

                analysis_result = await self.azure_client.generate_text(
                    system_prompt=self.DOMAIN_ANALYSIS_SYSTEM_PROMPT,
                    user_prompt=analysis_prompt
                )

                results[chunk_key] = analysis_result

            return results

        except Exception as e:
            self.logger.error(f"Documentation chunks analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Documentation chunks analysis failed: {str(e)}")


class ExpertAnalysisController:
    def __init__(self, generator: Optional[TextGenerator] = None):
        self.service = ExpertAnalysisService(generator)
        self.logger = logging.getLogger(__name__)
