import json
import os

FILE_PATH = "endpoints.json"

DEFAULT_ENDPOINTS = {
    "Get All Books": {
        "url": "http://127.0.0.1:8000/books",
        "method": "GET",
        "fields": []
    },
    "Create a New Book": {
        "url": "http://127.0.0.1:8000/create-book",
        "method": "POST",
        "fields": [
            {"name": "title", "type": "text", "placeholder": "Enter book title"},
            {"name": "author", "type": "text", "placeholder": "Enter author name"},
            {"name": "description", "type": "text", "placeholder": "Enter description"},
            {"name": "rating", "type": "number", "placeholder": "Enter rating (1-5)"}
        ]
    }
}

def load_endpoints():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    else:
        # Save default endpoints if the file does not exist
        save_endpoints(DEFAULT_ENDPOINTS)
        return DEFAULT_ENDPOINTS

def save_endpoints(endpoints):
    with open(FILE_PATH, "w") as file:
        json.dump(endpoints, file, indent=4)
