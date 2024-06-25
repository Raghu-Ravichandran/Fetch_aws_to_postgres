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
