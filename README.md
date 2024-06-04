# Equipment Check-In PDF Generator and Comment Poster

This project consists of two main scripts: one for generating a PDF document for equipment check-in and another for posting a comment with the generated PDF link on a ticketing system. The scripts use the ReportLab library for PDF generation and the Requests library for API interactions.

## Table of Contents
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Usage](#usage)
- [Code Overview](#code-overview)
  - [checkin.py](#checkinpy)
    - [MCLine Class](#mcline-class)
    - [TextField Class](#textfield-class)
    - [make_pdf Function](#make_pdf-function)
    - [get_ids_for_view Function](#get_ids_for_view-function)
    - [get_assets_for_user Function](#get_assets_for_user-function)
    - [get_user_balance Function](#get_user_balance-function)
    - [form_assets_csv Function](#form_assets_csv-function)
    - [ready_payload Function](#ready_payload-function)
    - [main Function (checkin.py)](#main-function-checkinpy)
  - [comment_post.py](#comment_postpy)
    - [main Function (comment_post.py)](#main-function-comment_postpy)
- [Logging](#logging)
- [Example](#example)

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
### Generating the PDF
Run the `checkin.py` script by providing a ticket ID as an argument:
```bash
python checkin.py <ticket_id>
```
This will generate a PDF document with the check-in details for the specified ticket ID.

### Posting the Comment
Run the `comment_post.py` script by providing the SharePoint URL and a file path:
```bash
python comment_post.py <sharepoint_url> <file_path_prefix>
```
This will post a comment on the ticket with a link to the generated PDF.

## Code Overview

### checkin.py

#### MCLine Class
Creates a flowable for a horizontal line in the PDF.

#### TextField Class
Creates a flowable for a text field in the PDF, allowing customization of width, height, and font size.

#### make_pdf Function
Generates a PDF document using data from a CSV file and user information.

#### get_ids_for_view Function
Retrieves ticket IDs for a specific view.

#### get_assets_for_user Function
Fetches the assets associated with a specific user.

#### get_user_balance Function
Fetches the balance amount for a specific user.

#### form_assets_csv Function
Creates a CSV file from the assets JSON data.

#### ready_payload Function
Retrieves data from a ticket and populates the configuration.

#### main Function (checkin.py)
Main function to create the check-in document for a given ticket ID.

### comment_post.py

#### main Function (comment_post.py)
Posts a comment on the ticket with a link to the generated PDF.

## Logging
Logging is configured to write to files named `CheckInAPI_<timestamp>.log` and `CommentPost_<timestamp>.log` in the working directory, recording the process flow and any errors encountered.

## Example
To create a PDF for ticket ID `12345`, run:
```bash
python checkin.py 12345
```
To post a comment with the SharePoint URL `http://sharepoint.example.com/doc` and file path prefix `Docs/username`, run:
```bash
python comment_post.py http://sharepoint.example.com/doc Docs/username
```
This will produce a PDF document with the equipment check-in details for the user associated with the given ticket ID and post a comment with the PDF link on the ticket.
