# Vishwakarma 🏗️

> **A typesafe Model Context Protocol (MCP) server for local LLMs. Built with FastAPI & Pydantic to unify data access for AI agents.**

Vishwakarma act as a **Universal Data Connector**, providing a unified, voice-optimized interface for LLMs to access disparate data sources (CRM, Support, Analytics). It handles data type identification, intelligent filtering, and ensures type-safe function calling for agents.

## 🚀 Features

- **Universal Interface**: One API to rule them all (CRM, Support, Analytics).
- **Voice Optimized**: Smart summarization and limiters for concise voice responses.
- **Type Safe**: Built with **FastAPI** and **Pydantic v2** for robust validation.
- **Local LLM Ready**: Tested with **Llama 3**, **Qwen 2.5**, and **LFM2**.
- **Dockerized**: Ready for deployment with `docker-compose`.

## 🛠️ Quick Start

### Local
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up --build
```

Visit docs at: 
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📜 Problem Statement & Requirements

### Assignment Overview

Build a production-quality **Universal Data Connector** using FastAPI that provides a unified interface for an LLM to access different data sources through function calling. The connector must be intelligent enough to identify data types, apply business rules, and optimize responses for voice conversations where bandwidth and latency matter.

### Business Context
You're building this for a SaaS company where customers need to query their data (CRM, support tickets, analytics) through voice conversations with an AI assistant. The key constraints are:
- Voice conversations require quick, concise responses (not massive data dumps)
- Data must be contextually relevant and filtered
- The LLM needs metadata to understand how to use each data source
- Multiple data sources should have a consistent interface

---

## 📋 Requirements

### Core Functionality
1. **FastAPI Server** with health checks and proper error handling
2. **Multiple Data Connectors** (at least 3 types):
   - Customer CRM data
   - Support ticket system
   - Analytics/metrics data
3. **Intelligent Data Filtering**:
   - Automatic pagination for large datasets
   - Business rules engine to filter data appropriately
   - Smart summarization for voice contexts
4. **LLM Function Calling Interface**:
   - OpenAPI schema generation for function calling
   - Clear parameter validation
   - Structured responses with metadata
5. **Data Type Detection & Handling**:
   - Identify whether data is tabular, time-series, hierarchical, etc.
   - Apply appropriate transformations
   - Include data freshness/staleness indicators

### Technical Requirements
- Python 3.11+
- FastAPI with Pydantic v2 models
- Proper logging and error handling
- Type hints throughout
- Configuration management (environment variables)
- Mock data generators included
- Docker deployment ready

### Voice-Optimized Business Rules
Implement rules like:
- **Limit results**: Default max 10 items for voice
- **Prioritization**: Return most recent/relevant first
- **Summarization**: Aggregate metrics instead of raw data when appropriate
- **Context awareness**: Include helpful metadata (e.g., "showing 3 of 47 results")
- **Freshness indicators**: "Data as of 2 hours ago"

---

## 🏗️ Architecture

```
universal-data-connector/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py           # Shared models
│   │   ├── crm.py              # CRM data models
│   │   ├── support.py          # Support ticket models
│   │   └── analytics.py        # Analytics models
│   ├── connectors/
│   │   ├── __init__.py
│   │   ├── base.py             # Base connector interface
│   │   ├── crm_connector.py    # CRM data connector
│   │   ├── support_connector.py
│   │   └── analytics_connector.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_identifier.py  # Identifies data types
│   │   ├── business_rules.py   # Business rules engine
│   │   └── voice_optimizer.py  # Voice-specific optimizations
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── data.py             # Data access endpoints
│   └── utils/
│       ├── __init__.py
│       ├── mock_data.py        # Mock data generators
│       └── logging.py          # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── test_connectors.py
│   ├── test_business_rules.py
│   └── test_api.py
├── data/
│   ├── customers.json          # Sample CRM data
│   ├── support_tickets.json    # Sample support data
│   └── analytics.json          # Sample metrics
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🎓 Learning Objectives

By completing this exercise, you will demonstrate:
1. **API Design**: Creating clean, RESTful APIs with FastAPI
2. **Type Safety**: Using Pydantic models and Python type hints
3. **Abstraction**: Building reusable base classes and interfaces
4. **Business Logic**: Implementing smart filtering and rules
5. **LLM Integration**: Understanding function calling patterns
6. **Production Readiness**: Logging, error handling, configuration
7. **Voice UX Considerations**: Optimizing for conversational AI

---

## ✅ Evaluation Criteria

### Code Quality (30%)
- Clean, readable code with proper structure
- Type hints and Pydantic models used correctly
- Comprehensive error handling
- Logging throughout

### Functionality (30%)
- All endpoints working correctly
- Business rules properly implemented
- Data filtering and optimization working
- Mock data realistic and useful

### LLM Integration (20%)
- OpenAPI schema properly generated
- Function calling examples work
- Responses optimized for voice
- Good parameter validation

### Documentation (20%)
- Clear README with setup instructions
- Inline code comments where needed
- API documentation (auto-generated + custom)
- Example usage scenarios

---

## 🚀 Getting Started

### Phase 1: Setup (Day 1)
1. Set up project structure
2. Create base models and connector interface
3. Implement mock data generators
4. Get FastAPI running with health check

### Phase 2: Core Connectors (Days 2-3)
1. Implement CRM connector
2. Implement support ticket connector
3. Implement analytics connector
4. Add data type identification

### Phase 3: Business Rules (Day 4)
1. Build business rules engine
2. Implement voice optimizations
3. Add pagination and filtering
4. Test with sample queries

### Phase 4: LLM Integration (Day 5)
1. Create function calling schemas
2. Test with LLM (Claude or OpenAI)
3. Optimize response formats
4. Add metadata and context

### Phase 5: Polish (Day 6)
1. Add comprehensive logging
2. Write tests
3. Create Docker setup
4. Write documentation

---

## 📝 Submission Requirements

1. **GitHub Repository** with:
   - All source code
   - README with setup instructions
   - Sample .env file
   - Working Docker Compose setup

2. **Demo Video** (5 minutes max):
   - Show the API running
   - Demonstrate 3-4 example queries
   - Show LLM function calling integration
   - Explain one interesting technical decision

3. **Written Summary** (1 page):
   - Challenges faced and solutions
   - Design decisions and tradeoffs
   - What you'd improve with more time
   - What you learned

---

## 💡 Tips for Success

1. **Start Simple**: Get one connector working end-to-end before adding complexity
2. **Use Type Hints**: Let your IDE help you catch bugs early
3. **Test as You Go**: Don't wait until the end to test
4. **Think About the User**: Would this response make sense in a voice conversation?
5. **Document Your Thinking**: Add comments explaining "why" not just "what"
6. **Ask Questions**: If requirements are unclear, make reasonable assumptions and document them

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

---

## 🎉 Bonus Challenges (Optional)

If you finish early and want to go further:
1. Add caching layer (Redis) for frequently accessed data
2. Implement rate limiting per data source
3. Add streaming responses for large datasets
4. Create a web UI to test the API
5. Add authentication and API key management
6. Implement webhook support for real-time data updates
7. Add data export functionality (CSV, Excel)

Good luck! We're excited to see what you build. 🚀

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker-compose up --build
```

Visit: http://localhost:8000/docs
