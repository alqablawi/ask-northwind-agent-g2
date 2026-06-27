# Ask Northwind Agent — Project Issues

This document is the full task backlog for the instructor repository. Each issue can be copied into GitHub Issues and assigned to a milestone/branch.

---

## Milestone M0 — Project setup

### [M0-1] Create Anaconda environment

**Description:**
Create the local Python environment used by the instructor and students.

**Acceptance criteria:**
- Environment created with Python 3.13.
- Environment name is `military_student`.
- README includes the corrected command: `conda create --name military_student python=3.13`.
- Students can activate it with `conda activate military_student`.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:setup` |
| Priority | P0 |
| Milestone | M0 Setup |
| Estimate (h) | 1 |
| Branch | `chore/m0-1-conda-env` |

---

### [M0-2] Initialize project structure

**Description:**
Create the initial backend project layout for a production-style FastAPI app.

**Acceptance criteria:**
- `app/` package exists.
- `app/main.py` starts the FastAPI app.
- `app/api/`, `app/core/`, `app/db/`, `app/agents/`, `app/tools/`, `app/memory/`, `app/schemas/`, and `app/services/` exist.
- Project can run locally with `uvicorn`.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:backend` |
| Priority | P0 |
| Milestone | M0 Setup |
| Estimate (h) | 2 |
| Branch | `chore/m0-2-project-structure` |

---

### [M0-3] Add Python dependency management

**Description:**
Add project dependencies and a repeatable installation workflow.

**Acceptance criteria:**
- Dependency file exists.
- FastAPI, Uvicorn, Pydantic Settings, SQLAlchemy/SQLModel, Psycopg, LangChain/LangGraph, Redis client, HTTP client, and linting packages are included.
- Installation command is documented.
- No API keys are hardcoded.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:setup` |
| Priority | P0 |
| Milestone | M0 Setup |
| Estimate (h) | 2 |
| Branch | `chore/m0-3-dependencies` |

---

### [M0-4] Add code quality tooling

**Description:**
Add formatting and linting tooling for the project.

**Acceptance criteria:**
- Ruff is configured.
- Manual smoke-check commands are documented.
- Formatting and lint commands are documented.
- Tooling works from a clean environment.

**Commands:**
```powershell
ruff check .
ruff format .
uvicorn app.main:app --reload
```

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:quality` |
| Priority | P1 |
| Milestone | M0 Setup |
| Estimate (h) | 2 |
| Branch | `chore/m0-4-quality-tooling` |

---

### [M0-5] Create environment configuration

**Description:**
Create `.env.example` and typed settings for local, Docker, and deployment usage.

**Acceptance criteria:**
- `.env.example` includes database, Redis, OpenRouter LLM, and app settings.
- Settings are loaded through Pydantic Settings.
- LLM settings use `LLM_PROVIDER=openrouter`, `LLM_BASE_URL`, and `OPENROUTER_API_KEY`.
- Missing required settings produce clear startup errors.
- Secrets are not committed.

**Files:**
- `.env.example`
- `app/core/settings.py`

**Commands:**
```powershell
copy .env.example .env
```

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:config` |
| Priority | P0 |
| Milestone | M0 Setup |
| Estimate (h) | 2 |
| Branch | `chore/m0-5-env-config` |

---

## Milestone M1 — FastAPI foundation

### [M1-1] Build FastAPI app entrypoint

**Description:**
Implement a simple FastAPI app entrypoint and central router registration.

**Acceptance criteria:**
- App title is `Ask Northwind Agent`.
- Routers are registered under `/api/v1`.
- App startup loads settings.
- API docs are available in local development.

**Files:**
- `app/main.py`
- `app/api/v1/router.py`

**Commands:**
```powershell
uvicorn app.main:app --reload
```

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P0 |
| Milestone | M1 API Foundation |
| Estimate (h) | 2 |
| Branch | `feat/m1-1-fastapi-app` |

---

### [M1-2] Add health endpoint

**Description:**
Add a basic health endpoint for local testing, Docker, and deployment checks.

**Acceptance criteria:**
- `GET /api/v1/health` returns app status.
- Response includes app name and environment.
- Endpoint does not require LLM or database availability.
- Manual smoke check confirms successful response.

**Files:**
- `app/api/v1/health.py`
- `app/api/v1/router.py`

**Commands:**
```powershell
uvicorn app.main:app --reload
curl http://127.0.0.1:8000/api/v1/health
```

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P0 |
| Milestone | M1 API Foundation |
| Estimate (h) | 1 |
| Branch | `feat/m1-2-health-endpoint` |

---

## Milestone M2 — PostgreSQL and Northwind

### [M2-1] Add PostgreSQL service with Docker Compose

**Description:**
Add PostgreSQL to Docker Compose for local development.

**Acceptance criteria:**
- `postgres` service runs locally.
- Database, username, password, and port are configured through env vars.
- Data persists through a Docker volume.
- Healthcheck confirms database readiness.
- Host port uses `55433` to avoid conflicts with local PostgreSQL `5432` and existing Docker PostgreSQL `55432`.

**Research notes:**
- Use the official PostgreSQL Docker image for the first database service.
- The official image supports `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` for first-run initialization.
- Use `pg_isready` for the Docker healthcheck because it verifies PostgreSQL readiness without requiring the FastAPI app.
- Northwind data will be loaded in `M2-2` from an open PostgreSQL Northwind SQL script source such as `pthom/northwind_psql`.
- Northwind seed scripts can later be mounted into `/docker-entrypoint-initdb.d/`, which the PostgreSQL image runs only when the data directory is first initialized.

**Port decision:**
- Local PostgreSQL engine already uses host port `5432`.
- Existing `enara_ai-postgres` container already uses host port `55432`.
- This project uses host port `55433` and container port `5432` to stay isolated.

**Files:**
- `docker-compose.yml`
- `.env.example`
- `app/core/settings.py`

**Commands:**
```powershell
docker compose config
docker compose up -d postgres
docker compose ps
```

**Command explanations:**
- `docker compose config`: validates the Compose file and prints the final configuration after applying `.env` variables.
- `docker compose up -d postgres`: creates and starts only the `postgres` service from `docker-compose.yml`.
- `up`: creates and starts containers.
- `-d`: detached mode; keeps the container running in the background.
- `postgres`: the service name to start.
- `docker compose ps`: lists the services, status, ports, and health for this Compose project.

**Compose line explanations:**
- `name`: isolates Docker resources for this project.
- `services.postgres`: defines this project's dedicated PostgreSQL container.
- `image`: chooses the official PostgreSQL Docker image.
- `container_name`: gives the container a predictable teaching-friendly name.
- `restart`: controls whether Docker restarts the container automatically.
- `environment`: passes database initialization variables into the container.
- `ports`: maps host port `55433` to container port `5432`.
- `volumes`: persists PostgreSQL data outside the container filesystem.
- `healthcheck`: tells Docker how to know PostgreSQL is ready.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:database` |
| Priority | P0 |
| Milestone | M2 Database |
| Estimate (h) | 2 |
| Branch | `feat/m2-1-postgres-compose` |

---

### [M2-2] Load Northwind sample database

**Description:**
Seed PostgreSQL with the Northwind sample database.

**Acceptance criteria:**
- Northwind schema and data are loaded automatically.
- Core tables exist: customers, orders, order details, products, categories, suppliers, employees.
- Seed process is documented.
- Students can reset the database.

**Source:**
- Use `pthom/northwind_psql` as the PostgreSQL-compatible Northwind source.
- SQL file: `northwind.sql`.
- Pinned raw URL: `https://raw.githubusercontent.com/pthom/northwind_psql/cd0ef28d66369fbe177778e604e4be0f153c9e5c/northwind.sql`.
- File size is about `350 KB`, so it is small enough to commit into this teaching repository.

**Seed plan:**
- Download the SQL file into `db/init/01_northwind.sql`.
- Mount `db/init/` into the PostgreSQL container at `/docker-entrypoint-initdb.d/`.
- The official PostgreSQL image automatically runs `.sql` files in `/docker-entrypoint-initdb.d/` only when the data volume is first initialized.
- Because `M2-1` already created an empty `northwind` database volume, loading automatically now requires a reset with `docker compose down -v`.

**Reset warning:**
- `docker compose down -v` deletes this project's PostgreSQL volume only.
- It should not affect the local PostgreSQL engine on `5432` or the existing `enara_ai-postgres` container on `55432`.
- Use this reset only while the project database is still disposable classroom data.

**Files:**
- `db/init/01_northwind.sql`
- `docker-compose.yml`
- `README.md`
- `New-Item -ItemType Directory -Path "db/init" -Force; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/pthom/northwind_psql/cd0ef28d66369fbe177778e604e4be0f153c9e5c/northwind.sql" -OutFile "db/init/01_northwind.sql"`
- `docker compose down -v`
- `docker compose up -d postgres`

**Commands:**
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/pthom/northwind_psql/cd0ef28d66369fbe177778e604e4be0f153c9e5c/northwind.sql" -OutFile "db/init/01_northwind.sql"
docker compose down -v
docker compose up -d postgres
docker exec ask_northwind_postgres psql -U postgres -d northwind -c "\\dt"
```

**Command explanations:**
- `Invoke-WebRequest`: downloads the Northwind SQL file using PowerShell.
- `-Uri`: the remote source URL.
- `-OutFile`: the local destination path for the downloaded SQL file.
- `docker compose down -v`: stops this Compose project and removes its named volumes so PostgreSQL can re-run init scripts.
- `down`: stops and removes containers and the Compose network.
- `-v`: removes named volumes for this Compose project; this resets the project database.
- `docker compose up -d postgres`: starts the fresh PostgreSQL container in the background.
- `docker exec ask_northwind_postgres ...`: runs a command inside the running PostgreSQL container.
- `psql`: PostgreSQL command-line client.
- `-U postgres`: connects using the `postgres` user.
- `-d northwind`: connects to the `northwind` database.
- `-c "\\dt"`: runs one psql command to list tables.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:database` |
| Priority | P0 |
| Milestone | M2 Database |
| Estimate (h) | 3 |
| Branch | `feat/m2-2-load-northwind` |

---

### [M2-3] Implement database connection layer

**Description:**
Create the database engine/session layer used by API routes and tools.

**Acceptance criteria:**
- App connects to PostgreSQL using settings.
- Connection lifecycle is handled safely.
- Database errors are converted into clear application errors.
- Unit/integration test verifies a simple query.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:database` |
| Priority | P0 |
| Milestone | M2 Database |
| Estimate (h) | 3 |
| Branch | `feat/m2-3-db-connection` |

---

### [M2-4] Add schema inspection service

**Description:**
Implement a service that reads database tables, columns, primary keys, and relationships.

**Acceptance criteria:**
- Service lists available tables.
- Service describes a selected table.
- Output is compact enough for agent context.
- System tables are excluded.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:database` |
| Priority | P1 |
| Milestone | M2 Database |
| Estimate (h) | 3 |
| Branch | `feat/m2-4-schema-inspection` |

---

### [M2-5] Add read-only SQL execution service

**Description:**
Create a safe SQL execution service for agent-generated queries.

**Acceptance criteria:**
- Only `SELECT` statements are allowed.
- Dangerous statements are rejected.
- Query timeout is enforced.
- Row limit is enforced.
- Result is returned as serializable JSON.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:database` |
| Priority | P0 |
| Milestone | M2 Database |
| Estimate (h) | 4 |
| Branch | `feat/m2-5-readonly-sql` |

---

### [M2-6] Add database smoke endpoint

**Description:**
Add a developer endpoint that verifies the API can query Northwind.

**Acceptance criteria:**
- `GET /api/v1/db/smoke` runs a simple read-only query.
- Endpoint returns table count or sample product count.
- Endpoint is safe for local development.
- Test covers success and database unavailable cases.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P1 |
| Milestone | M2 Database |
| Estimate (h) | 2 |
| Branch | `feat/m2-6-db-smoke-endpoint` |

---

## Milestone M3 — Agent tools

### [M3-1] Define tool interface

**Description:**
Create a consistent interface for tools used by the agent.

**Acceptance criteria:**
- Each tool has name, description, input schema, and output schema.
- Tool errors are normalized.
- Tool execution can be traced.
- Tools are easy to register with the agent.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:agent` |
| Priority | P0 |
| Milestone | M3 Agent Tools |
| Estimate (h) | 3 |
| Branch | `feat/m3-1-tool-interface` |

---

### [M3-2] Build list tables tool

**Description:**
Expose database table discovery as an agent tool.

**Acceptance criteria:**
- Tool returns Northwind business tables.
- Tool output is concise.
- Tool handles database errors.
- Tool has tests.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:agent` |
| Priority | P0 |
| Milestone | M3 Agent Tools |
| Estimate (h) | 2 |
| Branch | `feat/m3-2-list-tables-tool` |

---

### [M3-3] Build describe table tool

**Description:**
Expose table schema details as an agent tool.

**Acceptance criteria:**
- Tool accepts a table name.
- Tool returns columns, types, nullable fields, and relationship hints.
- Invalid tables return a controlled error.
- Tool has tests.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:agent` |
| Priority | P0 |
| Milestone | M3 Agent Tools |
| Estimate (h) | 2 |
| Branch | `feat/m3-3-describe-table-tool` |

---

### [M3-4] Build run SQL query tool

**Description:**
Expose safe read-only SQL execution as an agent tool.

**Acceptance criteria:**
- Tool accepts a SQL string.
- Tool rejects non-read-only SQL.
- Tool returns rows, columns, and row count.
- Tool records the executed query for debugging.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:agent` |
| Priority | P0 |
| Milestone | M3 Agent Tools |
| Estimate (h) | 3 |
| Branch | `feat/m3-4-run-sql-tool` |

---

### [M3-5] Add tool audit trail

**Description:**
Capture which tools were used during each chat request.

**Acceptance criteria:**
- Tool name, input summary, output summary, and duration are captured.
- Sensitive values are not logged.
- API response includes `tools_used`.
- Logs are useful for classroom debugging.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:observability` |
| Priority | P1 |
| Milestone | M3 Agent Tools |
| Estimate (h) | 3 |
| Branch | `feat/m3-5-tool-audit-trail` |

---

## Milestone M4 — ReAct SQL Agent

### [M4-1] Create ReAct system prompt

**Description:**
Design the system prompt that explains the agent role, tool rules, and answer format.

**Acceptance criteria:**
- Prompt instructs the agent to inspect schema before SQL when needed.
- Prompt requires read-only behavior.
- Prompt prevents unsupported claims.
- Prompt asks for concise business-friendly answers.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:prompting` |
| Priority | P0 |
| Milestone | M4 ReAct Agent |
| Estimate (h) | 3 |
| Branch | `feat/m4-1-react-prompt` |

---

### [M4-2] Implement SQL agent loop

**Description:**
Implement the ReAct flow that chooses tools and produces final answers.

**Acceptance criteria:**
- Agent can call schema and SQL tools.
- Agent returns a final natural-language answer.
- Tool errors are recoverable when possible.
- Max iterations are enforced.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:agent` |
| Priority | P0 |
| Milestone | M4 ReAct Agent |
| Estimate (h) | 5 |
| Branch | `feat/m4-2-sql-agent-loop` |

---

### [M4-3] Add chat request and response schemas

**Description:**
Define the API schemas for the chat endpoint after the database tools and agent flow are introduced.

**Acceptance criteria:**
- `ChatRequest` includes `message`, `session_id`, and optional metadata.
- `ChatResponse` includes `answer`, `session_id`, `tools_used`, and optional `sources`.
- Error response shape is consistent.
- Schema examples appear in Swagger UI.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P0 |
| Milestone | M4 ReAct Agent |
| Estimate (h) | 2 |
| Branch | `feat/m4-3-chat-schemas` |

---

### [M4-4] Add chat endpoint

**Description:**
Expose the agent through a FastAPI endpoint.

**Acceptance criteria:**
- `POST /api/v1/chat` accepts `message` and `session_id`.
- Endpoint calls the ReAct SQL agent.
- Response includes answer, session id, tools used, and sources.
- Endpoint handles validation and agent errors.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P0 |
| Milestone | M4 ReAct Agent |
| Estimate (h) | 3 |
| Branch | `feat/m4-4-chat-endpoint` |

---

### [M4-5] Add SQL answer examples

**Description:**
Add example questions that demonstrate the SQL agent capabilities.

**Acceptance criteria:**
- Examples include top products, best customers, revenue by country, low stock, and employee performance.
- Each example has expected behavior.
- Examples are usable in class demos.
- Examples avoid requiring exact deterministic LLM wording.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docs` |
| Priority | P1 |
| Milestone | M4 ReAct Agent |
| Estimate (h) | 2 |
| Branch | `docs/m4-5-sql-agent-examples` |

---

### [M4-6] Add manual agent smoke checks

**Description:**
Add manual checks for the agent flow without introducing pytest yet.

**Acceptance criteria:**
- Checklist covers successful SQL answer.
- Checklist covers invalid SQL rejection.
- Checklist covers max-iteration protection.
- Commands are usable by students on Windows.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docs` |
| Priority | P1 |
| Milestone | M4 ReAct Agent |
| Estimate (h) | 3 |
| Branch | `docs/m4-6-agent-smoke-checks` |

---

## Milestone M5 — Embeddings and RAG

### [M5-1] Enable pgvector

**Description:**
Add vector search support inside PostgreSQL using pgvector.

**Acceptance criteria:**
- PostgreSQL image supports pgvector.
- Vector extension is enabled.
- Vector table migration exists.
- Compose setup runs locally.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:rag` |
| Priority | P0 |
| Milestone | M5 Embeddings |
| Estimate (h) | 3 |
| Branch | `feat/m5-1-pgvector` |

---

### [M5-2] Create product knowledge documents

**Description:**
Create text documents for product descriptions, category notes, supplier notes, shipping policy, and return policy.

**Acceptance criteria:**
- Documents are generated from or aligned with Northwind products/categories.
- Each document has metadata.
- Documents are small enough for teaching embeddings.
- Seed data is repeatable.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:data` |
| Priority | P1 |
| Milestone | M5 Embeddings |
| Estimate (h) | 3 |
| Branch | `feat/m5-2-knowledge-docs` |

---

### [M5-3] Implement embedding service

**Description:**
Create a service that converts text documents and questions into embeddings.

**Acceptance criteria:**
- Service supports configured embedding provider.
- API key is read from env when needed.
- Embedding dimension is validated.
- Failures return clear errors.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:rag` |
| Priority | P0 |
| Milestone | M5 Embeddings |
| Estimate (h) | 4 |
| Branch | `feat/m5-3-embedding-service` |

---

### [M5-4] Add vector ingestion command

**Description:**
Add a command/script to embed knowledge documents and store them in pgvector.

**Acceptance criteria:**
- Command can be run locally.
- Existing vectors can be refreshed.
- Ingestion logs count of processed documents.
- Ingestion is documented for students.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:rag` |
| Priority | P0 |
| Milestone | M5 Embeddings |
| Estimate (h) | 3 |
| Branch | `feat/m5-4-vector-ingestion` |

---

### [M5-5] Build semantic search tool

**Description:**
Expose vector search over product knowledge documents as an agent tool.

**Acceptance criteria:**
- Tool accepts a natural-language query.
- Tool returns top-k relevant chunks with metadata.
- Similarity threshold is configurable.
- Tool output can be cited in final answers.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:agent` |
| Priority | P0 |
| Milestone | M5 Embeddings |
| Estimate (h) | 3 |
| Branch | `feat/m5-5-semantic-search-tool` |

---

### [M5-6] Add hybrid SQL + RAG agent behavior

**Description:**
Teach the agent when to use SQL, semantic search, or both.

**Acceptance criteria:**
- Agent uses SQL for numeric/business analytics questions.
- Agent uses vector search for policy/description questions.
- Agent can combine SQL results with retrieved context.
- Final answer explains sources used.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:agent` |
| Priority | P0 |
| Milestone | M5 Embeddings |
| Estimate (h) | 5 |
| Branch | `feat/m5-6-hybrid-agent` |

---

## Milestone M6 — Memory and sessions

### [M6-1] Add conversation tables

**Description:**
Persist chat sessions and messages in PostgreSQL.

**Acceptance criteria:**
- `chat_sessions` table exists.
- `chat_messages` table exists.
- Each message stores role, content, timestamp, and metadata.
- Session id is unique per conversation.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:memory` |
| Priority | P0 |
| Milestone | M6 Memory |
| Estimate (h) | 3 |
| Branch | `feat/m6-1-conversation-tables` |

---

### [M6-2] Save chat history

**Description:**
Store user and assistant messages after each chat request.

**Acceptance criteria:**
- User messages are saved before agent execution.
- Assistant responses are saved after success.
- Failed requests store useful error metadata when appropriate.
- Tests verify persistence.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:memory` |
| Priority | P0 |
| Milestone | M6 Memory |
| Estimate (h) | 3 |
| Branch | `feat/m6-2-save-chat-history` |

---

### [M6-3] Load recent chat history into context

**Description:**
Inject recent conversation turns into the agent context.

**Acceptance criteria:**
- Recent turns are loaded by `session_id`.
- Context is limited by max turns or token budget.
- Follow-up questions can refer to previous turns.
- Tests cover a follow-up question scenario.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:memory` |
| Priority | P0 |
| Milestone | M6 Memory |
| Estimate (h) | 4 |
| Branch | `feat/m6-3-context-history` |

---

### [M6-4] Working memory with Redis — minimal

**Description:**
Minimal per-conversation working memory in Redis to keep recent turns in context.

**Acceptance criteria:**
- Recent turns cached per conversation with TTL.
- Injected into context assembly within the token budget.
- Namespaced per student/conversation.
- Redis service exists in Docker Compose.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:memory` |
| Priority | P1 |
| Milestone | M6 Memory |
| Estimate (h) | 4 |
| Branch | `feat/m6-4-working-memory-redis` |

---

### [M6-5] Add session retrieval endpoint

**Description:**
Expose a simple endpoint to inspect previous messages for a session.

**Acceptance criteria:**
- `GET /api/v1/sessions/{session_id}/messages` returns messages.
- Pagination or limit is supported.
- Endpoint is useful for demos and debugging.
- Response excludes sensitive metadata.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P2 |
| Milestone | M6 Memory |
| Estimate (h) | 2 |
| Branch | `feat/m6-5-session-messages-endpoint` |

---

## Milestone M7 — Docker Compose full stack

### [M7-1] Add Dockerfile for API

**Description:**
Containerize the FastAPI application after the local API, database, agent, and memory flow are clear.

**Acceptance criteria:**
- Dockerfile builds the API image.
- Container starts with Uvicorn.
- Environment variables are read at runtime.
- Image exposes the API port.
- Image can be used later by Docker Compose.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docker` |
| Priority | P0 |
| Milestone | M7 Docker |
| Estimate (h) | 2 |
| Branch | `feat/m7-1-api-dockerfile` |

---

### [M7-2] Build full local Docker Compose stack

**Description:**
Run the full system locally with one Docker Compose command.

**Acceptance criteria:**
- Services include `api`, `postgres`, and `redis`.
- API waits for dependencies.
- Environment variables are wired correctly.
- `docker compose up --build` starts the stack.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docker` |
| Priority | P0 |
| Milestone | M7 Docker |
| Estimate (h) | 4 |
| Branch | `feat/m7-2-full-compose-stack` |

---

### [M7-3] Add database admin UI

**Description:**
Add an optional database UI for teaching and debugging.

**Acceptance criteria:**
- Adminer or pgAdmin runs through Compose.
- Connection instructions are documented.
- Service can be disabled for deployment.
- No production secrets are exposed.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docker` |
| Priority | P2 |
| Milestone | M7 Docker |
| Estimate (h) | 2 |
| Branch | `feat/m7-3-db-admin-ui` |

---

### [M7-4] Add Docker smoke checks

**Description:**
Add a repeatable manual checklist or script to verify the local stack.

**Acceptance criteria:**
- Health endpoint passes.
- Database smoke endpoint passes.
- Chat endpoint returns a response.
- Instructions are usable by students on Windows.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docker` |
| Priority | P1 |
| Milestone | M7 Docker |
| Estimate (h) | 3 |
| Branch | `docs/m7-4-docker-smoke-checks` |

---

## Milestone M8 — Safety, observability, and polish

### [M8-1] Add structured logging

**Description:**
Add useful logs for requests, agent runs, and tool calls.

**Acceptance criteria:**
- Request id is included in logs.
- Tool duration is logged.
- SQL text is logged only when safe.
- Errors include enough context for debugging.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:observability` |
| Priority | P1 |
| Milestone | M8 Production Readiness |
| Estimate (h) | 3 |
| Branch | `feat/m8-1-structured-logging` |

---

### [M8-2] Add API error handling

**Description:**
Create consistent error handling for validation, database, Redis, and agent failures.

**Acceptance criteria:**
- Errors return consistent JSON shape.
- Internal stack traces are not exposed.
- Logs keep enough debugging detail.
- Tests cover common failure cases.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P1 |
| Milestone | M8 Production Readiness |
| Estimate (h) | 3 |
| Branch | `feat/m8-2-error-handling` |

---

### [M8-3] Add input limits and guardrails

**Description:**
Protect the API and agent from oversized requests and unsafe behavior.

**Acceptance criteria:**
- Message length limit is enforced.
- SQL row limit is enforced.
- Agent max iterations are enforced.
- Clear error is returned when limits are exceeded.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:safety` |
| Priority | P0 |
| Milestone | M8 Production Readiness |
| Estimate (h) | 3 |
| Branch | `feat/m8-3-input-guardrails` |

---

### [M8-4] Add CORS configuration

**Description:**
Prepare the API to be called from a browser frontend or API docs tool.

**Acceptance criteria:**
- Allowed origins are configurable.
- Local development origin is supported.
- Production default is restrictive.
- CORS behavior is documented.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:api` |
| Priority | P2 |
| Milestone | M8 Production Readiness |
| Estimate (h) | 1 |
| Branch | `feat/m8-4-cors-config` |

---

## Milestone M9 — Deployment

### [M9-1] Create production Docker image

**Description:**
Prepare a production-ready API container image.

**Acceptance criteria:**
- Image builds without development-only assumptions.
- App runs from environment variables.
- Container has a healthcheck.
- Build instructions are documented.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:deployment` |
| Priority | P0 |
| Milestone | M9 Deployment |
| Estimate (h) | 3 |
| Branch | `feat/m9-1-production-image` |

---

### [M9-2] Prepare managed database deployment

**Description:**
Document how to deploy PostgreSQL and load Northwind data in a hosted environment.

**Acceptance criteria:**
- Managed PostgreSQL option is selected.
- Northwind seed process is documented for deployment.
- pgvector support is verified or alternative is documented.
- Connection string is stored as an environment variable.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:deployment` |
| Priority | P0 |
| Milestone | M9 Deployment |
| Estimate (h) | 4 |
| Branch | `docs/m9-2-managed-postgres` |

---

### [M9-3] Deploy API endpoint

**Description:**
Deploy the FastAPI app and expose a public endpoint.

**Acceptance criteria:**
- Public `/api/v1/health` endpoint works.
- Public `/api/v1/chat` endpoint works with configured LLM and database.
- Environment variables are configured securely.
- Deployment steps are documented.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:deployment` |
| Priority | P0 |
| Milestone | M9 Deployment |
| Estimate (h) | 5 |
| Branch | `feat/m9-3-deploy-api` |

---

### [M9-4] Add deployment smoke test checklist

**Description:**
Create a checklist to validate the deployed application.

**Acceptance criteria:**
- Checklist verifies health, database, Redis/memory, and chat.
- Includes example `curl` requests.
- Includes rollback notes.
- Students can run the checklist after deployment.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:deployment` |
| Priority | P1 |
| Milestone | M9 Deployment |
| Estimate (h) | 2 |
| Branch | `docs/m9-4-deployment-smoke-tests` |

---

## Milestone M10 — Instructor and student material

### [M10-1] Create lesson roadmap

**Description:**
Create a teaching roadmap that maps project issues to classroom sessions.

**Acceptance criteria:**
- Sessions are ordered from setup to deployment.
- Each session has goal, demo, student task, and homework.
- Issues are grouped by session.
- Roadmap supports both student groups.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docs` |
| Priority | P0 |
| Milestone | M10 Teaching Material |
| Estimate (h) | 3 |
| Branch | `docs/m10-1-lesson-roadmap` |

---

### [M10-2] Create instructor solution branches

**Description:**
Prepare instructor-only branches or tags for each milestone.

**Acceptance criteria:**
- Each milestone has a solution branch or tag.
- Branch names match the issue roadmap.
- Instructor can reset demos safely.
- Student repos can receive selected commits later.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:instructor` |
| Priority | P1 |
| Milestone | M10 Teaching Material |
| Estimate (h) | 4 |
| Branch | `chore/m10-2-solution-branches` |

---

### [M10-3] Create student assignment templates

**Description:**
Create reusable assignment instructions for both student groups.

**Acceptance criteria:**
- Each assignment has objective, starter instructions, hints, and acceptance criteria.
- Assignments avoid leaking instructor solution code.
- Templates are easy to copy into GitHub Issues.
- Group 1 and Group 2 can use the same structure.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docs` |
| Priority | P1 |
| Milestone | M10 Teaching Material |
| Estimate (h) | 3 |
| Branch | `docs/m10-3-assignment-templates` |

---

### [M10-4] Add final demo script

**Description:**
Create a script for the final classroom demo from local Docker to deployed endpoint.

**Acceptance criteria:**
- Demo starts with clean Docker Compose.
- Demo asks SQL, RAG, and memory questions.
- Demo shows logs/tool usage.
- Demo ends with deployment endpoint test.

**Fields:**
| Field | Value |
|---|---|
| Issue type | Task |
| Label | `area:docs` |
| Priority | P1 |
| Milestone | M10 Teaching Material |
| Estimate (h) | 3 |
| Branch | `docs/m10-4-final-demo-script` |
