import streamlit as st
import requests
from requests.exceptions import RequestException

# Function to check the status of each URL
def check_url_status(url):
    try:
        response = requests.get(url, timeout=5)  # Timeout to prevent hanging
        return response.status_code, "OK" if response.ok else "Error"
    except RequestException as e:
        return None, f"Error: {e}"

# Streamlit application
def main():
    st.title("Website Link Tester")
    st.write("This tool tests if the given links are accessible and working properly.")

    # Input URLs separated by newlines
    url_list = st.text_area("Enter website URLs (one per line):")
    if st.button("Test Links"):
        # Parse URLs and remove empty lines
        urls = [url.strip() for url in url_list.splitlines() if url.strip()]

        if urls:
            st.write("Testing URLs...")
            results = []
            for url in urls:
                status_code, status_text = check_url_status(url)
                results.append((url, status_code, status_text))

            # Display results in a table
            st.write("## Test Results")
            for url, status_code, status_text in results:
                st.write(f"**{url}** - Status: `{status_code}` - {status_text}")
        else:
            st.error("Please enter at least one URL.")

if __name__ == "__main__":
    main()
