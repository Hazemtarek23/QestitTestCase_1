from typing import List, Dict, Optional
from fastapi import HTTPException
import asyncio
import logging
from services.llama_client import LlamaClient
from services.ports import TextGenerator


class RiskAssessmentRequest:
    """Request model for risk assessment"""

    def __init__(self, user_story: str, analysis_text: str, documentation_chunks: Optional[List[str]] = None,
                 feature_title: Optional[str] = None, analysis_type: Optional[str] = "comprehensive"):
        self.user_story = user_story
        self.analysis_text = analysis_text
        self.documentation_chunks = documentation_chunks
        self.feature_title = feature_title
        self.analysis_type = analysis_type


class RiskDetail:
    def __init__(self, pattern: str, message: str, severity: str, category: str):
        self.pattern = pattern
        self.message = message
        self.severity = severity
        self.category = category


class RiskAssessmentMetadata:
    def __init__(self, issues: int, warnings: int, infos: int, criticals: int):
        self.issues = issues
        self.warnings = warnings
        self.infos = infos
        self.criticals = criticals


class RiskAssessmentResult:
    """Result model for risk assessment"""

    def __init__(self, risk_assessment: str, risk_level: str, risk_factors: List[Dict[str, str]],
                 mitigation_strategies: List[str], monitoring_recommendations: List[str],
                 risk_score: float = 0.0, total_risks: int = 0, risk_details: List[RiskDetail] = None,
                 risk_categories: List[str] = None, prompt_used: str = "",
                 metadata: RiskAssessmentMetadata = None, status: str = "success", error: Optional[str] = None):
        self.risk_assessment = risk_assessment
        self.risk_level = risk_level
        self.risk_factors = risk_factors
        self.mitigation_strategies = mitigation_strategies
        self.monitoring_recommendations = monitoring_recommendations
        self.risk_score = risk_score
        self.total_risks = total_risks
        self.risk_details = risk_details or []
        self.risk_categories = risk_categories or []
        self.prompt_used = prompt_used
        self.metadata = metadata or RiskAssessmentMetadata(0, 0, 0, 0)
        self.status = status
        self.error = error


class RiskAnalysisService:
    def __init__(self, generator: Optional[TextGenerator] = None):
        self.azure_client = generator or LlamaClient()
        self.logger = logging.getLogger(__name__)

        # System prompts for risk analysis using Linear Q™ methodology
        self.risk_analysis_system_prompt = """You are a risk analysis expert with deep domain knowledge in technical and business risk assessment using the Linear Q™ methodology. Your task is to identify, analyze, and provide mitigation strategies for risks in system implementations.

Use this structure for your analysis:

## Risk Assessment Summary
Overview of key risks and their potential impact

## Detailed Risk Analysis
| Risk Category | Risk Description | Likelihood | Impact | Current Controls | Risk Level |
|---------------|------------------|------------|--------|------------------|------------|
| Technical | Description | High/Medium/Low | High/Medium/Low | Existing controls | High/Medium/Low |
| Business | Description | High/Medium/Low | High/Medium/Low | Existing controls | High/Medium/Low |

## Risk Mitigation Strategies
1. Strategy for highest risk
2. Strategy for medium risk
3. Strategy for low risk

## Risk Monitoring Plan
- Key metrics to monitor
- Monitoring frequency
- Thresholds for action
- Escalation paths

## Contingency Planning
- Worst-case scenario plans
- Fallback options
- Recovery procedures"""

    async def analyze_risk(self, request: RiskAssessmentRequest) -> RiskAssessmentResult:
        """Comprehensive risk analysis method"""
        try:
            if request.analysis_type == "quick":
                return await self._quick_risk_analysis(request.user_story, request.analysis_text)
            elif request.analysis_type == "comprehensive":
                return await self._comprehensive_risk_analysis(
                    request.user_story,
                    request.analysis_text,
                    request.documentation_chunks,
                    request.feature_title
                )
            else:
                raise ValueError(f"Unknown analysis type: {request.analysis_type}")
        except Exception as e:
            self.logger.error(f"Risk analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")

    async def _quick_risk_analysis(self, user_story: str, analysis_text: str) -> RiskAssessmentResult:
        """Quick risk assessment for immediate needs"""
        prompt = f"""
        Perform quick risk assessment based on:

        User Story: {user_story}
        Analysis Text: {analysis_text}

        Provide:
        1. Top 3 risks with likelihood and impact
        2. Brief mitigation strategies
        3. Overall risk level (high/medium/low)
        """

        response = await self.azure_client.generate_text(
            system_prompt=self.risk_analysis_system_prompt,
            user_prompt=prompt
        )

        return self._parse_risk_response(response)

    async def _comprehensive_risk_analysis(self, user_story: str, analysis_text: str,
                                           documentation_chunks: Optional[List[str]],
                                           feature_title: str) -> RiskAssessmentResult:
        """Detailed risk analysis with documentation review"""
        # Analyze documentation chunks if provided
        chunk_analyses = []
        if documentation_chunks:
            chunk_analyses = await self._analyze_risk_in_documentation(user_story, documentation_chunks)

        prompt = f"""
        Perform comprehensive risk assessment for: {feature_title}

        User Story: {user_story}
        Primary Analysis: {analysis_text}
        Documentation Insights: {chunk_analyses if chunk_analyses else "No additional documentation provided"}

        Provide detailed risk assessment including:
        1. Categorized risks (technical, business, operational)
        2. Likelihood and impact assessment
        3. Mitigation strategies for each major risk
        4. Monitoring plan
        5. Contingency planning
        6. Overall risk level assessment
        """

        response = await self.azure_client.generate_text(
            system_prompt=self.risk_analysis_system_prompt,
            user_prompt=prompt
        )

        return self._parse_risk_response(response)

    async def _analyze_risk_in_documentation(self, user_story: str, documentation_chunks: List[str]) -> List[str]:
        """Analyze documentation for risk-related information"""
        tasks = []
        for chunk in documentation_chunks:
            task = self._analyze_single_chunk_for_risk(user_story, chunk)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [result for result in results if not isinstance(result, Exception)]

    async def _analyze_single_chunk_for_risk(self, user_story: str, chunk: str) -> str:
        """Analyze a single documentation chunk for risks"""
        prompt = f"""
        Analyze this documentation chunk for potential risks relevant to the user story:

        User Story: {user_story}
        Documentation Chunk: {chunk}

        Identify:
        1. Any explicit risk mentions
        2. Potential implicit risks
        3. Risk factors in requirements
        4. Technical constraints that could lead to risk
        """

        response = await self.azure_client.generate_text(
            system_prompt="You are a risk analysis assistant. Identify potential risks in technical documentation.",
            user_prompt=prompt
        )

        return response

    def _parse_risk_response(self, content: str) -> RiskAssessmentResult:
        """Parse the risk analysis response into structured data"""
        # Simplified parsing - in production you'd want more robust parsing
        lines = content.split('\n')

        # Extract overall risk level
        risk_level = "medium"
        for line in lines:
            if "overall risk level" in line.lower():
                if "high" in line.lower():
                    risk_level = "high"
                elif "low" in line.lower():
                    risk_level = "low"
                break

        # Extract risk factors (simplified)
        risk_factors = []
        in_risk_table = False
        for line in lines:
            if "risk category" in line.lower() and "|" in line:
                in_risk_table = True
                continue
            elif "|" in line and in_risk_table:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 6:
                    risk_factors.append({
                        "category": parts[0],
                        "description": parts[1],
                        "likelihood": parts[2],
                        "impact": parts[3],
                        "current_controls": parts[4],
                        "level": parts[5]
                    })
            elif line.startswith('#') and in_risk_table:
                in_risk_table = False

        # Extract mitigation strategies
        mitigations = []
        in_mitigation = False
        for line in lines:
            if "mitigation" in line.lower() and line.startswith('#'):
                in_mitigation = True
                continue
            elif line.startswith('#') and in_mitigation:
                in_mitigation = False
            elif in_mitigation and line.strip():
                if line.startswith('-') or line.startswith('*') or line[0].isdigit():
                    mitigations.append(line.strip().lstrip('-*1234567890. '))

        # Extract monitoring recommendations
        monitoring = []
        in_monitoring = False
        for line in lines:
            if "monitoring" in line.lower() and line.startswith('#'):
                in_monitoring = True
                continue
            elif line.startswith('#') and in_monitoring:
                in_monitoring = False
            elif in_monitoring and line.strip():
                if line.startswith('-') or line.startswith('*'):
                    monitoring.append(line.strip().lstrip('-* '))

        return RiskAssessmentResult(
            risk_assessment=content,
            risk_level=risk_level,
            risk_factors=risk_factors,
            mitigation_strategies=mitigations,
            monitoring_recommendations=monitoring
        )


class RiskAssessmentRouter:
    def __init__(self, generator: Optional[TextGenerator] = None):
        self.service = RiskAnalysisService(generator)
        self.logger = logging.getLogger(__name__)
