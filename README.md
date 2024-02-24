# Setting Up and Running the Flask Application

This guide will walk you through setting up a virtual environment, installing the required dependencies, and running the Flask application both locally and as a Docker container.

## Setting Up a Virtual Environment

To isolate our project dependencies, we'll use a virtual environment. Follow these steps to set it up:

1. Navigate to the project directory in your terminal.
2. Run the following command to create a virtual environment named `venv`:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows, run:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux, run:
     ```
     source venv/bin/activate
     ```

## Installing Dependencies

With the virtual environment activated, install the project dependencies by running:

python app.py

# DOCKER

## Build docker with the command
docker build -t excel-magic-api .
