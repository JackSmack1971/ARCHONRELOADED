# AGENTS Instructions

## Security Requirements
- NEVER hardcode API keys; use environment variables.
- ALWAYS validate user inputs before processing.
- ALWAYS include timeout and retry logic for external API calls.
- ALWAYS wrap operations in try/except and raise custom exceptions.

## Coding Standards
- Functions must not exceed 30 lines.
- Use async/await for I/O-bound operations.
- Provide type hints and appropriate error handling.
- Write tests for all new code and maintain at least 80% coverage.
