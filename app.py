import streamlit as st
import requests

# Blynk configuration
BLYNK_AUTH_TOKEN = "2wzUwRv1MrP_-OarfCkzZ6R39EC76pa1" # Replace with your Blynk token
BLYNK_VPIN = "V4"  # The virtual pin you're using

# Fetch data from Blynk cloud
def fetch_blynk_data():
    url = f"https://blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&vpin={BLYNK_VPIN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

# Streamlit UI
st.title("Blynk Data Fetcher")

st.write("Fetching data from Blynk...")

blynk_value = fetch_blynk_data()

if blynk_value is not None:
    st.write(f"Value from Blynk (V4): {blynk_value}")
else:
    st.write("Failed to fetch data from Blynk.")

# Optionally, add a refresh button
if st.button('Refresh'):
    st.experimental_rerun()
