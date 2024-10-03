import streamlit as st
import requests

# Blynk configuration
BLYNK_AUTH_TOKEN = "2wzUwRv1MrP_-OarfCkzZ6R39EC76pa1" # Replace with your Blynk token
BLYNK_VPIN = "v4"  # The virtual pin you're using

def fetch_blynk_data():
    url = f"https://blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&vpin={BLYNK_VPIN}"
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
else:
    st.write("Failed to fetch data from Blynk.")
