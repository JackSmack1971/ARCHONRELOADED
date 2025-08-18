# Python MCP Server Guidelines for AI Agents

## Project Overview

This is a Python-based Model Context Protocol (MCP) server implementation using the official Python MCP SDK. The project follows FastMCP framework patterns for rapid development while supporting low-level server APIs for advanced use cases.

### Core Technologies
- **Framework**: Python MCP SDK with FastMCP framework
- **Protocol Version**: 2025-06-18 (latest)
- **Python Version**: 3.8+ (recommended 3.11+)
- **Package Manager**: uv (preferred) / pip
- **Transport**: STDIO (local) / Streamable HTTP (cloud)
- **Authentication**: OAuth 2.1 with resource server support

## Development Workflow and Git Requirements

### Git Workflow Constraints
- **CRITICAL**: Do not create new branches - work on current branch only
- **REQUIRED**: Commit all changes using `git add . && git commit -m "message"`
- **REQUIRED**: Check git status after changes to ensure clean worktree
- **FORBIDDEN**: Do not modify or amend existing commits
- **FORBIDDEN**: Do not use git rebase or force push

### File Citations Required
- Use `F:file_path†L<line>` format when referencing specific code lines
- Include terminal output citations using chunk_id for command results
- Cite modified files in summaries using `F:` format
- Always reference AGENTS.md files when following guidelines

### Development Commands
```bash
# Install dependencies with CLI tools
uv add "mcp[cli]"

# Create virtual environment
uv venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Run server in development mode
uv run mcp dev server.py

# Install server for Claude Desktop
uv run mcp install server.py --name "My MCP Server"

# Development with additional dependencies
uv run mcp dev server.py --with pandas --with numpy

# Formatting and linting
uv run ruff format .
uv run ruff check . --fix
uv run pyright

# Testing
uv run pytest
```

## Project Structure

```
python/src/mcp/
├── server/
│   ├── __init__.py
│   ├── main.py            # Server entry point
│   ├── tools/             # Tool implementations
│   │   ├── __init__.py
│   │   ├── data_tools.py  # Data processing tools
│   │   └── api_tools.py   # External API tools
│   ├── resources/         # Resource handlers
│   │   ├── __init__.py
│   │   └── file_resources.py
│   ├── auth/              # Authentication handlers
│   │   ├── __init__.py
│   │   └── token_verifier.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── client/                # Client implementations
│   ├── __init__.py
│   └── test_client.py
├── tests/                 # Test files
│   ├── __init__.py
│   ├── test_server.py
│   └── test_tools.py
├── config/                # Configuration files
│   ├── __init__.py
│   └── settings.py
├── requirements.txt       # Dependencies
├── pyproject.toml        # Project configuration
└── .env.example          # Environment template
```

## FastMCP Framework Guidelines (Recommended)

### Server Creation and Configuration
- **REQUIRED**: Use FastMCP for new server implementations
- **REQUIRED**: Set appropriate debug and log levels for environment
- **REQUIRED**: Configure host and port for production deployment

```python
# ✅ Correct - FastMCP server setup
from mcp.server.fastmcp import FastMCP

# Development configuration
mcp = FastMCP("Development Server", debug=True, log_level="DEBUG")

# Production configuration
mcp = FastMCP(
    "Production Server",
    host="0.0.0.0",      # Allow external connections
    port=8000,
    debug=False,         # Disable debug in production
    log_level="INFO",
    stateless_http=True  # Required for cloud deployment
)
```

### Tool Definition Best Practices
- **REQUIRED**: Include descriptive docstrings for all tools
- **REQUIRED**: Use proper type hints for parameters and return values
- **REQUIRED**: Validate all input parameters
- **PREFERRED**: Use async for I/O operations
- **PREFERRED**: Implement progress reporting for long-running tasks

```python
# ✅ Correct - Tool definition pattern
from mcp.server.fastmcp import FastMCP, Context

@mcp.tool()
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        Sum of a and b
    """
    return a + b

@mcp.tool()
async def fetch_data(url: str, ctx: Context) -> dict:
    """Fetch data from external API with progress reporting.
    
    Args:
        url: API endpoint URL
        ctx: MCP context for progress reporting
        
    Returns:
        API response data
    """
    # REQUIRED: Validate input
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL format")
    
    await ctx.info(f"Fetching data from {url}")
    
    try:
        # Implementation with proper error handling
        response = await fetch_api_data(url)
        await ctx.info("Data fetched successfully")
        return response
    except Exception as e:
        await ctx.error(f"Failed to fetch data: {str(e)}")
        raise
```

### Resource Definition Patterns
- **REQUIRED**: Validate resource URIs and parameters
- **REQUIRED**: Implement proper error handling
- **PREFERRED**: Use static resources for configuration data
- **PREFERRED**: Use dynamic resources for file system access

```python
# ✅ Correct - Resource definition patterns
@mcp.resource("config://settings")
def get_settings() -> str:
    """Return application configuration."""
    return json.dumps({
        "theme": "dark",
        "version": "1.0",
        "debug": False
    })

@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """Read document by name with validation.
    
    Args:
        name: Document name (alphanumeric, hyphens, underscores only)
        
    Returns:
        Document content
    """
    # REQUIRED: Validate input parameters
    if not name.replace("_", "").replace("-", "").isalnum():
        raise ValueError("Invalid document name format")
    
    # REQUIRED: Prevent path traversal
    if ".." in name or "/" in name or "\\" in name:
        raise ValueError("Invalid characters in document name")
    
    document_path = f"documents/{name}.txt"
    if not os.path.exists(document_path):
        raise FileNotFoundError(f"Document {name} not found")
    
    with open(document_path, 'r', encoding='utf-8') as f:
        return f.read()
```

### Context and Progress Reporting
- **REQUIRED**: Use Context for progress reporting in long-running operations
- **REQUIRED**: Report meaningful progress messages
- **PREFERRED**: Include structured progress data

```python
# ✅ Correct - Progress reporting pattern
@mcp.tool()
async def process_batch(items: list[str], ctx: Context) -> dict:
    """Process batch of items with progress reporting.
    
    Args:
        items: List of items to process
        ctx: MCP context for progress reporting
        
    Returns:
        Processing results with statistics
    """
    total_items = len(items)
    processed = []
    failed = []
    
    await ctx.info(f"Starting batch processing of {total_items} items")
    
    for i, item in enumerate(items):
        try:
            # Report progress
            progress = (i + 1) / total_items
            await ctx.report_progress(
                progress=progress,
                total=1.0,
                message=f"Processing item {i + 1}/{total_items}: {item}"
            )
            
            result = await process_single_item(item)
            processed.append(result)
            await ctx.debug(f"Successfully processed item {i + 1}")
            
        except Exception as e:
            await ctx.warning(f"Failed to process item {i + 1}: {str(e)}")
            failed.append({"item": item, "error": str(e)})
    
    await ctx.info(f"Batch processing completed: {len(processed)} success, {len(failed)} failed")
    
    return {
        "processed_count": len(processed),
        "failed_count": len(failed),
        "success_rate": len(processed) / total_items if total_items > 0 else 0,
        "results": processed,
        "failures": failed
    }
```

## Low-Level Server API (Advanced Use Cases)

### Server Initialization with Lifespan Management
- **REQUIRED**: Use lifespan context for resource management
- **REQUIRED**: Properly handle startup and shutdown
- **REQUIRED**: Implement cleanup in finally blocks

```python
# ✅ Correct - Low-level server with lifespan management
import asyncio
from contextlib import asynccontextmanager
from mcp.server.lowlevel import Server
from mcp.server import types
import mcp.server.stdio

@asynccontextmanager
async def server_lifespan(_server: Server):
    """Manage server startup and shutdown resources."""
    # Initialize resources
    db = await Database.connect()
    cache = await RedisCache.connect()
    
    try:
        yield {
            "db": db,
            "cache": cache,
            "startup_time": datetime.now()
        }
    finally:
        # REQUIRED: Cleanup resources
        await db.disconnect()
        await cache.disconnect()

server = Server("advanced-server", lifespan=server_lifespan)
```

### Handler Registration with Output Schemas
- **REQUIRED**: Define input and output schemas for all tools
- **REQUIRED**: Return structured data matching output schema
- **PREFERRED**: Use type hints that match schema definitions

```python
# ✅ Correct - Handler with structured output
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools with proper schema definition."""
    return [
        types.Tool(
            name="query_database",
            description="Execute database query and return results",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 1000
                    }
                },
                "required": ["query"]
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "rows": {
                        "type": "array",
                        "description": "Query results",
                        "items": {"type": "object"}
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of rows returned"
                    },
                    "execution_time_ms": {
                        "type": "number",
                        "description": "Query execution time in milliseconds"
                    }
                },
                "required": ["rows", "count", "execution_time_ms"]
            }
        )
    ]

@server.call_tool()
async def handle_tool_call(name: str, arguments: dict) -> dict:
    """Handle tool calls with structured output matching schema."""
    if name == "query_database":
        # Access lifespan context
        ctx = server.request_context
        db = ctx.lifespan_context["db"]
        
        query = arguments["query"]
        limit = arguments.get("limit", 100)
        
        # REQUIRED: Validate input
        if not query.strip():
            raise ValueError("Query cannot be empty")
        
        start_time = time.time()
        rows = await db.execute_query(query, limit=limit)
        execution_time = (time.time() - start_time) * 1000
        
        # Return structured data matching output schema
        return {
            "rows": rows,
            "count": len(rows),
            "execution_time_ms": round(execution_time, 2)
        }
    
    raise ValueError(f"Unknown tool: {name}")
```

## Client Development

### STDIO Client Pattern
- **REQUIRED**: Use proper error handling for client connections
- **REQUIRED**: Initialize session before use
- **PREFERRED**: Use context managers for resource cleanup

```python
# ✅ Correct - STDIO client implementation
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_mcp_client():
    """Standard MCP client connection pattern."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server", "main.py", "stdio"],
        env={
            "UV_INDEX": os.environ.get("UV_INDEX", ""),
            "PYTHONPATH": os.environ.get("PYTHONPATH", "")
        }
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # REQUIRED: Initialize connection
                await session.initialize()
                
                # List and use resources
                resources = await session.list_resources()
                if resources.resources:
                    resource_uri = resources.resources[0].uri
                    content = await session.read_resource(resource_uri)
                    print(f"Resource content: {content}")
                
                # Call tools
                tools = await session.list_tools()
                if tools.tools:
                    tool_name = tools.tools[0].name
                    result = await session.call_tool(tool_name, {"param": "value"})
                    print(f"Tool result: {result}")
                    
    except Exception as e:
        print(f"Client error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(run_mcp_client())
```

### HTTP Client with Authentication
- **REQUIRED**: Implement secure token storage
- **REQUIRED**: Handle OAuth flow properly
- **PREFERRED**: Use environment variables for client configuration

```python
# ✅ Correct - HTTP client with OAuth authentication
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.auth import OAuthClientProvider, OAuthClientMetadata
from pydantic import AnyUrl

class SecureTokenStorage:
    """Secure token storage implementation."""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
    
    async def save_token(self, token_data: dict) -> None:
        """Save token data securely."""
        # REQUIRED: Implement secure storage (encryption, etc.)
        pass
    
    async def load_token(self) -> dict | None:
        """Load token data securely."""
        # REQUIRED: Implement secure retrieval
        pass

async def run_authenticated_client():
    """HTTP client with OAuth authentication."""
    oauth_auth = OAuthClientProvider(
        server_url="http://localhost:8001",
        client_metadata=OAuthClientMetadata(
            client_name="My MCP Client",
            redirect_uris=[AnyUrl("http://localhost:3000/callback")],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            scope="user data.read"
        ),
        storage=SecureTokenStorage("/secure/path/tokens"),
        redirect_handler=handle_oauth_redirect,
        callback_handler=handle_oauth_callback
    )

    async with streamablehttp_client(
        "http://localhost:8001/mcp", 
        auth=oauth_auth
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Use authenticated session
            tools = await session.list_tools()
            # ... rest of client logic
```

## Authentication and Security

### OAuth 2.1 Resource Server Implementation
- **REQUIRED**: Implement proper token verification
- **REQUIRED**: Validate token signatures and expiration
- **REQUIRED**: Check required scopes for protected resources
- **REQUIRED**: Implement rate limiting

```python
# ✅ Correct - Production OAuth implementation
from mcp.server.auth.provider import TokenVerifier, AccessToken
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
import jwt
import time

class ProductionTokenVerifier(TokenVerifier):
    """Production-grade OAuth token verification."""
    
    def __init__(self, jwt_secret: str, issuer: str):
        self.jwt_secret = jwt_secret
        self.issuer = issuer
        self.rate_limiter = {}  # Implement proper rate limiting
    
    async def verify_token(self, token: str) -> AccessToken | None:
        """Verify OAuth token with comprehensive validation."""
        try:
            # REQUIRED: Verify token signature and decode
            payload = jwt.decode(
                token, 
                self.jwt_secret, 
                algorithms=["HS256"],
                issuer=self.issuer
            )
            
            # REQUIRED: Check expiration
            if payload.get("exp", 0) < time.time():
                return None
            
            # REQUIRED: Validate required fields
            sub = payload.get("sub")
            scopes = payload.get("scopes", [])
            
            if not sub:
                return None
            
            # REQUIRED: Rate limiting check
            if await self._is_rate_limited(sub):
                return None
            
            return AccessToken(
                sub=sub,
                scopes=scopes,
                exp=payload.get("exp"),
                iat=payload.get("iat")
            )
            
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            # Log security-related errors
            logger.warning(f"Token verification error: {str(e)}")
            return None
    
    async def _is_rate_limited(self, subject: str) -> bool:
        """Implement rate limiting logic."""
        # REQUIRED: Implement actual rate limiting
        current_time = time.time()
        # ... rate limiting implementation
        return False

# Server with authentication
mcp = FastMCP(
    "Secure Server",
    token_verifier=ProductionTokenVerifier(
        jwt_secret=os.environ["JWT_SECRET"],
        issuer=os.environ["JWT_ISSUER"]
    ),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(os.environ["ISSUER_URL"]),
        resource_server_url=AnyHttpUrl(os.environ["RESOURCE_SERVER_URL"]),
        required_scopes=["user", "data.read"]
    )
)
```

### Security Best Practices
- **NEVER** hard-code credentials in source code
- **ALWAYS** use environment variables for sensitive configuration
- **REQUIRED**: Validate and sanitize all external input
- **REQUIRED**: Use HTTPS in production deployments
- **REQUIRED**: Implement proper error handling without exposing internal details

```python
# ✅ Correct - Secure configuration pattern
import os
from typing import Optional

class SecurityConfig:
    """Secure configuration management."""
    
    def __init__(self):
        # REQUIRED: Load from environment
        self.jwt_secret = self._get_required_env("JWT_SECRET")
        self.database_url = self._get_required_env("DATABASE_URL")
        self.api_key = self._get_required_env("API_KEY")
        
        # Optional with defaults
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.log_level = os.environ.get("LOG_LEVEL", "INFO")
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable with validation."""
        value = os.environ.get(key)
        if not value:
            raise ValueError(f"Required environment variable {key} not set")
        return value
    
    @staticmethod
    def validate_input(data: str, max_length: int = 1000) -> str:
        """Validate and sanitize input data."""
        if not data or not data.strip():
            raise ValueError("Input cannot be empty")
        
        if len(data) > max_length:
            raise ValueError(f"Input too long (max {max_length} characters)")
        
        # Remove potentially dangerous characters
        sanitized = data.strip()
        # Add more sanitization as needed
        
        return sanitized
```

## Error Handling and Logging

### Exception Management Patterns
- **REQUIRED**: Use structured logging with appropriate levels
- **REQUIRED**: Handle specific exception types appropriately
- **REQUIRED**: Never expose internal errors to clients
- **PREFERRED**: Implement retry logic for transient failures

```python
# ✅ Correct - Comprehensive error handling
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

@mcp.tool()
async def robust_data_processor(data: str, ctx: Context) -> Dict[str, Any]:
    """Tool with comprehensive error handling and logging."""
    try:
        # REQUIRED: Input validation
        validated_data = SecurityConfig.validate_input(data, max_length=5000)
        
        await ctx.info(f"Processing {len(validated_data)} characters of data")
        
        # Main processing logic
        result = await process_data_with_retry(validated_data)
        
        await ctx.info("Data processing completed successfully")
        logger.info(f"Successfully processed data of length {len(validated_data)}")
        
        return {
            "status": "success",
            "result": result,
            "processed_length": len(validated_data)
        }
        
    except ValueError as e:
        # Client error - safe to expose message
        error_msg = f"Invalid input: {str(e)}"
        await ctx.error(error_msg)
        logger.warning(f"Validation error: {str(e)}")
        raise ValueError(error_msg)
    
    except (ConnectionError, TimeoutError) as e:
        # Network error - retry logic
        logger.exception(f"Network error in data_processor: {str(e)}")
        await ctx.warning("Network error occurred, retrying...")
        
        try:
            # REQUIRED: Implement retry with backoff
            result = await process_data_with_retry(validated_data, retry_count=3)
            await ctx.info("Retry successful")
            return {"status": "success", "result": result}
        except Exception:
            await ctx.error("Failed after retries")
            raise ConnectionError("Service temporarily unavailable")
    
    except Exception as e:
        # Unknown error - log details but don't expose
        logger.exception(f"Unexpected error in robust_data_processor: {str(e)}")
        await ctx.error("Internal server error occurred")
        raise RuntimeError("Internal server error")

async def process_data_with_retry(data: str, retry_count: int = 1) -> str:
    """Process data with exponential backoff retry logic."""
    import asyncio
    
    for attempt in range(retry_count + 1):
        try:
            # Actual processing logic here
            return f"Processed: {data[:50]}..."
        except (ConnectionError, TimeoutError) as e:
            if attempt == retry_count:
                raise
            
            wait_time = 2 ** attempt  # Exponential backoff
            logger.info(f"Retry attempt {attempt + 1} after {wait_time}s")
            await asyncio.sleep(wait_time)
```

### Progress and Status Reporting
- **REQUIRED**: Report progress for operations longer than 5 seconds
- **REQUIRED**: Include meaningful status messages
- **PREFERRED**: Report estimated completion time when possible

```python
# ✅ Correct - Detailed progress reporting
@mcp.tool()
async def comprehensive_analyzer(
    dataset_url: str, 
    analysis_type: str, 
    ctx: Context
) -> Dict[str, Any]:
    """Comprehensive data analysis with detailed progress reporting."""
    
    analysis_steps = [
        "Downloading dataset",
        "Validating data format",
        "Preprocessing data",
        "Running analysis",
        "Generating report"
    ]
    
    results = {}
    start_time = time.time()
    
    await ctx.info(f"Starting {analysis_type} analysis on dataset: {dataset_url}")
    
    for i, step in enumerate(analysis_steps):
        step_start = time.time()
        
        try:
            # Report step progress
            step_progress = i / len(analysis_steps)
            await ctx.report_progress(
                progress=step_progress,
                total=1.0,
                message=f"Step {i + 1}/{len(analysis_steps)}: {step}"
            )
            
            # Execute step
            if step == "Downloading dataset":
                data = await download_with_progress(dataset_url, ctx)
                results["data_size"] = len(data)
            elif step == "Validating data format":
                validation_result = await validate_dataset(data)
                results["validation"] = validation_result
            # ... other steps
            
            step_time = time.time() - step_start
            await ctx.debug(f"Completed '{step}' in {step_time:.2f}s")
            
        except Exception as e:
            await ctx.error(f"Failed at step '{step}': {str(e)}")
            raise
    
    total_time = time.time() - start_time
    await ctx.info(f"Analysis completed in {total_time:.2f}s")
    
    return {
        "analysis_type": analysis_type,
        "execution_time": total_time,
        "results": results,
        "status": "completed"
    }

async def download_with_progress(url: str, ctx: Context) -> bytes:
    """Download with progress reporting."""
    # Implementation with progress updates
    # await ctx.report_progress(...) at regular intervals
    pass
```

## Testing and Development

### Testing Patterns
- **REQUIRED**: Test all tools and resources
- **REQUIRED**: Mock external dependencies
- **PREFERRED**: Use pytest with async support
- **PREFERRED**: Test error conditions and edge cases

```python
# ✅ Correct - Comprehensive testing pattern
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from mcp.server.fastmcp import FastMCP, Context

@pytest.fixture
async def test_server():
    """Create test server instance with mocked dependencies."""
    mcp = FastMCP("Test Server", debug=True)
    
    @mcp.tool()
    async def test_tool(input_data: str, ctx: Context) -> str:
        """Test tool for unit testing."""
        await ctx.info(f"Processing: {input_data}")
        return f"Processed: {input_data}"
    
    @mcp.resource("test://config/{name}")
    def test_resource(name: str) -> str:
        """Test resource for unit testing."""
        return f"Config for {name}"
    
    return mcp

@pytest.mark.asyncio
async def test_tool_success(test_server):
    """Test successful tool execution."""
    # Mock context
    mock_ctx = AsyncMock(spec=Context)
    
    # Call tool directly (testing business logic)
    result = await test_server._tools["test_tool"]["func"]("test_input", mock_ctx)
    
    # Verify results
    assert result == "Processed: test_input"
    mock_ctx.info.assert_called_once_with("Processing: test_input")

@pytest.mark.asyncio
async def test_tool_validation_error(test_server):
    """Test tool input validation."""
    mock_ctx = AsyncMock(spec=Context)
    
    # Test with invalid input
    with pytest.raises(ValueError):
        await test_server._tools["test_tool"]["func"]("", mock_ctx)

@pytest.mark.asyncio
@patch('external_service.api_call')
async def test_external_api_integration(mock_api_call, test_server):
    """Test integration with external APIs."""
    # Mock external API response
    mock_api_call.return_value = {"status": "success", "data": "test_data"}
    
    # Test tool that uses external API
    result = await call_tool_with_external_api("test_input")
    
    # Verify API was called correctly
    mock_api_call.assert_called_once()
    assert result["status"] == "success"

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling and recovery."""
    with patch('external_service.failing_call', side_effect=ConnectionError("Network error")):
        with pytest.raises(ConnectionError):
            await tool_with_retry_logic("test_input")

# Integration test
@pytest.mark.asyncio
async def test_full_server_workflow():
    """Test complete server workflow end-to-end."""
    # This would test actual MCP protocol communication
    pass
```

### Pre-commit and Code Quality
- **REQUIRED**: Use ruff for formatting and linting
- **REQUIRED**: Use pyright for type checking
- **PREFERRED**: Set up pre-commit hooks for consistency

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/microsoft/pyright
    rev: v1.1.338
    hooks:
      - id: pyright
```

## Performance Optimization

### Async Best Practices
- **REQUIRED**: Use async/await for all I/O operations
- **REQUIRED**: Implement connection pooling for external services
- **PREFERRED**: Use asyncio.gather for parallel operations
- **PREFERRED**: Set appropriate timeouts

```python
# ✅ Correct - Async optimization patterns
import asyncio
import aiohttp
from typing import List, Dict, Any

class OptimizedMCPServer:
    """MCP server with performance optimizations."""
    
    def __init__(self):
        self.http_session = None
        self.db_pool = None
    
    async def startup(self):
        """Initialize connection pools."""
        # HTTP connection pool
        connector = aiohttp.TCPConnector(
            limit=100,          # Total connection pool size
            limit_per_host=30,  # Per-host connection limit
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(
            total=30.0,         # Total timeout
            sock_read=10.0,     # Socket read timeout
            sock_connect=5.0    # Socket connect timeout
        )
        
        self.http_session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        
        # Database connection pool
        self.db_pool = await create_db_pool(
            min_size=5,
            max_size=20,
            command_timeout=10.0
        )
    
    async def shutdown(self):
        """Cleanup connection pools."""
        if self.http_session:
            await self.http_session.close()
        if self.db_pool:
            await self.db_pool.close()

@mcp.tool()
async def parallel_data_fetcher(urls: List[str], ctx: Context) -> Dict[str, Any]:
    """Fetch data from multiple URLs in parallel."""
    
    async def fetch_single_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Fetch data from single URL with error handling."""
        try:
            async with session.get(url) as response:
                data = await response.json()
                return {"url": url, "status": "success", "data": data}
        except Exception as e:
            return {"url": url, "status": "error", "error": str(e)}
    
    # REQUIRED: Limit concurrent operations
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests
    
    async def fetch_with_semaphore(url: str) -> Dict[str, Any]:
        async with semaphore:
            return await fetch_single_url(server.http_session, url)
    
    await ctx.info(f"Fetching data from {len(urls)} URLs in parallel")
    
    # Execute all requests in parallel
    results = await asyncio.gather(
        *[fetch_with_semaphore(url) for url in urls],
        return_exceptions=True
    )
    
    # Process results
    successful = [r for r in results if isinstance(r, dict) and r.get("status") == "success"]
    failed = [r for r in results if isinstance(r, dict) and r.get("status") == "error"]
    
    await ctx.info(f"Completed: {len(successful)} success, {len(failed)} failed")
    
    return {
        "total_urls": len(urls),
        "successful": len(successful),
        "failed": len(failed),
        "results": results
    }
```

### Memory Management
- **REQUIRED**: Stream large datasets instead of loading into memory
- **REQUIRED**: Clean up resources in finally blocks
- **PREFERRED**: Use generators for large data processing

```python
# ✅ Correct - Memory-efficient data processing
@mcp.tool()
async def stream_processor(data_source: str, ctx: Context) -> Dict[str, Any]:
    """Process large datasets efficiently with streaming."""
    
    total_processed = 0
    total_size = 0
    error_count = 0
    
    try:
        # Stream processing for large datasets
        async for batch in stream_data_batches(data_source, batch_size=1000):
            try:
                # Process in chunks to manage memory
                processed_batch = await process_batch_efficiently(batch)
                
                batch_size = len(processed_batch)
                total_processed += batch_size
                total_size += sum(len(str(item)) for item in processed_batch)
                
                # Report progress periodically
                if total_processed % 5000 == 0:
                    await ctx.info(f"Processed {total_processed:,} records")
                
                # Memory cleanup for large batches
                del processed_batch
                del batch
                
            except Exception as e:
                error_count += 1
                await ctx.warning(f"Error processing batch: {str(e)}")
                if error_count > 10:  # Circuit breaker
                    raise RuntimeError("Too many processing errors")
    
    except Exception as e:
        await ctx.error(f"Stream processing failed: {str(e)}")
        raise
    
    finally:
        # Cleanup any remaining resources
        await cleanup_streaming_resources()
    
    return {
        "total_processed": total_processed,
        "total_size_bytes": total_size,
        "error_count": error_count,
        "status": "completed"
    }

async def stream_data_batches(source: str, batch_size: int):
    """Generator for streaming data in batches."""
    # Implementation that yields batches without loading entire dataset
    pass
```

## Environment Configuration and Deployment

### Environment Variables and Configuration
- **REQUIRED**: Use environment variables for all configuration
- **REQUIRED**: Validate required environment variables at startup
- **PREFERRED**: Use .env files for local development

```python
# ✅ Correct - Environment configuration
import os
from typing import Optional
from pydantic import BaseSettings, AnyHttpUrl

class MCPSettings(BaseSettings):
    """MCP server configuration with validation."""
    
    # Server configuration
    server_name: str = "MCP Server"
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
    
    # Database configuration
    database_url: str
    redis_url: Optional[str] = None
    
    # Authentication
    jwt_secret: str
    jwt_issuer: str
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    
    # External APIs
    api_base_url: AnyHttpUrl
    api_key: str
    api_timeout: float = 30.0
    
    # Performance
    max_concurrent_requests: int = 100
    connection_pool_size: int = 20
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Load and validate configuration
settings = MCPSettings()

# Create server with configuration
mcp = FastMCP(
    settings.server_name,
    host=settings.host,
    port=settings.port,
    debug=settings.debug,
    log_level=settings.log_level
)
```

### Production Deployment Checklist
- [ ] **Environment**: Set `debug=False` and appropriate log levels
- [ ] **Security**: Enable HTTPS, validate OAuth tokens, sanitize inputs
- [ ] **Monitoring**: Implement health checks and error tracking
- [ ] **Performance**: Configure connection pooling and timeouts
- [ ] **Scaling**: Use stateless HTTP for horizontal scaling
- [ ] **Logging**: Set up structured logging with appropriate levels
- [ ] **Secrets**: Use secure secret management (not environment variables in production)

```python
# ✅ Correct - Production deployment configuration
from mcp.server.fastmcp import FastMCP

# Production server setup
mcp = FastMCP(
    "Production MCP Server",
    stateless_http=True,    # Required for serverless/cloud
    json_response=True,     # Disable SSE for some platforms
    host="0.0.0.0",        # Allow external connections
    port=int(os.environ.get("PORT", 8000)),
    debug=False,
    log_level="INFO"
)

# Health check endpoint
@mcp.tool()
def health_check() -> Dict[str, Any]:
    """Health check endpoint for load balancers."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "server": "mcp-server"
    }

# Graceful shutdown handling
import signal
import sys

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    print("Shutting down gracefully...")
    # Perform cleanup
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

## Known Issues and Mitigations

### Common Issues and Solutions

#### ENOENT Errors on macOS
- **CAUSE**: Python path issues after Homebrew upgrades
- **SOLUTION**: Rebuild virtual environment

```bash
# Fix for macOS ENOENT errors
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]"
```

#### Connection Timeout Issues
- **USE**: Float timeouts for precise control
- **IMPLEMENT**: Exponential backoff for retries
- **MONITOR**: Connection health with heartbeat

```python
# ✅ Correct - Timeout handling
import asyncio

async def robust_api_call(url: str, timeout: float = 5.5) -> dict:
    """API call with proper timeout handling."""
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=timeout)
    ) as session:
        for attempt in range(3):
            try:
                async with session.get(url) as response:
                    return await response.json()
            except asyncio.TimeoutError:
                if attempt == 2:  # Last attempt
                    raise
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)
```

#### Memory Leaks in Long-Running Servers
- **CLOSE**: Database connections properly in lifespan context
- **CLEAR**: Cached data periodically
- **USE**: Weak references for circular dependencies

## Version Compatibility and Migration

### Current Protocol Version: 2025-06-18
- **REMOVED**: JSON-RPC batching (deprecated from 2025-03-26)
- **NEW**: Structured tool outputs with schema validation
- **ENHANCED**: OAuth security requirements
- **ADDED**: Audio content support

### Migration Guidelines
- **UPDATE**: To latest SDK version regularly
- **REMOVE**: Any JSON-RPC batching code
- **IMPLEMENT**: Structured output schemas for all tools
- **UPGRADE**: OAuth implementation to meet security requirements
- **TEST**: Thoroughly after protocol version updates

### Backward Compatibility
- **MAINTAIN**: Support for clients on older protocol versions when possible
- **DOCUMENT**: Breaking changes in release notes
- **PROVIDE**: Migration scripts for major version updates

## Pull Request Guidelines

### PR Title Format
`[Component] Brief description of changes`

Examples:
- `[Tools] Add database query tool with structured output`
- `[Auth] Implement OAuth 2.1 token verification`
- `[Server] Add health check endpoint for production`

### PR Description Template
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Breaking change
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Security Checklist
- [ ] Input validation implemented
- [ ] No credentials in code
- [ ] Error messages don't expose internals
- [ ] Authentication/authorization tested

## Checklist
- [ ] Code follows project conventions
- [ ] Type hints added for new code
- [ ] Docstrings added for public functions
- [ ] Logging implemented appropriately
- [ ] Error handling implemented
- [ ] Tests pass locally
- [ ] No security vulnerabilities introduced
```

## Additional Resources

- [MCP Official Documentation](https://docs.mcp.dev/)
- [Python MCP SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Framework Guide](https://github.com/modelcontextprotocol/python-sdk/tree/main/src/mcp/server/fastmcp)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)

## Key Reminders for AI Agents

1. **Always commit changes** after modifications using git
2. **Use FastMCP framework** for new server implementations
3. **Implement proper error handling** and input validation
4. **Use async/await** for all I/O operations
5. **Include progress reporting** for long-running tasks
6. **Validate OAuth tokens** properly in production
7. **Test comprehensively** with pytest and mocking
8. **Cite files and terminal outputs** as required
9. **Check AGENTS.md compliance** for all modifications
10. **Use environment variables** for all configuration
