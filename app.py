import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('data/state_wise_daily.csv')

# Convert 'Date_YMD' column to datetime format
data['Date_YMD'] = pd.to_datetime(data['Date_YMD'])

# State codes to full names mapping
state_mapping = {
    "TT": "Total",
    "AN": "Andaman and Nicobar Islands",
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CH": "Chandigarh",
    "CT": "Chhattisgarh",
    "DN": "Dadra and Nagar Haveli and Daman and Diu",
    "DD": "Daman and Diu",
    "DL": "Delhi",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JK": "Jammu and Kashmir",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Odisha",
    "PY": "Puducherry",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TG": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UT": "Uttarakhand",
    "WB": "West Bengal",
    "UN": "Unassigned",
}

# Sidebar for user input
st.sidebar.header("Filter Options")

# Date range selection
start_date = st.sidebar.date_input("Start Date", data['Date_YMD'].min())
end_date = st.sidebar.date_input("End Date", data['Date_YMD'].max())

# Case type selection
case_type = st.sidebar.radio("Select Case Type", ['Confirmed', 'Recovered', 'Deceased'])

# State selection
state_choices = list(state_mapping.values())
selected_states = st.sidebar.multiselect("Select States", state_choices, default=["Total"])

# Filter the data based on user input
filtered_data = data[
    (data['Date_YMD'] >= pd.to_datetime(start_date)) &
    (data['Date_YMD'] <= pd.to_datetime(end_date)) &
    (data['Status'] == case_type)
]

# Map selected states back to codes
selected_state_codes = [code for code, name in state_mapping.items() if name in selected_states]

# Main app display
st.title("COVID-19 State-Wise Data Visualization")
st.write(f"Visualizing **{case_type}** cases from {start_date} to {end_date}.")

if not filtered_data.empty:
    # Filter columns for selected states
    filtered_data = filtered_data[['Date_YMD', 'Status'] + selected_state_codes]
    st.dataframe(filtered_data)

    # Plot the data
    st.header(f"Trend for {case_type} Cases")
    plt.figure(figsize=(10, 6))
    for code in selected_state_codes:
        plt.plot(filtered_data['Date_YMD'], filtered_data[code], label=state_mapping[code])

    plt.xlabel("Date")
    plt.ylabel(f"{case_type} Cases")
    plt.title(f"{case_type} Cases Trend")
    plt.legend()
    plt.grid()
    st.pyplot(plt)
else:
    st.write("No data available for the selected filters.")
