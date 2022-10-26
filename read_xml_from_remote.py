import boto3
import botocore

s3 = boto3.resource('s3')

bucket = s3.Bucket('rentext')
exists = True
try:
    s3.meta.client.head_bucket(Bucket='rentext')
    print("Connection successful")
except botocore.exceptions.ClientError as e:
    if e == '404':
        exists = False

