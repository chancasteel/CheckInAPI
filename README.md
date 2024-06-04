# Equipment Check-In PDF Generator

This project generates a PDF document for equipment check-in using data from a CSV file and user information retrieved via an API. The generated PDF includes a list of assets, user information, and signature fields. It utilizes the ReportLab library for PDF generation and logging to keep track of the process.

## Table of Contents
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Usage](#usage)
- [Code Overview](#code-overview)
  - [MCLine Class](#mcline-class)
  - [TextField Class](#textfield-class)
  - [make_pdf Function](#make_pdf-function)
  - [get_ids_for_view Function](#get_ids_for_view-function)
  - [get_assets_for_user Function](#get_assets_for_user-function)
  - [get_user_balance Function](#get_user_balance-function)
  - [form_assets_csv Function](#form_assets_csv-function)
  - [ready_payload Function](#ready_payload-function)
  - [main Function](#main-function)

## Requirements
- Python 3.x
- Required libraries:
  - `requests`
  - `reportlab`

You can install the necessary libraries using:
```bash
pip install requests reportlab
```

## Configuration
Create a `config.py` file with the following structure to store your configuration:
```python
# config.py
path = {
    'image': 'path/to/logo.png',  # Path to your logo image
    'pdf': 'path/to/output.pdf',  # Path where the PDF will be saved
    'csv': 'path/to/data.csv'     # Path where the CSV will be saved
}

credentials = {
    'url': 'https://api.example.com',  # Base URL for your API
    'headers': {
        'Authorization': 'Bearer your_token',  # API authentication token
        'Content-Type': 'application/json'
    }
}

ticket = {
    'username': '',
    'fullname': '',
    'userid': '',
    'ticket_id_url': '',
    'location': ''
}
```

## Usage
Run the script by providing a ticket ID as an argument:
```bash
python checkin.py <ticket_id>
```
This will generate a PDF document with the check-in details for the specified ticket ID.

## Code Overview

### MCLine Class
Creates a flowable for a horizontal line in the PDF.

### TextField Class
Creates a flowable for a text field in the PDF, allowing customization of width, height, and font size.

### make_pdf Function
Generates a PDF document using data from a CSV file and user information.

### get_ids_for_view Function
Retrieves ticket IDs for a specific view.

### get_assets_for_user Function
Fetches the assets associated with a specific user.

### get_user_balance Function
Fetches the balance amount for a specific user.

### form_assets_csv Function
Creates a CSV file from the assets JSON data.

### ready_payload Function
Retrieves data from a ticket and populates the configuration.

### main Function
Main function to create the check-in document for a given ticket ID. 

## Logging
Logging is configured to write to a file named `CheckInAPI_<timestamp>.log` in the working directory, recording the process flow and any errors encountered.

## Example
To create a PDF for ticket ID `12345`, run:
```bash
python checkin.py 12345
```
This will produce a PDF document with the equipment check-in details for the user associated with the given ticket ID.
