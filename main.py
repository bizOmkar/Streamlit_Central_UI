import streamlit as st
from utils.file_handler import load_endpoints, save_endpoints
from utils.api_requests import send_request
from utils.ui_components import render_input_fields
import pandas as pd
from io import BytesIO

# Initialize session state
if "endpoints" not in st.session_state:
    st.session_state["endpoints"] = load_endpoints()

# Streamlit UI
st.title("Dynamic API Interaction")

# API selection
options = list(st.session_state["endpoints"].keys()) + ["Custom API"]
selected_option = st.selectbox("Select an API Endpoint", options)

# Handle custom API creation
if selected_option == "Custom API":
    st.subheader("Create a New API")
    with st.form("add_endpoint_form"):
        new_name = st.text_input("API Name (to display in dropdown)")
        new_url = st.text_input("API URL")
        new_method = st.selectbox("HTTP Method", ["GET", "POST"])
        new_fields = st.text_area(
            "Fields (Enter JSON format, e.g., [{'name': 'field1', 'type': 'text', 'placeholder': 'Enter field1'}])"
        )
        submitted = st.form_submit_button("Add API")

        if submitted:
            try:
                parsed_fields = eval(new_fields) if new_fields.strip() else []
                st.session_state["endpoints"][new_name] = {
                    "url": new_url,
                    "method": new_method,
                    "fields": parsed_fields
                }
                save_endpoints(st.session_state["endpoints"])
                st.success(f"Added new API: {new_name}")
            except Exception as e:
                st.error(f"Failed to add API. Error: {e}")

elif selected_option:
    endpoint = st.session_state["endpoints"][selected_option]
    st.subheader(f"Endpoint: {selected_option}")
    st.write(f"**Method:** {endpoint['method']}")
    st.write(f"**URL:** {endpoint['url']}")

    # Input fields for parameters
    input_values, file_input = render_input_fields(endpoint.get("fields", []))

    # Send request
    if st.button("Send Request"):
        try:
            # Send the API request
            response = send_request(endpoint["url"], endpoint["method"], input_values, file_input)
            st.write(input_values, file_input)
            # Check response status
            if response.status_code == 200:
                st.success("Request Successful!")

                # Detect response type
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    response_data = response.json()
                    
                    # User toggle between JSON and DataFrame
                    display_format = st.radio("Choose Display Format", ["JSON", "DataFrame"], index=0)
                    if display_format == "JSON":
                        st.subheader("Response (JSON Format):")
                        st.json(response_data)
                    elif display_format == "DataFrame":
                        st.subheader("Response (DataFrame Format):")
                        try:
                            if isinstance(response_data, list):
                                df = pd.DataFrame(response_data)
                            elif isinstance(response_data, dict) and "data" in response_data:
                                df = pd.DataFrame(response_data["data"])
                            else:
                                df = None

                            if df is not None:
                                st.dataframe(df)
                            else:
                                st.warning("The response cannot be displayed as a DataFrame.")
                        except Exception as e:
                            st.error(f"Failed to parse response as DataFrame: {e}")
                elif "text/plain" in content_type:
                    st.subheader("Response (Plain Text):")
                    st.text(response.text)
                elif "application/octet-stream" in content_type or "application/" in content_type:
                    st.subheader("Response (File Download):")
                    file_name = response.headers.get("Content-Disposition", "attachment").split("filename=")[-1].strip()
                    st.download_button(label="Download File", data=response.content, file_name=file_name)
                else:
                    st.warning("Unknown Content Type. Displaying raw response:")
                    st.text(response.text)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# import streamlit as st
# from utils.file_handler import load_endpoints, save_endpoints
# from utils.api_requests import send_request
# from utils.ui_components import render_input_fields
# import pandas as pd

# # Initialize session state
# if "endpoints" not in st.session_state:
#     st.session_state["endpoints"] = load_endpoints()

# # Streamlit UI
# st.title("Dynamic API Interaction")

# # API selection
# options = list(st.session_state["endpoints"].keys()) + ["Custom API"]
# selected_option = st.selectbox("Select an API Endpoint", options)

# # Handle custom API creation
# if selected_option == "Custom API":
#     st.subheader("Create a New API")
#     with st.form("add_endpoint_form"):
#         new_name = st.text_input("API Name (to display in dropdown)")
#         new_url = st.text_input("API URL")
#         new_method = st.selectbox("HTTP Method", ["GET", "POST"])
#         new_fields = st.text_area(
#             "Fields (Enter JSON format, e.g., [{'name': 'field1', 'type': 'text', 'placeholder': 'Enter field1'}])"
#         )
#         submitted = st.form_submit_button("Add API")

#         if submitted:
#             try:
#                 parsed_fields = eval(new_fields) if new_fields.strip() else []
#                 st.session_state["endpoints"][new_name] = {
#                     "url": new_url,
#                     "method": new_method,
#                     "fields": parsed_fields
#                 }
#                 save_endpoints(st.session_state["endpoints"])
#                 st.success(f"Added new API: {new_name}")
#             except Exception as e:
#                 st.error(f"Failed to add API. Error: {e}")

# elif selected_option:
#     endpoint = st.session_state["endpoints"][selected_option]
#     st.subheader(f"Endpoint: {selected_option}")
#     st.write(f"**Method:** {endpoint['method']}")
#     st.write(f"**URL:** {endpoint['url']}")

#     # Input fields for parameters
#     input_values, file_input = render_input_fields(endpoint.get("fields", []))

#     # Option to choose display format before sending the request
#     display_format = st.radio("Choose Response Format", ["JSON", "DataFrame"], index=0)

#     if st.button("Send Request"):
#         try:
#             # Send the API request
#             response = send_request(endpoint["url"], endpoint["method"], input_values, file_input)
            
#             # Check response status
#             if response.status_code == 200:
#                 st.success("Request Successful!")
#                 response_data = response.json()

#                 # Handle response based on the selected format
#                 if display_format == "JSON":
#                     st.subheader("Response (JSON Format):")
#                     st.json(response_data)
#                 elif display_format == "DataFrame":
#                     st.subheader("Response (DataFrame Format):")
#                     try:
#                         if isinstance(response_data, list):
#                             df = pd.DataFrame(response_data)
#                         elif isinstance(response_data, dict) and "data" in response_data:
#                             df = pd.DataFrame(response_data["data"])
#                         else:
#                             df = None

#                         if df is not None:
#                             st.dataframe(df)
#                         else:
#                             st.warning("The response cannot be displayed as a DataFrame.")
#                     except Exception as e:
#                         st.error(f"Failed to parse response as DataFrame: {e}")
#             else:
#                 st.error(f"Error: {response.status_code}")
#                 st.write(response.text)
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
