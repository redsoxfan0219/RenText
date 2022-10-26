import boto3
import botocore
import os



def upload_file(file_name, bucket, object_name):

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(file_name, bucket, object_name)

def execute_file_upload():
    
    folder = "/Users/benjaminmoran/eebo_tcp_data/data/eebo_raw/eebo_raw_combined"
    bucket = 'rentext'

    for file in os.listdir(folder):

        file_name = f"{folder}/{file}"
        object_name_suffix = file_name.split("/")[7]
        object_name = f"eebo_raw_xml/{object_name_suffix}"
        print(object_name)
        upload_file(file_name, bucket, object_name)

if __name__ == "__main__":
    execute_file_upload()

