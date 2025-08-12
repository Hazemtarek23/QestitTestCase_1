"""Test Case Controller
RESTful API controller for test case generation"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import os
from datetime import datetime
from services.test_case_service import TestCaseService

class TestCaseRequest(BaseModel):
    """Request model for test case generation"""
    user_input: str
    technical_analysis: Optional[str] = ""
    domain_analysis: Optional[str] = ""
    screen_navigation: Optional[str] = ""
    test_risk: Optional[str] = ""
    test_plan: Optional[str] = ""
    feature_prefix: Optional[str] = "TC"
    iteration_count: Optional[int] = 10
    raw_input_chunk: Optional[str] = ""

class TestCaseFromFileRequest(BaseModel):
    """Request model for test case generation from file"""
    feature_prefix: Optional[str] = "TC"
    iteration_count: Optional[int] = 10

class TestCaseController:
    """Controller for test case generation endpoints"""

    def __init__(self):
        self.service = TestCaseService()
        self.router = APIRouter()
        self.logger = logging.getLogger(__name__)
        # Register routes
        self._register_routes()

    def _register_routes(self):
        """Register all routes for the controller"""

        @self.router.post("/generate")
        async def generate_test_cases(request: TestCaseRequest):
            """
            Generate test cases based on provided analysis and requirements
            """
            try:
                self.logger.info(
                    f"Generating {request.iteration_count} test cases with prefix '{request.feature_prefix}'")

                result = self.service.generate_test_cases(
                    user_input=request.user_input,
                    technical_analysis=request.technical_analysis,
                    domain_analysis=request.domain_analysis,
                    screen_navigation=request.screen_navigation,
                    test_risk=request.test_risk,
                    test_plan=request.test_plan,
                    feature_prefix=request.feature_prefix,
                    iteration_count=request.iteration_count,
                    raw_input_chunk=request.raw_input_chunk
                )

                if result["success"]:
                    return {
                        "status": "success",
                        "message": f"Successfully generated {result['generated_count']} test cases",
                        "data": {
                            "generated_count": result["generated_count"],
                            "feature_prefix": result["feature_prefix"],
                            "timestamp": result["timestamp"],
                            "files": {
                                "markdown": result["markdown_path"].replace("\\", "/") if result[
                                    "markdown_path"] else None,
                                "excel": result["excel_path"].replace("\\", "/") if result["excel_path"] else None,
                                "pdf": result["pdf_path"].replace("\\", "/") if result["pdf_path"] else None
                            }
                        },
                        "test_cases_preview": result["test_cases_content"][:500] + "..." if len(
                            result["test_cases_content"]) > 500 else result["test_cases_content"]
                    }
                else:
                    raise HTTPException(status_code=500, detail=f"Test case generation failed: {result['error']}")

            except Exception as e:
                self.logger.error(f"Error in generate_test_cases endpoint: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

        @self.router.post("/generate-from-file")
        async def generate_test_cases_from_file(
                file: UploadFile = File(...),
                feature_prefix: str = Form("TC"),
                iteration_count: int = Form(10)
        ):
            """
            Generate test cases from uploaded file content
            """
            temp_file_path = None
            try:
                # Validate file
                if not file.filename:
                    raise HTTPException(status_code=400, detail="No file uploaded")

                # Save uploaded file temporarily
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_filename = "".join(c for c in file.filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
                temp_filename = f"{timestamp}_{safe_filename.replace(' ', '_')}"
                temp_file_path = f"temp/{temp_filename}"

                # Ensure temp directory exists
                os.makedirs("temp", exist_ok=True)

                # Save file
                await file.seek(0)
                with open(temp_file_path, "wb") as f:
                    while chunk := await file.read(8192):
                        f.write(chunk)

                self.logger.info(f"File saved temporarily at: {temp_file_path}")

                # Generate test cases
                result = self.service.generate_test_cases_from_file(
                    file_path=temp_file_path,
                    feature_prefix=feature_prefix,
                    iteration_count=iteration_count
                )

                if result["success"]:
                    return {
                        "status": "success",
                        "message": f"Successfully generated {result['generated_count']} test cases from file",
                        "data": {
                            "source_file": file.filename,
                            "generated_count": result["generated_count"],
                            "feature_prefix": result["feature_prefix"],
                            "timestamp": result["timestamp"],
                            "files": {
                                "markdown": result["markdown_path"].replace("\\", "/") if result[
                                    "markdown_path"] else None,
                                "excel": result["excel_path"].replace("\\", "/") if result["excel_path"] else None,
                                "pdf": result["pdf_path"].replace("\\", "/") if result["pdf_path"] else None
                            }
                        },
                        "test_cases_preview": result["test_cases_content"][:500] + "..." if len(
                            result["test_cases_content"]) > 500 else result["test_cases_content"]
                    }
                else:
                    raise HTTPException(status_code=500, detail=f"Test case generation failed: {result['error']}")

            except Exception as e:
                self.logger.error(f"Error in generate_test_cases_from_file endpoint: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
            finally:
                # Clean up temporary file
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.remove(temp_file_path)
                        self.logger.info(f"Cleaned up temporary file: {temp_file_path}")
                    except Exception as cleanup_error:
                        self.logger.warning(f"Failed to clean up temporary file {temp_file_path}: {str(cleanup_error)}")

        @self.router.get("/health")
        async def health_check():
            """
            Health check endpoint to verify the service is running
            """
            try:
                return {
                    "status": "healthy",
                    "service": "test_case_controller",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Test Case Controller is running successfully with LLM"
                }
            except Exception as e:
                self.logger.error(f"Health check failed: {str(e)}")
                raise HTTPException(status_code=500, detail="Service unhealthy")

        @self.router.get("/status")
        async def get_status():
            """
            Get detailed status information about the controller and service
            """
            try:
                return {
                    "controller_status": "active",
                    "service_status": "initialized",
                    "ai_provider": "LLM",
                    "endpoints": [
                        "/generate",
                        "/generate-from-file",
                        "/health",
                        "/status"
                    ],
                    "supported_file_types": [
                        "text", "markdown", "pdf", "docx", "txt"
                    ],
                    "temp_directory": "temp/",
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                self.logger.error(f"Status check failed: {str(e)}")
                raise HTTPException(status_code=500, detail="Unable to retrieve status")

    def get_router(self) -> APIRouter:
        """
        Get the configured router instance
        """
        return self.router

    def cleanup(self):
        """
        Cleanup method for graceful shutdown
        """
        try:
            # Clean up any remaining temporary files
            temp_dir = "temp"
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        self.logger.warning(f"Failed to remove temp file {file_path}: {str(e)}")

            self.logger.info("TestCaseController cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

# Factory function for creating controller instance
def create_test_case_controller() -> TestCaseController:
    """
    Factory function to create and configure a TestCaseController instance

    Returns:
        TestCaseController: Configured controller instance
    """
    return TestCaseController()
