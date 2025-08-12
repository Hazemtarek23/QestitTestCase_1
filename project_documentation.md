# Qcentric - AI-Powered Document Analysis & Test Generation System

## Project Overview

**Qcentric** is a sophisticated AI-powered document processing system that leverages Azure OpenAI models to automatically analyze documents, assess risks, provide expert reviews, and generate comprehensive test cases. The system is built with modern Python technologies including FastAPI, follows SOLID principles, and provides both backend API services and a professional frontend interface.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [API Endpoints](#api-endpoints)
5. [AI Services](#ai-services)
6. [Frontend Interface](#frontend-interface)
7. [Configuration & Environment](#configuration--environment)
8. [Deployment & Docker](#deployment--docker)
9. [Technical Features](#technical-features)
10. [Usage Examples](#usage-examples)

---

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   FastAPI Backend│    │  AI Services    │
│   (HTML/CSS/JS) │◄──►│   (Python)       │◄──►│  (Azure OpenAI) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Static Files  │    │   Controllers    │    │   Models        │
│   (CSS/JS)      │    │   (Business Logic)│   │   (Data Models) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Design Principles
- **SOLID Principles**: Dependency Inversion, Single Responsibility, Open/Closed
- **Dependency Injection**: Centralized service management
- **Separation of Concerns**: Clear separation between UI, business logic, and AI services
- **Modular Architecture**: Pluggable AI backends and services

---

## Project Structure

```
Qcentric/
├── main.py                          # Main FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Docker container definition
├── app.log                         # Application logs
├── app.log                         # Application logs
├── conf/                           # Configuration modules
│   ├── __init__.py
│   ├── azure_openai_config.py      # Azure OpenAI configuration
│   ├── documentation_analysis_workflow.py
│   └── expert_knowledge_workflow.py
├── controllers/                     # API route controllers
│   ├── __init__.py
│   ├── document_analysis_router.py # Document analysis endpoints
│   ├── expert_analysis_router.py   # Expert analysis endpoints
│   ├── generate_test_cases_logic.py # Test case generation logic
│   ├── openai_test_router.py       # OpenAI integration
│   ├── risk_assessment_router.py   # Risk assessment endpoints
│   └── upload_router.py            # File upload handling
├── models/                         # Data models and schemas
│   ├── __init__.py
│   ├── document_analysis_model.py  # Document analysis data models
│   ├── expert_model.py             # Expert analysis models
│   ├── risk_model.py               # Risk assessment models
│   ├── test_case_model.py          # Test case data models
│   └── upload_models.py            # File upload models
├── services/                       # Business logic services
│   ├── __init__.py
│   ├── ai_analysis_prompts.py     # AI prompt templates
│   ├── ai_service.py               # AI service orchestration
│   ├── enhanced_test_case_service.py # Enhanced test case generation
│   ├── excel_generator.py          # Excel file generation
│   ├── expert_knowledge_service.py # Expert knowledge processing
│   ├── azure_openai_client.py      # Azure OpenAI API client
│   ├── integrated_workflow_service.py # End-to-end workflow
│   ├── openai_client.py            # OpenAI API client
│   ├── pdf_generator.py            # PDF file generation
│   ├── ports.py                    # Abstract interfaces (SOLID)
│   ├── risk_assessment_service.py  # Risk assessment logic
│   ├── swagger_service.py          # API documentation
│   ├── test_case_service.py        # Core test case generation
│   └── upload_service.py           # File upload processing
├── static/                         # Frontend static files
│   ├── index.html                  # Main UI interface
│   └── styles.css                  # Professional styling
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── chunker.py                  # Text chunking utilities
│   ├── excel_generator.py          # Excel generation utilities
│   └── excel_writer.py             # Excel writing utilities
├── uploads/                        # Temporary uploaded files
├── outputs/                        # Generated output files
└── temp/                           # Temporary processing files
```

---

## Core Components

### 1. Main Application (`main.py`)
- **FastAPI Application**: Main web framework with CORS middleware
- **Lifespan Management**: Application startup/shutdown handling
- **Service Initialization**: Dependency injection setup
- **Route Registration**: API endpoint registration
- **Static File Serving**: Frontend UI hosting at `/ui` endpoint

### 2. AI Service Layer
- **AzureOpenAIClient**: Primary AI service using Azure OpenAI models
- **TextGenerator Protocol**: Abstract interface for AI services (SOLID principle)
- **Fallback Mechanisms**: Azure OpenAI models and deterministic content generation
- **Model Management**: Azure OpenAI model selection and fallback

### 3. Business Logic Controllers
- **DocumentAnalysisController**: Document processing and analysis
- **RiskAssessmentRouter**: Risk evaluation and mitigation
- **ExpertAnalysisController**: Expert review and validation
- **EnhancedTestCaseService**: Large-scale test case generation

---

## API Endpoints

### Core Processing Endpoints

#### 1. `/process` - Main Document Processing
```http
POST /process
Content-Type: multipart/form-data

Parameters:
- file: UploadFile (PDF, DOCX, TXT, MD)
- use_enhanced_service: bool (default: true)
- iteration_count: int (default: 300)
- feature_prefix: str (default: "TC")

Response:
{
  "status": "success",
  "service_used": "Enhanced Large-Scale Test Case Service",
  "ai_model": "gpt-4.1",
  "test_case_count": 300,
  "files": {
    "test_cases_excel": "path/to/excel.xlsx",
    "test_cases_markdown": "path/to/markdown.md"
  }
}
```

#### 2. `/api/full-workflow` - Complete Workflow Processing
```http
POST /api/full-workflow
Content-Type: multipart/form-data

Parameters:
- file: UploadFile
- user_story: str (optional)
- feature_title: str (optional)
- feature_prefix: str (default: "TC")
- iteration_count: int (default: 300)

Response:
{
  "workflow_steps": {
    "step_1_analysis": {"file": "path/to/analysis.pdf"},
    "step_2_risk": {"file": "path/to/risk.pdf"},
    "step_3_expert": {"file": "path/to/expert.pdf"},
    "step_4_test_cases": {
      "files": {
        "excel": "path/to/test_cases.xlsx",
        "markdown": "path/to/test_cases.md"
      }
    }
  }
}
```

### Utility Endpoints

#### 3. `/api/download/{filename}` - File Download
```http
GET /api/download/{filename}
Response: File download
```

#### 4. `/api/outputs` - List Generated Files
```http
GET /api/outputs
Response: List of available output files
```

#### 5. `/health` - Health Check
```http
GET /health
Response: System health status
```

---

## AI Services

### AzureOpenAIClient
**Purpose**: Primary AI text generation service using Azure OpenAI models

**Features**:
- **API Integration**: Azure OpenAI API support
- **Model Selection**: Azure OpenAI model selection
- **Fallback Content**: Deterministic content generation when AI fails
- **Professional Quality**: High-quality text generation using GPT models

**Configuration**:
```python
# Environment Variables
AZURE_OPENAI_KEY=6f1e77250eec438d9898ae26045e8581
AZURE_OPENAI_MODEL=gpt-4.1
AZURE_OPENAI_ENDPOINT=https://insurenxtpresentation.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

**Model Capabilities**:
1. GPT-4.1 for high-quality text generation
2. GPT-4.1-mini for faster processing
3. GPT-4.1-nano for lightweight tasks
4. Deterministic fallback content

### Enhanced Test Case Service
**Purpose**: Generate professional, large-scale test cases

**Features**:
- **Batch Processing**: Handles 300+ test cases efficiently
- **Professional Formatting**: Excel with advanced styling
- **Comprehensive Coverage**: Banking domain expertise
- **Realistic Test Data**: Arabic, Western, and Asian names/addresses

**Test Case Categories**:
1. **Core Banking Operations** (35%): Account management, transactions, loans
2. **Digital Banking** (20%): Internet banking, mobile apps, ATMs
3. **Risk & Compliance** (15%): AML/KYC, credit risk, fraud detection
4. **Back Office** (10%): Settlement, accounting, operations
5. **Customer Experience** (10%): Customer service, relationship management
6. **Integration** (5%): System integrations, security
7. **Analytics** (5%): Business intelligence, reporting

---

## Frontend Interface

### UI Components
- **Modern Design**: Professional banking application aesthetic
- **3D Animations**: Tilt effects, progress animations, confetti
- **Responsive Layout**: Mobile and desktop optimized
- **Progress Tracking**: Real-time processing status
- **File Management**: Drag-and-drop file uploads

### User Experience Features
- **File Upload**: Support for PDF, DOCX, TXT, MD formats
- **Progress Visualization**: Step-by-step processing indicators
- **Result Display**: Download links for generated files
- **Error Handling**: Comprehensive error messages and debugging
- **Responsive Design**: Works on all device sizes

### Technical Implementation
- **Vanilla JavaScript**: No external framework dependencies
- **CSS3 Animations**: Advanced visual effects and transitions
- **FormData API**: Efficient file upload handling
- **Fetch API**: Modern HTTP request handling
- **Local Storage**: User preference persistence

---

## Configuration & Environment

### Environment Variables
```bash
# Required
AZURE_OPENAI_KEY=6f1e77250eec438d9898ae26045e8581

# Optional (with defaults)
AZURE_OPENAI_MODEL=gpt-4.1
AZURE_OPENAI_ENDPOINT=https://insurenxtpresentation.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### Configuration Files
- **docker-compose.yml**: Environment variable configuration
- **Dockerfile**: Container environment setup

---

## Deployment & Docker

### Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  qcentric:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AZURE_OPENAI_KEY=6f1e77250eec438d9898ae26045e8581
      - AZURE_OPENAI_ENDPOINT=https://insurenxtpresentation.openai.azure.com/
      - AZURE_OPENAI_API_VERSION=2024-12-01-preview
      - AZURE_OPENAI_MODEL=gpt-4.1
    volumes:
      - ./outputs:/app/outputs
      - ./uploads:/app/uploads
```

### Container Features
- **Multi-stage Build**: Optimized Python runtime
- **Volume Mounting**: Persistent file storage
- **Port Exposure**: HTTP access on port 8000
- **Environment Configuration**: Secure API key management

---

## Technical Features

### SOLID Principles Implementation
1. **Single Responsibility**: Each service has one clear purpose
2. **Open/Closed**: Services can be extended without modification
3. **Liskov Substitution**: AI services are interchangeable
4. **Interface Segregation**: Clean, focused interfaces
5. **Dependency Inversion**: High-level modules don't depend on low-level modules

### Performance Optimizations
- **Async/Await**: Non-blocking I/O operations
- **Batch Processing**: Efficient handling of large datasets
- **Memory Management**: Streaming file processing
- **Caching**: Model and response caching
- **Connection Pooling**: HTTP connection reuse

### Security Features
- **CORS Configuration**: Controlled cross-origin access
- **File Validation**: Upload file type and size checking
- **API Key Management**: Secure environment variable usage
- **Input Sanitization**: XSS and injection prevention
- **Error Handling**: Secure error message disclosure

---

## Usage Examples

### 1. Basic Document Processing
```bash
# Upload a document and generate test cases
curl -X POST "http://localhost:8000/process" \
  -F "file=@document.pdf" \
  -F "iteration_count=50" \
  -F "feature_prefix=TC"
```

### 2. Complete Workflow Processing
```bash
# Run full analysis workflow
curl -X POST "http://localhost:8000/api/full-workflow" \
  -F "file=@requirements.pdf" \
  -F "user_story=User wants to transfer money" \
  -F "feature_title=Money Transfer Feature" \
  -F "iteration_count=100"
```

### 3. Frontend Usage
1. **Access UI**: Navigate to `http://localhost:8000/ui`
2. **Upload File**: Select PDF, DOCX, TXT, or MD file
3. **Set Parameters**: Choose test case count (10-500)
4. **Start Processing**: Click "Start Analysis"
5. **Monitor Progress**: Watch real-time processing status
6. **Download Results**: Access generated Excel and Markdown files

---

## File Generation Capabilities

### Excel Output Features
- **Professional Formatting**: Headers, borders, colors, fonts
- **Multiple Worksheets**: Organized by test categories
- **Data Validation**: Dropdowns and input restrictions
- **Conditional Formatting**: Visual status indicators
- **Auto-sizing**: Column width optimization

### Markdown Output Features
- **Structured Format**: Clear hierarchy and organization
- **Code Blocks**: Syntax highlighting for technical content
- **Tables**: Formatted test case data
- **Links**: Cross-references and navigation
- **Metadata**: Generation timestamps and model information

### PDF Output Features
- **Professional Layout**: Corporate document styling
- **Table of Contents**: Automated navigation
- **Page Numbering**: Consistent pagination
- **Header/Footer**: Branding and metadata
- **Multi-format Support**: Various page sizes and orientations

---

## Error Handling & Fallbacks

### AI Service Fallbacks
1. **Primary**: Azure OpenAI API with GPT-4.1 models
2. **Secondary**: Azure OpenAI GPT-4.1-mini models
3. **Tertiary**: Azure OpenAI GPT-4.1-nano models
4. **Final**: Deterministic content generation

### Error Recovery
- **Automatic Retry**: Failed API calls retry automatically
- **Graceful Degradation**: Service continues with reduced functionality
- **User Notification**: Clear error messages and suggestions
- **Logging**: Comprehensive error tracking and debugging

---

## Monitoring & Logging

### Application Logs
- **Structured Logging**: JSON format for easy parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Performance Metrics**: Processing time and resource usage
- **Error Tracking**: Detailed error context and stack traces

### Health Monitoring
- **Endpoint Health**: `/health` endpoint for monitoring
- **Service Status**: AI service availability checking
- **Resource Usage**: Memory and CPU monitoring
- **Response Times**: API performance metrics

---

## Future Enhancements

### Planned Features
1. **Multi-language Support**: Arabic, English, and other languages
2. **Advanced AI Models**: GPT-4, Claude, and other cutting-edge models
3. **Real-time Collaboration**: Multi-user document processing
4. **API Rate Limiting**: Usage-based access control
5. **Advanced Analytics**: Processing insights and metrics

### Scalability Improvements
1. **Microservices Architecture**: Service decomposition
2. **Message Queues**: Asynchronous processing
3. **Load Balancing**: Multiple instance support
4. **Database Integration**: Persistent data storage
5. **Caching Layer**: Redis or similar caching

---

## Conclusion

Qcentric represents a sophisticated, enterprise-grade document processing system that combines modern web technologies with cutting-edge AI capabilities. The system's architecture follows industry best practices, implements SOLID principles, and provides a robust foundation for automated document analysis and test case generation.

The combination of FastAPI backend, professional frontend interface, and intelligent AI services creates a powerful tool for organizations requiring automated document processing, risk assessment, and comprehensive test case generation. The system's modular design ensures maintainability and extensibility for future enhancements.

With its comprehensive error handling, fallback mechanisms, and professional output generation, Qcentric provides a reliable solution for businesses looking to automate their document analysis and testing workflows while maintaining high quality and professional standards.

---

## Technical Specifications

- **Backend Framework**: FastAPI (Python 3.8+)
- **AI Provider**: Azure OpenAI (with deterministic fallback)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **File Formats**: PDF, DOCX, TXT, MD (input); Excel, Markdown, PDF (output)
- **API Protocol**: RESTful HTTP with multipart form data
- **Authentication**: API key-based (configurable)
- **Deployment**: Docker containerization
- **Performance**: Async processing, batch operations, streaming
- **Scalability**: Stateless design, horizontal scaling support

