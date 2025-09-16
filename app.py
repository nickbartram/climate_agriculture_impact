# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect, text
import Resources.postgres_key as pk
import plotly.express as px
import statsmodels.api as sm

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
inspector = inspect(engine)
tables = inspector.get_table_names()
selected_table = st.sidebar.selectbox("Select a table:", tables)

if selected_table:
    columns = inspector.get_columns(selected_table)
    schema_df = pd.DataFrame(columns)
    st.sidebar.subheader(f"Schema: {selected_table}")
    st.sidebar.dataframe(schema_df)

    # Custom table descriptions
    table_descriptions = {
        "co2": ("C02 emissions in Canada and the United States from 1908 - 2023. "
                "'co2' and 'total_ghg' are in metric tons, make sure to filer to country."
                "Data from OWID (Our World in Data), full source cited in Github repo README: "
                "https://github.com/nickbartram/climate_agriculture_impact"
        ),
        "rainfall": ("Total precipitation (mm) in Canada and the United States from 1908 - 2023. Make sure to filter for country. "
                     "Data from CCKP (Climate Change Knowledge Port - World Bank), full source cited in Github repo README: "
                    "https://github.com/nickbartram/climate_agriculture_impact"
        ),
        "diet_persons": ("Total number of people (in millions) unable to afford a healthy diet in Canada and the United States "
                         "from 2017 - 2023. Make sure to filter for country. Data from FAO (Food and Agriculture Organization - World Bank), "
                         "full source cited in Github repo README: "
                        "https://github.com/nickbartram/climate_agriculture_impact"
        ),
        "diet_percentage": ("Total percentage of people unable to afford a healthy diet in Canada and the United States "
                         "from 2017 - 2023. Make sure to filter for country. Data from FAO (Food and Agriculture Organization - World Bank), "
                         "full source cited in Github repo README: "
                        "https://github.com/nickbartram/climate_agriculture_impact"
        ),
        "na_crops": ("Total production of corn and wheat in Canada and the United States from  1908 - 2023 "
                     "Data from Statistics Canada and United States Department of Agriculture respectively. Make sure to filter for country. "
                     "Full source cited in Github repo README: https://github.com/nickbartram/climate_agriculture_impact"
        )
    }

    # Display the blurb
    if selected_table in table_descriptions:
        st.sidebar.markdown(f"**About this table:**\n{table_descriptions[selected_table]}")
    else:
        st.sidebar.markdown("**No custom description available for this table.**")

# -------------------
# Main area
# -------------------
st.title("🌍 Climate Data Explorer")

if not selected_table:
    st.info("Choose a table from the sidebar to start.")
else:
    # All columns
    all_columns = [col["name"] for col in inspector.get_columns(selected_table)]

    # Columns to display
    selected_columns = st.multiselect("Select columns to display:", all_columns, default=all_columns[:])

    # -------------------
    # Country / ISO filter
    # -------------------
    filter_col = None
    if "country" in all_columns:
        filter_col = "country"
    elif "iso_code" in all_columns:
        filter_col = "iso_code"

    if filter_col:
        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT DISTINCT {filter_col} FROM {selected_table} ORDER BY {filter_col};"))
                rows = result.fetchall()
                filter_values = [r[0] for r in rows if r[0] is not None]
        except Exception as e:
            st.error(f"Could not fetch distinct {filter_col} values: {e}")
            filter_values = []

        selected_filter = st.selectbox(f"Filter by {filter_col}:", ["All"] + filter_values)
    else:
        selected_filter = "All"

    # -------------------
    # Build + run query
    # -------------------
    cols_sql = ", ".join(selected_columns) if selected_columns else "*"

    if st.button("Run Query"):
        try:
            if selected_filter != "All" and filter_col:
                sql = text(f"SELECT {cols_sql} FROM {selected_table} WHERE {filter_col} = :filter_val LIMIT 100;")
                st.session_state.df = pd.read_sql(sql, engine, params={"filter_val": selected_filter})
            else:
                sql = text(f"SELECT {cols_sql} FROM {selected_table} LIMIT 100;")
                st.session_state.df = pd.read_sql(sql, engine)

            # Convert object/TEXT columns to string to avoid Arrow warnings
            for col in st.session_state.df.select_dtypes(include=["object"]).columns:
                st.session_state.df[col] = st.session_state.df[col].astype(str)

        except Exception as e:
            st.error(f"Error running query: {e}")
            st.session_state.df = None

    # -------------------
    # Display + plot if df exists
    # -------------------
    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df

        st.subheader("Query Results")
        st.dataframe(df)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            st.subheader("Plot Data")

            x_col = st.selectbox("X-axis column:", numeric_cols, index=0)
            y_col = st.selectbox("Y-axis column:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)

            plot_type = st.radio("Select plot type:", ["Line Plot", "Scatter Plot"], horizontal=True)
            add_regression = st.checkbox("Add linear regression trendline")

            # Determine grouping column
            group_col = None
            if "country" in df.columns:
                group_col = "country"
            elif "iso_code" in df.columns:
                group_col = "iso_code"

            # Base plot
            if plot_type == "Line Plot":
                if group_col:
                    fig = px.line(
                        df,
                        x=x_col,
                        y=y_col,
                        color=group_col,
                        title=f"{y_col} vs {x_col} by {group_col}"
                    )
                else:
                    fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")

                # Add regression only if checkbox is checked
                if add_regression and group_col:
                    # Separate regression per group
                    for group_val, df_group in df.groupby(group_col):
                        df_group = df_group[[x_col, y_col]].dropna().sort_values(x_col)
                        X = sm.add_constant(df_group[x_col])
                        model = sm.OLS(df_group[y_col], X).fit()
                        df_group["regression"] = model.predict(X)
                        fig.add_traces(
                            px.line(df_group, x=x_col, y="regression")
                            .update_traces(line=dict(color="red", dash="dash"))
                            .data
                        )
                elif add_regression:
                    # Single regression if no grouping
                    df_reg = df[[x_col, y_col]].dropna().sort_values(x_col)
                    X = sm.add_constant(df_reg[x_col])
                    model = sm.OLS(df_reg[y_col], X).fit()
                    df_reg["regression"] = model.predict(X)
                    fig.add_traces(
                        px.line(df_reg, x=x_col, y="regression")
                        .update_traces(line=dict(color="red", dash="dash"))
                        .data
                    )

            else:  # Scatter plot
                fig = px.scatter(
                    df,
                    x=x_col,
                    y=y_col,
                    color=group_col if group_col else None,
                    title=f"{y_col} vs {x_col}" + (f" by {group_col}" if group_col else ""),
                    trendline="ols" if add_regression else None
                )

            st.plotly_chart(fig)



# -------------------
# Custom SQL playground (bottom of page)
# -------------------
st.markdown("---")  # horizontal rule for separation
st.subheader("💻 SQL Playground")
st.markdown(
    "For advanced users: enter a custom SQL query to explore the data directly. "
    "Be careful — this is just for experimentation and could return large results."
)

custom_query = st.text_area(
    "Enter your SQL query:",
    value=f"SELECT * FROM {selected_table} LIMIT 10;" if selected_table else ""
)

if st.button("Run Custom SQL"):
    if custom_query.strip() == "":
        st.warning("Please enter a SQL query.")
    else:
        try:
            df_custom = pd.read_sql(custom_query, engine)
            # Convert object columns to string
            for col in df_custom.select_dtypes(include=["object"]).columns:
                df_custom[col] = df_custom[col].astype(str)

            st.subheader("Custom SQL Results")
            st.dataframe(df_custom)

        except Exception as e:
            st.error(f"Error running custom query: {e}")


