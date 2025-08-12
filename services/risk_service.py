from typing import List, Dict, Optional
from fastapi import HTTPException
from typing import Any
from pydantic import BaseModel
import asyncio


class RiskAssessmentRequest(BaseModel):
    """Request model for risk assessment"""
    user_story: str
    analysis_text: str
    documentation_chunks: Optional[List[str]] = None
    feature_title: Optional[str] = None
    analysis_type: Optional[str] = "comprehensive"  # comprehensive, quick, domain_specific


class RiskAssessmentResult(BaseModel):
    """Result model for risk assessment"""
    risk_analysis: str
    risk_level: str  # high, medium, low
    risk_factors: List[Dict[str, str]]
    mitigation_strategies: List[str]
    monitoring_recommendations: List[str]


class RiskAnalysisService:
    def __init__(self, client: Any, deployment_name: str):
        self.client = client
        self.deployment_name = deployment_name

        # System prompts for risk analysis
        self.risk_analysis_system_prompt = """You are a risk analysis expert with deep domain knowledge in technical and business risk assessment. Your task is to identify, analyze, and provide mitigation strategies for risks in system implementations.

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

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": self.risk_analysis_system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.1
        )

        content = response.choices[0].message.content
        return self._parse_risk_response(content)

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

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": self.risk_analysis_system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.1
        )

        content = response.choices[0].message.content
        return self._parse_risk_response(content)

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

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system",
                 "content": "You are a risk analysis assistant. Identify potential risks in technical documentation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1
        )

        return response.choices[0].message.content

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
            risk_analysis=content,
            risk_level=risk_level,
            risk_factors=risk_factors,
            mitigation_strategies=mitigations,
            monitoring_recommendations=monitoring
        )