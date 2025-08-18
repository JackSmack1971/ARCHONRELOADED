# Python Services Guidelines for AI Agents

## Service Overview

This directory contains Python-based microservices built with FastAPI, featuring vector database capabilities via Supabase/pgvector and Model Context Protocol (MCP) integrations. Each service is designed to be independently deployable with proper authentication, monitoring, and performance optimization.

## Directory Structure

```
python/src/services/
├── shared/                 # Shared libraries and utilities
│   ├── auth/              # Authentication middleware
│   ├── database/          # Database connection and models
│   ├── vector/            # Vector operations and embeddings
│   └── mcp/              # MCP server utilities
├── api-gateway/          # FastAPI gateway service
├── auth-service/         # Authentication and user management
├── vector-service/       # Vector search and embeddings
├── mcp-server/          # Model Context Protocol server
└── docs/                # Service documentation
```

## Core Technologies

- **Backend Framework**: FastAPI 0.115.12+ with Python 3.11+
- **Database**: Supabase PostgreSQL with pgvector extension
- **Vector Operations**: pgvector with HNSW indexing
- **Authentication**: JWT with OAuth 2.1, Supabase Auth
- **MCP Integration**: Python MCP SDK for AI agent communication
- **Container Runtime**: Docker with multi-stage builds
- **Async Framework**: asyncio with proper async/await patterns

## Development Workflow

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install "fastapi[standard]" "mcp[cli]" supabase python-multipart
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing and Validation
```bash
# Run all tests
pytest tests/ -v --cov=src

# Test specific service
pytest tests/test_vector_service.py -v

# Run linting and formatting
ruff format .
ruff check . --fix
pyright  # Type checking

# Test MCP server
uv run mcp dev server.py
```

## FastAPI Service Standards

### Application Structure
- **Use proper package structure**: Organize with separate modules for routes, models, dependencies, and configuration
- **Install with standard dependencies**: Use `pip install "fastapi[standard]"` for comprehensive FastAPI features
- **Create virtual environments**: Always use isolated Python environments for dependency management
- **Configure settings with Pydantic**: Use `BaseSettings` for environment-based configuration

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    app_name: str = "Python Service"
    database_url: str
    supabase_url: str
    supabase_key: str
    secret_key: str
    openapi_url: str = "/openapi.json"  # Set to "" in production

@lru_cache()
def get_settings():
    return Settings()
```

### Security Implementation
- **Always use HTTPS in production**: Configure SSL/TLS certificates and disable HTTP
- **Implement proper CORS policies**: Configure `CORSMiddleware` with specific allowed origins
- **Validate all user inputs**: Use Pydantic models for request validation and sanitize user content
- **Use dependency injection for authentication**: Centralize auth logic in reusable dependencies
- **Store passwords securely**: Always hash passwords using bcrypt, never store plaintext

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not validate_jwt_token(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_user_from_token(credentials.credentials)
```

### Router Organization
- **Use APIRouter for modular organization**: Group related endpoints with shared configuration
- **Configure router-level dependencies**: Apply common dependencies like authentication at router level
- **Set proper HTTP status codes**: Use appropriate status codes for different response scenarios
- **Add comprehensive documentation**: Include summary, description, and response examples

## Supabase + pgvector Integration

### Database Configuration
- **Enable pgvector extension properly**: Use `create extension if not exists vector with schema extensions;`
- **Verify pgvector version**: Ensure version 0.6+ for accelerated HNSW build speeds
- **Use correct connection strings**: Session pooler (port 5432) for long operations, transaction pooler (port 6543) for short queries
- **Size vector columns appropriately**: Match dimensions to embedding model (384 for gte-small, 1536 for OpenAI)

```python
# Database session management
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### Vector Operations
- **Choose appropriate distance function**: Use `<=>` (cosine) for normalized embeddings, `<#>` (inner product), `<->` (L2)
- **Use HNSW over IVFFlat**: HNSW provides better performance and robustness
- **Create indexes on populated tables**: Never create IVFFlat indexes on empty tables
- **Implement similarity search functions**: Create PL/pgSQL functions for reusable searches

```python
# Vector similarity search via RPC
async def search_similar_documents(
    query_embedding: list[float],
    match_threshold: float = 0.7,
    match_count: int = 5
):
    supabase = get_supabase_client()
    result = await supabase.rpc('match_documents', {
        'query_embedding': query_embedding,
        'match_threshold': match_threshold,
        'match_count': match_count
    })
    return result.data
```

### Row Level Security (RLS)
- **Enable RLS on all user-facing tables**: Use `alter table enable row level security;`
- **Create specific policies for each operation**: Define separate policies for SELECT, INSERT, UPDATE, DELETE
- **Use auth.uid() for user-based access**: Filter rows based on authenticated user
- **Optimize RLS performance**: Wrap JWT functions in SELECT statements for initPlan caching

## MCP Server Development

### Server Configuration
- **Use FastMCP for rapid development**: Leverage the high-level FastMCP framework for quick server creation
- **Configure for production deployment**: Set `debug=False`, appropriate host/port, and logging levels
- **Implement proper authentication**: Use OAuth 2.1 with token verification for secured endpoints
- **Enable stateless HTTP for cloud**: Use `stateless_http=True` for serverless deployments

```python
from mcp.server.fastmcp import FastMCP, Context

# Production MCP server setup
mcp = FastMCP(
    "Vector Search Service",
    host="0.0.0.0",
    port=8001,
    debug=False,
    log_level="INFO",
    stateless_http=True  # For cloud deployment
)
```

### Tool Implementation
- **Provide descriptive docstrings**: All tools must have clear documentation for AI agents
- **Use async for I/O operations**: Implement async tools for database and API calls
- **Report progress for long operations**: Use context reporting for user feedback
- **Validate input parameters**: Always sanitize and validate tool inputs

```python
@mcp.tool()
async def search_knowledge_base(
    query: str, 
    category: str | None = None,
    limit: int = 5,
    ctx: Context
) -> dict:
    """Search the knowledge base using vector similarity.
    
    Args:
        query: Search query to find similar documents
        category: Optional category filter
        limit: Maximum number of results (1-20)
        
    Returns:
        Dict containing search results with similarity scores
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    
    if limit < 1 or limit > 20:
        raise ValueError("Limit must be between 1 and 20")
    
    await ctx.info(f"Searching knowledge base for: {query}")
    
    # Generate embedding for query
    embedding = await generate_embedding(query)
    
    # Search vector database
    results = await search_similar_documents(
        embedding, 
        category_filter=category,
        limit=limit
    )
    
    await ctx.info(f"Found {len(results)} relevant documents")
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }
```

### Resource Management
- **Implement lifespan management**: Use context managers for database connections
- **Close resources properly**: Ensure cleanup in finally blocks or async context managers
- **Cache expensive operations**: Use appropriate caching for embeddings and database queries

## Authentication and Security

### JWT and OAuth Implementation
- **Use Supabase Auth for user management**: Leverage built-in authentication flows
- **Validate JWT tokens properly**: Check signature, expiration, and required claims
- **Implement scope-based authorization**: Use OAuth scopes for fine-grained access control
- **Store secrets securely**: Use environment variables and secure secret management

```python
import jwt
from datetime import datetime, timezone

async def verify_jwt_token(token: str) -> dict | None:
    """Verify JWT token and return user claims."""
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            options={"verify_exp": True}
        )
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            return None
            
        return payload
        
    except jwt.InvalidTokenError:
        return None
```

### API Security
- **Rate limit all endpoints**: Implement request throttling to prevent abuse
- **Validate input schemas**: Use Pydantic models for all request/response validation
- **Sanitize user inputs**: Prevent injection attacks through proper validation
- **Log security events**: Track authentication failures and suspicious activity

## Async Programming Best Practices

### Database Operations
- **Use async SQLAlchemy**: Implement async database sessions for better performance
- **Handle connection pooling**: Configure appropriate pool sizes for your workload
- **Implement proper transaction management**: Use async context managers for transactions
- **Avoid blocking operations**: Use asyncio-compatible libraries for all I/O

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def create_document_with_embedding(
    db: AsyncSession,
    title: str,
    content: str,
    user_id: str
) -> dict:
    """Create document with vector embedding."""
    async with db.begin():
        # Generate embedding
        embedding = await generate_embedding(content)
        
        # Create document
        document = Document(
            title=title,
            content=content,
            user_id=user_id,
            embedding=embedding
        )
        
        db.add(document)
        await db.flush()  # Get ID without committing
        
        # Transaction commits automatically due to context manager
        return {"id": document.id, "title": title}
```

### Background Tasks
- **Use FastAPI BackgroundTasks**: For fire-and-forget operations
- **Implement proper error handling**: Log exceptions in background tasks
- **Avoid shared state**: Use dependency injection for background task resources

```python
from fastapi import BackgroundTasks

async def process_document_embedding(doc_id: int, content: str):
    """Background task to generate and store document embedding."""
    try:
        embedding = await generate_embedding(content)
        await update_document_embedding(doc_id, embedding)
        logger.info(f"Generated embedding for document {doc_id}")
    except Exception as e:
        logger.error(f"Failed to process embedding for document {doc_id}: {e}")

@app.post("/documents/")
async def create_document(
    document: DocumentCreate,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    # Create document first
    doc = await create_document_record(document, current_user.id)
    
    # Process embedding in background
    background_tasks.add_task(
        process_document_embedding,
        doc.id,
        document.content
    )
    
    return doc
```

## Testing Standards

### Test Organization
- **Separate test types**: Unit tests in `tests/unit/`, integration in `tests/integration/`
- **Use pytest fixtures**: Create reusable test data and mock objects
- **Test async code properly**: Use `pytest-asyncio` for async test functions
- **Mock external dependencies**: Use `pytest-mock` for database and API mocking

```python
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

@pytest.fixture
async def test_client():
    """Create test client with dependency overrides."""
    app.dependency_overrides[get_db] = lambda: mock_db_session
    app.dependency_overrides[get_current_user] = lambda: test_user
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_vector_search(test_client):
    """Test vector similarity search endpoint."""
    response = await test_client.post(
        "/search/",
        json={"query": "test query", "limit": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) <= 5
```

### Security Testing
- **Test authentication flows**: Verify token validation and user identification
- **Test authorization**: Ensure proper access control for protected resources
- **Test input validation**: Verify rejection of malformed or malicious inputs
- **Test rate limiting**: Ensure endpoints properly throttle requests

## Error Handling and Logging

### Exception Management
- **Use structured exception handling**: Create custom exception classes for business logic
- **Log errors with context**: Include relevant information for debugging
- **Return appropriate HTTP status codes**: Use FastAPI HTTPException with proper codes
- **Implement graceful degradation**: Provide fallback responses when possible

```python
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class VectorSearchError(Exception):
    """Custom exception for vector search operations."""
    pass

async def safe_vector_search(query_embedding: list[float]) -> list[dict]:
    """Vector search with proper error handling."""
    try:
        results = await search_similar_documents(query_embedding)
        return results
    
    except ConnectionError as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search service temporarily unavailable"
        )
    
    except VectorSearchError as e:
        logger.warning(f"Vector search failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Search error: {str(e)}"
        )
    
    except Exception as e:
        logger.exception("Unexpected error in vector search")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### Monitoring and Observability
- **Implement health checks**: Create endpoints for service health monitoring
- **Use structured logging**: Log in JSON format with correlation IDs
- **Track performance metrics**: Monitor response times and resource usage
- **Set up alerting**: Configure alerts for error rates and performance degradation

## Docker Deployment

### Container Configuration
- **Use multi-stage builds**: Separate dependency installation from runtime
- **Use slim Python images**: Choose `python:3.11-slim` for smaller images
- **Configure proper CMD**: Use uvicorn with correct options for production
- **Set working directory**: Use `/code` as standard working directory

```dockerfile
FROM python:3.11-slim as builder

WORKDIR /code

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /code

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY ./src /code/src
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Run migrations and start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 80 --proxy-headers"]
```

### Environment Configuration
- **Use environment variables**: Configure all settings via environment variables
- **Separate development and production**: Use different configurations for each environment
- **Include health checks**: Add Docker health check commands
- **Set proper resource limits**: Configure memory and CPU limits

## Performance Optimization

### Database Performance
- **Use connection pooling**: Configure appropriate pool sizes for async connections
- **Implement query optimization**: Use proper indexes and avoid N+1 queries
- **Cache frequent queries**: Use Redis or in-memory caching for repeated operations
- **Monitor query performance**: Use EXPLAIN ANALYZE for slow queries

### Vector Operations
- **Optimize embedding generation**: Batch embedding requests when possible
- **Use appropriate index settings**: Configure HNSW parameters for your workload
- **Cache embeddings**: Store and reuse embeddings for identical content
- **Implement query result caching**: Cache similarity search results with TTL

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
async def get_cached_embedding(content: str) -> list[float]:
    """Generate embedding with caching for identical content."""
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # Check cache first
    cached = await redis_client.get(f"embedding:{content_hash}")
    if cached:
        return json.loads(cached)
    
    # Generate new embedding
    embedding = await generate_embedding(content)
    
    # Cache for 1 hour
    await redis_client.setex(
        f"embedding:{content_hash}",
        3600,
        json.dumps(embedding)
    )
    
    return embedding
```

## Code Quality and Standards

### Type Hints and Documentation
- **Use comprehensive type hints**: Type all function parameters and return values
- **Write detailed docstrings**: Follow Google or NumPy docstring format
- **Document complex algorithms**: Explain vector operations and business logic
- **Maintain API documentation**: Keep OpenAPI/Swagger docs current

```python
from typing import Optional, List, Dict, Any

async def process_user_query(
    query: str,
    user_id: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Process user search query with vector similarity.
    
    Args:
        query: User's search query text
        user_id: Authenticated user identifier  
        filters: Optional filters for search results
        limit: Maximum number of results to return
        
    Returns:
        List of matching documents with metadata
        
    Raises:
        ValueError: If query is empty or limit is invalid
        AuthenticationError: If user_id is invalid
    """
    # Implementation here
    pass
```

### Code Organization
- **Follow PEP 8 style guidelines**: Use consistent formatting and naming
- **Organize imports properly**: Group standard library, third-party, and local imports
- **Keep functions focused**: Single responsibility principle for better testing
- **Use dependency injection**: Avoid global state and hard dependencies

## Production Deployment Checklist

### Security Verification
- [ ] **HTTPS enabled**: SSL/TLS certificates configured
- [ ] **Authentication working**: JWT validation and user identification
- [ ] **Authorization implemented**: Role-based access control
- [ ] **Input validation active**: All endpoints validate request data
- [ ] **Secrets secured**: No hardcoded credentials in code
- [ ] **Rate limiting configured**: API throttling in place

### Performance Validation
- [ ] **Database indexes created**: Vector and metadata indexes built
- [ ] **Connection pooling configured**: Appropriate pool sizes set
- [ ] **Caching implemented**: Embedding and query result caching
- [ ] **Monitoring active**: Health checks and metrics collection
- [ ] **Resource limits set**: Docker memory and CPU limits

### Operational Readiness
- [ ] **Logging configured**: Structured logging with appropriate levels
- [ ] **Error tracking enabled**: Exception monitoring and alerting
- [ ] **Backup procedures**: Database backup and recovery tested
- [ ] **Documentation current**: API docs and runbooks updated
- [ ] **Load testing completed**: Performance under expected load verified

## Common Issues and Troubleshooting

### Vector Operations
- **Empty index performance**: Never create IVFFlat indexes on empty tables
- **Dimension mismatches**: Validate embedding dimensions match table schema
- **Slow similarity searches**: Ensure proper indexes and query optimization
- **Memory issues**: Monitor memory usage during large vector operations

### Authentication Problems
- **Token expiration**: Implement proper token refresh mechanisms  
- **CORS issues**: Configure middleware for frontend integration
- **Session persistence**: Handle auth state properly in SPAs
- **Permission errors**: Verify RLS policies and user scopes

### Database Connectivity
- **Connection timeouts**: Use appropriate timeout settings for operations
- **Pool exhaustion**: Monitor connection usage and tune pool sizes
- **Migration failures**: Test schema changes in staging environment
- **Deadlock issues**: Implement proper transaction ordering

### MCP Integration
- **Tool registration failures**: Verify tool schemas and descriptions
- **Resource access errors**: Check authentication and authorization
- **Progress reporting issues**: Implement proper context usage
- **Deployment problems**: Ensure stateless configuration for cloud

For additional troubleshooting, refer to service-specific documentation in the `/docs` directory and monitor application logs for detailed error information.
