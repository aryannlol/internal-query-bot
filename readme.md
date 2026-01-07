Internal Query Bot (RAG-based Knowledge Hub)
--------------------------------------------

### Overview

Internal Query Bot is a developer-managed Retrieval-Augmented Generation (RAG) system designed to answer internal company questions using uploaded documents such as HR policies, IT guidelines, and engineering docs.

The system supports **admin-controlled document uploads**, **one-click index rebuild**, and **instant querying** via API.

### Architecture

*   **Backend**: FastAPI
    
*   **Embeddings**: Sentence-Transformers
    
*   **Vector DB**: ChromaDB (persistent, DuckDB + Parquet)
    
*   **LLM**: Ollama (local, e.g. qwen3:4b)
    
*   **Indexing Strategy**: Full rebuild for correctness
    

### Project Structure (simplified)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   app/  ├── admin/            # rebuild pipeline  ├── api.py            # API routes  ├── ingestion/        # document loading & chunking  ├── embeddings/       # embedding generation  ├── vectorstore/      # ChromaDB interface  ├── retrieval/        # vector search  ├── generation/       # answer generation  ├── scripts/          # batch evaluation  └── main.py           # FastAPI app   `

### Setup

#### 1\. Create virtual environment

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv .venv  source .venv/bin/activate  # Windows: .venv\Scripts\activate   `

#### 2\. Install dependencies

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

#### 3\. Start Ollama

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   ollama run qwen3:4b   `

Leave it running.

### Running the Application

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   uvicorn app.main:app --reload   `

Open Swagger UI:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   http://127.0.0.1:8000/docs   `

### Admin Workflow (Important)

#### Upload documents and rebuild index

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   POST /admin/upload-and-rebuild   `

*   Upload one or more .md / .txt files
    
*   This performs a **full rebuild**:
    
    *   old index deleted
        
    *   documents re-ingested
        
    *   embeddings regenerated
        
    *   vector store rebuilt
        

This guarantees correctness and avoids stale data.

### Querying

Use:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   POST /query   `

The system retrieves relevant chunks from ChromaDB and generates answers using the LLM.

### Design Decisions

*   **Full rebuild strategy** is used instead of incremental updates for simplicity and correctness.
    
*   Intended for **internal knowledge bases** with controlled document updates.
    
*   Supports extension to multi-collection or incremental updates if required.
    

### Limitations

*   No user authentication
    
*   Single knowledge domain per index
    
*   Synchronous rebuild (blocking)
    

### Future Improvements

*   Multi-collection support (HR / IT / Engineering)
    
*   Incremental document updates
    
*   Admin UI
    
*   Evaluation metrics dashboard