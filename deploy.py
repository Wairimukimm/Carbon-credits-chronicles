import streamlit as st
import pandas as pd
import plotly.express as px


# Sidebar filters
st.sidebar.title("Filters")
selected_country = st.sidebar.selectbox("Select Country", merged_df["Entity"].unique())
start_year = st.sidebar.slider("Select Start Year", min_value=merged_df["Year"].min(), max_value=merged_df["Year"].max(), value=merged_df["Year"].min())
end_year = st.sidebar.slider("Select End Year", min_value=merged_df["Year"].min(), max_value=merged_df["Year"].max(), value=merged_df["Year"].max())

# Filter data based on selected country and years
filtered_df = merged_df[(merged_df["Entity"] == selected_country) & (merged_df["Year"].between(start_year, end_year))]

# Display emissions trend
st.title("Carbon Credit Initiative Analysis")
st.header(f"Emissions Trend for {selected_country} from {start_year} to {end_year}")
fig = px.line(filtered_df, x="Year", y="Annual CO₂ emissions", title="Annual CO₂ emissions trend")
st.plotly_chart(fig)

# Display project information
st.header("Carbon Credit Projects Information")
st.write(filtered_df[["Project ID", "Total Offset Credits Issued", "Year", "Organization", "Project Name"]])

# Additional analysis (to be implemented)
st.header("Additional Analysis")
# Add more Streamlit components for further analysis and insights

