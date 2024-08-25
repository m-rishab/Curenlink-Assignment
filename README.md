## Project Overview

This project automates the process of responding to patient meal picture queries for Curelink, which provides care for patients with conditions like PCOS, pregnancy, and preconception. The goal is to replace human effort in this process with AI-generated responses, ensuring they align with each patient's diet chart and health profile.

## Technologies Used

- **Python**: Data handling and interaction with the AI model.
- **Anthropic Claude API**: Used the `claude-3-5-sonnet-20240620` model to generate responses.

## Project Structure

- `queries.json`: Sample patient queries, including their profile context, chat history, and ideal responses.
- `app.py`: The Python script that processes the queries and generates AI-based responses.
- `output.json`: The generated responses based on the queries.
- `README.md`: This document providing an overview of the project.

## How It Works

1. **Input Parsing**: The script loads and parses the patient queries from `queries.json`.
2. **AI Response Generation**: For each query, the script uses the `claude-3-5-sonnet-20240620` model to generate a response that matches the patient's diet chart and specific health conditions.
3. **Output**: The generated responses are saved in `output.json` in the required format.

## Running the Project

1. Ensure you have Python installed.
2. Install the required packages:
    ```bash
    pip install anthropic
    ```
3. Run the script:
    ```bash
    python app.py
    ```
4. The responses will be saved in the `output.json` file.
