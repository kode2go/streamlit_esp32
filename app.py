import streamlit as st
import requests
import plotly.graph_objs as go
from datetime import datetime

# Blynk configuration
BLYNK_AUTH_TOKEN = "_Tx2yYYTCFm4Q0tzfLZmc_87QBkEdxYt"  # Replace with your Blynk token
BLYNK_VPIN = "V4"  # The virtual pin you're using

# Lists to store fetched values and their corresponding timestamps for plotting
fetched_values = []
timestamps = []

def fetch_blynk_data():
    url = f"https://ny3.blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&vpin={BLYNK_VPIN}"
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

# Add a refresh button
if st.button('Refresh'):
    blynk_value = fetch_blynk_data()  # Fetch new data when button is pressed
else:
    blynk_value = fetch_blynk_data()  # Initial fetch on app load

# Display the fetched value
if blynk_value is not None:
    st.write(f"Value from Blynk (V4): {blynk_value}")
    # Store the fetched value and the current timestamp for plotting
    try:
        fetched_values.append(float(blynk_value))  # Convert to float for the gauge and plot
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Store current timestamp
        timestamps.append(current_time)
        
        # Create a string to display all timestamps and values
        all_data = "\n".join(f"Timestamp: {ts}, Value: {val}" for ts, val in zip(timestamps, fetched_values))
        
        # Display in text area
        st.text_area("Captured Timestamps and Values", 
                      all_data, 
                      height=300)
    except ValueError:
        st.write("Invalid data received from Blynk, unable to convert to float.")
else:
    st.write("Failed to fetch data from Blynk.")

# Gauge Display
if fetched_values:
    st.subheader("Gauge")
    st.metric(label="Blynk Value", value=fetched_values[-1])  # Display the latest value as a gauge

# Plotting the values using Plotly
if len(fetched_values) > 1:
    st.subheader("Value Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=fetched_values, mode='lines+markers', name='Blynk Value'))
    fig.update_layout(title='Blynk Value Over Time',
                      xaxis_title='Timestamp',
                      yaxis_title='Value',
                      showlegend=True,
                      xaxis_tickangle=-45)  # Rotate x-axis labels for better readability
    st.plotly_chart(fig)
