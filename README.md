# AWS Chatbot

This project provides a simple natural language chatbot that can answer questions about your AWS account using the LangChain framework.

## Features

The chatbot exposes custom tools backed by boto3 for:

- Counting the number of S3 buckets that are publicly accessible.
- Listing all S3 buckets in the account.
- Listing example objects in a specific S3 bucket.
- Finding the instance type of an EC2 instance by IP address.
- Listing IAM policies attached to a given user.

These tools are combined with an OpenAI chat model via LangChain's function calling agent to allow natural language interaction.

## Usage

1. Install dependencies (requires Python 3.12 or later):

```bash
pip install -r requirements.txt
```

2. Export your AWS credentials and an OpenAI API key:

```bash
export AWS_ACCESS_KEY_ID=...  # or configure using any AWS method
export AWS_SECRET_ACCESS_KEY=...
export OPENAI_API_KEY=...
```

3. Run the chatbot:

```bash
python -m awschatbot.chatbot
```

You can then ask questions such as:

- "How many S3 buckets are exposed to the public?"
- "List all S3 buckets in the account."
- "What data does the S3 bucket my-bucket hold?"
- "What is the size of the EC2 instance with IP 1.2.3.4?"
- "What permissions does the user alice have?"

Note that the tools rely on boto3 and therefore require access credentials with appropriate permissions.
