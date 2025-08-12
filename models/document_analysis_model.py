# controllers/document_analysis_router.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Any
from pydantic import BaseModel
from typing import Dict, List, Set, Any, Optional
import unicodedata
import logging


# Pydantic models for request/response
class DocumentChunk(BaseModel):
    chunk_id: str
    content: str


class MultiChunkAnalysisRequest(BaseModel):
    user_story: str
    chunks: List[DocumentChunk]


class SingleAnalysisRequest(BaseModel):
    text: str


class TechnicalAnalysisResponse(BaseModel):
    chunk_id: str
    analysis: str


class MultiChunkAnalysisResponse(BaseModel):
    user_story: str
    analyses: List[TechnicalAnalysisResponse]


class DocumentAnalysisRouter:
    def __init__(self, client: Any, deployment_name: str):
        self.client = client
        self.deployment_name = deployment_name
        self.router = APIRouter()
        self.logger = logging.getLogger(__name__)

        # Technical analysis system prompt from the workflow
        self.TECHNICAL_ANALYSIS_SYSTEM_PROMPT = """You are a technical documentation analysis assistant. Your task is to provide a comprehensive overview of ALL relevant technical information from this documentation chunk.

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
| ... | ... | ... | ... |

*Extraction Depth: How complete is the information extracted*
*System Relevancy: How important is this for understanding the system*

## Important Attributes and Data
| Attribute/Field Name | Description | Data Type | Validation Rules | Required | Technical Notes |
|----------------------|-------------|-----------|------------------|----------|----------------|
| Field 1 | Description | String/Number/etc | Rules | Yes/No | Notes |
| Field 2 | Description | String/Number/etc | Rules | Yes/No | Notes |
| ... | ... | ... | ... | ... | ... |

## Business Process Tables
| Process Name | Process Description | Process Steps | Input Requirements | Output Results | Technical Implementation Details |
|--------------|---------------------|---------------|-------------------|---------------|----------------------------------|
| Process 1 | Description | Steps | Inputs | Outputs | Implementation |
| Process 2 | Description | Steps | Inputs | Outputs | Implementation |
| ... | ... | ... | ... | ... | ... |

## System Requirements Tables
| Requirement ID | Requirement Description | Requirement Type | Priority | Implementation Status | Technical Constraints |
|----------------|-------------------------|-----------------|----------|------------------------|------------------------|
| REQ-1 | Description | Functional/Non-functional | High/Medium/Low | Status | Constraints |
| REQ-2 | Description | Functional/Non-functional | High/Medium/Low | Status | Constraints |
| ... | ... | ... | ... | ... | ... |

When information in a table cell is missing, use 'N/A' as value.
Create appropriate sections only for information found in the chunk.
Use proper markdown syntax for all tables and sections.
"""

        self._routes()

    def _routes(self):
        @self.router.post("/analyze", response_model=Dict)
        async def analyze_document(request: SingleAnalysisRequest):
            """Original single document analysis endpoint"""
            try:
                result = await self.analyze_document_logic(request.text)
                return JSONResponse(content={"analysis": result}, ensure_ascii=False)
            except Exception as e:
                self.logger.error(f"Single document analysis failed: {str(e)}")
                return JSONResponse(status_code=500, content={"error": str(e)})

        @self.router.post("/analyze-technical", response_model=Dict)
        async def analyze_technical_document(request: SingleAnalysisRequest):
            """Technical analysis using the workflow system prompt"""
            try:
                result = await self.analyze_technical_document_logic(request.text)
                return JSONResponse(content={"analysis": result}, ensure_ascii=False)
            except Exception as e:
                self.logger.error(f"Technical document analysis failed: {str(e)}")
                return JSONResponse(status_code=500, content={"error": str(e)})

        @self.router.post("/analyze-multi-chunk", response_model=MultiChunkAnalysisResponse)
        async def analyze_multi_chunk_documents(request: MultiChunkAnalysisRequest):
            """Multi-chunk technical analysis following the workflow pattern"""
            try:
                analyses = []

                for chunk in request.chunks:
                    analysis_result = await self.analyze_chunk_technical_logic(
                        chunk.content,
                        request.user_story
                    )

                    analyses.append(TechnicalAnalysisResponse(
                        chunk_id=chunk.chunk_id,
                        analysis=analysis_result
                    ))

                return MultiChunkAnalysisResponse(
                    user_story=request.user_story,
                    analyses=analyses
                )

            except Exception as e:
                self.logger.error(f"Multi-chunk analysis failed: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.post("/analyze-workflow-chunks", response_model=Dict)
        async def analyze_workflow_chunks(request: MultiChunkAnalysisRequest):
            """Analyze chunks following the exact workflow pattern (6 chunks)"""
            try:
                if len(request.chunks) != 6:
                    raise HTTPException(
                        status_code=400,
                        detail="This endpoint requires exactly 6 documentation chunks"
                    )

                results = {}

                for i, chunk in enumerate(request.chunks, 1):
                    chunk_key = f"tech_analysis_chunk_{i}"
                    analysis_result = await self.analyze_chunk_technical_logic(
                        chunk.content,
                        request.user_story
                    )
                    results[chunk_key] = analysis_result

                return JSONResponse(
                    content={
                        "user_story": request.user_story,
                        "workflow_version": "0.7",
                        "analyses": results
                    },
                    ensure_ascii=False
                )

            except Exception as e:
                self.logger.error(f"Workflow chunks analysis failed: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

    async def analyze_document_logic(self, text: str) -> str:
        """Original document analysis logic"""
        try:
            text = self._sanitize_text(text)

            prompt = f"""
            Please analyze the following document and provide a comprehensive analysis:

            Document Content:
            {text}

            Please provide:
            1. Executive Summary
            2. Key Findings
            3. Main Topics Covered
            4. Document Structure Analysis
            5. Content Quality Assessment
            """

            response = await self._call_azure_openai(
                system_content="You are a professional document analyst. Provide thorough and structured analysis.",
                user_content=prompt
            )

            return response

        except Exception as e:
            raise Exception(f"Document analysis failed: {str(e)}")

    async def analyze_technical_document_logic(self, text: str) -> str:
        """Technical document analysis using workflow system prompt"""
        try:
            text = self._sanitize_text(text)

            user_prompt = f"""Analyze the following documentation chunk for technical details:
{text}

Focus on extracting technical information that would be essential for understanding system behavior and creating test cases."""

            response = await self._call_azure_openai(
                system_content=self.TECHNICAL_ANALYSIS_SYSTEM_PROMPT,
                user_content=user_prompt
            )

            return response

        except Exception as e:
            raise Exception(f"Technical document analysis failed: {str(e)}")

    async def analyze_chunk_technical_logic(self, chunk_content: str, user_story: str) -> str:
        """Analyze individual chunk following workflow pattern"""
        try:
            chunk_content = self._sanitize_text(chunk_content)
            user_story = self._sanitize_text(user_story)

            user_prompt = f"""User Story Context: {user_story}

Analyze the following documentation chunk for technical details:
{chunk_content}

Focus on extracting technical information that would be essential for understanding system behavior and creating test cases."""

            response = await self._call_azure_openai(
                system_content=self.TECHNICAL_ANALYSIS_SYSTEM_PROMPT,
                user_content=user_prompt
            )

            return response

        except Exception as e:
            raise Exception(f"Chunk technical analysis failed: {str(e)}")

    async def _call_azure_openai(self, system_content: str, user_content: str) -> str:
        """Centralized AI API call (model-agnostic)"""
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=4000,  # Increased for technical analysis
                temperature=0.3
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"AI API call failed: {str(e)}")

    def _sanitize_text(self, text: str) -> str:
        """Normalize text to avoid encoding issues (e.g., ''' and Arabic)"""
        if not text:
            return ""
        return unicodedata.normalize("NFKC", text)

    def get_workflow_config(self) -> Dict[str, Any]:
        """Return the workflow configuration for reference"""
        return {
            "version": "0.7",
            "id": "1_Documentation_analysis",
            "description": "Analyze documentation to create technical understanding foundation for test cases",
            "supported_endpoints": [
                "/analyze",
                "/analyze-technical",
                "/analyze-multi-chunk",
                "/analyze-workflow-chunks"
            ],
            "chunk_count": 6,
            "output_format": "structured_markdown"
        }


# Usage example for integration
