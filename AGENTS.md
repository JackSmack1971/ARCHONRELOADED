# AGENTS.md: Comprehensive AI Collaboration Guide for ARCHON RELOADED

This document provides essential context and technical knowledge for AI models interacting with the ARCHON RELOADED platform. Adhering to these guidelines will ensure consistency, maintain code quality, and optimize agent performance across all aspects of the system.

**Current Date:** Sunday, August 17, 2025  
**Optimized for:** OpenAI Codex, Claude, GitHub Copilot Workspace, and other modern AI coding agents  
**Framework Compatibility:** Supports MCP (Model Context Protocol) integration

---

## 1. Project Overview & Architecture

### Primary Mission
ARCHON RELOADED is a next-generation microservices-based AI development platform that integrates with AI coding tools through the Model Context Protocol (MCP). It provides intelligent knowledge management, real-time collaboration, and RAG (Retrieval-Augmented Generation) capabilities for AI-powered development workflows.

### Business Domain
- **Primary:** AI Development Tools & Developer Productivity
- **Secondary:** Knowledge Management & AI-Assisted Software Engineering
- **Tertiary:** Real-time Collaboration & Document Processing

### Core System Features
- **MCP Integration:** Seamless connectivity with Claude Code, Cursor, and Windsurf
- **Knowledge Management:** Real-time knowledge base with vector search capabilities
- **Project Management:** Task and project management with AI agent collaboration
- **Document Processing:** RAG pipeline with parallel processing and embedding generation
- **Real-time Features:** WebSocket-based updates and live collaboration
- **Microservices Architecture:** Independent, scalable services with clear boundaries

### System Architecture Principles
- **Cloud-native:** Container-ready microservices with Kubernetes support
- **Event-driven:** Asynchronous communication via WebSocket and message queues
- **API-first:** RESTful design with comprehensive OpenAPI documentation
- **Type-safe:** Full TypeScript and Pydantic model validation
- **Scalable:** Horizontal scaling with proper load balancing and caching

---

## 2. Technology Stack & Dependencies

### Core Technologies
- **Backend Languages:** Python 3.12+ (primary), TypeScript 5.x, JavaScript ES2023
- **Frontend Framework:** React 18.x with TypeScript and modern hooks
- **Build Tools:** Vite 6.x for frontend, uv for Python package management
- **Runtime Environments:** Node.js 20.x, Python 3.12+

### Framework Stack
- **Backend API:** FastAPI with Socket.IO for real-time features
- **AI Agents:** PydanticAI for intelligent agent development
- **MCP Protocol:** HTTP-based MCP server implementation
- **Frontend Build:** Vite + TypeScript + React with hot module replacement
- **Documentation:** Docusaurus for comprehensive project documentation

### Database & Storage
- **Primary Database:** Supabase (PostgreSQL with pgvector extension)
- **Vector Storage:** pgvector for embeddings and similarity search
- **Caching Layer:** Redis for session management and real-time features
- **File Storage:** Supabase Storage for document and media assets

### Container & Orchestration
- **Containerization:** Docker with multi-stage builds
- **Orchestration:** Docker Compose for development, Kubernetes-ready for production
- **Service Mesh:** Internal communication via HTTP/WebSocket APIs
- **Load Balancing:** nginx or cloud load balancer for production

### Package Management
- **Python:** `uv` (modern, fast package manager)
- **JavaScript/TypeScript:** `npm` (consistent with Node.js ecosystem)
- **Container:** Docker with optimized layer caching

---

## 3. Project Structure & Organization

### Repository Architecture
```
ARCHON-RELOADED/
├── python/                     # Backend services (Python)
│   ├── src/
│   │   ├── server/            # FastAPI main application
│   │   │   ├── main.py        # Server entry point
│   │   │   ├── routes/        # API route handlers
│   │   │   ├── services/      # Business logic layer
│   │   │   ├── models/        # Pydantic data models
│   │   │   └── config/        # Configuration management
│   │   ├── mcp/               # MCP server implementation
│   │   │   ├── server.py      # MCP protocol server
│   │   │   ├── tools/         # MCP tool definitions
│   │   │   └── handlers/      # Request handlers
│   │   ├── agents/            # PydanticAI agent services
│   │   │   ├── server.py      # Agent service entry
│   │   │   ├── agents/        # Individual agent definitions
│   │   │   ├── tools/         # Agent tool implementations
│   │   │   └── workflows/     # Multi-agent workflows
│   │   └── shared/            # Shared utilities and types
│   ├── tests/                 # Comprehensive test suite
│   │   ├── server/            # API server tests
│   │   ├── mcp/               # MCP protocol tests
│   │   ├── agents/            # Agent behavior tests
│   │   └── integration/       # End-to-end tests
│   ├── migration/             # Database schema migrations
│   └── pyproject.toml         # Python dependencies & config
├── archon-ui-main/            # Frontend application (React)
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── atoms/         # Basic components (buttons, inputs)
│   │   │   ├── molecules/     # Composite components (forms, cards)
│   │   │   └── organisms/     # Complex components (layouts, dashboards)
│   │   ├── features/          # Feature-specific components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API communication layer
│   │   ├── stores/            # State management (Redux/Zustand)
│   │   ├── types/             # TypeScript type definitions
│   │   ├── utils/             # Utility functions
│   │   └── main.tsx           # Application entry point
│   ├── test/                  # Frontend test suite
│   ├── public/                # Static assets
│   ├── package.json           # Dependencies & scripts
│   ├── vite.config.ts         # Vite build configuration
│   └── vitest.config.ts       # Test configuration
├── docs/                      # Docusaurus documentation
│   ├── docs/                  # Documentation content
│   ├── blog/                  # Project blog posts
│   ├── src/                   # Custom documentation components
│   └── docusaurus.config.js   # Documentation site config
├── docker-compose.yml         # Multi-container development setup
├── .env.example               # Environment variable template
└── README.md                  # Project overview & setup
```

### Module Organization Principles
- **Service Separation:** Each service (server, mcp, agents) operates independently
- **Layered Architecture:** Clear separation between routes, services, and data layers
- **Feature Organization:** Frontend organized by features rather than technical concerns
- **Shared Resources:** Common utilities and types in dedicated shared modules
- **Test Colocation:** Tests organized to mirror source code structure

---

## 4. Development Environment & Workflow

### Local Development Setup

#### Prerequisites
1. **Python 3.12+** with `uv` package manager
2. **Node.js 20.x** with `npm`
3. **Docker & Docker Compose** for containerized services
4. **Git** for version control

#### Initial Setup Commands
```bash
# 1. Clone and navigate to project
git clone <repository-url>
cd ARCHON-RELOADED

# 2. Backend setup (Python)
cd python
uv sync --frozen --all-extras --dev
# Creates virtual environment and installs all dependencies

# 3. Frontend setup (React)
cd ../archon-ui-main
npm install
# Installs Node.js dependencies

# 4. Environment configuration
cp .env.example .env
# Edit .env with your Supabase and OpenAI credentials

# 5. Database setup
docker compose up -d supabase
# Wait for database to be ready, then run migrations

# 6. Start all services
docker compose up -d
```

#### Development Commands
```bash
# Backend development
cd python
uv run python -m src.server.main          # FastAPI server
uv run python -m src.mcp.server           # MCP server
uv run python -m src.agents.server        # PydanticAI agents

# Frontend development
cd archon-ui-main
npm run dev                                # Vite dev server with HMR

# Testing
uv run pytest                             # Python tests
npm run test                              # Frontend tests (Vitest)

# Code quality
uv run ruff format .                      # Python formatting
uv run ruff check . --fix                # Python linting
npm run lint                              # TypeScript linting
npm run type-check                        # TypeScript compilation check
```

#### Development Workflow
1. **Feature Branches:** Create feature branches from `main`
2. **Local Testing:** Run all tests before committing
3. **Code Quality:** Ensure formatting and linting pass
4. **Documentation:** Update relevant documentation
5. **Pull Requests:** Create PR with comprehensive description

### Docker Development Environment
```yaml
# docker-compose.yml structure
services:
  # Database services
  supabase:
    image: supabase/supabase:latest
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # Backend services
  api-server:
    build:
      context: ./python
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - supabase
      - redis

  mcp-server:
    build:
      context: ./python
      dockerfile: Dockerfile.mcp
    ports:
      - "8001:8001"

  # Frontend service
  frontend:
    build:
      context: ./archon-ui-main
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
```

---

## 5. Coding Standards & Conventions

### General Principles
- **Type Safety First:** Strict typing in both TypeScript and Python
- **Immutable Patterns:** Prefer immutable data structures and pure functions
- **Error Handling:** Comprehensive error handling with proper logging
- **Performance Conscious:** Consider performance implications of all architectural decisions
- **Security Minded:** Validate all inputs, sanitize outputs, secure by default

### Python Coding Standards

#### Code Style & Formatting
- **Formatter:** Black with 100-character line length
- **Linter:** Ruff with comprehensive rule set
- **Import Sorting:** isort integrated with Ruff
- **Type Checking:** mypy or pyright for static analysis

```python
# Style example
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import Depends, HTTPException, status

class UserCreateRequest(BaseModel):
    """User creation request model with validation."""
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[str, Field(regex=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')]
    password: Annotated[str, Field(min_length=8)]

async def create_user(
    request: UserCreateRequest,
    db: Annotated[Database, Depends(get_database)],
) -> UserResponse:
    """Create a new user with validation and error handling."""
    try:
        # Business logic here
        user = await db.create_user(request)
        return UserResponse.from_orm(user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        ) from e
```

#### Naming Conventions
- **Variables/Functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `SCREAMING_SNAKE_CASE`
- **Private Members:** `_leading_underscore`
- **Files:** `snake_case.py`

#### FastAPI Specific Patterns
- **Dependency Injection:** Use FastAPI's dependency system extensively
- **Pydantic Models:** All request/response models must use Pydantic
- **Async/Await:** Use async for all I/O operations
- **Error Handling:** Standardized HTTPException usage
- **OpenAPI Documentation:** Comprehensive docstrings and examples

```python
# FastAPI best practices
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(
    title="ARCHON RELOADED API",
    description="AI Development Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Extract and validate user from JWT token."""
    token = credentials.credentials
    payload = decode_jwt(token)
    return await get_user_by_id(payload["user_id"])

@app.post("/api/v1/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> TaskResponse:
    """Create a new task with background processing."""
    task = await create_task_service(task_data, current_user.id)
    background_tasks.add_task(send_task_notification, task.id)
    return TaskResponse.from_orm(task)
```

#### PydanticAI Patterns
- **Agent Definition:** Use typed dependencies for better IDE support
- **Tool Implementation:** Comprehensive docstrings for LLM understanding
- **Error Handling:** Use ModelRetry for recoverable errors
- **Output Validation:** Structured output types with Pydantic models

```python
# PydanticAI best practices
from pydantic_ai import Agent, RunContext, ModelRetry
from dataclasses import dataclass

@dataclass
class AgentDependencies:
    db_conn: DatabaseConnection
    api_client: HttpClient

agent = Agent(
    'openai:gpt-4o',
    deps_type=AgentDependencies,
    system_prompt="You are a helpful AI assistant for the ARCHON platform."
)

@agent.tool
async def search_knowledge_base(
    ctx: RunContext[AgentDependencies], 
    query: str,
    max_results: int = 10
) -> list[str]:
    """Search the knowledge base for relevant information.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (1-50)
        
    Returns:
        List of relevant knowledge base entries
    """
    try:
        results = await ctx.deps.db_conn.vector_search(query, max_results)
        return [result.content for result in results]
    except DatabaseError as e:
        raise ModelRetry(f"Database search failed: {e}")
```

### TypeScript/React Coding Standards

#### Code Style & Formatting
- **Formatter:** Prettier with 2-space indentation
- **Linter:** ESLint with TypeScript rules
- **Import Organization:** Automatic import sorting
- **Naming Convention:** camelCase for variables/functions, PascalCase for components/types

```typescript
// TypeScript style example
import React, { useState, useCallback, useMemo } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Button } from '@/components/atoms/Button';
import { TaskCard } from '@/components/molecules/TaskCard';
import type { Task, CreateTaskRequest } from '@/types/task';

interface TaskListProps {
  userId: string;
  onTaskCreate?: (task: Task) => void;
}

export const TaskList: React.FC<TaskListProps> = ({ userId, onTaskCreate }) => {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  const { data: tasks, isLoading, error } = useQuery({
    queryKey: ['tasks', userId, filter],
    queryFn: () => fetchTasks(userId, filter),
    staleTime: 30_000, // 30 seconds
  });

  const createTaskMutation = useMutation({
    mutationFn: (request: CreateTaskRequest) => createTask(request),
    onSuccess: (task) => {
      onTaskCreate?.(task);
      // Invalidate and refetch tasks
      queryClient.invalidateQueries(['tasks', userId]);
    },
  });

  const handleCreateTask = useCallback((taskData: CreateTaskRequest) => {
    createTaskMutation.mutate(taskData);
  }, [createTaskMutation]);

  const filteredTasks = useMemo(() => {
    if (!tasks) return [];
    return tasks.filter(task => {
      switch (filter) {
        case 'active': return !task.completed;
        case 'completed': return task.completed;
        default: return true;
      }
    });
  }, [tasks, filter]);

  if (isLoading) return <div>Loading tasks...</div>;
  if (error) return <div>Error loading tasks: {error.message}</div>;

  return (
    <div className="task-list">
      <div className="task-filters">
        {(['all', 'active', 'completed'] as const).map(filterOption => (
          <Button
            key={filterOption}
            variant={filter === filterOption ? 'primary' : 'secondary'}
            onClick={() => setFilter(filterOption)}
          >
            {filterOption}
          </Button>
        ))}
      </div>
      
      <div className="task-grid">
        {filteredTasks.map(task => (
          <TaskCard
            key={task.id}
            task={task}
            onUpdate={handleTaskUpdate}
          />
        ))}
      </div>
    </div>
  );
};
```

#### React 18 Patterns
- **Concurrent Features:** Use useTransition for non-urgent updates
- **Performance:** Strategic use of React.memo and useMemo
- **Error Boundaries:** Implement for robust error handling
- **Suspense:** Use for code splitting and async components

```typescript
// React 18 concurrent features
import { useTransition, useDeferredValue, startTransition } from 'react';

export const SearchResults: React.FC = () => {
  const [isPending, startTransition] = useTransition();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  
  const deferredQuery = useDeferredValue(query);

  const handleSearch = (newQuery: string) => {
    setQuery(newQuery); // Urgent update
    startTransition(() => {
      // Non-urgent update that won't block UI
      searchKnowledgeBase(newQuery).then(setResults);
    });
  };

  return (
    <div>
      <SearchInput onChange={handleSearch} />
      {isPending && <LoadingSpinner />}
      <ResultsList results={results} query={deferredQuery} />
    </div>
  );
};
```

#### Socket.IO Integration
- **Connection Management:** Proper connection lifecycle handling
- **Event Typing:** Strong typing for all Socket.IO events
- **Error Handling:** Comprehensive error and reconnection logic
- **Performance:** Event throttling and cleanup

```typescript
// Socket.IO client integration
import { io, Socket } from 'socket.io-client';
import { useEffect, useState, useCallback } from 'react';

interface ServerToClientEvents {
  'task:updated': (task: Task) => void;
  'task:created': (task: Task) => void;
  'user:joined': (user: User) => void;
}

interface ClientToServerEvents {
  'task:subscribe': (taskId: string) => void;
  'task:unsubscribe': (taskId: string) => void;
}

export const useSocket = () => {
  const [socket, setSocket] = useState<Socket<ServerToClientEvents, ClientToServerEvents> | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socketInstance = io('http://localhost:8000', {
      transports: ['websocket', 'polling'],
      auth: {
        token: getAuthToken(),
      },
    });

    socketInstance.on('connect', () => {
      setIsConnected(true);
      console.log('Connected to server');
    });

    socketInstance.on('disconnect', (reason) => {
      setIsConnected(false);
      console.log('Disconnected:', reason);
    });

    socketInstance.on('connect_error', (error) => {
      console.error('Connection error:', error);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  const subscribeToTask = useCallback((taskId: string) => {
    socket?.emit('task:subscribe', taskId);
  }, [socket]);

  return {
    socket,
    isConnected,
    subscribeToTask,
  };
};
```

### Vite Configuration
- **Modern Build Target:** ES2023 for modern browsers
- **Optimization:** Tree shaking and code splitting
- **Development:** Hot module replacement and fast refresh
- **Environment:** Proper environment variable handling

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [
    react({
      // Use SWC for faster builds
      jsxRuntime: 'automatic',
    }),
  ],
  
  build: {
    target: 'ES2023',
    sourcemap: process.env.NODE_ENV === 'development',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash-es', 'date-fns'],
        },
      },
    },
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@types': path.resolve(__dirname, 'src/types'),
    },
  },

  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://localhost:8000',
        ws: true,
      },
    },
  },

  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
});
```

---

## 6. Database Architecture & Vector Operations

### Supabase PostgreSQL Setup

#### Core Configuration
- **Database:** PostgreSQL 15+ with pgvector extension
- **Vector Dimensions:** 384 (gte-small), 1536 (OpenAI ada-002), 4096 (large models)
- **Extensions:** pgvector, pg_net, pg_cron, hstore for AI workflows
- **Connection Pooling:** Session pooler (port 5432) for migrations, transaction pooler (port 6543) for queries

#### Vector Table Design
```sql
-- Knowledge base documents with vector embeddings
CREATE TABLE documents (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  document_type VARCHAR(50) NOT NULL,
  category_id BIGINT REFERENCES categories(id),
  project_id BIGINT REFERENCES projects(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  embedding vector(384), -- Using gte-small embeddings
  metadata JSONB DEFAULT '{}'::jsonb,
  
  -- Indexing for performance
  CONSTRAINT documents_title_length CHECK (length(title) > 0),
  CONSTRAINT documents_content_length CHECK (length(content) > 0)
);

-- Vector similarity index (HNSW for best performance)
CREATE INDEX documents_embedding_idx ON documents 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Additional indexes for filtering
CREATE INDEX documents_category_idx ON documents (category_id);
CREATE INDEX documents_project_idx ON documents (project_id);
CREATE INDEX documents_type_idx ON documents (document_type);
CREATE INDEX documents_created_idx ON documents (created_at DESC);
```

#### Vector Search Functions
```sql
-- Similarity search with filtering
CREATE OR REPLACE FUNCTION match_documents (
  query_embedding vector(384),
  match_threshold float DEFAULT 0.7,
  match_count int DEFAULT 10,
  filter_project_id bigint DEFAULT null,
  filter_category_id bigint DEFAULT null
)
RETURNS TABLE (
  id bigint,
  title text,
  content text,
  document_type varchar(50),
  similarity float,
  metadata jsonb
)
LANGUAGE sql STABLE
AS $$
  SELECT
    documents.id,
    documents.title,
    documents.content,
    documents.document_type,
    1 - (documents.embedding <=> query_embedding) as similarity,
    documents.metadata
  FROM documents
  WHERE 
    (filter_project_id IS NULL OR project_id = filter_project_id)
    AND (filter_category_id IS NULL OR category_id = filter_category_id)
    AND 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY (documents.embedding <=> query_embedding) ASC
  LIMIT match_count;
$$;

-- Hybrid search combining text and vector similarity
CREATE OR REPLACE FUNCTION hybrid_search (
  query_text text,
  query_embedding vector(384),
  match_count int DEFAULT 10,
  text_weight float DEFAULT 0.3,
  vector_weight float DEFAULT 0.7
)
RETURNS TABLE (
  id bigint,
  title text,
  content text,
  combined_score float
)
LANGUAGE sql STABLE
AS $$
  WITH text_search AS (
    SELECT 
      id,
      title,
      content,
      ts_rank_cd(to_tsvector('english', title || ' ' || content), plainto_tsquery('english', query_text)) as text_score
    FROM documents
    WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', query_text)
  ),
  vector_search AS (
    SELECT 
      id,
      title,
      content,
      1 - (embedding <=> query_embedding) as vector_score
    FROM documents
    ORDER BY embedding <=> query_embedding
    LIMIT match_count * 2
  )
  SELECT 
    COALESCE(ts.id, vs.id) as id,
    COALESCE(ts.title, vs.title) as title,
    COALESCE(ts.content, vs.content) as content,
    (COALESCE(ts.text_score, 0) * text_weight + COALESCE(vs.vector_score, 0) * vector_weight) as combined_score
  FROM text_search ts
  FULL OUTER JOIN vector_search vs ON ts.id = vs.id
  ORDER BY combined_score DESC
  LIMIT match_count;
$$;
```

#### Row Level Security (RLS)
```sql
-- Enable RLS on documents table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Users can only access documents from their projects
CREATE POLICY "Users can view own project documents"
  ON documents FOR SELECT
  USING (
    project_id IN (
      SELECT project_id 
      FROM project_members 
      WHERE user_id = (SELECT auth.uid())
    )
  );

-- Optimized RLS policy with caching
CREATE POLICY "Users can modify own project documents"
  ON documents FOR ALL
  USING ((SELECT auth.uid()) = created_by);

-- Index for RLS performance
CREATE INDEX documents_created_by_idx ON documents (created_by);
```

### Database Migration Strategy
```sql
-- migration/001_initial_schema.sql
-- Core tables for the ARCHON platform

-- Users and authentication
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Projects and workspaces
CREATE TABLE projects (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  description TEXT,
  owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
  settings JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks and project management
CREATE TABLE tasks (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  title TEXT NOT NULL,
  description TEXT,
  status task_status DEFAULT 'pending',
  priority task_priority DEFAULT 'medium',
  project_id BIGINT REFERENCES projects(id) ON DELETE CASCADE,
  assigned_to UUID REFERENCES users(id),
  created_by UUID REFERENCES users(id) NOT NULL,
  due_date TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Knowledge base categories
CREATE TABLE categories (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  description TEXT,
  project_id BIGINT REFERENCES projects(id) ON DELETE CASCADE,
  parent_id BIGINT REFERENCES categories(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Document processing and embeddings
CREATE TABLE document_chunks (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  document_id BIGINT REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,
  embedding vector(384),
  token_count INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(document_id, chunk_index)
);

-- Vector index for chunks
CREATE INDEX document_chunks_embedding_idx ON document_chunks 
USING hnsw (embedding vector_cosine_ops);
```

---

## 7. API Design & Communication Patterns

### RESTful API Standards
- **Base URL:** `/api/v1/` for all API endpoints
- **HTTP Methods:** Proper usage of GET, POST, PUT, PATCH, DELETE
- **Status Codes:** Comprehensive use of appropriate HTTP status codes
- **Content Type:** JSON for all request/response bodies
- **Error Format:** Consistent error response structure

#### API Endpoint Structure
```python
# Standard API response models
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None
    pagination: Optional[PaginationInfo] = None

class PaginationInfo(BaseModel):
    """Pagination metadata."""
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

# Example endpoint implementation
@router.get("/documents", response_model=APIResponse[list[DocumentResponse]])
async def list_documents(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database)
) -> APIResponse[list[DocumentResponse]]:
    """List documents with pagination and filtering."""
    
    # Build query with filters
    query_params = {
        "user_id": current_user.id,
        "category_id": category_id,
        "search": search
    }
    
    # Get paginated results
    documents, total_count = await db.get_documents_paginated(
        offset=(page - 1) * limit,
        limit=limit,
        **query_params
    )
    
    # Build response
    return APIResponse(
        success=True,
        data=[DocumentResponse.from_orm(doc) for doc in documents],
        pagination=PaginationInfo(
            page=page,
            limit=limit,
            total=total_count,
            total_pages=math.ceil(total_count / limit),
            has_next=page * limit < total_count,
            has_prev=page > 1
        )
    )
```

#### Error Handling Standards
```python
# Custom exception classes
class APIException(HTTPException):
    """Base API exception with logging."""
    
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        logger.error(f"API Error: {error_code} - {detail}")

class ValidationException(APIException):
    """Input validation errors."""
    
    def __init__(self, detail: str, field: str = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )
        self.field = field

class ResourceNotFoundException(APIException):
    """Resource not found errors."""
    
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_type} with id {resource_id} not found",
            error_code="RESOURCE_NOT_FOUND"
        )

# Global exception handler
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """Handle API exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "error_code": exc.error_code,
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### WebSocket/Socket.IO Integration
- **Namespace Organization:** Logical separation by feature
- **Event Naming:** Consistent `domain:action` pattern
- **Authentication:** JWT-based authentication for all connections
- **Error Handling:** Comprehensive error and reconnection handling

#### Socket.IO Server Configuration
```python
# Socket.IO server setup with FastAPI
from socketio import AsyncServer
from fastapi import FastAPI
import socketio

# Create Socket.IO server
sio = AsyncServer(
    cors_allowed_origins=["http://localhost:3000"],
    logger=True,
    engineio_logger=True
)

app = FastAPI()

# Mount Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# Authentication middleware
@sio.event
async def connect(sid, environ, auth):
    """Handle client connection with authentication."""
    try:
        token = auth.get('token') if auth else None
        if not token:
            await sio.emit('error', {'message': 'Authentication required'}, room=sid)
            return False
            
        user = await verify_jwt_token(token)
        if not user:
            await sio.emit('error', {'message': 'Invalid token'}, room=sid)
            return False
            
        # Store user session
        await sio.save_session(sid, {'user_id': user.id, 'username': user.username})
        
        # Join user to personal room
        await sio.enter_room(sid, f"user:{user.id}")
        
        logger.info(f"User {user.username} connected: {sid}")
        return True
        
    except Exception as e:
        logger.error(f"Connection error: {e}")
        return False

# Event handlers
@sio.event
async def join_project(sid, data):
    """Join a project room for real-time updates."""
    session = await sio.get_session(sid)
    user_id = session['user_id']
    project_id = data.get('project_id')
    
    # Verify user has access to project
    if await has_project_access(user_id, project_id):
        await sio.enter_room(sid, f"project:{project_id}")
        await sio.emit('project:joined', {'project_id': project_id}, room=sid)
        
        # Notify other project members
        await sio.emit('user:joined_project', {
            'user_id': user_id,
            'username': session['username'],
            'project_id': project_id
        }, room=f"project:{project_id}", skip_sid=sid)

@sio.event
async def task_update(sid, data):
    """Handle task updates with real-time broadcast."""
    session = await sio.get_session(sid)
    user_id = session['user_id']
    
    task_id = data.get('task_id')
    updates = data.get('updates', {})
    
    try:
        # Update task in database
        task = await update_task(task_id, updates, user_id)
        
        # Broadcast to project members
        await sio.emit('task:updated', {
            'task_id': task.id,
            'task': task.dict(),
            'updated_by': session['username'],
            'timestamp': datetime.utcnow().isoformat()
        }, room=f"project:{task.project_id}")
        
    except Exception as e:
        await sio.emit('error', {'message': str(e)}, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    session = await sio.get_session(sid)
    if session:
        logger.info(f"User {session.get('username')} disconnected: {sid}")
```

#### Client-Side Socket Integration
```typescript
// Socket.IO client with React integration
import { useEffect, useState, useContext } from 'react';
import { io, Socket } from 'socket.io-client';
import { AuthContext } from '@/contexts/AuthContext';

interface SocketContextType {
  socket: Socket | null;
  isConnected: boolean;
  joinProject: (projectId: string) => void;
  leaveProject: (projectId: string) => void;
}

export const SocketContext = createContext<SocketContextType>({
  socket: null,
  isConnected: false,
  joinProject: () => {},
  leaveProject: () => {},
});

export const SocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const { user, token } = useContext(AuthContext);

  useEffect(() => {
    if (!user || !token) return;

    const socketInstance = io('http://localhost:8000', {
      auth: { token },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    socketInstance.on('connect', () => {
      console.log('Connected to server');
      setIsConnected(true);
    });

    socketInstance.on('disconnect', (reason) => {
      console.log('Disconnected:', reason);
      setIsConnected(false);
    });

    socketInstance.on('error', (error) => {
      console.error('Socket error:', error);
      toast.error(`Connection error: ${error.message}`);
    });

    // Real-time event handlers
    socketInstance.on('task:updated', (data) => {
      // Update local state or invalidate queries
      queryClient.invalidateQueries(['tasks', data.task.project_id]);
      toast.info(`Task "${data.task.title}" updated by ${data.updated_by}`);
    });

    socketInstance.on('user:joined_project', (data) => {
      toast.info(`${data.username} joined the project`);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, [user, token]);

  const joinProject = useCallback((projectId: string) => {
    socket?.emit('join_project', { project_id: projectId });
  }, [socket]);

  const leaveProject = useCallback((projectId: string) => {
    socket?.emit('leave_project', { project_id: projectId });
  }, [socket]);

  return (
    <SocketContext.Provider value={{ socket, isConnected, joinProject, leaveProject }}>
      {children}
    </SocketContext.Provider>
  );
};
```

### MCP (Model Context Protocol) Integration
- **Protocol Version:** Latest MCP specification
- **Transport:** HTTP-based for cloud deployment compatibility
- **Tool Definition:** Comprehensive tool descriptions for AI agents
- **Error Handling:** Proper error responses and retry mechanisms

#### MCP Server Implementation
```python
# MCP server with FastMCP framework
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel
from typing import Optional, List

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    project_id: Optional[str] = None

class DocumentResult(BaseModel):
    id: str
    title: str
    content: str
    similarity: float
    metadata: dict

# Initialize MCP server
mcp = FastMCP("ARCHON Knowledge Server")

@mcp.tool()
async def search_knowledge_base(
    ctx: Context,
    query: str,
    max_results: int = 10,
    project_id: Optional[str] = None
) -> List[DocumentResult]:
    """Search the ARCHON knowledge base using vector similarity.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (1-50)
        project_id: Optional project ID to filter results
        
    Returns:
        List of relevant documents with similarity scores
    """
    try:
        await ctx.info(f"Searching knowledge base for: {query}")
        
        # Generate query embedding
        embedding = await generate_embedding(query)
        
        # Search database
        results = await search_documents_vector(
            embedding=embedding,
            limit=max_results,
            project_id=project_id
        )
        
        await ctx.info(f"Found {len(results)} relevant documents")
        
        return [
            DocumentResult(
                id=str(doc.id),
                title=doc.title,
                content=doc.content[:500] + "..." if len(doc.content) > 500 else doc.content,
                similarity=doc.similarity,
                metadata=doc.metadata or {}
            )
            for doc in results
        ]
        
    except Exception as e:
        await ctx.error(f"Knowledge base search failed: {str(e)}")
        raise

@mcp.tool()
async def create_task(
    ctx: Context,
    title: str,
    description: str,
    project_id: str,
    priority: str = "medium"
) -> dict:
    """Create a new task in the ARCHON platform.
    
    Args:
        title: Task title
        description: Detailed task description
        project_id: ID of the project to create task in
        priority: Task priority (low, medium, high, urgent)
        
    Returns:
        Created task information
    """
    try:
        await ctx.info(f"Creating task: {title}")
        
        task_data = {
            "title": title,
            "description": description,
            "project_id": project_id,
            "priority": priority,
            "status": "pending"
        }
        
        task = await create_task_service(task_data)
        
        await ctx.info(f"Task created successfully: {task.id}")
        
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "created_at": task.created_at.isoformat(),
            "project_id": str(task.project_id)
        }
        
    except Exception as e:
        await ctx.error(f"Task creation failed: {str(e)}")
        raise

@mcp.resource("project://info/{project_id}")
async def get_project_info(project_id: str) -> str:
    """Get project information and context.
    
    Args:
        project_id: Project identifier
        
    Returns:
        Project information as formatted text
    """
    project = await get_project_by_id(project_id)
    if not project:
        raise ValueError(f"Project {project_id} not found")
    
    info = f"""
    Project: {project.name}
    Description: {project.description}
    Created: {project.created_at.strftime('%Y-%m-%d')}
    Owner: {project.owner.full_name}
    
    Recent Activity:
    """
    
    # Add recent tasks and documents
    recent_tasks = await get_recent_tasks(project_id, limit=5)
    for task in recent_tasks:
        info += f"- Task: {task.title} ({task.status})\n"
    
    return info

# Configure for cloud deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.sse_app("/mcp"), host="0.0.0.0", port=8001)
```

---

## 8. Security & Authentication Standards

### Authentication Architecture
- **Primary Method:** JWT-based authentication with refresh tokens
- **Token Storage:** Secure HTTP-only cookies for web clients
- **Session Management:** Redis-based session storage
- **Multi-factor Authentication:** TOTP support for enhanced security

#### JWT Implementation
```python
# JWT utilities with security best practices
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class JWTManager:
    """Secure JWT token management."""
    
    def __init__(self, private_key_path: str, public_key_path: str):
        self.private_key = self._load_private_key(private_key_path)
        self.public_key = self._load_public_key(public_key_path)
        self.algorithm = "RS256"
        self.access_token_expire = timedelta(minutes=15)
        self.refresh_token_expire = timedelta(days=7)
    
    def create_access_token(self, user_id: str, scopes: List[str] = None) -> str:
        """Create short-lived access token."""
        now = datetime.utcnow()
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + self.access_token_expire,
            "type": "access",
            "scopes": scopes or []
        }
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create long-lived refresh token."""
        now = datetime.utcnow()
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + self.refresh_token_expire,
            "type": "refresh"
        }
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = "access") -> dict:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token, 
                self.public_key, 
                algorithms=[self.algorithm],
                options={"require": ["sub", "iat", "exp", "type"]}
            )
            
            if payload.get("type") != token_type:
                raise jwt.InvalidTokenError(f"Invalid token type: {payload.get('type')}")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )

# Authentication dependency
async def get_current_user(
    request: Request,
    db: Database = Depends(get_database)
) -> User:
    """Extract and validate current user from JWT token."""
    
    # Try to get token from Authorization header
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    else:
        # Try to get token from secure cookie
        token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Verify token
    jwt_manager = get_jwt_manager()
    payload = jwt_manager.verify_token(token, "access")
    
    # Get user from database
    user = await db.get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
```

### Input Validation & Sanitization
- **Pydantic Models:** Comprehensive validation for all API inputs
- **SQL Injection Prevention:** Parameterized queries and ORM usage
- **XSS Prevention:** Input sanitization and output encoding
- **File Upload Security:** Type validation and size limits

```python
# Input validation patterns
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import re

class DocumentCreateRequest(BaseModel):
    """Document creation with comprehensive validation."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=50000)
    category_id: Optional[int] = Field(None, gt=0)
    tags: List[str] = Field(default_factory=list, max_items=10)
    is_public: bool = Field(default=False)
    
    @validator('title')
    def validate_title(cls, v):
        """Validate and sanitize title."""
        if not v.strip():
            raise ValueError('Title cannot be empty')
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', v.strip())
        return sanitized
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content length and basic sanitization."""
        if len(v.strip()) < 10:
            raise ValueError('Content must be at least 10 characters')
        
        # Basic HTML tag removal (use proper sanitizer in production)
        sanitized = re.sub(r'<script.*?</script>', '', v, flags=re.DOTALL | re.IGNORECASE)
        return sanitized.strip()
    
    @validator('tags')
    def validate_tags(cls, v):
        """Validate and sanitize tags."""
        sanitized_tags = []
        for tag in v:
            if tag and tag.strip():
                # Only allow alphanumeric and basic punctuation
                clean_tag = re.sub(r'[^a-zA-Z0-9\-_\s]', '', tag.strip())
                if clean_tag and len(clean_tag) <= 30:
                    sanitized_tags.append(clean_tag.lower())
        
        return list(set(sanitized_tags))  # Remove duplicates

# File upload validation
from fastapi import UploadFile, HTTPException
import magic

async def validate_file_upload(file: UploadFile) -> None:
    """Validate uploaded file security."""
    
    # Check file size (10MB limit)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 10MB limit"
        )
    
    # Validate file type using python-magic
    file_type = magic.from_buffer(content, mime=True)
    allowed_types = {
        'text/plain',
        'text/markdown',
        'application/pdf',
        'application/json',
        'image/jpeg',
        'image/png',
        'image/webp'
    }
    
    if file_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_type} not allowed"
        )
    
    # Reset file pointer
    await file.seek(0)
```

### Authorization & Permissions
- **Role-Based Access Control (RBAC):** User roles with specific permissions
- **Resource-Based Permissions:** Fine-grained access control per resource
- **API Key Management:** Secure API key generation and validation
- **Rate Limiting:** Prevent abuse with request throttling

```python
# Permission system
from enum import Enum
from functools import wraps

class Permission(str, Enum):
    """System permissions."""
    READ_DOCUMENTS = "read:documents"
    WRITE_DOCUMENTS = "write:documents"
    DELETE_DOCUMENTS = "delete:documents"
    MANAGE_PROJECTS = "manage:projects"
    MANAGE_USERS = "manage:users"
    ADMIN_ACCESS = "admin:access"

class Role(str, Enum):
    """User roles with associated permissions."""
    VIEWER = "viewer"
    CONTRIBUTOR = "contributor"
    MANAGER = "manager"
    ADMIN = "admin"

ROLE_PERMISSIONS = {
    Role.VIEWER: [Permission.READ_DOCUMENTS],
    Role.CONTRIBUTOR: [Permission.READ_DOCUMENTS, Permission.WRITE_DOCUMENTS],
    Role.MANAGER: [
        Permission.READ_DOCUMENTS,
        Permission.WRITE_DOCUMENTS,
        Permission.DELETE_DOCUMENTS,
        Permission.MANAGE_PROJECTS
    ],
    Role.ADMIN: [perm for perm in Permission]
}

def require_permission(permission: Permission):
    """Decorator to require specific permission."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from function arguments
            current_user = None
            for arg in args:
                if isinstance(arg, User):
                    current_user = arg
                    break
            
            if not current_user:
                current_user = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Check permission
            user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission {permission.value} required"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage example
@router.delete("/documents/{document_id}")
@require_permission(Permission.DELETE_DOCUMENTS)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database)
) -> APIResponse[None]:
    """Delete a document with permission check."""
    
    # Additional resource-level check
    document = await db.get_document(document_id)
    if not document:
        raise ResourceNotFoundException("Document", str(document_id))
    
    # Check if user owns the document or has admin access
    if (document.created_by != current_user.id and 
        current_user.role != Role.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own documents"
        )
    
    await db.delete_document(document_id)
    
    return APIResponse(
        success=True,
        message="Document deleted successfully"
    )
```

---

## 9. Testing Strategy & Quality Assurance

### Test Architecture
- **Backend Testing:** pytest with comprehensive fixtures and mocking
- **Frontend Testing:** Vitest with React Testing Library
- **Integration Testing:** End-to-end testing with Playwright
- **Load Testing:** Performance testing with locust or artillery

#### Python Testing Setup
```python
# conftest.py - pytest configuration
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.server.main import app
from src.server.database import get_database
from src.server.auth import get_current_user

# Test database configuration
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost/test_archon"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True
    )
    yield engine
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine):
    """Create test database session."""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Start transaction
        await session.begin()
        yield session
        # Rollback all changes
        await session.rollback()

@pytest.fixture
def test_user():
    """Create test user data."""
    return {
        "id": "test-user-123",
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "role": "contributor"
    }

@pytest.fixture
def authenticated_client(test_user):
    """Create authenticated test client."""
    
    # Override auth dependency
    async def override_get_current_user():
        return User(**test_user)
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as client:
        yield client
    
    # Clean up
    app.dependency_overrides.clear()

@pytest.fixture
async def async_client():
    """Create async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Example test cases
@pytest.mark.asyncio
async def test_create_document(authenticated_client, test_session):
    """Test document creation with authentication."""
    
    document_data = {
        "title": "Test Document",
        "content": "This is a test document with sufficient content length.",
        "category_id": 1,
        "tags": ["test", "example"]
    }
    
    response = authenticated_client.post("/api/v1/documents", json=document_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == document_data["title"]
    assert len(data["data"]["tags"]) == 2

@pytest.mark.asyncio
async def test_search_documents_vector(test_session, test_user):
    """Test vector search functionality."""
    
    # Create test documents with embeddings
    test_docs = [
        {
            "title": "Python Programming",
            "content": "Python is a powerful programming language.",
            "embedding": [0.1, 0.2, 0.3] * 128  # Mock 384-dim embedding
        },
        {
            "title": "JavaScript Basics",
            "content": "JavaScript is used for web development.",
            "embedding": [0.2, 0.3, 0.4] * 128
        }
    ]
    
    # Insert test data
    for doc_data in test_docs:
        doc = Document(**doc_data, created_by=test_user["id"])
        test_session.add(doc)
    await test_session.commit()
    
    # Test search
    query_embedding = [0.15, 0.25, 0.35] * 128
    results = await search_documents_vector(
        test_session,
        embedding=query_embedding,
        limit=5
    )
    
    assert len(results) >= 2
    assert results[0].similarity > 0.8  # Should find close matches

@pytest.mark.asyncio
async def test_websocket_connection(async_client):
    """Test WebSocket connection and messaging."""
    
    with async_client.websocket_connect("/ws") as websocket:
        # Test connection
        data = websocket.receive_json()
        assert data["type"] == "connection_established"
        
        # Test message echo
        test_message = {"type": "test", "data": "hello"}
        websocket.send_json(test_message)
        
        response = websocket.receive_json()
        assert response["type"] == "echo"
        assert response["data"] == test_message

# Performance testing
@pytest.mark.asyncio
async def test_document_search_performance(test_session):
    """Test search performance with large dataset."""
    import time
    
    # Create many test documents
    documents = []
    for i in range(1000):
        doc = Document(
            title=f"Document {i}",
            content=f"Content for document {i} with various keywords.",
            embedding=[random.random() for _ in range(384)],
            created_by="test-user"
        )
        documents.append(doc)
    
    test_session.add_all(documents)
    await test_session.commit()
    
    # Measure search performance
    start_time = time.time()
    query_embedding = [random.random() for _ in range(384)]
    
    results = await search_documents_vector(
        test_session,
        embedding=query_embedding,
        limit=10
    )
    
    search_time = time.time() - start_time
    
    assert len(results) == 10
    assert search_time < 0.1  # Should complete in under 100ms
```

#### Frontend Testing Setup
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
    css: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
});

// src/test/setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock Socket.IO
vi.mock('socket.io-client', () => ({
  io: vi.fn(() => ({
    on: vi.fn(),
    off: vi.fn(),
    emit: vi.fn(),
    disconnect: vi.fn(),
    connected: true,
  })),
}));

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn(() => ({
  observe: vi.fn(),
  disconnect: vi.fn(),
  unobserve: vi.fn(),
}));

// Example React component tests
// src/components/TaskList.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TaskList } from './TaskList';
import { TaskProvider } from '@/contexts/TaskContext';

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

const renderWithProviders = (component: React.ReactElement) => {
  const queryClient = createTestQueryClient();
  
  return render(
    <QueryClientProvider client={queryClient}>
      <TaskProvider>
        {component}
      </TaskProvider>
    </QueryClientProvider>
  );
};

describe('TaskList Component', () => {
  it('renders task list correctly', async () => {
    const mockTasks = [
      { id: '1', title: 'Test Task 1', status: 'pending' },
      { id: '2', title: 'Test Task 2', status: 'completed' },
    ];

    // Mock API response
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: mockTasks }),
    } as Response);

    renderWithProviders(<TaskList userId="test-user" />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.getByText('Test Task 2')).toBeInTheDocument();
    });
  });

  it('handles task creation', async () => {
    renderWithProviders(<TaskList userId="test-user" />);

    const createButton = screen.getByRole('button', { name: /create task/i });
    fireEvent.click(createButton);

    const titleInput = screen.getByLabelText(/task title/i);
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    const submitButton = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/tasks'),
        expect.objectContaining({
          method: 'POST',
          body: expect.stringContaining('New Task'),
        })
      );
    });
  });

  it('filters tasks correctly', async () => {
    const mockTasks = [
      { id: '1', title: 'Active Task', status: 'pending' },
      { id: '2', title: 'Done Task', status: 'completed' },
    ];

    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: mockTasks }),
    } as Response);

    renderWithProviders(<TaskList userId="test-user" />);

    await waitFor(() => {
      expect(screen.getByText('Active Task')).toBeInTheDocument();
      expect(screen.getByText('Done Task')).toBeInTheDocument();
    });

    // Filter to completed tasks
    const completedFilter = screen.getByRole('button', { name: /completed/i });
    fireEvent.click(completedFilter);

    expect(screen.queryByText('Active Task')).not.toBeInTheDocument();
    expect(screen.getByText('Done Task')).toBeInTheDocument();
  });
});

// Hook testing
// src/hooks/useSocket.test.ts
import { renderHook, act } from '@testing-library/react';
import { useSocket } from './useSocket';

describe('useSocket Hook', () => {
  it('connects to socket server', () => {
    const { result } = renderHook(() => useSocket());

    expect(result.current.socket).toBeTruthy();
    expect(result.current.isConnected).toBe(true);
  });

  it('handles socket events', () => {
    const { result } = renderHook(() => useSocket());
    const mockCallback = vi.fn();

    act(() => {
      result.current.socket?.on('test-event', mockCallback);
      result.current.socket?.emit('test-event', { data: 'test' });
    });

    expect(mockCallback).toHaveBeenCalled();
  });
});
```

### Integration & E2E Testing
```typescript
// e2e/tests/document-workflow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Document Management Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[data-testid=email]', 'test@example.com');
    await page.fill('[data-testid=password]', 'testpassword');
    await page.click('[data-testid=login-button]');
    await page.waitForURL('/dashboard');
  });

  test('create and search documents', async ({ page }) => {
    // Navigate to documents
    await page.click('[data-testid=nav-documents]');
    await page.waitForURL('/documents');

    // Create new document
    await page.click('[data-testid=create-document]');
    await page.fill('[data-testid=document-title]', 'E2E Test Document');
    await page.fill('[data-testid=document-content]', 'This is a test document created during E2E testing.');
    await page.click('[data-testid=save-document]');

    // Verify document was created
    await expect(page.locator('[data-testid=success-message]')).toBeVisible();
    await expect(page.locator('text=E2E Test Document')).toBeVisible();

    // Test search functionality
    await page.fill('[data-testid=search-input]', 'E2E Test');
    await page.press('[data-testid=search-input]', 'Enter');

    // Verify search results
    await expect(page.locator('[data-testid=search-results]')).toBeVisible();
    await expect(page.locator('text=E2E Test Document')).toBeVisible();
  });

  test('real-time collaboration', async ({ browser }) => {
    // Create second browser context for collaboration test
    const context2 = await browser.newContext();
    const page2 = await context2.newPage();

    // Login with second user
    await page2.goto('/login');
    await page2.fill('[data-testid=email]', 'user2@example.com');
    await page2.fill('[data-testid=password]', 'testpassword2');
    await page2.click('[data-testid=login-button]');

    // Both users join the same project
    await page.goto('/projects/test-project');
    await page2.goto('/projects/test-project');

    // User 1 creates a task
    await page.click('[data-testid=create-task]');
    await page.fill('[data-testid=task-title]', 'Collaboration Test Task');
    await page.click('[data-testid=save-task]');

    // Verify User 2 sees the new task in real-time
    await expect(page2.locator('text=Collaboration Test Task')).toBeVisible({ timeout: 5000 });

    await context2.close();
  });
});
```

---

## 10. AI Agent Integration & MCP Tools

### PydanticAI Agent Architecture
- **Agent Design:** Modular agents with specific capabilities
- **Tool Integration:** Comprehensive tool ecosystem for various tasks
- **Context Management:** Proper dependency injection and context passing
- **Error Recovery:** Robust error handling with ModelRetry patterns

#### Core Agent Definitions
```python
# src/agents/knowledge_agent.py
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class KnowledgeAgentDependencies:
    """Dependencies for the knowledge management agent."""
    db_conn: DatabaseConnection
    embedding_service: EmbeddingService
    vector_search: VectorSearchService

class KnowledgeSearchResult(BaseModel):
    """Structured result from knowledge search."""
    documents: List[dict]
    total_results: int
    search_time_ms: float
    suggestions: List[str]

class DocumentSummary(BaseModel):
    """Document analysis and summary."""
    summary: str
    key_points: List[str]
    related_topics: List[str]
    confidence_score: float

# Initialize knowledge management agent
knowledge_agent = Agent(
    'openai:gpt-4o',
    deps_type=KnowledgeAgentDependencies,
    system_prompt="""You are ARCHON's Knowledge Assistant, an expert at managing and retrieving information from the platform's knowledge base.

Your capabilities include:
- Searching and retrieving relevant documents using vector similarity
- Analyzing document content and extracting key insights
- Suggesting related topics and connections
- Summarizing complex information into digestible formats
- Recommending document organization improvements

Always provide accurate, helpful responses and cite your sources when referencing specific documents."""
)

@knowledge_agent.tool
async def search_knowledge_base(
    ctx: RunContext[KnowledgeAgentDependencies],
    query: str,
    max_results: int = 10,
    include_categories: Optional[List[str]] = None,
    min_similarity: float = 0.7
) -> KnowledgeSearchResult:
    """Search the knowledge base using vector similarity and text matching.
    
    Args:
        query: Search query in natural language
        max_results: Maximum number of results to return (1-50)
        include_categories: Optional list of categories to filter by
        min_similarity: Minimum similarity threshold (0.0-1.0)
        
    Returns:
        Structured search results with metadata
    """
    try:
        start_time = time.time()
        await ctx.info(f"Searching knowledge base for: {query}")
        
        # Generate query embedding
        query_embedding = await ctx.deps.embedding_service.generate_embedding(query)
        
        # Perform vector search
        results = await ctx.deps.vector_search.search(
            embedding=query_embedding,
            limit=max_results,
            categories=include_categories,
            min_similarity=min_similarity
        )
        
        search_time = (time.time() - start_time) * 1000
        
        # Generate suggestions for query refinement
        suggestions = await generate_search_suggestions(query, results)
        
        await ctx.info(f"Found {len(results)} documents in {search_time:.1f}ms")
        
        return KnowledgeSearchResult(
            documents=[doc.to_dict() for doc in results],
            total_results=len(results),
            search_time_ms=search_time,
            suggestions=suggestions
        )
        
    except DatabaseError as e:
        await ctx.error(f"Database search failed: {e}")
        raise ModelRetry(f"Knowledge base temporarily unavailable: {e}")
    except Exception as e:
        await ctx.error(f"Unexpected search error: {e}")
        raise

@knowledge_agent.tool
async def analyze_document(
    ctx: RunContext[KnowledgeAgentDependencies],
    document_id: str,
    analysis_type: str = "summary"
) -> DocumentSummary:
    """Analyze a document and provide insights.
    
    Args:
        document_id: ID of the document to analyze
        analysis_type: Type of analysis (summary, keywords, topics, full)
        
    Returns:
        Comprehensive document analysis
    """
    try:
        await ctx.info(f"Analyzing document {document_id}")
        
        # Retrieve document
        document = await ctx.deps.db_conn.get_document(document_id)
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        # Perform analysis based on type
        if analysis_type == "summary":
            analysis = await analyze_document_content(
                document.content,
                document.title,
                focus="summary"
            )
        elif analysis_type == "keywords":
            analysis = await extract_keywords_and_topics(document.content)
        else:
            analysis = await comprehensive_document_analysis(document)
        
        # Find related documents
        related_docs = await ctx.deps.vector_search.find_similar(
            document.embedding,
            exclude_id=document_id,
            limit=5
        )
        
        related_topics = [doc.title for doc in related_docs]
        
        await ctx.info(f"Document analysis completed for {document.title}")
        
        return DocumentSummary(
            summary=analysis.summary,
            key_points=analysis.key_points,
            related_topics=related_topics,
            confidence_score=analysis.confidence
        )
        
    except Exception as e:
        await ctx.error(f"Document analysis failed: {e}")
        raise ModelRetry(f"Unable to analyze document: {e}")

@knowledge_agent.tool
async def suggest_document_organization(
    ctx: RunContext[KnowledgeAgentDependencies],
    project_id: str
) -> dict:
    """Analyze project documents and suggest better organization.
    
    Args:
        project_id: ID of the project to analyze
        
    Returns:
        Organization suggestions and improvements
    """
    await ctx.info(f"Analyzing document organization for project {project_id}")
    
    # Get all project documents
    documents = await ctx.deps.db_conn.get_project_documents(project_id)
    
    if not documents:
        return {"message": "No documents found in this project"}
    
    # Analyze document clustering and relationships
    clusters = await analyze_document_clusters(documents)
    orphaned_docs = await find_orphaned_documents(documents)
    category_suggestions = await suggest_categories(documents)
    
    await ctx.info(f"Organization analysis complete: {len(clusters)} clusters identified")
    
    return {
        "total_documents": len(documents),
        "suggested_clusters": clusters,
        "orphaned_documents": orphaned_docs,
        "category_suggestions": category_suggestions,
        "recommendations": generate_organization_recommendations(clusters, orphaned_docs)
    }

# Project management agent
@dataclass
class ProjectAgentDependencies:
    """Dependencies for project management agent."""
    db_conn: DatabaseConnection
    notification_service: NotificationService
    task_service: TaskService

project_agent = Agent(
    'openai:gpt-4o',
    deps_type=ProjectAgentDependencies,
    system_prompt="""You are ARCHON's Project Management Assistant, specialized in helping teams organize work, track progress, and optimize productivity.

Your capabilities include:
- Creating and managing tasks with proper prioritization
- Analyzing project progress and identifying bottlenecks
- Suggesting workflow improvements and optimizations
- Generating project reports and status updates
- Coordinating team activities and deadlines

Always focus on practical, actionable advice that helps teams work more efficiently."""
)

@project_agent.tool
async def create_project_task(
    ctx: RunContext[ProjectAgentDependencies],
    title: str,
    description: str,
    priority: str = "medium",
    due_date: Optional[str] = None,
    assigned_to: Optional[str] = None,
    project_id: str = None
) -> dict:
    """Create a new task with intelligent prioritization and assignment.
    
    Args:
        title: Clear, descriptive task title
        description: Detailed task description with acceptance criteria
        priority: Task priority (low, medium, high, urgent)
        due_date: Optional due date in ISO format
        assigned_to: Optional user ID to assign the task to
        project_id: Project ID where task should be created
        
    Returns:
        Created task information with recommendations
    """
    try:
        await ctx.info(f"Creating task: {title}")
        
        # Validate and enhance task data
        task_data = await enhance_task_data({
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "assigned_to": assigned_to,
            "project_id": project_id
        })
        
        # Create task
        task = await ctx.deps.task_service.create_task(task_data)
        
        # Generate assignment recommendations if not assigned
        if not assigned_to:
            recommendations = await suggest_task_assignment(
                ctx.deps.db_conn,
                task_data,
                project_id
            )
        else:
            recommendations = []
        
        # Send notifications
        if assigned_to:
            await ctx.deps.notification_service.notify_task_assigned(
                task.id,
                assigned_to
            )
        
        await ctx.info(f"Task created successfully: {task.id}")
        
        return {
            "task": task.to_dict(),
            "assignment_recommendations": recommendations,
            "estimated_completion": await estimate_task_completion(task_data),
            "related_tasks": await find_related_tasks(ctx.deps.db_conn, task_data)
        }
        
    except Exception as e:
        await ctx.error(f"Task creation failed: {e}")
        raise ModelRetry(f"Unable to create task: {e}")

@project_agent.tool
async def analyze_project_progress(
    ctx: RunContext[ProjectAgentDependencies],
    project_id: str,
    time_period: str = "last_30_days"
) -> dict:
    """Analyze project progress and identify areas for improvement.
    
    Args:
        project_id: ID of the project to analyze
        time_period: Analysis time period (last_7_days, last_30_days, last_quarter)
        
    Returns:
        Comprehensive project analysis with recommendations
    """
    await ctx.info(f"Analyzing project progress for {project_id}")
    
    # Get project data
    project = await ctx.deps.db_conn.get_project(project_id)
    tasks = await ctx.deps.db_conn.get_project_tasks(project_id, time_period)
    team_members = await ctx.deps.db_conn.get_project_members(project_id)
    
    # Analyze metrics
    progress_metrics = calculate_progress_metrics(tasks)
    team_performance = analyze_team_performance(tasks, team_members)
    bottlenecks = identify_project_bottlenecks(tasks)
    velocity_trend = calculate_velocity_trend(tasks, time_period)
    
    # Generate recommendations
    recommendations = generate_project_recommendations(
        progress_metrics,
        team_performance,
        bottlenecks,
        velocity_trend
    )
    
    await ctx.info("Project analysis completed")
    
    return {
        "project_name": project.name,
        "analysis_period": time_period,
        "progress_metrics": progress_metrics,
        "team_performance": team_performance,
        "identified_bottlenecks": bottlenecks,
        "velocity_trend": velocity_trend,
        "recommendations": recommendations,
        "next_actions": prioritize_next_actions(recommendations)
    }
```

#### Multi-Agent Workflow Coordination
```python
# src/agents/coordinator.py
from pydantic_ai import Agent, RunContext
from typing import Dict, Any, List

class WorkflowCoordinator:
    """Coordinates multiple agents for complex workflows."""
    
    def __init__(self):
        self.knowledge_agent = knowledge_agent
        self.project_agent = project_agent
        self.agents = {
            "knowledge": self.knowledge_agent,
            "project": self.project_agent
        }
    
    async def execute_workflow(
        self,
        workflow_type: str,
        input_data: Dict[str, Any],
        dependencies: Any
    ) -> Dict[str, Any]:
        """Execute a multi-step workflow using multiple agents."""
        
        if workflow_type == "project_knowledge_analysis":
            return await self._project_knowledge_analysis(input_data, dependencies)
        elif workflow_type == "document_task_creation":
            return await self._document_task_creation(input_data, dependencies)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
    
    async def _project_knowledge_analysis(
        self,
        input_data: Dict[str, Any],
        dependencies: Any
    ) -> Dict[str, Any]:
        """Analyze project knowledge and suggest improvements."""
        
        project_id = input_data["project_id"]
        
        # Step 1: Analyze project progress
        project_analysis = await self.project_agent.run(
            f"Analyze the progress and status of project {project_id}",
            deps=dependencies.project_deps
        )
        
        # Step 2: Analyze knowledge organization
        knowledge_analysis = await self.knowledge_agent.run(
            f"Suggest better organization for documents in project {project_id}",
            deps=dependencies.knowledge_deps
        )
        
        # Step 3: Generate integrated recommendations
        combined_insights = await self._generate_combined_insights(
            project_analysis.output,
            knowledge_analysis.output
        )
        
        return {
            "project_analysis": project_analysis.output,
            "knowledge_analysis": knowledge_analysis.output,
            "combined_insights": combined_insights,
            "recommended_actions": self._prioritize_actions(combined_insights)
        }
    
    async def _document_task_creation(
        self,
        input_data: Dict[str, Any],
        dependencies: Any
    ) -> Dict[str, Any]:
        """Create tasks based on document analysis."""
        
        document_id = input_data["document_id"]
        
        # Step 1: Analyze document content
        doc_analysis = await self.knowledge_agent.run(
            f"Analyze document {document_id} and identify actionable items",
            deps=dependencies.knowledge_deps
        )
        
        # Step 2: Create tasks based on analysis
        tasks_created = []
        for actionable_item in doc_analysis.output.get("actionable_items", []):
            task_result = await self.project_agent.run(
                f"Create a task for: {actionable_item['description']}",
                deps=dependencies.project_deps
            )
            tasks_created.append(task_result.output)
        
        return {
            "document_analysis": doc_analysis.output,
            "tasks_created": tasks_created,
            "workflow_summary": f"Created {len(tasks_created)} tasks from document analysis"
        }

# Agent coordination service
class AgentOrchestrationService:
    """Service for managing agent interactions and workflows."""
    
    def __init__(self, dependencies: Dict[str, Any]):
        self.dependencies = dependencies
        self.coordinator = WorkflowCoordinator()
        self.active_sessions = {}
    
    async def start_agent_session(
        self,
        user_id: str,
        agent_type: str,
        context: Dict[str, Any]
    ) -> str:
        """Start a new agent session for a user."""
        
        session_id = generate_session_id()
        
        session_config = {
            "user_id": user_id,
            "agent_type": agent_type,
            "context": context,
            "created_at": datetime.utcnow(),
            "conversation_history": []
        }
        
        self.active_sessions[session_id] = session_config
        
        return session_id
    
    async def send_message_to_agent(
        self,
        session_id: str,
        message: str,
        additional_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Send a message to an agent in an active session."""
        
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        agent_type = session["agent_type"]
        agent = self.coordinator.agents.get(agent_type)
        
        if not agent:
            raise ValueError(f"Agent type {agent_type} not available")
        
        # Prepare context
        context = {
            **session["context"],
            **(additional_context or {}),
            "conversation_history": session["conversation_history"][-10:]  # Last 10 messages
        }
        
        # Get appropriate dependencies
        deps = self._get_agent_dependencies(agent_type)
        
        # Run agent
        try:
            result = await agent.run(message, deps=deps)
            
            # Update session history
            session["conversation_history"].append({
                "user_message": message,
                "agent_response": result.output,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return {
                "response": result.output,
                "session_id": session_id,
                "agent_type": agent_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return {
                "error": str(e),
                "session_id": session_id,
                "agent_type": agent_type
            }
    
    def _get_agent_dependencies(self, agent_type: str) -> Any:
        """Get appropriate dependencies for agent type."""
        
        if agent_type == "knowledge":
            return self.dependencies["knowledge"]
        elif agent_type == "project":
            return self.dependencies["project"]
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
```

### MCP Tool Integration
```python
# src/mcp/advanced_tools.py
from mcp.server.fastmcp import FastMCP, Context
from typing import List, Dict, Any, Optional
import asyncio

# Advanced MCP server with comprehensive toolset
mcp = FastMCP(
    "ARCHON Advanced MCP Server",
    description="Comprehensive toolset for ARCHON platform integration"
)

@mcp.tool()
async def execute_agent_workflow(
    ctx: Context,
    workflow_type: str,
    parameters: Dict[str, Any],
    agent_preferences: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Execute a complex multi-agent workflow.
    
    Args:
        workflow_type: Type of workflow (project_analysis, document_processing, task_automation)
        parameters: Workflow-specific parameters
        agent_preferences: Optional agent configuration preferences
        
    Returns:
        Workflow execution results with detailed status
    """
    await ctx.info(f"Starting workflow: {workflow_type}")
    
    try:
        # Initialize workflow coordinator
        coordinator = WorkflowCoordinator()
        
        # Prepare dependencies
        dependencies = await prepare_workflow_dependencies(parameters)
        
        # Execute workflow
        results = await coordinator.execute_workflow(
            workflow_type,
            parameters,
            dependencies
        )
        
        await ctx.info(f"Workflow completed successfully")
        
        return {
            "status": "completed",
            "workflow_type": workflow_type,
            "results": results,
            "execution_time": results.get("execution_time"),
            "next_steps": results.get("recommended_actions", [])
        }
        
    except Exception as e:
        await ctx.error(f"Workflow execution failed: {e}")
        return {
            "status": "failed",
            "workflow_type": workflow_type,
            "error": str(e),
            "recovery_suggestions": generate_recovery_suggestions(workflow_type, str(e))
        }

@mcp.tool()
async def batch_document_processing(
    ctx: Context,
    document_ids: List[str],
    processing_type: str,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Process multiple documents in batch with progress tracking.
    
    Args:
        document_ids: List of document IDs to process
        processing_type: Type of processing (embedding, summarization, categorization)
        options: Processing options and configuration
        
    Returns:
        Batch processing results with success/failure details
    """
    await ctx.info(f"Starting batch processing of {len(document_ids)} documents")
    
    results = {
        "processed": [],
        "failed": [],
        "total": len(document_ids),
        "processing_type": processing_type
    }
    
    # Process documents with progress reporting
    for i, doc_id in enumerate(document_ids):
        try:
            await ctx.report_progress(
                progress=(i + 1) / len(document_ids),
                total=1.0,
                message=f"Processing document {i + 1}/{len(document_ids)}"
            )
            
            # Process individual document
            if processing_type == "embedding":
                result = await generate_document_embeddings(doc_id, options)
            elif processing_type == "summarization":
                result = await summarize_document(doc_id, options)
            elif processing_type == "categorization":
                result = await categorize_document(doc_id, options)
            else:
                raise ValueError(f"Unknown processing type: {processing_type}")
            
            results["processed"].append({
                "document_id": doc_id,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            await ctx.warning(f"Failed to process document {doc_id}: {e}")
            results["failed"].append({
                "document_id": doc_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    success_rate = len(results["processed"]) / len(document_ids) * 100
    await ctx.info(f"Batch processing completed: {success_rate:.1f}% success rate")
    
    return {
        **results,
        "success_rate": success_rate,
        "completion_time": datetime.utcnow().isoformat()
    }

@mcp.tool()
async def intelligent_project_insights(
    ctx: Context,
    project_id: str,
    insight_types: List[str],
    time_range: str = "last_30_days"
) -> Dict[str, Any]:
    """Generate intelligent insights about project performance and health.
    
    Args:
        project_id: ID of the project to analyze
        insight_types: Types of insights to generate (productivity, collaboration, risks, trends)
        time_range: Analysis time range (last_7_days, last_30_days, last_quarter)
        
    Returns:
        Comprehensive project insights with actionable recommendations
    """
    await ctx.info(f"Generating insights for project {project_id}")
    
    insights = {}
    
    for insight_type in insight_types:
        try:
            if insight_type == "productivity":
                insights["productivity"] = await analyze_team_productivity(project_id, time_range)
            elif insight_type == "collaboration":
                insights["collaboration"] = await analyze_collaboration_patterns(project_id, time_range)
            elif insight_type == "risks":
                insights["risks"] = await identify_project_risks(project_id, time_range)
            elif insight_type == "trends":
                insights["trends"] = await analyze_project_trends(project_id, time_range)
            
            await ctx.debug(f"Generated {insight_type} insights")
            
        except Exception as e:
            await ctx.warning(f"Failed to generate {insight_type} insights: {e}")
            insights[insight_type] = {"error": str(e)}
    
    # Generate overall recommendations
    recommendations = await generate_project_recommendations(insights)
    
    return {
        "project_id": project_id,
        "analysis_period": time_range,
        "insights": insights,
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat()
    }

@mcp.resource("workspace://status/{workspace_id}")
async def get_workspace_status(workspace_id: str) -> str:
    """Get comprehensive workspace status and health metrics.
    
    Args:
        workspace_id: Workspace identifier
        
    Returns:
        Formatted workspace status report
    """
    workspace = await get_workspace_by_id(workspace_id)
    if not workspace:
        raise ValueError(f"Workspace {workspace_id} not found")
    
    # Gather workspace metrics
    projects = await get_workspace_projects(workspace_id)
    users = await get_workspace_users(workspace_id)
    documents = await get_workspace_documents(workspace_id)
    tasks = await get_workspace_tasks(workspace_id)
    
    # Calculate health metrics
    active_projects = len([p for p in projects if p.status == "active"])
    completion_rate = calculate_task_completion_rate(tasks)
    collaboration_score = calculate_collaboration_score(users, tasks)
    
    status_report = f"""
    # Workspace Status Report: {workspace.name}
    
    ## Overview
    - **Total Projects:** {len(projects)} ({active_projects} active)
    - **Team Members:** {len(users)}
    - **Documents:** {len(documents)}
    - **Tasks:** {len(tasks)}
    
    ## Health Metrics
    - **Task Completion Rate:** {completion_rate:.1f}%
    - **Collaboration Score:** {collaboration_score:.1f}/10
    - **Document Activity:** {await calculate_document_activity(documents)}
    
    ## Recent Activity
    {await get_recent_workspace_activity(workspace_id, limit=5)}
    
    ## Recommendations
    {await generate_workspace_recommendations(workspace_id)}
    """
    
    return status_report

# Configure MCP server for production
if __name__ == "__main__":
    import uvicorn
    
    # Production configuration
    uvicorn.run(
        mcp.sse_app("/mcp"),
        host="0.0.0.0",
        port=8001,
        log_level="info",
        access_log=True,
        reload=False  # Disable in production
    )
```

---

## 11. Performance Optimization & Monitoring

### Database Performance
- **Connection Pooling:** Optimized connection management for high concurrency
- **Query Optimization:** Efficient queries with proper indexing strategies
- **Vector Search Performance:** HNSW indexing with tuned parameters
- **Caching Strategy:** Multi-layer caching with Redis and application-level cache

#### Database Optimization Strategies
```python
# Database connection pooling and optimization
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import QueuePool
from redis.asyncio import Redis
import aioredis

class DatabaseManager:
    """Optimized database connection and query management."""
    
    def __init__(self, database_url: str, redis_url: str):
        # Optimized PostgreSQL connection pool
        self.engine = create_async_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=20,          # Base pool size
            max_overflow=30,       # Additional connections
            pool_pre_ping=True,    # Validate connections
            pool_recycle=3600,     # Recycle connections hourly
            echo=False,            # Disable query logging in production
            query_cache_size=1200  # Increase query cache
        )
        
        # Redis connection pool
        self.redis = Redis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
            retry_on_timeout=True,
            socket_keepalive=True,
            socket_keepalive_options={},
        )
        
        # Query cache configuration
        self.query_cache = {}
        self.cache_ttl = {
            "documents": 300,      # 5 minutes
            "projects": 600,       # 10 minutes
            "users": 900,          # 15 minutes
            "vectors": 1800        # 30 minutes
        }
    
    async def get_session(self) -> AsyncSession:
        """Get optimized database session."""
        return AsyncSession(
            self.engine,
            expire_on_commit=False,
            autoflush=False        # Manual flush for better control
        )
    
    async def execute_cached_query(
        self,
        cache_key: str,
        query_func: callable,
        ttl: int = 300
    ) -> Any:
        """Execute query with Redis caching."""
        
        # Try cache first
        cached_result = await self.redis.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        # Execute query
        result = await query_func()
        
        # Cache result
        await self.redis.setex(
            cache_key,
            ttl,
            json.dumps(result, default=str)
        )
        
        return result

# Vector search optimization
class OptimizedVectorSearch:
    """High-performance vector search with caching and batching."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.embedding_cache = {}
        self.search_cache = {}
    
    async def search_with_cache(
        self,
        query_embedding: List[float],
        limit: int = 10,
        project_id: Optional[str] = None,
        cache_duration: int = 300
    ) -> List[dict]:
        """Vector search with intelligent caching."""
        
        # Create cache key from embedding hash and parameters
        cache_key = f"vector_search:{hash(tuple(query_embedding))}:{limit}:{project_id}"
        
        return await self.db.execute_cached_query(
            cache_key,
            lambda: self._execute_vector_search(query_embedding, limit, project_id),
            cache_duration
        )
    
    async def _execute_vector_search(
        self,
        query_embedding: List[float],
        limit: int,
        project_id: Optional[str]
    ) -> List[dict]:
        """Execute optimized vector search query."""
        
        async with self.db.get_session() as session:
            # Optimized vector search with proper indexing
            query = """
            SELECT 
                d.id,
                d.title,
                d.content,
                d.metadata,
                1 - (d.embedding <=> $1::vector) as similarity
            FROM documents d
            WHERE 
                ($2::bigint IS NULL OR d.project_id = $2)
                AND d.embedding <=> $1::vector < 0.5  -- Pre-filter for performance
            ORDER BY d.embedding <=> $1::vector
            LIMIT $3
            """
            
            result = await session.execute(
                text(query),
                (query_embedding, project_id, limit)
            )
            
            return [
                {
                    "id": row.id,
                    "title": row.title,
                    "content": row.content[:500],  # Truncate for performance
                    "metadata": row.metadata,
                    "similarity": float(row.similarity)
                }
                for row in result.fetchall()
            ]
    
    async def batch_vector_search(
        self,
        queries: List[Dict[str, Any]]
    ) -> List[List[dict]]:
        """Batch multiple vector searches for efficiency."""
        
        # Execute searches concurrently
        tasks = [
            self.search_with_cache(
                query["embedding"],
                query.get("limit", 10),
                query.get("project_id")
            )
            for query in queries
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions gracefully
        return [
            result if not isinstance(result, Exception) else []
            for result in results
        ]

# Application-level caching
from cachetools import TTLCache
from functools import wraps

class ApplicationCache:
    """Application-level caching for expensive operations."""
    
    def __init__(self):
        self.caches = {
            "embeddings": TTLCache(maxsize=1000, ttl=3600),     # 1 hour
            "documents": TTLCache(maxsize=5000, ttl=1800),      # 30 minutes
            "users": TTLCache(maxsize=1000, ttl=2700),          # 45 minutes
            "projects": TTLCache(maxsize=500, ttl=1800)         # 30 minutes
        }
    
    def cached(self, cache_type: str, key_func: callable = None):
        """Decorator for caching function results."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    cache_key = f"{func.__name__}:{hash(tuple(args))}:{hash(tuple(sorted(kwargs.items())))}"
                
                # Check cache
                cache = self.caches.get(cache_type)
                if cache and cache_key in cache:
                    return cache[cache_key]
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Store in cache
                if cache:
                    cache[cache_key] = result
                
                return result
            return wrapper
        return decorator

# Usage example
app_cache = ApplicationCache()

@app_cache.cached("embeddings", lambda text: f"embed:{hash(text)}")
async def generate_embedding_cached(text: str) -> List[float]:
    """Generate embedding with caching."""
    return await embedding_service.generate_embedding(text)

@app_cache.cached("documents", lambda doc_id: f"doc:{doc_id}")
async def get_document_cached(doc_id: str) -> dict:
    """Get document with caching."""
    return await document_service.get_document(doc_id)
```

### Frontend Performance Optimization
```typescript
// Performance optimization for React frontend
import { memo, useMemo, useCallback, lazy, Suspense } from 'react';
import { QueryClient } from '@tanstack/react-query';
import { debounce, throttle } from 'lodash-es';

// Query client optimization
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,        // 5 minutes
      cacheTime: 10 * 60 * 1000,       // 10 minutes
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      retry: (failureCount, error) => {
        // Smart retry logic
        if (error.status === 404 || error.status === 403) {
          return false;
        }
        return failureCount < 3;
      },
    },
    mutations: {
      retry: 1,
    },
  },
});

// Optimized component patterns
interface DocumentListProps {
  projectId: string;
  searchQuery?: string;
}

export const DocumentList = memo<DocumentListProps>(({ projectId, searchQuery }) => {
  // Debounced search to reduce API calls
  const debouncedSearch = useMemo(
    () => debounce((query: string) => {
      // Trigger search
      queryClient.invalidateQueries(['documents', projectId]);
    }, 300),
    [projectId]
  );

  // Memoized filter function
  const filterDocuments = useCallback((docs: Document[], query: string) => {
    if (!query) return docs;
    
    const lowercaseQuery = query.toLowerCase();
    return docs.filter(doc => 
      doc.title.toLowerCase().includes(lowercaseQuery) ||
      doc.content.toLowerCase().includes(lowercaseQuery)
    );
  }, []);

  // Optimized data fetching with pagination
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading
  } = useInfiniteQuery({
    queryKey: ['documents', projectId, searchQuery],
    queryFn: ({ pageParam = 0 }) => fetchDocuments({
      projectId,
      page: pageParam,
      limit: 20,
      search: searchQuery
    }),
    getNextPageParam: (lastPage, pages) => {
      return lastPage.hasNext ? pages.length : undefined;
    },
    enabled: !!projectId,
    staleTime: 5 * 60 * 1000,
  });

  // Virtual scrolling for large lists
  const { items, measureElement } = useVirtualizer({
    count: data?.pages.flatMap(page => page.documents).length ?? 0,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 120,
  });

  if (isLoading) return <DocumentListSkeleton />;

  return (
    <div ref={parentRef} className="document-list-container">
      <div className="document-list-content">
        {items.map((virtualItem) => {
          const document = data?.pages
            .flatMap(page => page.documents)
            [virtualItem.index];
          
          return (
            <div
              key={virtualItem.key}
              ref={measureElement}
              className="document-item"
              style={{
                transform: `translateY(${virtualItem.start}px)`,
              }}
            >
              <DocumentCard document={document} />
            </div>
          );
        })}
      </div>
      
      {/* Infinite scroll trigger */}
      <InfiniteScrollTrigger
        hasNextPage={hasNextPage}
        isFetchingNextPage={isFetchingNextPage}
        fetchNextPage={fetchNextPage}
      />
    </div>
  );
});

// Code splitting and lazy loading
const AdminPanel = lazy(() => import('./AdminPanel'));
const AnalyticsDashboard = lazy(() => import('./AnalyticsDashboard'));
const DocumentEditor = lazy(() => import('./DocumentEditor'));

export const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/documents" element={<DocumentList />} />
      <Route 
        path="/admin" 
        element={
          <Suspense fallback={<AdminLoadingSkeleton />}>
            <AdminPanel />
          </Suspense>
        } 
      />
      <Route 
        path="/analytics" 
        element={
          <Suspense fallback={<AnalyticsLoadingSkeleton />}>
            <AnalyticsDashboard />
          </Suspense>
        } 
      />
      <Route 
        path="/documents/:id/edit" 
        element={
          <Suspense fallback={<EditorLoadingSkeleton />}>
            <DocumentEditor />
          </Suspense>
        } 
      />
    </Routes>
  );
};

// Performance monitoring hooks
export const usePerformanceMonitoring = () => {
  useEffect(() => {
    // Monitor Core Web Vitals
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(console.log);
      getFID(console.log);
      getFCP(console.log);
      getLCP(console.log);
      getTTFB(console.log);
    });
  }, []);
};

// Bundle size optimization
export const optimizedImports = {
  // Use specific imports instead of barrel exports
  lodash: {
    // ❌ Bad: import _ from 'lodash';
    // ✅ Good: import { debounce, throttle } from 'lodash-es';
  },
  
  // Tree-shakeable icon imports
  icons: {
    // ❌ Bad: import * as Icons from 'lucide-react';
    // ✅ Good: import { Search, Plus, Settings } from 'lucide-react';
  },
  
  // Date library optimization
  dates: {
    // ✅ Use date-fns with specific function imports
    // import { formatDistanceToNow, parseISO } from 'date-fns';
  }
};
```

### Monitoring & Observability
```python
# Comprehensive monitoring setup
import logging
import time
import psutil
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from datadog import initialize, statsd
import structlog

# Structured logging configuration
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'archon_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'archon_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

VECTOR_SEARCH_DURATION = Histogram(
    'archon_vector_search_duration_seconds',
    'Vector search operation duration',
    ['index_type', 'result_count']
)

ACTIVE_CONNECTIONS = Gauge(
    'archon_active_connections',
    'Number of active database connections'
)

DOCUMENT_PROCESSING_TIME = Histogram(
    'archon_document_processing_seconds',
    'Document processing time',
    ['processing_type', 'document_size_category']
)

# Performance monitoring middleware
from fastapi import Request, Response
import time

@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    """Comprehensive request monitoring."""
    start_time = time.time()
    
    # Extract request information
    method = request.method
    endpoint = request.url.path
    
    # Add request ID for tracing
    request_id = str(uuid.uuid4())[:8]
    
    # Structured logging
    logger.info(
        "Request started",
        request_id=request_id,
        method=method,
        endpoint=endpoint,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host
    )
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Update metrics
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
        
        # Log response
        logger.info(
            "Request completed",
            request_id=request_id,
            status_code=response.status_code,
            duration_ms=duration * 1000,
            response_size=response.headers.get("content-length", 0)
        )
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        
        # Log error
        logger.error(
            "Request failed",
            request_id=request_id,
            error=str(e),
            duration_ms=duration * 1000,
            exc_info=True
        )
        
        # Update error metrics
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=500
        ).inc()
        
        raise

# Database performance monitoring
class DatabaseMonitor:
    """Monitor database performance and health."""
    
    def __init__(self, engine):
        self.engine = engine
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start database monitoring tasks."""
        asyncio.create_task(self.monitor_connections())
        asyncio.create_task(self.monitor_query_performance())
    
    async def monitor_connections(self):
        """Monitor database connection pool."""
        while True:
            try:
                pool = self.engine.pool
                ACTIVE_CONNECTIONS.set(pool.checkedout())
                
                # Log pool stats
                logger.debug(
                    "Connection pool status",
                    size=pool.size(),
                    checked_out=pool.checkedout(),
                    overflow=pool.overflow(),
                    checked_in=pool.checkedin()
                )
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error("Connection monitoring failed", error=str(e))
                await asyncio.sleep(30)
    
    async def monitor_query_performance(self):
        """Monitor slow queries and performance."""
        while True:
            try:
                async with self.engine.begin() as conn:
                    # Check for slow queries
                    slow_queries = await conn.execute(text("""
                        SELECT query, mean_exec_time, calls
                        FROM pg_stat_statements
                        WHERE mean_exec_time > 1000  -- Queries slower than 1 second
                        ORDER BY mean_exec_time DESC
                        LIMIT 10
                    """))
                    
                    for query in slow_queries.fetchall():
                        logger.warning(
                            "Slow query detected",
                            query=query.query[:100],
                            avg_time_ms=query.mean_exec_time,
                            call_count=query.calls
                        )
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error("Query monitoring failed", error=str(e))
                await asyncio.sleep(600)

# Vector search performance monitoring
async def monitor_vector_search(
    embedding: List[float],
    limit: int,
    search_function: callable
) -> List[dict]:
    """Monitor vector search performance."""
    start_time = time.time()
    
    try:
        # Categorize search by result limit
        if limit <= 5:
            size_category = "small"
        elif limit <= 20:
            size_category = "medium"
        else:
            size_category = "large"
        
        # Execute search
        results = await search_function(embedding, limit)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Update metrics
        VECTOR_SEARCH_DURATION.labels(
            index_type="hnsw",
            result_count=len(results)
        ).observe(duration)
        
        # Log performance
        logger.info(
            "Vector search completed",
            duration_ms=duration * 1000,
            result_count=len(results),
            size_category=size_category
        )
        
        return results
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "Vector search failed",
            error=str(e),
            duration_ms=duration * 1000,
            limit=limit
        )
        raise

# System health monitoring
class SystemHealthMonitor:
    """Monitor system resource usage and health."""
    
    def __init__(self):
        self.cpu_gauge = Gauge('archon_cpu_usage_percent', 'CPU usage percentage')
        self.memory_gauge = Gauge('archon_memory_usage_percent', 'Memory usage percentage')
        self.disk_gauge = Gauge('archon_disk_usage_percent', 'Disk usage percentage')
        
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start system monitoring."""
        asyncio.create_task(self.monitor_system_resources())
    
    async def monitor_system_resources(self):
        """Monitor CPU, memory, and disk usage."""
        while True:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_gauge.set(cpu_percent)
                
                # Memory usage
                memory = psutil.virtual_memory()
                self.memory_gauge.set(memory.percent)
                
                # Disk usage
                disk = psutil.disk_usage('/')
                disk_percent = (disk.used / disk.total) * 100
                self.disk_gauge.set(disk_percent)
                
                # Log warnings for high usage
                if cpu_percent > 80:
                    logger.warning("High CPU usage", cpu_percent=cpu_percent)
                
                if memory.percent > 85:
                    logger.warning("High memory usage", memory_percent=memory.percent)
                
                if disk_percent > 90:
                    logger.warning("High disk usage", disk_percent=disk_percent)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error("System monitoring failed", error=str(e))
                await asyncio.sleep(60)

# Health check endpoints
@router.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": app_version,
        "checks": {}
    }
    
    try:
        # Database health
        async with get_database() as db:
            await db.execute(text("SELECT 1"))
            health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    try:
        # Redis health
        await redis_client.ping()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    try:
        # Vector search health
        test_embedding = [0.1] * 384
        await vector_search_service.health_check(test_embedding)
        health_status["checks"]["vector_search"] = "healthy"
    except Exception as e:
        health_status["checks"]["vector_search"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Return appropriate status code
    status_code = 200 if health_status["status"] == "healthy" else 503
    
    return Response(
        content=json.dumps(health_status),
        status_code=status_code,
        media_type="application/json"
    )

# Initialize monitoring on startup
@app.on_event("startup")
async def start_monitoring():
    """Initialize all monitoring systems."""
    
    # Start Prometheus metrics server
    start_http_server(9090)
    
    # Initialize system health monitoring
    SystemHealthMonitor()
    
    # Initialize database monitoring
    DatabaseMonitor(engine)
    
    logger.info("Monitoring systems initialized")
```

---

## 12. Production Deployment & DevOps

### Container Optimization
```dockerfile
# Multi-stage Dockerfile for Python backend
FROM python:3.12-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim as production

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from base stage
COPY --from=base /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY migration/ ./migration/

# Set proper ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.server.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# Frontend Dockerfile
FROM node:20-alpine as frontend-base

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Build stage
FROM frontend-base as build

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine as frontend-production

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### Kubernetes Deployment
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: archon-reloaded
  labels:
    name: archon-reloaded

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: archon-config
  namespace: archon-reloaded
data:
  DATABASE_URL: "postgresql://archon:password@postgres:5432/archon"
  REDIS_URL: "redis://redis:6379"
  LOG_LEVEL: "INFO"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: archon-secrets
  namespace: archon-reloaded
type: Opaque
data:
  openai-api-key: <base64-encoded-key>
  jwt-secret: <base64-encoded-secret>
  database-password: <base64-encoded-password>

---
# k8s/postgres.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: archon-reloaded
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: pgvector/pgvector:pg15
        env:
        - name: POSTGRES_DB
          value: archon
        - name: POSTGRES_USER
          value: archon
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: database-password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc

---
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: archon-backend
  namespace: archon-reloaded
spec:
  replicas: 3
  selector:
    matchLabels:
      app: archon-backend
  template:
    metadata:
      labels:
        app: archon-backend
    spec:
      containers:
      - name: backend
        image: archon/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: archon-config
              key: DATABASE_URL
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: archon-config
              key: REDIS_URL
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: openai-api-key
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: archon-secrets
              key: jwt-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

---
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: archon-frontend
  namespace: archon-reloaded
spec:
  replicas: 2
  selector:
    matchLabels:
      app: archon-frontend
  template:
    metadata:
      labels:
        app: archon-frontend
    spec:
      containers:
      - name: frontend
        image: archon/frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
# k8s/services.yaml
apiVersion: v1
kind: Service
metadata:
  name: archon-backend-service
  namespace: archon-reloaded
spec:
  selector:
    app: archon-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: archon-frontend-service
  namespace: archon-reloaded
spec:
  selector:
    app: archon-frontend
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: archon-ingress
  namespace: archon-reloaded
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/websocket-services: "archon-backend-service"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
spec:
  tls:
  - hosts:
    - archon.example.com
    secretName: archon-tls
  rules:
  - host: archon.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: archon-backend-service
            port:
              number: 8000
      - path: /socket.io
        pathType: Prefix
        backend:
          service:
            name: archon-backend-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: archon-frontend-service
            port:
              number: 80

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: archon-backend-hpa
  namespace: archon-reloaded
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: archon-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### CI/CD Pipeline
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_archon
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install uv
      run: pip install uv
    
    - name: Install dependencies
      run: |
        cd python
        uv sync --frozen --all-extras
    
    - name: Run linting
      run: |
        cd python
        uv run ruff check .
        uv run ruff format --check .
    
    - name: Run type checking
      run: |
        cd python
        uv run pyright
    
    - name: Run tests
      run: |
        cd python
        uv run pytest --cov=src --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:test@localhost:5432/test_archon
        REDIS_URL: redis://localhost:6379
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./python/coverage.xml

  test-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: archon-ui-main/package-lock.json
    
    - name: Install dependencies
      run: |
        cd archon-ui-main
        npm ci
    
    - name: Run linting
      run: |
        cd archon-ui-main
        npm run lint
    
    - name: Run type checking
      run: |
        cd archon-ui-main
        npm run type-check
    
    - name: Run tests
      run: |
        cd archon-ui-main
        npm run test:coverage
    
    - name: Build application
      run: |
        cd archon-ui-main
        npm run build

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build-and-push:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
    
    - name: Build and push backend image
      uses: docker/build-push-action@v5
      with:
        context: ./python
        file: ./python/Dockerfile
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/backend:latest
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Build and push frontend image
      uses: docker/build-push-action@v5
      with:
        context: ./archon-ui-main
        file: ./archon-ui-main/Dockerfile
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/frontend:latest
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v1
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG }}
    
    - name: Deploy to staging
      run: |
        kubectl apply -f k8s/ -n archon-staging
        kubectl rollout restart deployment/archon-backend -n archon-staging
        kubectl rollout restart deployment/archon-frontend -n archon-staging
        kubectl rollout status deployment/archon-backend -n archon-staging
        kubectl rollout status deployment/archon-frontend -n archon-staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v1
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
    
    - name: Deploy to production
      run: |
        kubectl apply -f k8s/ -n archon-production
        kubectl rollout restart deployment/archon-backend -n archon-production
        kubectl rollout restart deployment/archon-frontend -n archon-production
        kubectl rollout status deployment/archon-backend -n archon-production
        kubectl rollout status deployment/archon-frontend -n archon-production
    
    - name: Verify deployment
      run: |
        kubectl get pods -n archon-production
        kubectl get services -n archon-production
```

---

## 13. Security Hardening & Best Practices

### Application Security Checklist
- **Authentication:** Multi-factor authentication with JWT tokens
- **Authorization:** Role-based access control with fine-grained permissions
- **Input Validation:** Comprehensive validation and sanitization
- **Output Encoding:** Prevent XSS and injection attacks
- **Secrets Management:** Secure handling of API keys and credentials
- **Network Security:** TLS encryption and secure communication protocols

### Security Configuration
```python
# Security middleware and configuration
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets

app = FastAPI()

# Security headers middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self' wss: https:; "
        "font-src 'self' data:; "
        "object-src 'none'; "
        "media-src 'self'; "
        "frame-src 'none';"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=(), "
        "payment=(), usb=(), magnetometer=(), gyroscope=(), speaker=()"
    )
    
    return response

# HTTPS redirect in production
if app_config.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=app_config.allowed_hosts
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Session middleware with secure configuration
app.add_middleware(
    SessionMiddleware,
    secret_key=app_config.session_secret,
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=app_config.environment == "production"
)

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Input validation and sanitization
import bleach
import html
from pydantic import validator

class SecureTextInput(BaseModel):
    """Secure text input with validation and sanitization."""
    text: str
    
    @validator('text')
    def sanitize_text(cls, v):
        """Sanitize and validate text input."""
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        
        # Remove potentially dangerous HTML tags
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li']
        allowed_attributes = {}
        
        sanitized = bleach.clean(
            v,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
        
        # HTML encode for additional safety
        sanitized = html.escape(sanitized)
        
        # Length validation
        if len(sanitized) > 10000:
            raise ValueError("Text exceeds maximum length of 10,000 characters")
        
        return sanitized

# SQL injection prevention
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

async def safe_database_query(
    session: AsyncSession,
    query: str,
    parameters: dict = None
) -> Any:
    """Execute database query with parameterization to prevent SQL injection."""
    try:
        # Always use parameterized queries
        if parameters:
            result = await session.execute(text(query), parameters)
        else:
            result = await session.execute(text(query))
        
        return result.fetchall()
        
    except SQLAlchemyError as e:
        logger.error(f"Database query failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

# File upload security
import magic
from pathlib import Path

ALLOWED_MIME_TYPES = {
    'text/plain',
    'text/markdown',
    'application/pdf',
    'application/json',
    'image/jpeg',
    'image/png',
    'image/webp'
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_file_upload(file: UploadFile) -> None:
    """Comprehensive file upload validation."""
    
    # Read file content
    content = await file.read()
    await file.seek(0)  # Reset file pointer
    
    # Size validation
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # MIME type validation using python-magic
    detected_type = magic.from_buffer(content, mime=True)
    if detected_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {detected_type} is not allowed"
        )
    
    # Filename validation
    if not file.filename or '..' in file.filename or '/' in file.filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )
    
    # Extension validation
    file_extension = Path(file.filename).suffix.lower()
    allowed_extensions = {'.txt', '.md', '.pdf', '.json', '.jpg', '.jpeg', '.png', '.webp'}
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File extension {file_extension} is not allowed"
        )

# API key authentication
import hashlib
import hmac

class APIKeyAuth:
    """Secure API key authentication."""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()
    
    def generate_api_key(self, user_id: str) -> tuple[str, str]:
        """Generate API key and secret for a user."""
        key = secrets.token_urlsafe(32)
        secret = secrets.token_urlsafe(64)
        
        # Create HMAC signature
        signature = hmac.new(
            self.secret_key,
            f"{user_id}:{key}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        return key, f"{secret}:{signature}"
    
    def verify_api_key(self, api_key: str, api_secret: str, user_id: str) -> bool:
        """Verify API key and secret."""
        try:
            secret_part, signature = api_secret.split(':', 1)
            
            # Recreate signature
            expected_signature = hmac.new(
                self.secret_key,
                f"{user_id}:{api_key}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Use constant-time comparison
            return hmac.compare_digest(signature, expected_signature)
            
        except (ValueError, AttributeError):
            return False

# Environment-specific security configuration
class SecurityConfig:
    """Environment-specific security settings."""
    
    def __init__(self, environment: str):
        self.environment = environment
        
        if environment == "production":
            self.cookie_secure = True
            self.cookie_samesite = "strict"
            self.session_timeout = 3600  # 1 hour
            self.max_login_attempts = 3
            self.password_min_length = 12
            self.require_mfa = True
            
        elif environment == "staging":
            self.cookie_secure = True
            self.cookie_samesite = "lax"
            self.session_timeout = 7200  # 2 hours
            self.max_login_attempts = 5
            self.password_min_length = 8
            self.require_mfa = False
            
        else:  # development
            self.cookie_secure = False
            self.cookie_samesite = "lax"
            self.session_timeout = 86400  # 24 hours
            self.max_login_attempts = 10
            self.password_min_length = 6
            self.require_mfa = False

# Password security
import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password with bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def validate_password_strength(password: str) -> bool:
    """Validate password meets security requirements."""
    if len(password) < security_config.password_min_length:
        return False
    
    # Check for required character types
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    return all([has_upper, has_lower, has_digit, has_special])
```

---

## 14. Documentation Standards & Guidelines

### Docusaurus Documentation Site
- **Architecture Documentation:** Comprehensive system architecture guides
- **API Documentation:** Auto-generated OpenAPI documentation
- **User Guides:** Step-by-step usage instructions
- **Developer Guides:** Setup and contribution documentation

#### Documentation Structure
```markdown
docs/
├── intro.md                    # Project introduction and overview
├── getting-started/            # Quick start guides
│   ├── installation.md         # Installation instructions
│   ├── configuration.md        # Basic configuration
│   └── first-steps.md          # First steps tutorial
├── architecture/               # System architecture
│   ├── overview.md             # High-level architecture
│   ├── microservices.md        # Microservices design
│   ├── database.md             # Database schema and design
│   └── api-design.md           # API design principles
├── user-guide/                 # End-user documentation
│   ├── dashboard.md            # Dashboard usage
│   ├── documents.md            # Document management
│   ├── projects.md             # Project management
│   └── collaboration.md        # Real-time collaboration
├── developer-guide/            # Developer documentation
│   ├── setup.md                # Development environment
│   ├── contributing.md         # Contribution guidelines
│   ├── testing.md              # Testing guidelines
│   └── deployment.md           # Deployment procedures
├── api/                        # API documentation
│   ├── overview.md             # API overview
│   ├── authentication.md       # Auth documentation
│   ├── endpoints/              # Individual endpoint docs
│   └── websockets.md           # WebSocket documentation
├── integrations/               # Integration guides
│   ├── mcp.md                  # MCP integration
│   ├── ai-agents.md            # AI agent integration
│   └── third-party.md          # Third-party integrations
└── troubleshooting/            # Common issues and solutions
    ├── faq.md                  # Frequently asked questions
    ├── common-errors.md        # Common error resolutions
    └── performance.md          # Performance troubleshooting
```

#### Docusaurus Configuration
```javascript
// docusaurus.config.js
export default {
  title: 'ARCHON RELOADED',
  tagline: 'Next-Generation AI Development Platform',
  url: 'https://docs.archon.dev',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  
  organizationName: 'archon-ai',
  projectName: 'archon-reloaded',
  
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/archon-ai/archon-reloaded/tree/main/docs/',
          remarkPlugins: [
            [require('@docusaurus/remark-plugin-npm2yarn'), {sync: true}],
          ],
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/archon-ai/archon-reloaded/tree/main/docs/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
        },
      },
    ],
  ],
  
  themeConfig: {
    image: 'img/archon-social-card.jpg',
    navbar: {
      title: 'ARCHON RELOADED',
      logo: {
        alt: 'ARCHON Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/archon-ai/archon-reloaded',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/getting-started/installation',
            },
            {
              label: 'API Reference',
              to: '/docs/api/overview',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://discord.gg/archon',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/archon_ai',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/archon-ai/archon-reloaded',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} ARCHON AI. Built with Docusaurus.`,
    },
    
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
      additionalLanguages: ['python', 'typescript', 'docker', 'yaml'],
    },
    
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'archon-docs',
      contextualSearch: true,
      searchParameters: {},
      searchPagePath: 'search',
    },
  },
  
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'api',
        path: 'api',
        routeBasePath: 'api',
        sidebarPath: './sidebarsApi.js',
      },
    ],
  ],
};
```

### Code Documentation Standards
```python
# Python docstring standards (Google style)
def search_knowledge_base(
    query: str,
    limit: int = 10,
    project_id: Optional[str] = None,
    include_embeddings: bool = False
) -> SearchResults:
    """Search the knowledge base using vector similarity.
    
    This function performs a semantic search across all documents in the knowledge
    base using vector embeddings. It supports filtering by project and can optionally
    return the embeddings used for similarity calculation.
    
    Args:
        query: The search query in natural language. Should be at least 3 characters.
        limit: Maximum number of results to return. Must be between 1 and 100.
        project_id: Optional project ID to filter results. If None, searches all projects.
        include_embeddings: Whether to include embeddings in the response. 
            Defaults to False for performance.
    
    Returns:
        SearchResults object containing:
            - documents: List of matching documents with similarity scores
            - total_results: Total number of matches found
            - search_time_ms: Time taken to execute the search
            - query_embedding: The embedding used for search (if include_embeddings=True)
    
    Raises:
        ValueError: If query is too short or limit is out of range.
        DatabaseError: If the database connection fails.
        EmbeddingError: If embedding generation fails.
    
    Example:
        >>> results = search_knowledge_base(
        ...     query="machine learning algorithms",
        ...     limit=5,
        ...     project_id="proj_123"
        ... )
        >>> print(f"Found {len(results.documents)} documents")
        Found 5 documents
        
        >>> for doc in results.documents:
        ...     print(f"{doc.title}: {doc.similarity:.3f}")
        Deep Learning Basics: 0.892
        ML Model Training: 0.845
    
    Note:
        This function uses cached embeddings when available to improve performance.
        Vector similarity is calculated using cosine distance with HNSW indexing.
    """
    # Implementation here
    pass

# TypeScript documentation standards (JSDoc)
/**
 * Manages real-time collaboration features for document editing.
 * 
 * This class handles WebSocket connections, conflict resolution, and
 * synchronized editing state across multiple users. It implements
 * operational transformation for maintaining document consistency.
 * 
 * @example
 * ```typescript
 * const collaboration = new DocumentCollaboration({
 *   documentId: 'doc_123',
 *   userId: 'user_456',
 *   socketUrl: 'ws://localhost:8000'
 * });
 * 
 * await collaboration.connect();
 * collaboration.on('change', (change) => {
 *   console.log('Document changed:', change);
 * });
 * ```
 * 
 * @public
 */
export class DocumentCollaboration {
  /**
   * Configuration options for the collaboration session.
   */
  private readonly config: CollaborationConfig;
  
  /**
   * WebSocket connection for real-time communication.
   */
  private socket: Socket | null = null;
  
  /**
   * Creates a new document collaboration instance.
   * 
   * @param config - Configuration options for the collaboration session
   * @throws {Error} When configuration is invalid
   */
  constructor(config: CollaborationConfig) {
    if (!config.documentId || !config.userId) {
      throw new Error('Document ID and User ID are required');
    }
    
    this.config = config;
  }
  
  /**
   * Establishes connection to the collaboration server.
   * 
   * @returns Promise that resolves when connection is established
   * @throws {ConnectionError} When unable to connect to server
   * @throws {AuthenticationError} When authentication fails
   * 
   * @example
   * ```typescript
   * try {
   *   await collaboration.connect();
   *   console.log('Connected successfully');
   * } catch (error) {
   *   console.error('Connection failed:', error);
   * }
   * ```
   */
  async connect(): Promise<void> {
    // Implementation here
  }
  
  /**
   * Applies a change to the document with conflict resolution.
   * 
   * @param change - The change to apply to the document
   * @param options - Additional options for change application
   * @returns Promise resolving to the applied change with any transformations
   * 
   * @throws {ValidationError} When change format is invalid
   * @throws {ConflictError} When change conflicts cannot be resolved
   * 
   * @internal This method is used internally by the editor
   */
  async applyChange(
    change: DocumentChange, 
    options: ChangeOptions = {}
  ): Promise<AppliedChange> {
    // Implementation here
  }
}

/**
 * Configuration options for document collaboration.
 * 
 * @public
 */
export interface CollaborationConfig {
  /** Unique identifier for the document being edited */
  documentId: string;
  
  /** Unique identifier for the current user */
  userId: string;
  
  /** WebSocket server URL for real-time communication */
  socketUrl: string;
  
  /** 
   * Authentication token for secure connections 
   * @defaultValue undefined
   */
  authToken?: string;
  
  /** 
   * Maximum time to wait for server responses in milliseconds
   * @defaultValue 5000
   */
  timeout?: number;
  
  /** 
   * Whether to enable debug logging
   * @defaultValue false
   */
  debug?: boolean;
}
```

---

## 15. Troubleshooting Guide & Common Issues

### Development Environment Issues

#### Python/uv Issues
```bash
# Common uv problems and solutions

# Problem: uv command not found
# Solution: Install uv properly
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Problem: Virtual environment not activating
# Solution: Recreate virtual environment
rm -rf .venv
uv sync --frozen

# Problem: Package conflicts
# Solution: Clear cache and reinstall
uv cache clean
uv sync --frozen --refresh

# Problem: Import errors after installation
# Solution: Check Python path and virtual environment
uv run python -c "import sys; print(sys.path)"
uv run which python
```

#### Node.js/npm Issues
```bash
# Common Node.js problems and solutions

# Problem: npm install fails with permission errors
# Solution: Use node version manager and fix permissions
nvm use 20
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH

# Problem: Package version conflicts
# Solution: Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Problem: Vite build fails
# Solution: Check Node.js version and memory limits
node --version  # Should be 20.x
export NODE_OPTIONS="--max_old_space_size=4096"
npm run build
```

#### Docker Issues
```bash
# Common Docker problems and solutions

# Problem: Docker out of space
# Solution: Clean up Docker resources
docker system prune -a
docker volume prune
docker network prune

# Problem: Container won't start
# Solution: Check logs and configuration
docker-compose logs -f <service-name>
docker-compose config  # Validate compose file

# Problem: Database connection issues
# Solution: Verify network and timing
docker-compose up -d postgres
docker-compose exec postgres pg_isready -U archon
# Wait for database to be ready before starting other services
```

### Database Issues

#### PostgreSQL/pgvector Problems
```sql
-- Common database issues and solutions

-- Problem: pgvector extension not found
-- Solution: Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions;

-- Problem: Vector index creation fails
-- Solution: Check table data and recreate index
SELECT COUNT(*) FROM documents WHERE embedding IS NOT NULL;
-- Ensure table has data before creating HNSW index
DROP INDEX IF EXISTS documents_embedding_idx;
CREATE INDEX documents_embedding_idx ON documents 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Problem: Slow vector searches
-- Solution: Optimize index and queries
-- Check index usage
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM documents 
ORDER BY embedding <=> '[0.1,0.2,...]'::vector 
LIMIT 10;

-- Tune HNSW parameters
SET hnsw.ef_search = 100;  -- Increase for better recall

-- Problem: Connection pool exhaustion
-- Solution: Monitor and adjust pool settings
SELECT 
    count(*) as active_connections,
    max_conn,
    (count(*) * 100.0 / max_conn)::numeric(5,2) as usage_percent
FROM pg_stat_activity, 
     (SELECT setting::int as max_conn FROM pg_settings WHERE name = 'max_connections') s
WHERE state = 'active';
```

#### Supabase Specific Issues
```python
# Common Supabase problems and solutions

# Problem: RLS policies blocking queries
# Solution: Check and update RLS policies
async def debug_rls_issue(user_id: str, table: str):
    """Debug RLS policy issues."""
    
    # Check if RLS is enabled
    rls_status = await supabase.rpc('check_rls_status', {'table_name': table})
    print(f"RLS enabled for {table}: {rls_status}")
    
    # Test policy with specific user
    try:
        result = await supabase.table(table).select('*').eq('user_id', user_id).execute()
        print(f"Query successful: {len(result.data)} rows returned")
    except Exception as e:
        print(f"RLS blocking query: {e}")
        
        # Check user authentication
        user = await supabase.auth.get_user()
        print(f"Current user: {user.user.id if user.user else 'Not authenticated'}")

# Problem: Vector search not working
# Solution: Verify embedding dimensions and index
async def debug_vector_search():
    """Debug vector search issues."""
    
    # Check embedding dimensions
    result = await supabase.rpc('check_embedding_dimensions')
    print(f"Embedding dimensions: {result}")
    
    # Test vector search function
    test_embedding = [0.1] * 384  # Adjust dimension as needed
    try:
        results = await supabase.rpc('match_documents', {
            'query_embedding': test_embedding,
            'match_threshold': 0.5,
            'match_count': 5
        })
        print(f"Vector search working: {len(results)} results")
    except Exception as e:
        print(f"Vector search failed: {e}")
```

### API and WebSocket Issues

#### FastAPI Debugging
```python
# Debug FastAPI issues

# Problem: CORS errors
# Solution: Check CORS configuration
@app.middleware("http")
async def debug_cors(request: Request, call_next):
    """Debug CORS issues."""
    origin = request.headers.get("origin")
    print(f"Request origin: {origin}")
    print(f"Allowed origins: {cors_origins}")
    
    response = await call_next(request)
    return response

# Problem: 422 Validation errors
# Solution: Add detailed error reporting
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Provide detailed validation error information."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input")
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation failed",
            "errors": errors,
            "request_body": await request.body() if request.method in ["POST", "PUT", "PATCH"] else None
        }
    )

# Problem: Database connection errors
# Solution: Add connection health checks
@app.on_event("startup")
async def startup_event():
    """Verify database connectivity on startup."""
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
```

#### Socket.IO Debugging
```typescript
// Debug Socket.IO connection issues

// Problem: WebSocket connection fails
// Solution: Add comprehensive connection debugging
const socket = io('http://localhost:8000', {
  transports: ['websocket', 'polling'],
  upgrade: true,
  rememberUpgrade: true,
  autoConnect: true,
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: 5,
  timeout: 20000,
  debug: process.env.NODE_ENV === 'development'
});

// Enhanced error handling
socket.on('connect', () => {
  console.log('Connected to server:', socket.id);
  console.log('Transport:', socket.io.engine.transport.name);
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', {
    message: error.message,
    description: error.description,
    context: error.context,
    type: error.type
  });
  
  // Check common issues
  if (error.message.includes('CORS')) {
    console.log('CORS issue detected. Check server CORS configuration.');
  } else if (error.message.includes('timeout')) {
    console.log('Connection timeout. Check server availability.');
  }
});

socket.on('disconnect', (reason) => {
  console.log('Disconnected:', reason);
  
  if (reason === 'io server disconnect') {
    // Server initiated disconnect, manually reconnect
    console.log('Server disconnected client, attempting manual reconnection...');
    socket.connect();
  }
});

// Debug transport changes
socket.io.on('upgrade', () => {
  console.log('Transport upgraded to:', socket.io.engine.transport.name);
});

socket.io.on('upgradeError', (error) => {
  console.error('Transport upgrade failed:', error);
});
```

### Frontend Issues

#### React/Vite Debugging
```typescript
// Common React/Vite issues and solutions

// Problem: Hot module replacement not working
// Solution: Check Vite configuration and file paths
// vite.config.ts
export default defineConfig({
  server: {
    host: true,
    port: 3000,
    strictPort: true,
    hmr: {
      port: 3001,
      host: 'localhost'
    }
  },
  // Ensure proper file watching
  optimizeDeps: {
    include: ['react', 'react-dom']
  }
});

// Problem: Build failures
// Solution: Add build debugging
const debugBuild = {
  // Check for circular dependencies
  rollupOptions: {
    onwarn(warning, warn) {
      if (warning.code === 'CIRCULAR_DEPENDENCY') {
        console.warn('Circular dependency detected:', warning.message);
      }
      warn(warning);
    }
  }
};

// Problem: Memory leaks in React components
// Solution: Proper cleanup patterns
export const useWebSocket = () => {
  const [socket, setSocket] = useState<Socket | null>(null);
  
  useEffect(() => {
    const socketInstance = io('http://localhost:8000');
    setSocket(socketInstance);
    
    // Cleanup function is crucial
    return () => {
      console.log('Cleaning up WebSocket connection');
      socketInstance.disconnect();
    };
  }, []);
  
  // Cleanup on component unmount
  useEffect(() => {
    return () => {
      if (socket) {
        socket.removeAllListeners();
        socket.disconnect();
      }
    };
  }, [socket]);
  
  return socket;
};

// Problem: Query cache issues
// Solution: Proper cache invalidation
export const useDocumentMutations = () => {
  const queryClient = useQueryClient();
  
  const createDocument = useMutation({
    mutationFn: createDocumentAPI,
    onSuccess: (data) => {
      // Invalidate and refetch related queries
      queryClient.invalidateQueries(['documents']);
      queryClient.invalidateQueries(['projects', data.projectId]);
      
      // Update specific query cache
      queryClient.setQueryData(['document', data.id], data);
    },
    onError: (error) => {
      console.error('Document creation failed:', error);
      // Show user-friendly error message
      toast.error('Failed to create document. Please try again.');
    }
  });
  
  return { createDocument };
};
```

### Performance Issues

#### Database Performance Debugging
```python
# Debug database performance issues

async def debug_slow_queries():
    """Identify and analyze slow database queries."""
    
    async with engine.begin() as conn:
        # Find slow queries
        slow_queries = await conn.execute(text("""
            SELECT 
                query,
                calls,
                total_exec_time,
                mean_exec_time,
                rows,
                100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
            FROM pg_stat_statements 
            WHERE mean_exec_time > 100  -- Queries slower than 100ms
            ORDER BY mean_exec_time DESC
            LIMIT 10;
        """))
        
        print("=== SLOW QUERIES ===")
        for query in slow_queries.fetchall():
            print(f"Query: {query.query[:100]}...")
            print(f"Average time: {query.mean_exec_time:.2f}ms")
            print(f"Total calls: {query.calls}")
            print(f"Cache hit rate: {query.hit_percent:.1f}%")
            print("---")

async def debug_vector_search_performance():
    """Debug vector search performance issues."""
    
    # Check index statistics
    async with engine.begin() as conn:
        index_stats = await conn.execute(text("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                idx_tup_read,
                idx_tup_fetch,
                idx_blks_read,
                idx_blks_hit
            FROM pg_stat_user_indexes 
            WHERE indexname LIKE '%embedding%';
        """))
        
        print("=== VECTOR INDEX STATISTICS ===")
        for stat in index_stats.fetchall():
            print(f"Index: {stat.indexname}")
            print(f"Tuples read: {stat.idx_tup_read}")
            print(f"Cache hit ratio: {stat.idx_blks_hit / (stat.idx_blks_hit + stat.idx_blks_read) * 100:.1f}%")
            print("---")

# Memory usage debugging
import psutil
import asyncio

async def monitor_memory_usage():
    """Monitor application memory usage."""
    
    process = psutil.Process()
    
    while True:
        memory_info = process.memory_info()
        memory_percent = process.memory_percent()
        
        print(f"Memory usage: {memory_info.rss / 1024 / 1024:.1f} MB ({memory_percent:.1f}%)")
        
        if memory_percent > 80:
            print("WARNING: High memory usage detected!")
            
            # Check for memory leaks
            import gc
            gc.collect()
            print(f"Objects after garbage collection: {len(gc.get_objects())}")
        
        await asyncio.sleep(30)
```

#### Frontend Performance Debugging
```typescript
// Debug React performance issues

// Performance monitoring hook
export const usePerformanceDebug = (componentName: string) => {
  const renderCount = useRef(0);
  const lastRenderTime = useRef(Date.now());
  
  useEffect(() => {
    renderCount.current += 1;
    const now = Date.now();
    const timeSinceLastRender = now - lastRenderTime.current;
    
    console.log(`${componentName} render #${renderCount.current}, time since last: ${timeSinceLastRender}ms`);
    lastRenderTime.current = now;
  });
  
  // Log re-renders with reasons
  useWhyDidYouUpdate(componentName, props);
};

// Hook to track why component re-rendered
function useWhyDidYouUpdate(name: string, props: Record<string, any>) {
  const previous = useRef<Record<string, any>>();
  
  useEffect(() => {
    if (previous.current) {
      const allKeys = Object.keys({ ...previous.current, ...props });
      const changedProps: Record<string, { from: any; to: any }> = {};
      
      allKeys.forEach((key) => {
        if (previous.current![key] !== props[key]) {
          changedProps[key] = {
            from: previous.current![key],
            to: props[key],
          };
        }
      });
      
      if (Object.keys(changedProps).length) {
        console.log('[why-did-you-update]', name, changedProps);
      }
    }
    
    previous.current = props;
  });
}

// Debug bundle size and imports
// Use webpack-bundle-analyzer or similar tool
const analyzeBundleSize = () => {
  // Add to package.json scripts:
  // "analyze": "npm run build && npx vite-bundle-analyzer dist"
  
  // Check for large imports
  console.log('Large dependencies to watch:');
  console.log('- lodash: Use specific imports (lodash-es)');
  console.log('- moment: Consider date-fns instead');
  console.log('- entire icon libraries: Import specific icons only');
};

// Memory leak detection
export const useMemoryLeakDetection = () => {
  useEffect(() => {
    const checkMemory = () => {
      if ((performance as any).memory) {
        const memory = (performance as any).memory;
        console.log('Memory usage:', {
          used: Math.round(memory.usedJSHeapSize / 1048576),
          total: Math.round(memory.totalJSHeapSize / 1048576),
          limit: Math.round(memory.jsHeapSizeLimit / 1048576),
        });
      }
    };
    
    const interval = setInterval(checkMemory, 10000); // Check every 10 seconds
    
    return () => clearInterval(interval);
  }, []);
};
```

### Network and Connectivity Issues

#### API Request Debugging
```typescript
// Debug API request issues

// Enhanced axios configuration with debugging
const apiClient = axios.create({
  baseURL: process.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`, {
      headers: config.headers,
      data: config.data,
      params: config.params,
    });
    
    // Add request timestamp
    config.metadata = { startTime: Date.now() };
    
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    const endTime = Date.now();
    const duration = endTime - response.config.metadata.startTime;
    
    console.log(`API Response: ${response.status} ${response.config.url}`, {
      duration: `${duration}ms`,
      size: JSON.stringify(response.data).length,
      data: response.data,
    });
    
    if (duration > 5000) {
      console.warn(`Slow API request detected: ${response.config.url} took ${duration}ms`);
    }
    
    return response;
  },
  (error) => {
    const endTime = Date.now();
    const duration = error.config?.metadata?.startTime 
      ? endTime - error.config.metadata.startTime 
      : 0;
    
    console.error(`API Error: ${error.response?.status || 'Network Error'}`, {
      url: error.config?.url,
      duration: `${duration}ms`,
      message: error.message,
      response: error.response?.data,
    });
    
    // Handle specific error types
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - check server availability');
    } else if (error.response?.status === 429) {
      console.error('Rate limit exceeded - implement backoff strategy');
    } else if (error.response?.status >= 500) {
      console.error('Server error - check server logs');
    }
    
    return Promise.reject(error);
  }
);

// Network connectivity checker
export const useNetworkStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [connectionSpeed, setConnectionSpeed] = useState<string>('unknown');
  
  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      console.log('Network connection restored');
    };
    
    const handleOffline = () => {
      setIsOnline(false);
      console.log('Network connection lost');
    };
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    // Check connection speed
    if ('connection' in navigator) {
      const connection = (navigator as any).connection;
      setConnectionSpeed(connection.effectiveType || 'unknown');
      
      connection.addEventListener('change', () => {
        setConnectionSpeed(connection.effectiveType || 'unknown');
        console.log('Connection speed changed:', connection.effectiveType);
      });
    }
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  
  return { isOnline, connectionSpeed };
};
```

This comprehensive AGENTS.md file provides detailed technical guidance for AI agents working with the ARCHON RELOADED platform. It covers all aspects from basic setup to advanced troubleshooting, ensuring that AI agents have the complete context they need to work effectively with the codebase while maintaining high standards of code quality, security, and performance.
