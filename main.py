import boto3
import hashlib
import json
import psycopg2
from datetime import datetime

# URL for the SQS queue
queue_url = 'http://localhost:4566/000000000000/login-queue'

# Function to mask Personally Identifiable Information (PII) using SHA-256
def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Establish connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Initialize SQS client
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')  # Add this line to initialize the SQS client

# Receive messages from the SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10
)

# Process each message received from the SQS queue
for message in response.get('Messages', []):
    try:
        # Parse the JSON message body
        data = json.loads(message['Body'])
        
        # Debugging output to inspect the data
        print("Processing message:", data)
        
        # Extract necessary fields from the message
        user_id = data.get('user_id')
        device_type = data.get('device_type')
        ip = data.get('ip')
        device_id = data.get('device_id')
        locale = data.get('locale')
        app_version = data.get('app_version')
        create_date = data.get('create_date')
        
        # Validate presence of required fields
        if not all([user_id, device_type, ip, device_id, locale, app_version]):
            print("Error: Missing required data fields.")
            continue

        # Mask the IP and device ID fields
        masked_ip = mask_pii(ip)
        masked_device_id = mask_pii(device_id)
        
        # Parse or default the create_date
        if create_date:
            create_date = datetime.strptime(create_date, '%Y-%m-%d').date()
        else:
            create_date = datetime.today().date()  # Use current date as default

        # Insert processed data into PostgreSQL
        cursor.execute("""
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))
        conn.commit()

        # Delete the message from the SQS queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
    except Exception as e:
        # Handle any other exceptions (e.g., log the error, skip the message)
        print(f"Error processing message: {e}")
        continue

# Close the PostgreSQL connection
cursor.close()
conn.close()
