# Postman Testing Guide for QESTIT API

## Base URL
```
http://localhost:8000
```

## Available Endpoints

### 1. GET / - API Information
**Purpose**: Get API information and available endpoints
**Method**: GET
**URL**: `http://localhost:8000/`
**Headers**: None required
**Body**: None

**Expected Response**:
```json
{
  "message": "Enhanced AI Document Processing API with Azure OpenAI",
  "version": "3.0.0",
  "ai_provider": "Azure OpenAI",
  "current_model": "gpt-4.1",
  "endpoint": "https://insurenxtpresentation.openai.azure.com/",
  "available_endpoints": [...],
  "usage": {...}
}
```

### 2. GET /health - Health Check
**Purpose**: Check API health and service status
**Method**: GET
**URL**: `http://localhost:8000/health`
**Headers**: None required
**Body**: None

### 3. POST /api/full-workflow - Complete Workflow
**Purpose**: Process document through complete workflow (Analysis → Risk → Expert → Test Cases)
**Method**: POST
**URL**: `http://localhost:8000/api/full-workflow`
**Headers**: 
- `Content-Type`: `multipart/form-data`

**Body** (form-data):
- `file`: Upload a PDF, TXT, MD, DOC, or DOCX file
- `feature_prefix`: String (default: "TC")
- `iteration_count`: Number (default: 300)
- `user_story`: String (optional)
- `feature_title`: String (optional)

**Example Response**:
```json
{
  "status": "success",
  "message": "Full workflow completed successfully using Azure OpenAI model: gpt-4.1",
  "workflow_steps": {
    "step_1_analysis": {
      "status": "completed",
      "file": "path/to/analysis.md",
      "content_preview": "..."
    },
    "step_2_risk": {
      "status": "completed", 
      "file": "outputs/risk_assessment_20250810_155553.pdf",
      "content_preview": "..."
    },
    "step_3_expert": {
      "status": "completed",
      "file": "outputs/expert_analysis_20250810_155553.pdf", 
      "content_preview": "..."
    },
    "step_4_test_cases": {
      "status": "completed",
      "generated_count": 300,
      "files": {
        "markdown": "outputs/Enhanced_Test_Cases_TC_20250810_155928.md",
        "excel": "outputs/Professional_Test_Cases_TC_20250810_155928_300Cases.xlsx"
      }
    }
  }
}
```

### 4. GET /api/outputs - List All Output Files
**Purpose**: List all files in the outputs directory
**Method**: GET
**URL**: `http://localhost:8000/api/outputs`
**Headers**: None required
**Body**: None

**Expected Response**:
```json
{
  "files": [
    {
      "filename": "Professional_Test_Cases_TC_20250810_155928_300Cases.xlsx",
      "path": "outputs/Professional_Test_Cases_TC_20250810_155928_300Cases.xlsx",
      "size": 12345,
      "modified": "2025-08-10T15:59:28"
    }
  ]
}
```

### 5. GET /api/file-list - List Files by Type
**Purpose**: List files filtered by file type
**Method**: GET
**URL**: `http://localhost:8000/api/file-list?file_type=md`
**Headers**: None required
**Body**: None

**Query Parameters**:
- `file_type`: Optional. Values: `md`, `xlsx`, `pdf`, `txt`

**Example URLs**:
- `http://localhost:8000/api/file-list?file_type=md` - Markdown files
- `http://localhost:8000/api/file-list?file_type=xlsx` - Excel files  
- `http://localhost:8000/api/file-list?file_type=pdf` - PDF files
- `http://localhost:8000/api/file-list` - All files

### 6. GET /api/download/{filename} - Download File
**Purpose**: Download a specific file by filename
**Method**: GET
**URL**: `http://localhost:8000/api/download/{filename}`
**Headers**: None required
**Body**: None

**Example URLs**:
- `http://localhost:8000/api/download/Professional_Test_Cases_TC_20250810_155928_300Cases.xlsx`
- `http://localhost:8000/api/download/risk_assessment_20250810_155553.pdf`
- `http://localhost:8000/api/download/Enhanced_Test_Cases_TC_20250810_155928.md`

**Note**: The filename must be exact (case-sensitive) and the file must exist in either the `outputs` or `temp` directory.

## Testing Workflow

### Step 1: Test Basic Connectivity
1. GET `http://localhost:8000/` - Should return API info
2. GET `http://localhost:8000/health` - Should return health status

### Step 2: Test File Processing
1. POST `http://localhost:8000/api/full-workflow` with a document file
2. Note the generated filenames from the response

### Step 3: Test File Listing
1. GET `http://localhost:8000/api/outputs` - List all files
2. GET `http://localhost:8000/api/file-list?file_type=xlsx` - List Excel files
3. GET `http://localhost:8000/api/file-list?file_type=md` - List Markdown files

### Step 4: Test File Downloads
1. Use the exact filenames from Step 2 to download files
2. GET `http://localhost:8000/api/download/{exact_filename}`

## Common Issues and Solutions

### 404 Not Found for Downloads
- **Problem**: File not found when trying to download
- **Solution**: 
  1. Check the exact filename in the API response
  2. Verify the file exists using `/api/outputs` or `/api/file-list`
  3. Use the exact filename (case-sensitive)

### File Processing Errors
- **Problem**: Workflow fails during processing
- **Solution**:
  1. Check the API logs for detailed error messages
  2. Verify Azure OpenAI credentials are correct
  3. Check file format is supported (PDF, TXT, MD, DOC, DOCX)

### Large File Processing
- **Problem**: Timeout or memory issues with large files
- **Solution**:
  1. Use smaller files for testing
  2. Check the `iteration_count` parameter (lower values = faster processing)

## Postman Collection Setup

1. **Create New Collection**: "QESTIT API Tests"
2. **Set Base URL Variable**: `{{base_url}}` = `http://localhost:8000`
3. **Create Environment Variables**:
   - `base_url`: `http://localhost:8000`
   - `generated_filename`: (will be set from API responses)

4. **Test Scripts** (for automation):
   ```javascript
   // For full-workflow endpoint, extract filename
   if (pm.response.code === 200) {
       const response = pm.response.json();
       if (response.workflow_steps?.step_4_test_cases?.files?.excel) {
           const filename = response.workflow_steps.step_4_test_cases.files.excel.split('/').pop();
           pm.environment.set('generated_filename', filename);
       }
   }
   ```

## Expected File Types Generated

- **Document Analysis**: Markdown (.md) files
- **Risk Assessment**: PDF (.pdf) files  
- **Expert Analysis**: PDF (.pdf) files
- **Test Cases**: 
  - Excel (.xlsx) files with comprehensive test scenarios
  - Markdown (.md) files with formatted test cases

## Performance Notes

- **Small documents** (< 1MB): Processing time ~30-60 seconds
- **Medium documents** (1-5MB): Processing time ~1-3 minutes
- **Large documents** (> 5MB): Processing time ~3-10 minutes
- **Test case generation**: 300 test cases typically takes 2-5 minutes

## Troubleshooting

### Check API Logs
The API provides detailed logging. Look for:
- Service initialization messages
- Processing step completion
- File generation confirmations
- Error details with stack traces

### Verify Azure OpenAI
- Check environment variables are set correctly
- Verify API key has sufficient credits
- Confirm endpoint URL is accessible

### File System Issues
- Ensure `outputs/` and `temp/` directories exist
- Check file permissions
- Verify disk space is available
