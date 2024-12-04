# import requests

# def send_request(url, method, params=None, file_input=None):
#     try:
#         if method == "POST":
#             if file_input:
#                 files = {"file": (file_input.name, file_input.getvalue())}
#                 response = requests.post(url, files=files)
#             else:
#                 response = requests.post(url, json=params)
#         elif method == "GET":
#             response = requests.get(url, params=params)
#         return response
#     except requests.exceptions.RequestException as e:
#         raise RuntimeError(f"API Request failed: {e}")

# import requests

# def send_request(url, method, input_values, file_input):
#     """
#     Sends an HTTP request based on method, input values, and file input.
#     """
#     try:
#         # If the request method is POST and includes a file
#         if method == "POST" and file_input is not None:
#             # Prepare the multipart/form-data payload
#             files = {"file": (file_input.name, file_input.getvalue(), file_input.type)}
#             data = {key: value for key, value in input_values.items()}  # Add form fields
#             response = requests.post(url, data=data, files=files)
#         elif method == "POST":
#             # JSON payload for requests without files
#             response = requests.post(url, json=input_values)
#         elif method == "GET":
#             # Query parameters for GET requests
#             response = requests.get(url, params=input_values)
#         else:
#             raise ValueError(f"Unsupported HTTP method: {method}")
        
#         return response
#     except Exception as e:
#         raise RuntimeError(f"Error sending request: {e}")

import requests

def send_request(url, method, input_values=None, file_inputs=None):
    """
    Sends an HTTP request based on method, input values, and file inputs.

    Args:
    - url (str): The endpoint URL.
    - method (str): HTTP method (e.g., "GET", "POST").
    - input_values (dict): Key-value pairs for form fields or JSON payload.
    - file_inputs (list): A list of files, each being a dictionary with keys 'name', 'content', and 'type'.

    Returns:
    - Response object from the `requests` library.
    """
    try:
        if method == "POST":
            # Handle multipart/form-data if file_inputs are provided
            if file_inputs:
                files = [
                    ("file", (file_input["name"], file_input["content"], file_input["type"]))
                    for file_input in file_inputs
                ]
                data = input_values or {}  # Add any other form fields
                response = requests.post(url, data=data, files=files)
            else:
                # Handle JSON payload for POST without files
                response = requests.post(url, json=input_values)
        elif method == "GET":
            # Handle query parameters for GET
            response = requests.get(url, params=input_values)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    except Exception as e:
        raise RuntimeError(f"Error sending request: {e}")


