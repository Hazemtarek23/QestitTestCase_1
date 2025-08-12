# Quick Start Guide - QESTIT API Testing

## Prerequisites
- Python 3.8+ installed
- FastAPI server running on localhost:8000
- Azure OpenAI credentials configured

## 1. Start the API Server

```bash
# Navigate to your project directory
cd /path/to/qcentric

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 2. Test Basic Connectivity

### Using Python Script
```bash
python test_api.py
```

### Using Postman
1. GET `http://localhost:8000/` - API Information
2. GET `http://localhost:8000/health` - Health Check

## 3. Test File Processing

### Using Python Script
```bash
# Uncomment the file processing test in test_api.py
python test_api.py
```

### Using Postman
1. POST `http://localhost:8000/api/full-workflow`
2. Body: `multipart/form-data`
   - `file`: Upload a document (PDF, TXT, MD, DOC, DOCX)
   - `feature_prefix`: "TC"
   - `iteration_count`: "50" (for faster testing)
   - `user_story`: "As a customer, I want to transfer funds between accounts"
   - `feature_title`: "Fund Transfer Feature"

## 4. Test File Operations

### List Files
- GET `http://localhost:8000/api/outputs` - All files
- GET `http://localhost:8000/api/file-list?file_type=xlsx` - Excel files
- GET `http://localhost:8000/api/file-list?file_type=md` - Markdown files

### Download Files
- GET `http://localhost:8000/api/download/{filename}` - Replace {filename} with actual filename

## 5. Expected Results

### Successful Workflow Response
```json
{
  "status": "success",
  "workflow_steps": {
    "step_4_test_cases": {
      "files": {
        "excel": "outputs/Professional_Test_Cases_TC_20250810_155928_300Cases.xlsx",
        "markdown": "outputs/Enhanced_Test_Cases_TC_20250810_155928.md"
      }
    }
  }
}
```

### File Download
- Excel files: Professional test cases with 300+ scenarios
- Markdown files: Formatted test case documentation
- PDF files: Risk assessment and expert analysis reports

## 6. Troubleshooting

### Common Issues
1. **404 Not Found**: Check exact filename from API response
2. **Processing Errors**: Check API logs for detailed error messages
3. **Azure OpenAI Errors**: Verify API key and endpoint configuration

### Check Logs
The API provides detailed logging. Look for:
- Service initialization
- Processing step completion
- File generation confirmations
- Error details

## 7. Performance Notes

- **Small documents**: ~30-60 seconds
- **Medium documents**: ~1-3 minutes  
- **Large documents**: ~3-10 minutes
- **Test generation**: 50 test cases ~1-2 minutes, 300 test cases ~2-5 minutes

## 8. Next Steps

1. Test with your own documents
2. Adjust `iteration_count` for different test case volumes
3. Customize `feature_prefix` for your project
4. Use the generated files for your testing needs

## Support

- Check the detailed `postman_test_guide.md` for comprehensive testing
- Review API logs for debugging information
- Verify Azure OpenAI configuration in `env_template.txt`
