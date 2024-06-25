import boto3
import hashlib
import json
import psycopg2
from datetime import datetime

queue_url = 'http://localhost:4566/000000000000/login-queue'

def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10
)

for message in response.get('Messages', []):
    try:
        data = json.loads(message['Body'])
        
        # Debugging output to inspect the data
        print("Processing message:", data)
        
        user_id = data.get('user_id')
        device_type = data.get('device_type')
        ip = data.get('ip')
        device_id = data.get('device_id')
        locale = data.get('locale')
        app_version = data.get('app_version')
        create_date = data.get('create_date')
        
        if not all([user_id, device_type, ip, device_id, locale, app_version]):
            print("Error: Missing required data fields.")
            continue

        masked_ip = mask_pii(ip)
        masked_device_id = mask_pii(device_id)
        
        if create_date:
            create_date = datetime.strptime(create_date, '%Y-%m-%d').date()
        else:
            create_date = datetime.today().date()  # Use current date as default

        # Insert data into PostgreSQL
        cursor.execute("""
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))
        conn.commit()

        # Delete the message from the queue
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
