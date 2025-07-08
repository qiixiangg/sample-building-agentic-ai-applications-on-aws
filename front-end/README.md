# GenAI Workshop Front-end

This repository contains a Streamlit application for interacting with Amazon Bedrock Agents.

## Prerequisites

- Python 3.8 or higher
- AWS credentials configured with appropriate permissions for Amazon Bedrock
- Required Python packages (listed in `requirements.txt`)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd genai-workshop/front-end
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - The `.env` file already includes the `AWS_SECRET_NAME` of the secret that was created in the AWS environment for accessing the configured Bedrock agents
   - If you have deployed your AWS resources in a region other than us-east-1, update the `AWS_REGION` value accordingly

## Running the Streamlit App

To run the Streamlit application:

```bash
streamlit run app.py
```

This will start the Streamlit server and automatically open the application in your default web browser. If it doesn't open automatically, you can access it at http://localhost:8501.

## Application Features

- Connect to Amazon Bedrock Agents
- Chat with single or multiple agents
- View agent responses and interactions

## Troubleshooting

- Ensure your AWS credentials are properly configured
- Check that all required environment variables are set in the `.env` file
- Verify that you have the necessary permissions to access Amazon Bedrock services
