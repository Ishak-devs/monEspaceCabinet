import os
from io import BytesIO
from dotenv import load_dotenv
import boto3

load_dotenv()

def get_logo():
    print('obtaining logo from cloud')
    s3_client = boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT'),
        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY')
    )

    response = s3_client.get_object(Bucket='mybuckets', Key='logo.jpg')
    return BytesIO(response['Body'].read())