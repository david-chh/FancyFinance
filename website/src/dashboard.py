"""
IVY Financial Analytics Dashboard
Interactive dashboard for transaction data analysis with AI chatbot
"""

import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="IVY Financial Analytics",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Database connection configuration
@st.cache_resource
def get_database_connection():
    """PostgreSQL/Supabase connection"""
    engine = create_engine(
        "postgresql://postgres.njyncmeeqjrtultxcpgb:xtz1KQD-btj8nzf5gtz@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"
    )
    return engine


# Cached queries
@st.cache_data(ttl=300)  # 5 minutes
def load_transactions():
    """Load transaction data"""
    engine = get_database_connection()

    query = """
    SELECT 
        transaction_id,
        date,
        amount,
        description,
        reference,
        category,
        currency,
        counterparty,
        provider,
        transaction_type,
        is_stripe_invoice
    FROM ivy_data.transactions
    ORDER BY date DESC
    """

    df = pd.read_sql(query, engine)
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    return df


@st.cache_data(ttl=300)
def get_financial_summary(df):
    """Calculate financial summary"""
    total_income = df[df["amount"] > 0]["amount"].sum()
    total_expenses = df[df["amount"] < 0]["amount"].abs().sum()
    net_amount = total_income - total_expenses
    stripe_revenue = df[df["is_stripe_invoice"] == True]["amount"].sum()

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_amount": net_amount,
        "stripe_revenue": stripe_revenue,
        "total_transactions": len(df),
    }


@st.cache_data(ttl=300)
def get_monthly_trends(df):
    """Monthly trends analysis"""
    df["month_year"] = df["date"].dt.to_period("M").astype(str)

    monthly = (
        df.groupby(["month_year", "transaction_type"])["amount"]
        .agg(["sum", "count"])
        .reset_index()
    )
    monthly["abs_amount"] = monthly["sum"].abs()

    return monthly


def detect_invalid_transactions(df):
    """Detect invalid transactions"""
    invalid_conditions = [
        df["amount"].isna(),
        df["description"].isna(),
        df["category"].isna(),
        df["amount"] == 0,
        df["description"].str.len() < 3,
    ]

    df["is_invalid"] = False
    for condition in invalid_conditions:
        df.loc[condition, "is_invalid"] = True

    return df[df["is_invalid"] == True]


# Main interface
def main():
    st.title("💰 IVY Financial Analytics Dashboard")
    st.markdown("**Real-time financial transaction analysis**")

    # Sidebar
    st.sidebar.header("⚙️ Filters")

    # Load data
    try:
        df = load_transactions()
        st.sidebar.success(f"✅ {len(df)} transactions loaded")
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return

    # Filters
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(df["date"].min().date(), df["date"].max().date()),
        min_value=df["date"].min().date(),
        max_value=df["date"].max().date(),
    )

    categories = st.sidebar.multiselect(
        "🏷️ Categories", options=df["category"].unique(), default=df["category"].unique()
    )

    # Apply filters
    if len(date_range) == 2:
        df = df[
            (df["date"].dt.date >= date_range[0])
            & (df["date"].dt.date <= date_range[1])
        ]

    df = df[df["category"].isin(categories)]

    # Key metrics
    summary = get_financial_summary(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Total Revenue",
            f"${summary['total_income']:,.2f}",
            delta=f"{summary['total_transactions']} transactions",
        )

    with col2:
        st.metric(
            "💸 Total Expenses", f"${summary['total_expenses']:,.2f}", delta="Outflows"
        )

    with col3:
        st.metric(
            "📊 Net Result",
            f"${summary['net_amount']:,.2f}",
            delta="Revenue - Expenses",
            delta_color="normal" if summary["net_amount"] >= 0 else "inverse",
        )

    with col4:
        st.metric(
            "💳 STRIPE Revenue", f"${summary['stripe_revenue']:,.2f}", delta="Payments"
        )

    # Main charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Monthly Trends")
        monthly_data = get_monthly_trends(df)

        fig_monthly = px.bar(
            monthly_data,
            x="month_year",
            y="abs_amount",
            color="transaction_type",
            title="Revenue vs Expenses by Month",
            color_discrete_map={"income": "#00CC96", "expense": "#EF553B"},
        )
        fig_monthly.update_layout(height=400)
        st.plotly_chart(fig_monthly, use_container_width=True)

    with col2:
        st.subheader("🥧 Expenses by Category")
        expense_categories = (
            df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
        )

        fig_pie = px.pie(
            values=expense_categories.values,
            names=expense_categories.index,
            title="Expense Distribution",
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    # STRIPE Revenue Analysis
    st.subheader("💳 STRIPE Revenue Analysis")
    stripe_data = df[df["is_stripe_invoice"] == True].copy()

    if len(stripe_data) > 0:
        col1, col2 = st.columns(2)

        with col1:
            # STRIPE revenue timeline
            stripe_timeline = (
                stripe_data.groupby(stripe_data["date"].dt.date)["amount"]
                .sum()
                .reset_index()
            )

            fig_stripe = px.line(
                stripe_timeline,
                x="date",
                y="amount",
                title="STRIPE Revenue Timeline",
                markers=True,
            )
            fig_stripe.update_layout(height=300)
            st.plotly_chart(fig_stripe, use_container_width=True)

        with col2:
            # Top STRIPE revenue types
            stripe_summary = (
                stripe_data.groupby("description")["amount"]
                .agg(["sum", "count"])
                .reset_index()
            )
            stripe_summary = stripe_summary.sort_values("sum", ascending=False).head(5)

            fig_clients = px.bar(
                stripe_summary,
                x="sum",
                y="description",
                orientation="h",
                title="Top 5 STRIPE Revenue Types",
            )
            fig_clients.update_layout(height=300)
            st.plotly_chart(fig_clients, use_container_width=True)

    # Data Quality Analysis
    st.subheader("⚠️ Data Quality Analysis")
    invalid_transactions = detect_invalid_transactions(df.copy())

    col1, col2 = st.columns([1, 2])

    with col1:
        invalid_count = len(invalid_transactions)
        invalid_percentage = (invalid_count / len(df)) * 100 if len(df) > 0 else 0

        st.metric(
            "🔍 Invalid Transactions",
            f"{invalid_count}",
            delta=f"{invalid_percentage:.1f}% of total",
            delta_color="inverse" if invalid_count > 0 else "normal",
        )

        if invalid_count > 0:
            st.warning(f"⚠️ Found {invalid_count} transactions with quality issues")

    with col2:
        if len(invalid_transactions) > 0:
            st.write("**Problematic Transactions:**")
            st.dataframe(
                invalid_transactions[
                    ["transaction_id", "date", "amount", "description", "category"]
                ].head(10),
                use_container_width=True,
            )

    # Recent transactions table
    st.subheader("📋 Recent Transactions")
    recent_transactions = df.head(20)[
        ["date", "amount", "description", "category", "counterparty"]
    ]
    recent_transactions["amount"] = recent_transactions["amount"].apply(
        lambda x: f"${x:,.2f}"
    )

    st.dataframe(recent_transactions, use_container_width=True)

    # AI Financial Assistant with LangChain + OpenAI
    st.subheader("🤖 AI Financial Assistant")

    # Check if API key is configured
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        st.error("🔑 **OpenAI API Key Required**")
        st.write("To enable the AI assistant, please:")
        st.code(
            "1. Get an API key from https://platform.openai.com/api-keys\n2. Add it to your .env file: OPENAI_API_KEY=your_key_here\n3. Restart the dashboard"
        )
        return

    with st.expander("💬 Ask about your financial data", expanded=True):
        # Initialize session state for chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Load AI agent (cached)
        if "ai_agent_ready" not in st.session_state:
            try:
                with st.spinner("🔧 Initializing AI assistant..."):
                    from langchain_tools import create_financial_agent

                    st.session_state.ai_agent = create_financial_agent()
                    st.session_state.ai_agent_ready = True
                st.success("✅ AI Assistant is ready!")
            except Exception as e:
                st.error(f"❌ AI setup failed: {e}")
                st.session_state.ai_agent_ready = False
                return

        # Chat interface
        col1, col2 = st.columns([4, 1])

        with col1:
            user_question = st.text_input(
                "Ask me anything about your financial data:",
                placeholder="e.g., 'What were my biggest expenses last month?' or 'Am I profitable?'",
                key="financial_question",
            )

        with col2:
            ask_button = st.button("Ask AI", type="primary", use_container_width=True)

        # Process question
        if (
            (ask_button or user_question)
            and user_question
            and st.session_state.ai_agent_ready
        ):
            # Add user question to history
            st.session_state.chat_history.append(
                {"role": "user", "content": user_question}
            )

            # Get AI response
            with st.spinner("🤔 Analyzing your financial data..."):
                try:
                    from langchain_tools import chat_with_financial_data

                    response = chat_with_financial_data(user_question)

                    # Add AI response to history
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response}
                    )

                    # Clear input
                    st.session_state.financial_question = ""

                except Exception as e:
                    st.error(f"Error: {e}")
                    response = "I apologize, but I encountered an error while analyzing your data. Please try rephrasing your question."
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response}
                    )

        # Display chat history
        if st.session_state.chat_history:
            st.write("### 💬 Conversation History")

            for i, message in enumerate(
                reversed(st.session_state.chat_history[-6:])
            ):  # Show last 6 messages
                if message["role"] == "user":
                    st.write(f"**👤 You:** {message['content']}")
                else:
                    st.write(f"**🤖 AI Assistant:** {message['content']}")

                if i < len(st.session_state.chat_history[-6:]) - 1:
                    st.write("---")

        # Quick action buttons
        st.write("### 🚀 Quick Questions")
        col1, col2, col3 = st.columns(3)

        quick_questions = [
            "What's my financial summary?",
            "Show top expense categories",
            "How much STRIPE revenue?",
            "Are there invalid transactions?",
            "What's my profit margin?",
            "Monthly revenue trends",
        ]

        for i, question in enumerate(quick_questions):
            col = [col1, col2, col3][i % 3]
            with col:
                if st.button(question, key=f"quick_{i}", use_container_width=True):
                    # Process question directly
                    st.session_state.chat_history.append(
                        {"role": "user", "content": question}
                    )

                    with st.spinner("Analyzing your financial data..."):
                        try:
                            from langchain_tools import chat_with_financial_data

                            response = chat_with_financial_data(question)
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": response}
                            )
                        except Exception as e:
                            response = f"Error: {e}"
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": response}
                            )

                    st.rerun()

        # Clear chat history button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()

        # Help section
        with st.expander("💡 AI Assistant Help"):
            st.write("""
            **What can I help you with?**
            
            📊 **Financial Analysis:**
            - "What's my total profit this year?"
            - "Which categories cost me the most?"
            - "Show me all transactions over $500"
            
            💰 **Revenue Questions:**
            - "How much did I earn from STRIPE payments?"
            - "What's my monthly revenue trend?"
            - "Which was my best revenue month?"
            
            🔍 **Data Quality:**
            - "Are there any invalid transactions?"
            - "Show me suspicious transactions"
            - "What data quality issues do I have?"
            
            📅 **Time-based Analysis:**
            - "How did July compare to June?"
            - "What were my expenses last month?"
            - "Show me quarterly revenue breakdown"
            
            The AI can write SQL queries, analyze your data, and provide insights based on your actual transaction records.
            """)

    # AI Status indicator
    if st.session_state.get("ai_agent_ready", False):
        st.success("🟢 AI Assistant: Online and ready")
    else:
        st.warning("🟡 AI Assistant: Not configured")


if __name__ == "__main__":
    main()
