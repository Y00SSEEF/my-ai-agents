import streamlit as st
import pandas as pd
import io
import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px

# Load API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Page config
st.set_page_config(
    page_title="Smart Data Analyst",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        border-radius: 14px;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }

    .main-header p {
        margin: 0.5rem 0 0;
        opacity: 0.8;
        font-size: 1rem;
    }

    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .arabic-text {
        font-family: 'Segoe UI', Arial, sans-serif;
        direction: rtl;
        text-align: right;
        line-height: 2;
    }

    .report-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 2rem;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Smart Data Analyst</h1>
    <p>Upload your data — get instant AI-powered business insights</p>
</div>
""", unsafe_allow_html=True)

# Session state
if 'report' not in st.session_state:
    st.session_state.report = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    language = st.radio(
        "Report Language:",
        ["🌍 Auto-detect", "🇸🇦 Arabic", "🇬🇧 English", "🇫🇷 French"]
    )
    lang_map = {
        "🇸🇦 Arabic": "Arabic",
        "🇬🇧 English": "English",
        "🇫🇷 French": "French",
        "🌍 Auto-detect": "Auto-detect"
    }
    selected_lang = lang_map[language]
    st.divider()
    st.caption("Built by Youssef El Mansouri · AI Developer")

# Language prompt


def get_language_prompt(lang):
    if lang == "Arabic":
        return "You must respond entirely in Arabic. Use Arabic numbers and professional business Arabic language."
    elif lang == "French":
        return "Vous devez répondre entièrement en français. Utilisez un langage professionnel."
    elif lang == "English":
        return "Respond entirely in English. Use clear, professional business language."
    else:
        return "Detect the language of the column names in the data. If columns are in Arabic, respond in Arabic. If French, respond in French. Otherwise respond in English."


# File upload
uploaded_file = st.file_uploader(
    "📤 Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="Supports CSV and Excel files"
)

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(
            f"✅ File loaded — **{df.shape[0]} rows** and **{df.shape[1]} columns**")

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📋 Preview", "📊 Statistics", "📈 Charts", "🤖 AI Report"])

        # --- TAB 1: Preview ---
        with tab1:
            st.subheader("Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            st.subheader("Column Info")
            col_info = pd.DataFrame({
                "Column": df.columns,
                "Type": df.dtypes.values,
                "Missing Values": df.isnull().sum().values,
                "Unique Values": df.nunique().values
            })
            st.dataframe(col_info, use_container_width=True)

        # --- TAB 2: Statistics ---
        with tab2:
            st.subheader("Overview")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Rows", df.shape[0])
            c2.metric("Total Columns", df.shape[1])
            c3.metric("Missing Values", df.isnull().sum().sum())
            c4.metric("Duplicate Rows", df.duplicated().sum())

            numeric_cols = df.select_dtypes(
                include=['number']).columns.tolist()
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()

            if numeric_cols:
                st.subheader("Numeric Summary")
                st.dataframe(df[numeric_cols].describe(),
                             use_container_width=True)

            if cat_cols:
                st.subheader("Categorical Columns")
                for col in cat_cols[:3]:
                    st.write(f"**{col}** — top values:")
                    st.write(df[col].value_counts().head(5))

        # --- TAB 3: Charts ---
        with tab3:
            st.subheader("Visualizations")
            numeric_cols = df.select_dtypes(
                include=['number']).columns.tolist()
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()

            if numeric_cols:
                chart_type = st.selectbox(
                    "Chart type:", ["Bar Chart", "Line Chart", "Histogram", "Pie Chart"])
                col_x = st.selectbox("X-axis:", df.columns.tolist())

                if chart_type in ["Bar Chart", "Line Chart"]:
                    col_y = st.selectbox("Y-axis:", numeric_cols)
                    if chart_type == "Bar Chart":
                        fig = px.bar(df.head(20), x=col_x, y=col_y,
                                     title=f"{col_y} by {col_x}")
                    else:
                        fig = px.line(df.head(20), x=col_x, y=col_y,
                                      title=f"{col_y} by {col_x}")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Histogram":
                    col_h = st.selectbox("Column:", numeric_cols)
                    fig = px.histogram(
                        df, x=col_h, title=f"Distribution of {col_h}")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Pie Chart" and cat_cols:
                    col_p = st.selectbox("Column:", cat_cols)
                    counts = df[col_p].value_counts().head(10).reset_index()
                    counts.columns = [col_p, 'count']
                    fig = px.pie(counts, values='count', names=col_p,
                                 title=f"Distribution of {col_p}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns found for charts.")

        # --- TAB 4: AI Report ---
        with tab4:
            st.subheader("🤖 AI-Powered Business Report")

            if st.button("🚀 Generate Report", type="primary"):
                with st.spinner("Analyzing your data..."):
                    try:
                        numeric_cols = df.select_dtypes(
                            include=['number']).columns.tolist()
                        sample = df.head(15).to_string()
                        stats = df.describe().to_string() if numeric_cols else "No numeric data"
                        lang_instruction = get_language_prompt(selected_lang)

                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            temperature=0.3,
                            messages=[
                                {"role": "system", "content": f"""
You are an expert business data analyst. Analyze the data and write a clear, structured business report.
{lang_instruction}

Structure your report with these sections:
1. EXECUTIVE SUMMARY — what is this data about and what are the key findings
2. KEY METRICS — most important numbers from the data
3. TOP PERFORMERS — best products, customers, or categories
4. PROBLEMS & RISKS — anything that looks bad or needs attention
5. RECOMMENDATIONS — 3 to 5 clear actions the business should take
6. NEXT STEPS — what to do this week to improve

Use actual numbers from the data. Be specific. Use bullet points. Write professionally.
                                """},
                                {"role": "user", "content": f"""
Dataset info:
- Rows: {df.shape[0]}
- Columns: {df.shape[1]}
- Column names: {df.columns.tolist()}
- Missing values: {df.isnull().sum().sum()}
- Duplicate rows: {df.duplicated().sum()}

Statistics:
{stats}

Sample data (first 15 rows):
{sample}
                                """}
                            ]
                        )

                        st.session_state.report = response.choices[0].message.content
                        st.session_state.analysis_done = True

                    except Exception as e:
                        st.error(f"Error generating report: {e}")

            if st.session_state.analysis_done and st.session_state.report:
                st.markdown("### 📄 Your Report")
                st.markdown("---")

                is_arabic = selected_lang == "Arabic"

                if is_arabic:
                    st.markdown(f"""
                    <div class="report-box arabic-text">
                        {st.session_state.report.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="report-box">
                        {st.session_state.report.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Report",
                    data=st.session_state.report.encode('utf-8'),
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

        # Download cleaned data
        st.markdown("---")
        st.subheader("📥 Download Cleaned Data")
        col1, col2 = st.columns(2)

        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"cleaned_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Cleaned Data')
            output.seek(0)
            st.download_button(
                label="📥 Download as Excel",
                data=output,
                file_name=f"cleaned_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("👆 Upload a CSV or Excel file to get started")

st.markdown("---")
st.caption("📊 Smart Data Analyst · Built by Youssef El Mansouri · AI Developer")
