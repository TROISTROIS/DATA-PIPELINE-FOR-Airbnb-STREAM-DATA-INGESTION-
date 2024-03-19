import boto3
import json
import uuid
from faker import Faker
from random import randint
from datetime import datetime, timedelta


sqs_client = boto3.client('sqs')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/590183810146/airbnb-booking-queue'
fake = Faker()
def fake_data(x):
    for i in range(0, x):
        start_date = fake.date_this_century().strftime('%Y-%m-%d')
        end_date = fake.date_this_century().strftime('%Y-%m-%d')

        while datetime.strptime(end_date, '%Y-%m-%d') < datetime.strptime(start_date, '%Y-%m-%d'):
            end_date = fake.date_this_century().strftime('%Y-%m-%d')

        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        # Calculate a random number of days between 0 and 30
        days_difference = randint(0, 30)

        # Adjust the end date by adding the random number of days
        end_datetime = start_datetime + timedelta(days=days_difference)

        # Ensure end date is not after start date
        if end_datetime > start_datetime:
            end_date = end_datetime.strftime('%Y-%m-%d')

        data_format = {
            "bookingId": str(uuid.uuid4())[:10],
            "userId": str(uuid.uuid4())[:10],
            "propertyId": str(uuid.uuid4())[:15],
            "location": f"{fake.city()}, {fake.country()}",
            "startDate": start_date,
            "endDate": end_date,
            "price": randint(107, 700)
        }
        print(data_format)

def lambda_handler(event, context):
    data = fake_data(10)
    for item in data:
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(item)
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Sales order data published to SQS!')
    }





