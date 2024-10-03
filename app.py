import streamlit as st
import requests
import plotly.graph_objs as go # test

# Blynk configuration
BLYNK_AUTH_TOKEN = "_Tx2yYYTCFm4Q0tzfLZmc_87QBkEdxYt"  # Replace with your Blynk token
BLYNK_VPIN = "V4"  # The virtual pin you're using

# List to store fetched values for plotting
fetched_values = []

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

# Add a refresh button
if st.button('Refresh'):
    blynk_value = fetch_blynk_data()  # Fetch new data when button is pressed
else:
    blynk_value = fetch_blynk_data()  # Initial fetch on app load

# Display the fetched value
if blynk_value is not None:
    st.write(f"Value from Blynk (V4): {blynk_value}")
    # Store the fetched value for plotting
    try:
        fetched_values.append(float(blynk_value))  # Convert to float for the gauge and plot
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
    fig.add_trace(go.Scatter(x=list(range(len(fetched_values))), y=fetched_values, mode='lines+markers', name='Blynk Value'))
    fig.update_layout(title='Blynk Value Over Time',
                      xaxis_title='Fetch Number',
                      yaxis_title='Value',
                      showlegend=True)
    st.plotly_chart(fig)

