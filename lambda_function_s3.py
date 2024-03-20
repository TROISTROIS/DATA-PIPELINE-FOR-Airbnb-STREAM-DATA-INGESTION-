import json
import boto3

s3_client = boto3.client('s3')
target_bucket = "airbnb-s3-booking-records"
s3_key = f"filtered-data.json"


def lambda_handler(event, context):
    try:
        print("Event:--------->", event)
        # Extract the filtered data from the EventBridge event
        records = json.loads(event['detail']['Records']) if 'detail' in event and 'Records' in event['detail'] else []

        # Upload filtered data to S3
        for record in records:
            s3_client.put_object(Bucket=target_bucket, Key=s3_key, Body=json.dumps(record))

        # Get the count of records for the current order status
        count = len(records)
        print("There are {} records".format(count))

        return "Success"

    except Exception as err:
        print(err)





