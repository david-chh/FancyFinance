# 🏗️ Project CFA - Comprehensive Financial Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://python.org)
[![React](https://img.shields.io/badge/React-18.3%2B-61DAFB)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5%2B-blue)](https://typescriptlang.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-AI%20Agent-green)](https://langgraph-ai.github.io/langgraph/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple)](https://modelcontextprotocol.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue)](https://postgresql.org)

> **Advanced multi-component financial analytics platform powered by AI agents and modern web technologies**

A comprehensive solution combining intelligent invoice processing, AI-powered data analysis, and interactive financial dashboards built for the modern era.

## 📋 Project Summary

**Project CFA** is a sophisticated financial analytics ecosystem consisting of three integrated components:

1. **🧾 MCP Invoice Server** - Automated invoice downloading and transaction querying via Model Context Protocol
2. **🤖 LangGraph AI Agent** - Intelligent financial analysis and decision-making using advanced AI workflows
3. **🌐 Full-Stack Web Application** - Modern React frontend with Python backend for comprehensive financial dashboards

The platform enables businesses to automate invoice processing, gain AI-powered insights, and visualize financial data through beautiful, interactive dashboards.

## 🏛️ Architecture Overview

```
project-cfa/
├── 📦 invoices-mcp/           # MCP Server for Invoice Processing
│   ├── src/
│   │   ├── server.py          # FastMCP server implementation
│   │   ├── agent.py           # Invoice download automation
│   │   └── models.py          # Database models & queries
│   └── DATABASE_SETUP.md      # Database configuration guide
│
├── 🤖 langgraph-agent/        # AI Agent for Financial Analysis
│   ├── agent/
│   │   ├── agent.py           # LangGraph workflow definition
│   │   └── tools.py           # Financial analysis tools
│   └── langgraph.json         # Agent configuration
│
├── 🌐 website/                # Full-Stack Web Application
│   ├── src/                   # Python Backend
│   │   ├── dashboard.py       # Streamlit dashboard
│   │   ├── dlt_pipeline.py    # Data pipeline (DLT)
│   │   └── langchain_tools.py # AI integration
│   ├── data/                  # Financial datasets
│   ├── scripts/               # Utility scripts
│   ├── tests/                 # Test suites
│   └── website/               # React Frontend
│       ├── src/
│       │   ├── components/ui/ # shadcn/ui components
│       │   ├── pages/         # Application pages
│       │   └── hooks/         # React hooks
│       └── package.json       # Frontend dependencies
│
└── README.md                  # This file
```

## 🌟 Core Features

### 🧾 **Invoice MCP Server**
- **Automated Invoice Downloads** - Browser automation for merchant websites
- **OCR Content Extraction** - Mistral API-powered document processing
- **Transaction Database** - PostgreSQL with advanced querying capabilities
- **MCP Protocol Integration** - Standardized AI tool interface

### 🤖 **LangGraph AI Agent**
- **Intelligent Workflows** - Multi-step financial analysis automation
- **Decision Making** - AI-powered business insights and recommendations
- **Tool Orchestration** - Seamless integration with invoice and database systems
- **Graph-Based Logic** - Complex reasoning workflows

### 📊 **Web Application Backend**
- **DLT Data Pipeline** - Robust ETL processes for financial data
- **Streamlit Dashboard** - Interactive Python-based analytics interface
- **LangChain Integration** - Natural language querying of financial data
- **PostgreSQL/Supabase** - Cloud-native database solutions

### 🌐 **Modern React Frontend**
- **TypeScript & React 18** - Type-safe, modern web application
- **shadcn/ui Components** - Beautiful, accessible UI components
- **Tailwind CSS** - Utility-first styling framework
- **React Query** - Server state management
- **Responsive Design** - Mobile-first approach

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL database
- OpenAI API key
- Mistral API key (for OCR)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd project-cfa
```

### 2. Set Up MCP Invoice Server
```bash
cd invoices-mcp
uv sync  # or pip install -e .
```

Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
MISTRAL_API_KEY=your_mistral_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/database
```

### 3. Configure LangGraph Agent
```bash
cd ../langgraph-agent
uv sync  # or pip install -e .
```

### 4. Set Up Web Application
```bash
cd ../website

# Backend setup
pip install -r requirements.txt

# Frontend setup
cd website
npm install
```

### 5. Launch Components

**MCP Server:**
```bash
cd invoices-mcp
python src/server.py
```

**LangGraph Agent:**
```bash
cd langgraph-agent
langgraph dev
```

**Streamlit Dashboard:**
```bash
cd website
streamlit run src/dashboard.py
```

**React Frontend:**
```bash
cd website/website
npm run dev
```

## 🔧 Configuration

### Database Setup
1. Create PostgreSQL database
2. Set up `ivy_date` schema for transactions
3. Configure connection strings in each component
4. See `invoices-mcp/DATABASE_SETUP.md` for detailed instructions

### API Keys
- **OpenAI**: For LangChain and LangGraph AI capabilities
- **Mistral**: For OCR invoice content extraction
- Configure in respective `.env` files

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **AI/ML** | LangGraph, LangChain, OpenAI | AI agents and natural language processing |
| **Backend** | Python, FastAPI, Streamlit | Server-side logic and dashboards |
| **Frontend** | React, TypeScript, Tailwind | Modern web interface |
| **Database** | PostgreSQL, SQLAlchemy | Data storage and queries |
| **Integration** | MCP, Browser-use | Standardized protocols and automation |
| **DevOps** | uv, npm, Vite | Package management and build tools |

## 📊 Use Cases

### For Financial Analysts
- **Automated Invoice Processing** - Download and extract data from supplier websites
- **AI-Powered Insights** - Get intelligent recommendations on financial trends
- **Interactive Dashboards** - Visualize complex financial data with modern charts

### For Businesses
- **Transaction Analysis** - Deep dive into revenue streams and expense categories
- **Compliance Reporting** - Automated financial reporting and documentation
- **Predictive Analytics** - AI-driven forecasting and business intelligence

### For Developers
- **MCP Integration** - Extend with custom financial tools and protocols
- **AI Agent Workflows** - Build sophisticated multi-step analysis processes
- **Modern Web Stack** - Learn from a production-ready React/Python architecture

## 🔒 Security & Compliance

- ✅ **Environment Variables** - Secure API key management
- ✅ **Database Encryption** - Secure connection protocols
- ✅ **MCP Standards** - Standardized, secure AI tool integration
- ✅ **Data Validation** - Input sanitization and error handling

## 🚧 Development Roadmap

- [ ] **Enhanced AI Workflows** - More sophisticated LangGraph analysis patterns
- [ ] **Real-time Processing** - WebSocket integration for live updates
- [ ] **Mobile Applications** - React Native companion apps
- [ ] **Advanced OCR** - Multi-language invoice processing
- [ ] **API Gateway** - Unified API layer for all components
- [ ] **Kubernetes Deployment** - Container orchestration setup

## 🤝 Contributing

We welcome contributions to any component of the platform:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Component Guidelines
- **MCP Server**: Follow MCP protocol standards
- **LangGraph Agent**: Use proper graph workflow patterns
- **Web Application**: Maintain TypeScript strict mode and accessibility standards

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangGraph** - For powerful AI agent orchestration
- **Model Context Protocol** - For standardized AI tool integration
- **shadcn/ui** - For beautiful, accessible React components
- **Streamlit** - For rapid dashboard development
- **DLT** - For robust data pipeline tools

---

**🏗️ Built for the Future of Financial Analytics**

*Combining the power of AI agents, modern web technologies, and intelligent automation*