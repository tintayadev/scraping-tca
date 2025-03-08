# App Documentation

## Introduction

This Flask application is designed to generate a report csv of a certain page.

## Installation

### Prerequisites
- Python 3.11+
- Flask
- webdriver(Chrome)

### Steps to Install
0. copy env vars
    ``bash
    cp app/.env.EXAMPLE app/.env
    ``
1. Clone the repository:
   ```bash
   python -m venv venv && source venv/bin/activate
   ```
2. Navigate to the project directory:
   ```bash
   cd app
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the application, use the following command:

`python app.py`

## IMPORTANT

The reports are from the current date to [3 days after (function get_3days_after)](./app/scraper.py).
