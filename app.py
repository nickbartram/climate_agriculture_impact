# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect, text
import Resources.postgres_key as pk
import plotly.express as px

# -------------------
# Setup DB connection
# -------------------
engine = create_engine(
    f"postgresql+psycopg2://{pk.postgres_user}:{pk.postgres_pass}@climate-db.croamw4iqxpi.us-east-2.rds.amazonaws.com:5432/climate_db"
)

# -------------------
# Sidebar: Table schema
# -------------------
st.sidebar.title("Database Explorer")

# Create inspector
inspector = inspect(engine)
tables = inspector.get_table_names()
selected_table = st.sidebar.selectbox("Select a table to view schema:", tables)

if selected_table:
    columns = inspector.get_columns(selected_table)
    schema_df = pd.DataFrame(columns)
    st.sidebar.subheader(f"Schema: {selected_table}")
    st.sidebar.dataframe(schema_df)

# -------------------
# Main area: SQL query input
# -------------------
st.title("🌍 Climate Data Explorer")

query = st.text_area("Enter SQL query:", f"SELECT * FROM {selected_table} LIMIT 10;")

if st.button("Run Query"):
    try:
        df = pd.read_sql(query, engine)

        # Convert object/TEXT columns to string to avoid Arrow warnings
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str)

        # Show the data
        st.subheader("Query Results")
        st.dataframe(df)

        # Plot numeric columns automatically if any
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) >= 1:
            st.subheader("Numeric Plot")
            # Pick first two numeric columns for x/y if at least two
            x_col = numeric_cols[0]
            y_col = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")
