# Architectural Design Specifications

## 1. Task 1: Knowledge Brain
- **Ingestion**: Asynchronous HTML parsing, script/style sanitization via BeautifulSoup.
- **Retrieval**: Chunked tokenization with vector collection management using ChromaDB and OpenAI Embeddings (`text-embedding-3-small`).

## 2. Task 2: Inbox Agent
- **Triage**: Structured semantic output validation mapping via Pydantic AI (`gpt-4o`).
- **Context Injection**: RAG client pipeline linking Task 1 query vectors into drafting synthesis workflows.

## 3. Task 3: Meeting to Scope
- **Multi-Agent Flow**: Multi-stage linear mapping extracting raw criteria before engineering markdown scopes.
- **Diff Engine**: Token-based tracking to diff text state mutations across version matrices.

