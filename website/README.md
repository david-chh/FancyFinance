# 💰 FancyFinance - AI-Powered Financial Analytics

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue)](https://postgresql.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green)](https://openai.com)

> **Modern financial data pipeline with AI-powered analytics and natural language querying**

Created by **Sabrina Santos** for financial transaction analysis and business intelligence.

## 🌟 Features

### 📊 **Data Pipeline**
- **DLT (Data Load Tool)** integration for robust ETL processes
- **PostgreSQL/Supabase** cloud database storage
- **Custom CSV parsing** for malformed financial data
- **STRIPE payment processing** integration
- **Real-time data validation** and quality monitoring

### 🤖 **AI Analytics**
- **LangChain + OpenAI GPT-3.5** powered chatbot
- **Natural language queries** about your financial data
- **Smart routing** to specialized financial analysis tools
- **Real-time insights** on revenue, expenses, and profitability

### 📈 **Interactive Dashboard**
- **Streamlit** web interface with live financial metrics
- **Plotly visualizations** for trends and categories
- **Monthly revenue/expense tracking**
- **STRIPE revenue analysis**
- **Data quality monitoring**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database (or Supabase account)
- OpenAI API key

### 1. Clone & Install
```bash
git clone https://github.com/david-chh/FancyFinance.git
cd FancyFinance
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file in the root directory:
```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database
```

Create `.dlt/secrets.toml` for DLT configuration:
```toml
[destination.postgres.credentials]
database = "your_database_name"
username = "your_username"
password = "your_password"
host = "your_host"
port = 5432
```

### 3. Load Data
```bash
python src/dlt_pipeline.py
```

### 4. Launch Dashboard
```bash
streamlit run src/dashboard.py
```

## 📁 Project Structure

```
FancyFinance/
├── 📂 src/                     # Core application code
│   ├── dlt_pipeline.py         # Main data pipeline
│   ├── dashboard.py            # Streamlit web dashboard
│   └── langchain_tools.py      # AI analysis tools
├── 📂 data/                    # Data files
│   └── IVY Transaction Data - Sheet1.csv
├── 📂 scripts/                 # Utility scripts
│   ├── setup_chatbot.py        # AI setup wizard
│   ├── clean_db.py             # Database cleanup
│   ├── create_tables.py        # Schema creation
│   ├── debug_csv.py            # CSV debugging
│   └── simple_pipeline.py      # Minimal pipeline
├── 📂 tests/                   # Test scripts
│   ├── test_chatbot.py         # AI integration tests
│   ├── simple_ai_test.py       # Direct tool testing
│   └── test_connection.py      # Database tests
├── 📂 config/                  # Configuration files
├── 📂 docs/                    # Documentation
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎯 Usage Examples

### Data Pipeline
```bash
# Load transaction data to database
python src/dlt_pipeline.py

# View pipeline analytics
# Monthly summaries, top categories, STRIPE analysis automatically generated
```

### AI Financial Assistant
```python
from src.langchain_tools import chat_with_financial_data

# Ask natural language questions
response = chat_with_financial_data("What's my profit margin?")
response = chat_with_financial_data("Show me top expense categories")
response = chat_with_financial_data("How much STRIPE revenue did I earn?")
```

### Dashboard Features
- 💰 **Financial Metrics**: Revenue, expenses, profit margins
- 📊 **Interactive Charts**: Monthly trends, category breakdowns
- 💳 **STRIPE Analysis**: Payment processing insights
- 🤖 **AI Chat Interface**: Ask questions about your data
- ⚠️ **Quality Monitoring**: Invalid transaction detection

## 🔧 Configuration

### Database Setup
1. Create PostgreSQL database (or use Supabase)
2. Update connection details in `.env` and `.dlt/secrets.toml`
3. Run the pipeline to create tables automatically

### OpenAI Setup
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env` file as `OPENAI_API_KEY`
3. Test with: `python scripts/setup_chatbot.py`

### Data Format
The pipeline expects CSV files with columns:
- `transaction_id`, `date`, `amount`, `description`
- `category`, `counterparty`, `currency`, `reference`
- Automatic detection of STRIPE invoices

## 🧪 Testing

```bash
# Test AI tools directly
python tests/simple_ai_test.py

# Test full integration
python tests/test_chatbot.py

# Test database connection
python tests/test_connection.py
```

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Data Pipeline** | DLT + Python | ETL processing |
| **Database** | PostgreSQL/Supabase | Data storage |
| **AI Engine** | LangChain + OpenAI | Natural language processing |
| **Frontend** | Streamlit | Web dashboard |
| **Visualization** | Plotly | Interactive charts |
| **Data Processing** | Pandas + SQLAlchemy | Data manipulation |

## 📊 Financial Insights

The system provides automatic analysis of:

- **Revenue Streams**: Total income, STRIPE payments, monthly trends
- **Expense Categories**: Software, cloud services, venue rental, etc.
- **Profitability**: Net profit, profit margins, break-even analysis
- **Data Quality**: Invalid transactions, missing data detection
- **Business Intelligence**: Top clients, seasonal patterns, growth metrics

## 🤖 AI Capabilities

### Smart Query Routing
- **Financial summaries** → Direct database aggregation
- **Category analysis** → Expense/income categorization tools
- **STRIPE analysis** → Payment processing insights
- **Custom queries** → OpenAI-powered natural language processing

### Supported Questions
- "What's my total profit this year?"
- "Show me my biggest expense categories"
- "How much did I earn from STRIPE payments?"
- "Are there any invalid transactions?"
- "What's my monthly revenue trend?"

## 🔒 Security

- ✅ **Environment variables** for sensitive data
- ✅ **Git ignore** for API keys and credentials
- ✅ **Database connection** encryption
- ✅ **OpenAI API** secure communication

## 🚧 Roadmap

- [ ] Add more payment processor integrations
- [ ] Implement forecasting models
- [ ] Add export capabilities (PDF reports)
- [ ] Mobile responsive dashboard
- [ ] Multi-user authentication
- [ ] Real-time data streaming

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing dashboard framework
- **LangChain** for AI integration capabilities
- **DLT** for robust data pipeline tools
- **OpenAI** for powerful language models
- **Plotly** for beautiful visualizations

---

**Built with ❤️ by Sabrina Santos**

For questions or support, please open an issue on GitHub.