import json
import boto3
import uuid

s3 = boto3.client('s3')

BUCKET_NAME = 'wenner-image-uploads'

def lambda_handler(event, context):

    file_name = f"{uuid.uuid4()}.jpg"

    upload_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': file_name,
            'ContentType': 'image/jpeg'
        },
        ExpiresIn=240
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'uploadUrl': upload_url,
            'fileName': file_name
        })
    }