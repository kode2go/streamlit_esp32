import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
import time

# Blynk configuration
BLYNK_AUTH_TOKEN = "_Tx2yYYTCFm4Q0tzfLZmc_87QBkEdxYt"  # Replace with your Blynk token
BLYNK_VPIN = "V4"  # The virtual pin you're using

# Initialize the session state for storing data
if 'data_df' not in st.session_state:
    st.session_state.data_df = pd.DataFrame(columns=["Timestamp", "Value"])

def fetch_blynk_data():
    url = f"https://ny3.blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&{BLYNK_VPIN}"
    try:
        response = requests.get(url)
        # Debugging output: print status code and content
        st.write(f"Status code: {response.status_code}")
        st.write(f"Response content: {response.text}")
        
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        # Debugging output: print exception
        st.write(f"Error occurred: {e}")
        return None

# Streamlit UI
st.title("Blynk Data Fetcher")

st.write("Fetching data from Blynk...")

# Auto-refresh logic
if 'last_fetch_time' not in st.session_state:
    st.session_state.last_fetch_time = time.time()

# Check if it's time to refresh data
if time.time() - st.session_state.last_fetch_time > 1:  # Refresh every 10 seconds
    st.session_state.last_fetch_time = time.time()
    blynk_value = fetch_blynk_data()  # Fetch new data when time is up
else:
    blynk_value = None  # Do not fetch data if not time yet

# Display the fetched value
if blynk_value is not None:
    st.write(f"Value from Blynk (V4): {blynk_value}")
    # Store the fetched value and the current timestamp for DataFrame
    try:
        value_float = float(blynk_value)  # Convert to float for the gauge and DataFrame
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Store current timestamp
        
        # Append new data to the session state DataFrame
        new_row = pd.DataFrame({"Timestamp": [current_time], "Value": [value_float]})
        st.session_state.data_df = pd.concat([st.session_state.data_df, new_row], ignore_index=True)
        
        # Display the DataFrame
        st.subheader("Captured Data")
        st.dataframe(st.session_state.data_df)

        # Create a string to display all timestamps and values
        all_data = "\n".join(f"Timestamp: {ts}, Value: {val}" for ts, val in zip(st.session_state.data_df['Timestamp'], st.session_state.data_df['Value']))
        
        # Display in text area
        st.text_area("Captured Timestamps and Values", 
                      all_data, 
                      height=300)
    except ValueError:
        st.write("Invalid data received from Blynk, unable to convert to float.")
else:
    st.write("Waiting for data...")

# Gauge Display
if not st.session_state.data_df.empty:
    st.subheader("Gauge")
    st.metric(label="Blynk Value", value=st.session_state.data_df['Value'].iloc[-1])  # Display the latest value as a gauge

# Plotting the values using Plotly
if len(st.session_state.data_df) > 1:
    st.subheader("Value Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=st.session_state.data_df['Timestamp'], y=st.session_state.data_df['Value'], mode='lines+markers', name='Blynk Value'))
    fig.update_layout(title='Blynk Value Over Time',
                      xaxis_title='Timestamp',
                      yaxis_title='Value',
                      showlegend=True,
                      xaxis_tickangle=-45)  # Rotate x-axis labels for better readability
    st.plotly_chart(fig)

# Manual refresh button (if needed)
if st.button("Refresh Now"):
    st.rerun()  # Change made here
