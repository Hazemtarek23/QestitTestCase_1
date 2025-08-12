from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from typing import Any
from pydantic import BaseModel
import asyncio


class ExpertAnalysisRequest(BaseModel):
    """Request model for expert analysis"""
    user_story: str
    analysis_text: str
    risk_assessment: str
    documentation_chunks: Optional[List[str]] = None
    feature_title: Optional[str] = None
    analysis_type: Optional[str] = "comprehensive"  # comprehensive, quick, domain_specific


class ChunkAnalysisResult(BaseModel):
    """Result model for individual chunk analysis"""
    chunk_number: int
    summary: str
    content_overview: List[Dict[str, Any]]
    domain_specific_data: List[Dict[str, Any]]
    abbreviations: List[Dict[str, Any]]
    missing_information: List[Dict[str, Any]]


class ExpertAnalysisResponse(BaseModel):
    """Response model for expert analysis"""
    expert_analysis: str
    chunk_analyses: Optional[List[ChunkAnalysisResult]] = None
    consolidated_insights: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None
    action_plan: Optional[List[Dict[str, Any]]] = None


class ExpertAnalysisService:
    def __init__(self, client: Any, deployment_name: str):
        self.client = client
        self.deployment_name = deployment_name

        # Enhanced system prompt based on the workflow document
        self.domain_analysis_system_prompt = """You are a domain expert analysis assistant..."""  # Keep your existing prompt

        self.expert_synthesis_system_prompt = """You are a senior domain expert..."""  # Keep your existing prompt

    async def comprehensive_analysis(self, request: ExpertAnalysisRequest) -> ExpertAnalysisResponse:
        """Main method for comprehensive expert analysis"""
        try:
            if request.analysis_type == "quick":
                expert_analysis = await self._quick_analysis(
                    request.analysis_text,
                    request.risk_assessment,
                    request.user_story
                )
                return ExpertAnalysisResponse(expert_analysis=expert_analysis)

            elif request.analysis_type == "comprehensive":
                expert_analysis = await self._enhanced_analysis(
                    request.user_story,
                    request.analysis_text,
                    request.risk_assessment,
                    request.feature_title or "System Feature"
                )

                chunk_analyses = None
                consolidated_insights = None
                if request.documentation_chunks:
                    chunk_analyses = await self._analyze_documentation_chunks(
                        request.user_story,
                        request.documentation_chunks
                    )
                    consolidated_result = await self._consolidate_chunk_analyses(
                        request.user_story,
                        request.analysis_text,
                        request.risk_assessment,
                        chunk_analyses
                    )
                    consolidated_insights = consolidated_result["consolidated_insights"]

                return ExpertAnalysisResponse(
                    expert_analysis=expert_analysis["analysis"],
                    chunk_analyses=chunk_analyses,
                    consolidated_insights=consolidated_insights,
                    recommendations=expert_analysis["recommendations"],
                    action_plan=expert_analysis["action_plan"]
                )
            else:
                raise ValueError(f"Unknown analysis type: {request.analysis_type}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Comprehensive expert analysis failed: {str(e)}")

    async def domain_chunk_analysis(self, request: ExpertAnalysisRequest) -> ExpertAnalysisResponse:
        """Analyze multiple documentation chunks for domain-specific insights"""
        try:
            if not request.documentation_chunks:
                raise HTTPException(
                    status_code=400,
                    detail="Documentation chunks are required for this analysis type"
                )

            chunk_analyses = await self._analyze_documentation_chunks(
                request.user_story,
                request.documentation_chunks
            )

            consolidated_analysis = await self._consolidate_chunk_analyses(
                request.user_story,
                request.analysis_text,
                request.risk_assessment,
                chunk_analyses
            )

            return ExpertAnalysisResponse(
                expert_analysis=consolidated_analysis["expert_analysis"],
                chunk_analyses=chunk_analyses,
                consolidated_insights=consolidated_analysis["consolidated_insights"],
                recommendations=consolidated_analysis["recommendations"],
                action_plan=consolidated_analysis["action_plan"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Domain chunk analysis failed: {str(e)}")

    async def _quick_analysis(self, analysis_text: str, risk_text: str, user_story: str = "") -> str:
        """Quick expert analysis logic"""
        try:
            user_story_context = f"\nUser Story Context: {user_story}\n" if user_story else ""

            prompt = f"""
            As a domain expert, provide comprehensive expert analysis based on:
            {user_story_context}
            Document Analysis: {analysis_text}
            Risk Assessment: {risk_text}
            ..."""  # Keep your existing prompt structure

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self.expert_synthesis_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3500,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Quick expert analysis failed: {str(e)}")

    async def _enhanced_analysis(self, user_story: str, analysis_text: str,
                                 risk_text: str, feature_title: str) -> Dict[str, Any]:
        """Enhanced expert analysis with structured output"""
        try:
            prompt = f"""
            As a senior domain expert, provide comprehensive analysis for: {feature_title}
            User Story: {user_story}
            Document Analysis: {analysis_text}
            Risk Assessment: {risk_text}
            ..."""  # Keep your existing prompt structure

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self.expert_synthesis_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.2
            )

            analysis_content = response.choices[0].message.content
            recommendations = await self._extract_recommendations(analysis_content)
            action_plan = await self._extract_action_plan(analysis_content)

            return {
                "analysis": analysis_content,
                "recommendations": recommendations,
                "action_plan": action_plan
            }
        except Exception as e:
            raise Exception(f"Enhanced expert analysis failed: {str(e)}")

    async def _analyze_documentation_chunks(self, user_story: str,
                                            documentation_chunks: List[str]) -> List[ChunkAnalysisResult]:
        """Analyze multiple documentation chunks in parallel"""
        tasks = []
        for i, chunk in enumerate(documentation_chunks, 1):
            task = self._analyze_single_chunk(user_story, chunk, i)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        chunk_analyses = []
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                chunk_analyses.append(ChunkAnalysisResult(
                    chunk_number=i,
                    summary=f"Analysis failed: {str(result)}",
                    content_overview=[],
                    domain_specific_data=[],
                    abbreviations=[],
                    missing_information=[]
                ))
            else:
                chunk_analyses.append(result)
        return chunk_analyses

    async def _analyze_single_chunk(self, user_story: str, chunk_content: str,
                                    chunk_number: int) -> ChunkAnalysisResult:
        """Analyze a single documentation chunk"""
        try:
            prompt = f"""Analyze the following documentation chunk for domain-specific information:
            Documentation Chunk {chunk_number}: {chunk_content}
            User Story: {user_story}"""

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self.domain_analysis_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.2
            )

            analysis_content = response.choices[0].message.content
            return await self._parse_chunk_analysis(analysis_content, chunk_number)
        except Exception as e:
            raise Exception(f"Single chunk analysis failed for chunk {chunk_number}: {str(e)}")

    async def _consolidate_chunk_analyses(self, user_story: str, analysis_text: str,
                                          risk_text: str, chunk_analyses: List[ChunkAnalysisResult]) -> Dict[str, Any]:
        """Consolidate multiple chunk analyses into unified insights"""
        chunk_summaries = [f"Chunk {c.chunk_number}: {c.summary}" for c in chunk_analyses]

        prompt = f"""
        As a senior domain expert, consolidate these analyses:
        User Story: {user_story}
        Original Analysis: {analysis_text}
        Risk Assessment: {risk_text}
        Documentation Chunk Analyses: {" ".join(chunk_summaries)}"""

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": self.expert_synthesis_system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.2
        )

        consolidated_content = response.choices[0].message.content
        recommendations = await self._extract_recommendations(consolidated_content)
        action_plan = await self._extract_action_plan(consolidated_content)

        return {
            "expert_analysis": consolidated_content,
            "consolidated_insights": {
                "total_chunks_analyzed": len(chunk_analyses),
                "key_patterns": "Identified through cross-chunk analysis",
                "unified_domain_knowledge": "Consolidated domain expertise",
                "integrated_risk_factors": "Risk assessment integrated with domain findings"
            },
            "recommendations": recommendations,
            "action_plan": action_plan
        }

    async def _parse_chunk_analysis(self, analysis_content: str, chunk_number: int) -> ChunkAnalysisResult:
        """Parse the structured markdown analysis into structured data"""
        try:
            lines = analysis_content.split('\n')
            summary = ""
            for i, line in enumerate(lines):
                if line.startswith("## Summary"):
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() and not lines[j].startswith('#'):
                            summary = lines[j].strip()
                            break
                    break

            return ChunkAnalysisResult(
                chunk_number=chunk_number,
                summary=summary or "Domain analysis completed",
                content_overview=[],
                domain_specific_data=[],
                abbreviations=[],
                missing_information=[]
            )
        except Exception as e:
            return ChunkAnalysisResult(
                chunk_number=chunk_number,
                summary=f"Analysis completed with parsing limitations: {str(e)}",
                content_overview=[],
                domain_specific_data=[],
                abbreviations=[],
                missing_information=[]
            )

    async def _extract_recommendations(self, content: str) -> List[str]:
        """Extract recommendations from analysis content"""
        # Keep your existing implementation
        pass

    async def _extract_action_plan(self, content: str) -> List[Dict[str, Any]]:
        """Extract action plan items from analysis content"""
        # Keep your existing implementation
        pass