# ARCHON RELOADED — Product Requirements Document (PRD)
*Repo path:* `/docs/PRD.md` • *Doc owner:* Product (Jack) • *Engineering owners:* Platform + Knowledge Engine • *Last updated:* 2025-08-17

---

## 0) Document Status & Sources
- **Status:** Draft v0.9 (implementation-ready; SLO-gated rollouts defined)
- **Primary references:** Technical Spec (revised 2025-08-17), Cloud-Native Best Practices guide, Project README. fileciteturn0file1 fileciteturn0file0 fileciteturn0file2

---

## 1) Vision & Summary
ARCHON RELOADED is a **model-context platform** that gives AI coding tools (Claude Code, Cursor, Windsurf) **streamed, low-latency access to trustworthy project knowledge**. It standardizes ingestion, retrieval, and collaboration via **MCP (Model Context Protocol)** with **Streamable HTTP** as the primary transport, **Hyper Express** as the runtime, and a **Qdrant-backed RAG engine**. Target: **p95 dense search <200 ms**, **hybrid <350 ms**, **≥250 concurrent agent sessions/shard**. fileciteturn0file1 fileciteturn0file2

---

## 2) Goals, Non-Goals, Success
### 2.1 Goals
- **Seamless MCP integration** with primary Streamable HTTP + stdio fallback; SSE legacy for compatibility. fileciteturn0file1
- **High-quality RAG**: hybrid (dense+BM25), optional re-rank; first token from ingestion (TTFI) in **<30 s** for 50-page PDFs. fileciteturn0file1
- **Real-time collaboration** for agents and humans (live context sync, event log, session resume). fileciteturn0file2
- **SLO-driven ops** (latency, availability, concurrency) with burn-rate alerts, golden-signals dashboards. fileciteturn0file0

### 2.2 Non-Goals
- Full IDE feature parity; ARCHON is a **context/knowledge plane**, not an IDE. fileciteturn0file2
- Long-term support for SSE once Streamable HTTP coverage is universal (deprecation planned). fileciteturn0file1

### 2.3 Success Metrics (OKRs)
- **Latency:** p95 dense <200 ms; hybrid <350 ms (staging→prod parity). fileciteturn0file1
- **Scale:** ≥250 concurrent sessions/shard at <0.5% error rate. fileciteturn0file1
- **Availability:** ≥99.9% monthly; error-budget policy. fileciteturn0file2
- **Ingestion:** TTFI <30 s for 50-page PDF. fileciteturn0file1

---

## 3) Users & Use Cases
- **AI-assisted developers:** request codebase answers, API contracts, diffs; agent tool-calls hit ARCHON via MCP. fileciteturn0file2
- **Tech leads & doc writers:** orchestrate knowledge ingestion, search curation, and policy-gated sharing. fileciteturn0file2
- **Agents (LLM tools):** search_knowledge, ingest_document, suggest_queries, workspace/collab tools. fileciteturn0file2

---

## 4) Scope
### 4.1 In-Scope (MVP→Phase 2)
- MCP endpoints (Streamable HTTP primary; stdio secondary; SSE legacy). fileciteturn0file1
- Knowledge engine: **Qdrant** dense search; **hybrid** with BM25; **BGE-Large v1.5** / **Jina v2** embeddings via TEI/vLLM. fileciteturn0file1
- Real-time collab (WebSocket fan-out via Redis), session resume, audit trail. fileciteturn0file2
- Observability (OpenTelemetry → Prometheus/Grafana; logs to Loki; NGINX + Node tracing). fileciteturn0file0

### 4.2 Out-of-Scope (initial)
- Non-project web search at large; plugin marketplace (Phase 3+). fileciteturn0file1

---

## 5) System Overview & Key Decisions
- **Runtime:** Node.js 20 + **Hyper Express** for zero-copy HTTP/WS & native streaming; lower overhead than classic Express. fileciteturn0file0
- **Protocol:** **MCP Streamable HTTP** prioritized for future-proof, bidirectional, high-throughput transport. fileciteturn0file1
- **Retrieval:** **Qdrant** (HNSW; NVMe; replication; on-disk indexes), hybrid dense+BM25, optional re-ranking. fileciteturn0file0
- **Data split:** vectors in Qdrant; rich metadata in MongoDB; caching via Redis (read-through/write-through, Streams). fileciteturn0file0
- **Kubernetes:** HPA on CPU + **custom latency** metric; PDB; anti-affinity across AZs; dedicated NVMe pool for Qdrant. fileciteturn0file0
- **Observability:** OpenTelemetry instrumentation for Node & NGINX; golden signals; SLO burn-rate alerts. fileciteturn0file0

---

## 6) Functional Requirements
### 6.1 Knowledge Ingestion
- Upload/crawl → extract (PDF/DOCX/HTML/MD) → semantic chunk (250–500 tkn, 15–20% overlap) → batch embed (512–2048) → Qdrant upsert → warm caches. **TTFI <30 s** (50-page PDF). Idempotency via content hash. fileciteturn0file1 fileciteturn0file0
- **APIs:** `POST /api/knowledge/ingest`, `GET /api/knowledge/status/:job_id`. fileciteturn0file2

### 6.2 Retrieval & RAG
- Modes: `dense`, `sparse`, `hybrid(default)`; filters; thresholds; top-k; optional MMR/reranker. p95: dense <200 ms; hybrid <350 ms. fileciteturn0file1
- **APIs:** `POST /api/search`, `/api/search/dense`. fileciteturn0file2

### 6.3 MCP Integration
- **Endpoints:** `/mcp/stream` (primary), `/mcp/rpc` (JSON-RPC), `/mcp/sse` (legacy). ≥250 concurrent sessions/shard. fileciteturn0file2
- **Tools:** `search_knowledge`, `ingest_document`, `suggest_queries`, `create_workspace`, `sync_document`. fileciteturn0file2

### 6.4 Real-Time Collaboration
- WS events for search streaming, document ops (OT/CRDT optional), performance alerts, embedding-service health. fileciteturn0file2

### 6.5 Admin & Analytics
- SLO dashboards, vector latency panels, queue depth, cache hit ratio; policy-as-code for admin APIs. fileciteturn0file1 fileciteturn0file0

---

## 7) Non-Functional Requirements
### 7.1 Performance & Scale
- **Latency:** dense p95 <200 ms; hybrid p95 <350 ms; dense p99 <400 ms. fileciteturn0file1
- **Throughput:** ≥250 concurrent sessions/shard with <0.5% error. fileciteturn0file1
- **Resource hints:** App 300–500 mCPU / 512–768 Mi; Qdrant 4–8 vCPU / 16–64 Gi + NVMe. fileciteturn0file1

### 7.2 Availability, DR, Data
- **Availability:** ≥99.9%; weekly restore tests; DR: restore ≤2 h, RPO ≤15 m; Qdrant replication ≥2–3x. fileciteturn0file1
- **Data design:** vectors slim payloads in Qdrant; Mongo for rich metadata; Redis for hot paths and Streams for jobs. fileciteturn0file0

### 7.3 Security & Privacy
- OAuth2/OIDC; RBAC + OPA; mTLS (in-cluster), secrets via KMS/Vault/CSI; WAF/Ingress hardening; PII redaction. fileciteturn0file0

### 7.4 Observability
- OpenTelemetry for Node + NGINX module; Prometheus metrics (RED & event-loop lag); Loki logs; burn-rate alerts. fileciteturn0file0

---

## 8) Data Model (key entities)
- **KnowledgeItem(id, title, content, source_type, embedding_vector, metadata, timestamps)**; ops: `get_summary`, `update_embedding`. fileciteturn0file2  
- **Project(id, name, description, status)**; **Task(id, project_id, title, status, priority, assignee)**; **Source(id, url, type, crawl_status)**. fileciteturn0file2

---

## 9) External Integrations
- **Embeddings:** default **BGE-Large v1.5** (1024-D), alt **Jina v2**; served via **TEI/vLLM**, autoscaled; OpenAI/Cohere fallbacks. fileciteturn0file1
- **BM25:** Elasticsearch/Meilisearch for sparse leg; hybrid orchestrated in engine. fileciteturn0file2
- **MCP clients:** Claude Code (stdio), Cursor/Windsurf (Streamable HTTP). fileciteturn0file1

---

## 10) UX Requirements (Web UI)
- Real-time status for ingestion & search; streamed results; virtualized lists for large corpora; Tailwind + shadcn/ui. fileciteturn0file0 fileciteturn0file2
- Accessibility: keyboard-first ops; aria roles; high-contrast theme.

---

## 11) Telemetry, Metrics, & Alerts
- **Golden signals** (latency, traffic, errors, saturation) plus event-loop lag, active WS, Qdrant latency, cache hit ratio. fileciteturn0file0
- **SLO burn-rates** (2%/h, 5%/h); alert rules for search latency p95 breaches and availability drops. fileciteturn0file1

---

## 12) Release Plan & Milestones
- **Phase 1 (Weeks 1–4):** Hyper Express + MCP Streamable HTTP; Qdrant + TEI/vLLM; baseline telemetry.  
  **Exit:** dense p95 <250 ms; TTFI <30 s (staging). fileciteturn0file1  
- **Phase 2 (Weeks 5–10):** Cursor/Windsurf via Streamable HTTP; hybrid retrieval + reranker; collab.  
  **Exit:** hybrid p95 <350 ms; ≥200 sessions (staging). fileciteturn0file1  
- **Phase 3 (Weeks 11–16):** Caching tiers, DR drills, SLO burn-rate policies.  
  **Exit:** ≥250 sessions/shard; DR ≤2 h / RPO ≤15 m. fileciteturn0file1  
- **Phase 4 (Weeks 17–20):** Multi-region, soak tests, UAT, security gate.  
  **Exit:** 99.9% availability; security scans pass. fileciteturn0file1

---

## 13) Risks & Mitigations
1) **Transport coverage** (tools lacking Streamable HTTP) → keep stdio/SSE fallback; publish deprecation schedule. fileciteturn0file1  
2) **Vector I/O hotspots** → NVMe pools; replica pinning; multi-tier cache. fileciteturn0file1 fileciteturn0file0  
3) **Embedding throughput** → autoscale TEI/vLLM; adaptive batching; backpressure. fileciteturn0file1  
4) **Security drift** → OPA-gated admin APIs; vuln scans; distroless images. fileciteturn0file0

---

## 14) Acceptance Criteria (SLO-Gated)
- **A1:** `/api/search` hybrid p95 <350 ms over 1-hour k6 run at target RPS; no more than 0.5% 5xx. fileciteturn0file2  
- **A2:** Ingest 50-page PDF → first token streamed within 30 s (p95) with warmed workers. fileciteturn0file1  
- **A3:** ≥250 concurrent MCP sessions/shard; median event-loop lag <20 ms. fileciteturn0file1  
- **A4:** 99.9% 30-day availability; burn-rate alerts configured and tested. fileciteturn0file0

---

## 15) Test Plan (high level)
- **Unit/Integration:** schema guards, tool contracts, vector ops; Testcontainers for Qdrant/Mongo/Redis. fileciteturn0file0  
- **E2E:** Playwright for UI; WS flows; streamed results assertions. fileciteturn0file0  
- **Load/Soak:** k6/Artillery + MCP frame generator; HPA behavior, PDB adherence. fileciteturn0file1 fileciteturn0file0

---

## 16) Open Questions
- Reranker model choice (small cross-encoder vs heuristic MMR) at target latencies? fileciteturn0file1  
- Final SSE deprecation date post Streamable HTTP adoption thresholds? fileciteturn0file1

---

## 17) Appendix A — API Summary (excerpt)
- `POST /api/search` (hybrid) → `{results[], latency_ms}`; `POST /api/search/dense`; `POST /api/knowledge/ingest`; `GET /api/knowledge/status/:job_id`. fileciteturn0file2  
- MCP: `/mcp/stream` (primary), `/mcp/rpc`, `/mcp/sse` (legacy). fileciteturn0file2

---

# LLM Contract
*Repo path:* `/docs/llm_contract.json`

```json
{
  "name": "ARCHON-MCP",
  "version": "2.0.0",
  "transports": {
    "primary": "streamable-http",
    "secondary": "stdio",
    "legacy": "sse"
  },
  "endpoints": {
    "stream": "/mcp/stream",
    "rpc": "/mcp/rpc",
    "sse": "/mcp/sse"
  },
  "tools": {
    "search_knowledge": {
      "description": "Hybrid (dense+BM25) or dense-only knowledge search with optional filters",
      "params_schema": {
        "type": "object",
        "properties": {
          "query": { "type": "string", "minLength": 1, "maxLength": 1000 },
          "mode": { "type": "string", "enum": ["hybrid", "dense", "sparse"], "default": "hybrid" },
          "limit": { "type": "integer", "minimum": 1, "maximum": 100, "default": 10 },
          "threshold": { "type": "number", "minimum": 0, "maximum": 1 },
          "filters": { "type": "object", "additionalProperties": true }
        },
        "required": ["query"]
      },
      "response_schema": {
        "type": "object",
        "properties": {
          "results": { "type": "array", "items": { "type": "object" } },
          "latency_ms": { "type": "number" },
          "mode": { "type": "string" },
          "total_found": { "type": "integer" }
        },
        "required": ["results", "latency_ms"]
      },
      "slo": { "p95_latency_ms": 350 }
    },
    "ingest_document": {
      "description": "Queue a document for extraction, chunking, embedding, and indexing",
      "params_schema": {
        "type": "object",
        "properties": {
          "content": { "anyOf": [{ "type": "string" }, { "type": "object" }] },
          "metadata": {
            "type": "object",
            "properties": {
              "title": { "type": "string" },
              "source_type": { "type": "string", "enum": ["upload", "crawl", "api"] },
              "tags": { "type": "array", "items": { "type": "string" } }
            },
            "required": ["title", "source_type"]
          }
        },
        "required": ["content", "metadata"]
      },
      "response_schema": {
        "type": "object",
        "properties": {
          "job_id": { "type": "string" },
          "estimated_completion": { "type": "string" },
          "chunk_count": { "type": "integer" }
        },
        "required": ["job_id"]
      },
      "slo": { "ttfi_p95_seconds": 30 }
    },
    "suggest_queries": {
      "description": "Return query suggestions for partial text with confidence scores",
      "params_schema": {
        "type": "object",
        "properties": {
          "partial_query": { "type": "string", "minLength": 1 },
          "context": { "type": "array", "items": { "type": "string" } }
        },
        "required": ["partial_query"]
      },
      "response_schema": {
        "type": "object",
        "properties": {
          "suggestions": { "type": "array", "items": { "type": "string" } },
          "confidence_scores": { "type": "array", "items": { "type": "number" } }
        },
        "required": ["suggestions", "confidence_scores"]
      }
    },
    "create_workspace": {
      "description": "Provision a collaborative workspace for real-time sessions",
      "params_schema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "config": {
            "type": "object",
            "properties": {
              "real_time_sync": { "type": "boolean", "default": true },
              "max_participants": { "type": "integer", "minimum": 1, "maximum": 64, "default": 8 },
              "conflict_resolution": { "type": "string", "enum": ["ot", "crdt", "manual"], "default": "ot" }
            },
            "required": ["real_time_sync", "max_participants", "conflict_resolution"]
          }
        },
        "required": ["name", "config"]
      },
      "response_schema": {
        "type": "object",
        "properties": {
          "workspace_id": { "type": "string" },
          "join_url": { "type": "string" },
          "session_token": { "type": "string" }
        },
        "required": ["workspace_id", "join_url", "session_token"]
      }
    },
    "sync_document": {
      "description": "Apply a batch of document operations; returns applied ops & conflicts",
      "params_schema": {
        "type": "object",
        "properties": {
          "document_id": { "type": "string" },
          "operations": { "type": "array", "items": { "type": "object" } },
          "session_id": { "type": "string" }
        },
        "required": ["document_id", "operations", "session_id"]
      },
      "response_schema": {
        "type": "object",
        "properties": {
          "applied_ops": { "type": "array", "items": { "type": "object" } },
          "conflicts": { "type": "array", "items": { "type": "object" } },
          "document_version": { "type": "integer" }
        },
        "required": ["applied_ops", "document_version"]
      }
    }
  },
  "rate_limits": {
    "per_session": {
      "search_knowledge": { "rpm": 120, "burst": 30 },
      "ingest_document": { "rpm": 6, "burst": 2 }
    }
  },
  "quotas": {
    "max_concurrent_sessions_per_shard": 250
  },
  "error_model": {
    "fields": ["code", "message", "details", "trace_id", "timestamp", "suggested_retry_after_ms"],
    "examples": [
      { "code": "RATE_LIMITED", "message": "Too many requests", "suggested_retry_after_ms": 2000 },
      { "code": "VECTOR_BACKEND_SLOW", "message": "Search exceeded SLO thresholds" }
    ]
  },
  "observability": {
    "metrics": [
      "http_request_duration_p95",
      "active_sessions_count",
      "event_loop_lag_ms",
      "qdrant_search_latency_ms",
      "cache_hit_ratio"
    ],
    "slos": {
      "dense_search_p95_ms": 200,
      "hybrid_search_p95_ms": 350,
      "availability_pct": 99.9
    }
  },
  "security": {
    "auth": "oauth2|oidc",
    "rbac": true,
    "opa_policies": true,
    "telemetry_pii_redaction": true
  }
}
```
