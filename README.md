# AWS SQS to PostgreSQL Data Pipeline

## Description

This application reads JSON data from an AWS SQS Queue, masks sensitive data, and writes it to a PostgreSQL database.

## Getting Started

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Start the Docker containers using `docker-compose up -d`.
4. Run the application using `python main.py`.

## Usage

1. Ensure Docker containers for LocalStack and PostgreSQL are running.
2. Run the Python script to process messages from the SQS queue and insert them into the PostgreSQL database.

## Configuration

- No additional configuration required.

## Dependencies

- boto3
- psycopg2-binary

## File Structure

aws_sqs_to_postgres/
1. docker-compose.yml
2. main.py
3. requirements.txt


## Example

- Processed messages from the SQS queue will be inserted into the `user_logins` table in the PostgreSQL database.


## Acknowledgements

- The Docker images for LocalStack and PostgreSQL are provided by Fetch.

## Next Steps

- Add error handling and logging.
- Improve scalability for handling large datasets.
- Add unit tests for the application.

## Questions 

# How would you deploy this application in production?
1. Containerize the Application:
Use Docker to create a container for your application, ensuring all dependencies are included.

2. Use a Managed Service:
Deploy the application on a cloud platform like AWS ECS, AWS Fargate, or Kubernetes for scalability and reliability.

# What other components would you want to add to make this production ready?
1. Logging and Monitoring:
Integrate logging (e.g., using AWS CloudWatch) and monitoring tools to track application performance and issues.

2. Error Handling and Retries:
Implement robust error handling and retries for reading from the queue and writing to the database.

3. CI/CD Pipeline:
Set up a CI/CD pipeline for automated testing, building, and deployment.

# How can this application scale with a growing dataset.
1. Horizontal Scaling:
Use container orchestration tools like Kubernetes to scale the application horizontally by running multiple instances.

2. Database Optimization:
Optimize the PostgreSQL database with indexing and partitioning to handle large datasets efficiently.

# How can PII be recovered later on?
1. Secure Storage:
Store the original PII data securely and separately if needed for recovery, ensuring compliance with data protection regulations.

2. Encryption:
Use encryption for PII data storage and access controls to protect sensitive information.

# What are the assumptions you made?
1. The JSON structure from the SQS queue is consistent and follows the schema mentioned.
2. The Docker images provided have the required test data and configurations.
3. The masking function used (SHA256) is sufficient for identifying duplicate values while ensuring data privacy.
4. If the `create_date` field is missing, the current date is assumed to ensure all records are timestamped.

