# import dependencies
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import Resources.postgres_key as pk
import importlib
import streamlit as st
import plotly.express as px

# Setup up credentials
user = pk.postgres_user
password = pk.postgres_pass

# Create engine
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@climate-db.croamw4iqxpi.us-east-2.rds.amazonaws.com:5432/climate_db"
)

# Test the connecttion
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.fetchone())  # Should print (1,)
except Exception as e:
    print("Connection failed:", e)

# Title of streamlit app
st.title("🌍 Climate Data Explorer")

# Practice query
query = st.text_area("Enter SQL query:", "SELECT * FROM co2 LIMIT 10;")

if st.button("Run Query"):
    try:
        df = pd.read_sql(query, engine)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error: {e}")