import os
import json
import boto3
import logging
import http.client
from datetime import datetime
from urllib.parse import urlparse

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3_client = boto3.client('s3')

# Environment variables for configuration
BUCKET_NAME = os.getenv('BUCKET_NAME', 'default_bucket_name')  # Replace with your default bucket name
DESTINATION_URL = os.getenv('DESTINATION_URL', 'https://example.com/webhook')  # Replace with your default URL
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'default_verify_token')  # Replace with your default verify token

def forward_data_to_url(data):
    try:
        # Parse the URL
        parsed_url = urlparse(DESTINATION_URL)
        connection = http.client.HTTPSConnection(parsed_url.netloc)
        
        # Prepare headers and payload
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(data)
        
        # Send POST request
        connection.request("POST", parsed_url.path, payload, headers)
        
        # Get the response
        response = connection.getresponse()
        response_body = response.read().decode('utf-8')

        # Log the response
        logger.info("Forwarding response: %s", response.status)
        logger.info("Response body: %s", response_body)

        # Return response details
        return response.status, response_body

    except Exception as e:
        logger.error("Failed to forward data: %s", str(e))
        return None, str(e)

def lambda_handler(event, context):
    try:
        # Handle POST requests only
        if event['httpMethod'] == 'POST':
            # Parse the body
            body = event.get('body')
            if body:
                lead_data = json.loads(body)

                # Navigate the structure to extract page_id, leadgen_id, and changes
                entry = lead_data.get('entry', [])
                if entry:
                    changes = entry[0].get('changes', [])
                    value = changes[0].get('value', {}) if changes else {}
                    page_id = value.get('page_id')
                    leadgen_id = value.get('leadgen_id')

                    # Log extracted values for verification
                    logger.info("Extracted page_id: %s", page_id)
                    logger.info("Extracted leadgen_id: %s", leadgen_id)

                    # Generate folder structure
                    now = datetime.utcnow()
                    year = now.strftime('%Y')
                    month = now.strftime('%m')
                    day = now.strftime('%d')

                    # Map page_id to client name (optional)
                    if page_id == "444444444444":
                        client_name = "Test"  # Replace with your actual mapping logic
                    else:
                        client_name = f"client_{page_id}"

                    # Define the S3 object key (folder structure + filename)
                    object_key = f"{client_name}/{year}/{month}/{day}/{leadgen_id}.json"

                    # Upload data to S3
                    s3_client.put_object(
                        Bucket=BUCKET_NAME,
                        Key=object_key,
                        Body=json.dumps(lead_data),
                        ContentType='application/json'
                    )

                    logger.info("Data saved to S3: %s", object_key)

                    # Forward the "changes" dictionary only
                    status, response_body = forward_data_to_url(changes)

                    # Check for errors in the forwarding response
                    if status and status >= 400:
                        logger.error("Failed to forward data with status %s: %s", status, response_body)

                    # Respond to Facebook
                    return {
                        'statusCode': 200,
                        'body': 'Event processed and forwarded successfully'
                    }

                # If structure is invalid
                logger.error("Unexpected event structure: %s", json.dumps(lead_data))
                return {
                    'statusCode': 400,
                    'body': 'Invalid event structure'
                }

            # If body is missing
            return {
                'statusCode': 400,
                'body': 'Missing request body'
            }

        else:
            # Unsupported HTTP method
            return {
                'statusCode': 405,
                'body': 'Method Not Allowed'
            }

    except Exception as e:
        logger.error("Unhandled exception: %s", str(e))
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }