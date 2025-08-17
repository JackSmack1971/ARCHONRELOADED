# AGENTS.md: AI Collaboration Guide

This document provides essential context for AI models interacting with this project. Adhering to these guidelines will ensure consistency, maintain code quality, and optimize agent performance for the ARCHON RELOADED platform.

It is Sunday, August 17, 2025. This guide is optimized for clarity, efficiency, and maximum utility for modern AI coding agents like OpenAI's Codex, GitHub Copilot Workspace, and Claude.

## 1. Project Overview & Purpose

*   **Primary Goal:** ARCHON RELOADED is a next-generation microservices-based AI development platform that integrates with AI coding tools through the Model Context Protocol (MCP). It provides intelligent knowledge management, real-time collaboration, and RAG (Retrieval-Augmented Generation) capabilities for AI-powered development workflows.
*   **Business Domain:** AI Development Tools, Developer Productivity, Knowledge Management, AI-Assisted Software Engineering
*   **Key Features:** 
    - MCP integration with Claude Code, Cursor, and Windsurf
    - Real-time knowledge base management with vector search
    - Project and task management with AI agent collaboration
    - Document processing and RAG pipeline with parallel processing
    - WebSocket-based real-time updates and collaboration

## 2. Core Technologies & Stack

*   **Languages:** Python 3.12+, TypeScript 5.x, JavaScript ES2023
*   **Frameworks & Runtimes:** 
    - Backend: FastAPI + Socket.IO, PydanticAI agents
    - Frontend: React 18.x + Vite + TypeScript
    - MCP: HTTP-based MCP protocol server
    - Node.js 20.x (for frontend tooling)
*   **Databases:** 
    - Supabase (PostgreSQL with pgvector extension for embeddings)
    - Redis (for caching and real-time features)
*   **Key Libraries/Dependencies:** 
    - Backend: `uv` (package management), `fastapi`, `socket.io`, `pydantic-ai`, `supabase-py`, `openai`
    - Frontend: `vite`, `tailwindcss`, `@types/react`, `socket.io-client`, `vitest`
    - Testing: `pytest` (Python), `vitest` (TypeScript), `playwright` (E2E)
*   **Package Manager:** `uv` (Python), `npm` (JavaScript/TypeScript)
*   **Platforms:** Linux containers (Docker), Kubernetes-ready, Web browsers

## 3. Architectural Patterns & Structure

*   **Overall Architecture:** Cloud-native microservices architecture with clear separation of concerns. Each service has a dedicated responsibility: UI (React), API (FastAPI), MCP integration, and AI agents. Services communicate via HTTP APIs and WebSocket for real-time features.
*   **Directory Structure Philosophy:**
    *   `/python`: All Python backend services and shared code
        *   `/src`: Source code organized by service (server, mcp, agents)
        *   `/tests`: Comprehensive test suite with container-specific tests
        *   `/migration`: Database migration scripts
    *   `/archon-ui-main`: React frontend application
        *   `/src`: Frontend source organized by feature and component type
        *   `/test`: Vitest test suite with comprehensive mocking
    *   `/docs`: Docusaurus documentation site
    *   `/docker-compose.yml`: Multi-container orchestration
*   **Module Organization:** 
    - Backend uses FastAPI service layer pattern with dependency injection
    - Frontend uses component-based architecture with feature organization
    - Services communicate through well-defined HTTP APIs and WebSocket events
*   **Common Patterns & Idioms:**
    *   **Async/Await:** Extensive use of async patterns for I/O operations and real-time features
    *   **Dependency Injection:** FastAPI's dependency system for service management
    *   **Type Safety:** Strict TypeScript and Pydantic models for API contracts
    *   **Real-time Updates:** Socket.IO for live collaboration and progress tracking
    *   **Microservices:** Each service runs in isolated containers with health checks

## 4. Coding Conventions & Style Guide

*   **Formatting:** 
    - Python: Follow PEP 8, use Black formatter (line length: 100 characters)
    - TypeScript/JavaScript: Prettier with 2-space indentation, single quotes, trailing commas
    - No semicolons in TypeScript unless required
*   **Naming Conventions:** 
    - Python: `snake_case` for variables/functions, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
    - TypeScript: `camelCase` for variables/functions, `PascalCase` for types/interfaces/components, `SCREAMING_SNAKE_CASE` for constants
    - Files: `snake_case.py` for Python, `PascalCase.tsx` for React components, `camelCase.ts` for utilities
*   **API Design:** 
    - RESTful endpoints with consistent HTTP methods and status codes
    - Pydantic models for request/response validation
    - OpenAPI documentation auto-generated from FastAPI decorators
    - WebSocket events follow structured naming: `{domain}:{action}` (e.g., `task:updated`)
*   **Error Handling:** 
    - Python: Use FastAPI's HTTPException for API errors, custom exceptions for business logic
    - TypeScript: Use Result types for service layer, proper error boundaries in React
    - Structured logging with consistent error formatting across services
*   **Documentation Style:** 
    - Python: Google-style docstrings with type hints
    - TypeScript: JSDoc comments for complex functions and interfaces
    - API endpoints documented with FastAPI's automatic OpenAPI generation

## 5. Key Files & Entrypoints

*   **Main Entrypoints:** 
    - Backend API: `python/src/server/main.py` (FastAPI with Socket.IO)
    - MCP Server: `python/src/mcp_server.py` (HTTP-based MCP protocol)
    - Agents Service: `python/src/agents/server.py` (PydanticAI agents)
    - Frontend: `archon-ui-main/src/main.tsx` (React with Vite)
*   **Configuration:** 
    - Backend: `python/pyproject.toml` (dependencies), `.env` file (environment variables)
    - Frontend: `archon-ui-main/package.json`, `vite.config.ts`, `vitest.config.ts`
    - Containers: `docker-compose.yml` for local development
    - Database: `migration/complete_setup.sql` for schema initialization
*   **CI/CD Pipeline:** No GitHub Actions detected yet (fresh project), but structure supports standard CI/CD patterns

## 6. Development & Testing Workflow

*   **Local Development Environment:** 
    1. Install `uv` for Python dependency management
    2. Run `uv sync` in `/python` directory to install Python dependencies
    3. Run `npm install` in `/archon-ui-main` for frontend dependencies
    4. Set up `.env` file with Supabase and OpenAI credentials
    5. Use `docker compose up -d` to start all services locally
*   **Task Configuration:** 
    - Python: `uv run pytest` for testing, `uv run python -m src.server.main` for development
    - Frontend: `npm run dev` (development), `npm run build` (production), `npm run test` (Vitest)
    - Docker: `docker compose logs -f` for debugging, `docker compose restart` for service restarts
*   **Testing:** 
    - **Python**: pytest with container-specific test organization (server/, mcp/, agents/, integration/)
    - **Frontend**: Vitest with comprehensive mocking of Socket.IO and external services
    - **Test Structure**: Independent tests, minimal fixtures, fast execution (<30 seconds total)
    - **Coverage**: Target 80%+ coverage with meaningful test scenarios
*   **CI/CD Process:** 
    - Structure ready for standard pipeline: lint → type check → test → build → deploy
    - Multi-stage Docker builds for production optimization
    - Health checks configured for all services

## 7. Specific Instructions for AI Collaboration

*   **Contribution Guidelines:** 
    - Follow existing code style strictly (Black for Python, Prettier for TypeScript)
    - All new functionality requires corresponding unit tests
    - API changes must maintain backward compatibility or include migration strategy
    - Socket.IO events must be documented and maintain consistent naming patterns
*   **Security:** 
    - Never hardcode secrets or API keys; use environment variables
    - Validate all user inputs on both client and server sides
    - Use proper authentication for MCP connections and API endpoints
    - Sanitize file uploads and validate file types in document processing
*   **Dependencies:** 
    - Python: Use `uv add <package>` and commit updated `uv.lock`
    - Frontend: Use `npm install <package>` and commit updated `package-lock.json`
    - Always specify exact versions for critical dependencies
    - Prefer actively maintained packages with good TypeScript support
*   **Commit Messages & Pull Requests:** 
    - Follow Conventional Commits format: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
    - Include scope when relevant: `feat(mcp): add tool execution logging`
    - Pull requests should be focused and include test coverage
    - Document breaking changes clearly in commit messages
*   **Avoidances/Forbidden Actions:** 
    - **NEVER** use `@ts-expect-error` or `@ts-ignore` to suppress TypeScript errors
    - **DO NOT** create real Socket.IO connections in tests (use mocks)
    - **DO NOT** commit changes to lock files unless adding/updating dependencies
    - **NEVER** expose internal service ports externally without proper authentication
    - **DO NOT** use `any` type in TypeScript; prefer proper type definitions
*   **Debugging Guidance:** 
    - Use `docker compose logs -f <service-name>` to view specific service logs
    - Frontend errors: Check browser console and Network tab for API failures
    - Backend errors: Look for FastAPI error responses and structured logs
    - MCP issues: Verify transport configuration and check client/server logs
*   **Parallel Task Execution:** 
    - Tasks affecting different services can run simultaneously
    - Database migrations should be applied before dependent code changes
    - Frontend and backend tests can run in parallel during CI
*   **Pass/Fail Criteria:** 
    - All tests must pass: `uv run pytest` and `npm run test`
    - TypeScript compilation must succeed: `npm run build`
    - Python linting/formatting: Black and basic PEP 8 compliance
    - Services must start successfully via Docker Compose
*   **Breaking Down Large Work:** 
    - Separate database schema changes into dedicated migrations
    - Frontend changes should be componentized and tested independently
    - API changes should maintain backward compatibility during transitions
    - New MCP tools should be implemented with comprehensive test coverage

---

**Development Status:** This is a fresh project in early development with foundational architecture established. Focus on maintaining clean patterns as the codebase grows.
