import boto3
import base64
import json

# Create a Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name = 'us-east-1')

import boto3
import json

# Create a Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Define a function to handle the chatbot with memory
def chatbot_with_memory(conversation_history, user_input):
    print(" I reached here")
    # Append the new user message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            }
        ]
    })

    # Define the payload with conversation history
    payload = {
        "modelId": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "accept": "application/json",
        "contentType": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": conversation_history
        })
    }

    # Invoke the model
    response = bedrock_runtime.invoke_model(**payload)

    # Read and extract the model's response
    body = json.loads(response["body"].read())
    model_response = body['content'][0]['text']

    # Append the model's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": model_response
            }
        ]
    })
    print(conversation_history)

    # Return the response and updated conversation history
    return model_response, conversation_history

