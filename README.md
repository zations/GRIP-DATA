# 🧠 GRIP – Git Runtime Intelligence Platform

**GRIP** (Git Runtime Intelligence Platform) is an AI-powered developer assistant that combines runtime error tracing, semantic analysis, and intelligent debugging to help teams quickly identify and understand the root cause of software errors.  
Originally designed for the **AWS Bedrock Hackathon**, GRIP integrates local runtime intelligence with cloud-based LLM inference and vector retrieval.

---

## 🚀 Current Features (as of this build)

### 🧩 1. Error Origin Tracing Middleware
- Custom Django middleware (`error_origin.py`) that intercepts runtime exceptions.  
- Extracts complete **Python traceback context** — including function, file, and line numbers.  
- Dynamically inspects stack frames to identify **where a function/class was originally defined**.  
- Outputs a structured JSON object showing:
  - Error type and message  
  - Full call stack  
  - Likely symbol origins (e.g. `NoteForm` → `core/forms.py:12`)  

✅ Example output:
```json
{
  "error_type": "AttributeError",
  "error_message": "NoneType object has no attribute 'save'",
  "stack_frames": [...],
  "likely_origin_symbols": [
    {"symbol": "NoteForm", "defined_in": "core/forms.py", "definition_line": 12}
  ]
}
