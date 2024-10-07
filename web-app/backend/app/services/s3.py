from flask import current_app
import boto3
from botocore.client import Config
import os

def create_client():
    if os.environ["FLASK_ENV"] == "development":
        return boto3.client('s3',
            region_name=current_app.config['AWS_S3_REGION'],
            config=Config(signature_version='s3v4')
        )
    else:
        return boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=current_app.config['AWS_S3_REGION'],
            config=Config(signature_version='s3v4')
        )

def upload_file(file, object_name):
    """
    Uploads a file to an AWS S3 bucket
    """
    return create_client().put_object(Body=file, Bucket=current_app.config['AWS_S3_BUCKET'], Key=object_name)

def download_file(filename):
    """
    Downloads a file from an AWS S3 bucket
    """
    return create_client().get_object(Bucket=current_app.config['AWS_S3_BUCKET'], Key=filename)['Body']

def get_presigned_url(resource):
    return create_client().generate_presigned_url('get_object', Params = { 'Bucket': current_app.config['AWS_S3_BUCKET'], 'Key': resource }, ExpiresIn= 100)