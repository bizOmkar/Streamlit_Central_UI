import streamlit as st

def render_input_fields(fields):
    input_values = {}
    file_input = None

    for field in fields:
        if field["type"] == "text" or field["type"] == "string":
            input_values[field["name"]] = st.text_input(field["name"], placeholder=field.get("placeholder", ""))
        elif field["type"] == "number" or field["type"] == "int":
            input_values[field["name"]] = st.number_input(field["name"], step=1.0, format="%d" if field["type"] == "int" else None, placeholder=field.get("placeholder", ""))
        elif field["type"] == "file":
            file_input = st.file_uploader(field.get("placeholder", "Upload a file"), type=["csv", "txt", "pdf", "docx", "png", "jpg"])

    return input_values, file_input

