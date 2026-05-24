import json
import boto3
import uuid
from urllib.parse import unquote_plus
from datetime import datetime
from PIL import Image

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('images-metadata')

THUMBNAIL_BUCKET = 'wenner-image-thumbnails'

def log(message):
    print(json.dumps(message))

def lambda_handler(event, context):

    record = event['Records'][0]

    bucket = record['s3']['bucket']['name']
    key = unquote_plus(record['s3']['object']['key'])

    image_id = str(uuid.uuid4())

    log({
        'level': 'INFO',
        'message': 'Image uploaded',
        'bucket': bucket,
        'key': key,
        'imageId': image_id
    })

    download_path = f'/tmp/{key}'
    thumbnail_path = f'/tmp/thumb-{key}'

    s3.download_file(bucket, key, download_path)

    image = Image.open(download_path)

    image.thumbnail((250, 250))

    image.save(thumbnail_path)

    thumbnail_key = f'thumb-{key}'

    s3.upload_file(
        thumbnail_path,
        THUMBNAIL_BUCKET,
        thumbnail_key
    )

    table.put_item(
        Item={
            'imageId': image_id,
            'originalImage': key,
            'thumbnailImage': thumbnail_key,
            'createdAt': datetime.utcnow().isoformat()
        }
    )

    log({
        'level': 'INFO',
        'message': 'Thumbnail generated',
        'thumbnail': thumbnail_key
    })

    return {
        'statusCode': 200
    }