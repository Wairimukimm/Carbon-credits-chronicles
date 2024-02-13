import pandas as pd
import numpy
import sys
import random
import openai

import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA 
from sklearn.preprocessing import MinMaxScaler

import warnings
warnings.filterwarnings('ignore')


# Read data
df = pd.read_csv("./data/annual-co2-emissions-per-country.csv")
df1 = pd.read_csv("./data/cumulative-co-emissions.csv")

# Merge based on 'Entity', 'Code', and 'Year'
merged_df = pd.merge(df, df1, on=['Entity', 'Code', 'Year'])
df3 = pd.read_csv("./data/change-co2-annual-pct.csv")
merged_df = pd.merge(merged_df, df3, on=['Entity', 'Code', 'Year'])

df4 = pd.read_csv('./data/annual-share-of-co2-emissions.csv')
merged_df = pd.merge(merged_df, df4, on=['Entity', 'Code', 'Year'])
df5 = pd.read_csv('./data/co-emissions-per-capita.csv')
merged_df = pd.merge(merged_df, df5, on=['Entity', 'Code', 'Year'])

# Drop the code column
merged_df = merged_df.drop(['Code'], axis=1)

#Load the datasets by organization
df1 = pd.read_csv('./data/credits/ACR/ACR Issuances.csv')
df2 = pd.read_csv('./data/credits/CAR/CAR Issuances.csv')
df3 = pd.read_csv('./data/credits/Gold/Gold Issuances.csv')

# Assign the organization the dataset is from.
df1['Organization'] = 'ACR'
df2['Organization'] = 'CAR'
df3['Organization'] = 'Gold'


#Load the projects data
df1_projects = pd.read_csv('./data/credits/ACR/ACR Projects.csv')
df2_projects = pd.read_csv('./data/credits/CAR/CAR Projects.csv')
df3_projects = pd.read_csv('./data/credits/Gold/Gold Projects.csv')

#Rename the GS_ID to Project ID for merging.
df3_projects.rename(columns={'GS_ID': 'Project ID'}, inplace=True)

df1.rename(columns={'Issuance \r\nYear': 'Issuance Year', 'Total Credits Issued': 'Total Offset Credits Issued'}, inplace=True)
df2.rename(columns={'Issuance \r\nYear': 'Issuance Year'}, inplace=True)
df3.rename(columns={'Issuance \r\nYear': 'Issuance Year', 'Country':'Project Site Country', 'Quantity':'Total Offset Credits Issued'}, inplace=True)

def createNewDf(df, projects_df):
    columns = ["Project ID", "Total Offset Credits Issued", "Project Site Country", "Issuance Year", "Organization"]
    new_df = df[columns].copy()
    merged_new_df = pd.merge(new_df, projects_df[['Project ID', 'Project Name']], on='Project ID', how='left')
    return merged_new_df

new_df1 = createNewDf(df1, df1_projects)
new_df2 = createNewDf(df2, df2_projects)
new_df3 = createNewDf(df3, df3_projects)
merged_org_df = pd.concat([new_df1, new_df2, new_df3], ignore_index=True)
#drop missing values
merged_org_df.dropna()
#rename column
merged_org_df.rename(columns={'Issuance Year': 'Year'}, inplace=True)
merged_org_df['Total Offset Credits Issued'] = pd.to_numeric(merged_org_df['Total Offset Credits Issued'], errors='coerce')

# Merge the datasets on the shared variable Year and filter years between 2002 and 2021
merged_data= merged_df.merge(merged_org_df, on='Year', how='inner')
merged_data = merged_data[(merged_data['Year'] >= 2002) & (merged_data['Year'] <= 2021)]
merged_data['Total Offset Credits Issued'] = pd.to_numeric(merged_data['Total Offset Credits Issued'], errors='coerce')
# Drop rows with NaN values
merged_data.dropna(inplace=True)


# Dashboard Title with Styling
st.title('🌍 Carbon Credit Analysis Dashboard 🌿')
st.markdown('### Exploring the impact of carbon credits on emissions reduction')

st.markdown(
    """
    As the global community grapples with the urgent challenge of climate change, there is a pressing need for 
    comprehensive understanding and effective strategies to mitigate its impacts. Carbon credits, a key instrument 
    in climate change mitigation efforts, represent a mechanism through which organizations can offset their carbon 
    emissions by investing in emissions reduction projects elsewhere. These credits not only facilitate emission 
    reductions but also drive investments in sustainable development initiatives worldwide.
    
    """
)


# Sidebar Filters with Styling
st.sidebar.header('🔍 Filters')
year_range = st.sidebar.slider('Select Year Range', min_value=2002, max_value=2021, value=(2002, 2021))

# Filter data based on selected year range
filtered_data = merged_data[(merged_data['Year'] >= year_range[0]) & (merged_data['Year'] <= year_range[1])]

# Dashboard Overview with Styling
st.header('📊 Dashboard Overview')
st.markdown("""
            This dashboard provides insights into the impact of carbon credits on reducing carbon dioxide emissions.
            Use the filters on the left to customize.
            """)

## Metrics
st.subheader('📈 Metrics')

### Total Emissions
st.write(f"🌡 Total Emissions: {filtered_data['Annual CO₂ emissions'].sum()} tons")

### Total Emissions Reduction

total_emissions_reduction = filtered_data['Total Offset Credits Issued'].sum()
st.write(f"📉 Total Emissions Reduction: {total_emissions_reduction:.2f} tons")

### Total Carbon Credits Gained
carbon_credits_gained = total_emissions_reduction  # Assuming 1 ton of CO2 emissions reduction equals 1 carbon credit
st.write(f"💰 Total Carbon Credits Gained: {carbon_credits_gained} credits")

# Function to convert credits to dollars
def convert_credits_to_dollars(credits, credit_to_dollar_rate):
    return credits * credit_to_dollar_rate

# Slider for credit to dollar rate
credit_to_dollar_rate = st.slider('💵 Credit to Dollar Rate:', min_value=1, max_value=20, value=10)

max_value = max(0, min(int(carbon_credits_gained), sys.maxsize))  
value = min(0, max_value)  

min_value = 0

value = 0  # Set initial value
credits_to_convert = st.number_input("💳 Enter the number of credits to convert:", min_value=min_value, max_value=max_value, value=value)

# Convert credits to dollars
dollars = convert_credits_to_dollars(credits_to_convert, credit_to_dollar_rate)

# Display conversion result with styled text
st.markdown(f"<div style='color: blue; font-size: 18px;'>💲 {credits_to_convert} credits is equal to ${dollars}</div>", unsafe_allow_html=True)

# Display credit to dollar rate with styled text
st.markdown(f"<div style='color: green; font-size: 16px;'>1 credit = ${credit_to_dollar_rate}</div>", unsafe_allow_html=True)

# Forecasting total offset credits
st.subheader("Forecasting Total Offset Credits")

# Convert 'Year' to datetime format
merged_org_df['Year'] = pd.to_datetime(merged_org_df['Year'], format='%Y')

# Group by 'Year' and sum the 'Total Offset Credits Issued' for each year
credits_issued_yearly = merged_org_df.groupby('Year')['Total Offset Credits Issued'].sum()

# Scaling the data using MinMaxScaler
scaler = MinMaxScaler()
credits_issued_yearly_scaled = scaler.fit_transform(credits_issued_yearly.values.reshape(-1, 1))

# Fit ARIMA model
model = ARIMA(credits_issued_yearly_scaled, order=(5,1,0))
fitted_model = model.fit()

# Forecast
forecast_steps = 10  # Adjust this as needed
forecast = fitted_model.forecast(steps=forecast_steps)

# Inverse scaling the forecasted values
forecast_inverse = scaler.inverse_transform(forecast.reshape(-1, 1)).flatten()

# Extend index for the forecasted values
last_year = credits_issued_yearly.index[-2]
forecast_index = pd.date_range(start=last_year, periods=forecast_steps, freq='Y')  # Adjusted

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(credits_issued_yearly.index, credits_issued_yearly, label='Actual', color='blue')
plt.plot(forecast_index, forecast_inverse, label='Forecast', color='red', linestyle='--')
plt.title('Total Offset Credits Issued Over Time')
plt.xlabel('Year')
plt.ylabel('Total Offset Credits Issued')
plt.legend()
plt.grid(True)

# Display the plot
st.pyplot(plt)



# Convert 'Year' to datetime format
merged_org_df['Year'] = pd.to_datetime(merged_org_df['Year'], format='%Y')

# Group by 'Year' and sum the 'Total Offset Credits Issued' for each year
credits_issued_yearly = merged_org_df.groupby('Year')['Total Offset Credits Issued'].sum()

# Scaling the data using MinMaxScaler
scaler = MinMaxScaler()
credits_issued_yearly_scaled = scaler.fit_transform(credits_issued_yearly.values.reshape(-1, 1))

# Fit ARIMA model
model = ARIMA(credits_issued_yearly_scaled, order=(5,1,0))
fitted_model = model.fit()

# Sidebar for future years selection
selected_years = st.sidebar.slider('Select Future Years (2025-2050):', min_value=2025, max_value=2050, value=(2025, 2050))

# Calculate and display future credits only when the user interacts with the sidebar
if st.sidebar.button("Calculate Future Credits"):
    # Forecast
    forecast_steps = selected_years[1] - selected_years[0] + 1  # Forecasting for the selected future years
    forecast = fitted_model.forecast(steps=forecast_steps)

    # Inverse scaling the forecasted values
    forecast_inverse = scaler.inverse_transform(forecast.reshape(-1, 1)).flatten()

    # Future years
    future_years = pd.date_range(start=str(selected_years[0]), periods=forecast_steps, freq='Y')
    
    # Create a DataFrame for future credits
    future_credits_df = pd.DataFrame({'Year': future_years.year, 'Credits': forecast_inverse})

# Display future credits in a table format with custom styling
    st.write("<style>table {border-collapse: collapse;} th, td {border: 1px solid black; padding: 8px;}</style>",           unsafe_allow_html=True)
    st.write("Future Credits for Individual Years", unsafe_allow_html=True)
    st.write(future_credits_df)

# Calculate and display the total sum of future credits
    total_credits = sum(forecast_inverse)
    st.write("<hr>", unsafe_allow_html=True)  # Horizontal line for separation
    st.write(f"Total Future Credits for the Selected Years: {total_credits:.2f}")
    
    # Adding a slider to convert credits into dollars
    conversion_rate = st.slider('Credit to Dollar Conversion Rate:', min_value=0.01, max_value=10.0, value=0.1, step=0.01)

# Calculate credits in dollars
    credits_in_dollars = total_credits * conversion_rate

# Display credits in dollars
    st.write(f"Total Future Credits in Dollars for the Selected Years: ${credits_in_dollars:.2f}")

# Display a dad joke
    dad_jokes = [
    "Why did the carbon credits go to therapy? Because they had too much emission issues!",
    "What did one carbon credit say to the other? 'You're emitting too much!'",
    "Why was the climate scientist a great comedian? They had the best carbon-offsets!",
    "How do you cheer up a sad carbon credit? You give it some renewable energy!",
    "Why did the solar panel get a credit card? It wanted to improve its energy rating!",
    "Why was the tree awarded a credit score? Because it had outstanding environmental performance!",
    "What did the wind turbine say to the solar panel? 'Let's generate some clean credits!'"
]

# Select and display a random dad joke
    selected_joke = random.choice(dad_jokes)
    st.write("Dad Joke:", selected_joke)
    
    st.markdown("[Carbon Credit Pricing](https://8billiontrees.com/carbon-offsets-credits/new-buyers-market-guide/carbon-credit-pricing/)")


        
# Custom Collaboration Feature (Chat Widget)
st.markdown("## Custom Collaboration Feature: Chat")


# Set your OpenAI API key
openai.api_key = "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"


def generate_openai_response(question):
    try:
        response = openai.Completion.create(
            engine="davinci-002",  # You can experiment with different engines
            prompt=question,
            max_tokens=50  # Adjust max_tokens as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Input box for asking questions
question = st.text_input("Ask a question about climate change or carbon credits:", "")


if st.button("Ask"):
    if question:
        question = question.capitalize()  # Capitalize the first letter
        # Generate response using OpenAI API
        response = generate_openai_response(question)
        if response:
            st.write("Bot:", response)
    else:
        st.warning("Please ask a question")

# # Function to generate response using OpenAI API
# def generate_openai_response(question):
#     response = openai.Completion.create(
#         engine="davinci-002",  # You can experiment with different engines
#         prompt=question,
#         max_tokens=50  # Adjust max_tokens as needed
#     )
#     return response.choices[0].text.strip()

# # Input box for asking questions
# question = st.text_input("Ask a question about climate change or carbon credits:", "")

# # Fetch and display response upon submitting a question
# if st.button("Ask"):
#     if question:
#         question = question.capitalize()  # Capitalize the first letter
#         # Generate response using OpenAI API
#         response = generate_openai_response(question)
#         st.write("Bot:", response)
#     else:
#         st.warning("Please ask a question")

    

## Documentation and Tutorials
st.subheader('Documentation and Tutorials')

# Add link to climate change documentation
st.markdown("[Climate Change Documentation](https://www.bing.com/ck/a?!&&p=b134e78a2dc71b9aJmltdHM9MTcwNzI2NDAwMCZpZ3VpZD0yNThiZGE0NS1mMjZkLTY2OGYtMjViMC1jOGEyZjNlZjY3NTQmaW5zaWQ9NTE5NA&ptn=3&ver=2&hsh=3&fclid=258bda45-f26d-668f-25b0-c8a2f3ef6754&psq=climate+change&u=a1aHR0cHM6Ly93d3cudW4ub3JnL2VuL2NsaW1hdGVjaGFuZ2Uvd2hhdC1pcy1jbGltYXRlLWNoYW5nZQ&ntb=1)")

# Add link to carbon credit documentation
st.markdown("[Carbon Credit Documentation](https://www.bing.com/ck/a?!&&p=326400e649a18afeJmltdHM9MTcwNzI2NDAwMCZpZ3VpZD0yNThiZGE0NS1mMjZkLTY2OGYtMjViMC1jOGEyZjNlZjY3NTQmaW5zaWQ9NTIwOA&ptn=3&ver=2&hsh=3&fclid=258bda45-f26d-668f-25b0-c8a2f3ef6754&psq=+carbon+credit&u=a1aHR0cHM6Ly93d3cud2Vmb3J1bS5vcmcvYWdlbmRhLzIwMjAvMTEvY2FyYm9uLWNyZWRpdHMtd2hhdC1ob3ctZmlnaHQtY2xpbWF0ZS1jaGFuZ2Uv&ntb=1)")




# Section : Carbon Footprint Calculator
st.title("Carbon Footprint Calculator")

# Add input fields for users to enter information about their activities
st.subheader("Enter Your Information:")
energy_usage = st.number_input("Energy Usage (kWh/year):", min_value=0)
transportation = st.number_input("Transportation Emissions (kg CO2/year):", min_value=0)
lifestyle_choices = st.number_input("Lifestyle Choices (kg CO2/year):", min_value=0)

# Calculate total carbon footprint
total_carbon_footprint = energy_usage + transportation + lifestyle_choices

# Display the total carbon footprint to the user
st.subheader("Your Total Carbon Footprint:")
st.write(f"{total_carbon_footprint} kg CO2/year")



# Section : Virtual Tours of Sustainability Initiatives
st.title("Virtual Tours of Sustainability Initiatives")

# Add dropdown menu for selecting different virtual tours
tour_options = ["Renewable Energy Installation", "Green Building", "Eco-friendly Transportation System"]
selected_tour = st.selectbox("Select a Virtual Tour:", tour_options)

# Embed videos based on the selected tour
if selected_tour == "Renewable Energy Installation":
    st.write("Welcome to the virtual tour of a renewable energy installation!")
    st.video("https://www.youtube.com/watch?v=xJgrDYNwdHU")  
    

elif selected_tour == "Green Building":
    st.write("Welcome to the virtual tour of a green building!")
    st.video("https://www.youtube.com/watch?v=ISRC3b9I6Ks&t=28s")  
    

elif selected_tour == "Eco-friendly Transportation System":
    st.write("Welcome to the virtual tour of an eco-friendly transportation system!")
    st.video("https://www.youtube.com/watch?v=vadtYfkvnI0&t=14s")  

    
# Help and Support
st.header('Help and Support')

# Provide options for customer support
st.write("If you need further assistance, please reach out to our customer support team:")
st.write("- Email: support@example.com")
st.write("- Phone: +254 (123) 67789")
st.write("- Live Chat: [Chat Now](https://www.example.com/live-chat)")