@echo off
REM Configure app to use local llama.cpp server (OpenAI-compatible)
set USE_LLAMA_SERVER=1
set LLAMA_SERVER_BASE_URL=http://127.0.0.1:8080
set LLAMA_MODEL=unsloth.Q4_K_M.gguf

REM Optional: disable SSL verification for local HTTP
set LLAMA_VERIFY_SSL=true

REM Launch API
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info

