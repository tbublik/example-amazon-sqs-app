import time
from time import gmtime, strftime
import boto3
import logging
import json
import cv2
import numpy
import hashlib
from decimal import *
import ast

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Analyzer:

    def job(self):
        logger.info("Job started")

        # Initialize boto3
        sqs = boto3.resource('sqs')
        s3 = boto3.resource('s3')
        dynamodb = boto3.resource('dynamodb')

        # Get Amazon System Manager Parameters
        sqsUrl = boto3.client('ssm').get_parameter(
            Name='sqsUrl',
            WithDecryption=False
        )['Parameter']['Value']
        imageAnalyticsTableName = boto3.client('ssm').get_parameter(
            Name='imageAnalyticsTable',
            WithDecryption=False
        )['Parameter']['Value']

        # Poll Amazon SQS messages
        queue = sqs.Queue(url=sqsUrl)
        messages = queue.receive_messages(WaitTimeSeconds=20)

        color_names = ['blue', 'green', 'red']
        items = []

        for message in messages:
            logger.info(f"Message {message.message_id} recieved.")
            # Read Amazon SQS message
            event = ast.literal_eval(json.loads(message.body)["Message"])
            s3key = event["Records"][0]["s3"]["object"]["key"]
            s3bucket = event["Records"][0]["s3"]["bucket"]["name"]

            # Get image from Amazon S3
            response = s3.Object(
                bucket_name=s3bucket,
                key=s3key
            )
            file_bytes = numpy.frombuffer(response.get()['Body'].read(), dtype=numpy.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED) # OpenCV uses BGR color schema instead of RGB

            # Calculate image hash and calculate amount of pixels per color
            hash = hashlib.md5(img)
            avg_color_per_row = numpy.average(img, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)

            # Generate DynamoDB item
            item = {'checksum': hash.hexdigest()}
            for i in range(len(avg_color)-1):
                if avg_color[i] > 0:
                    item[color_names[i]] = int(avg_color[i])
            items.append(item)

            message.delete() # Remove message from the queue
            logger.info(f"Message {message.message_id} has been digested.")
        
        # Store in DynamoDB
        if len(items) > 0:
            table = dynamodb.Table(imageAnalyticsTableName)
            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(
                        Item = item
                    )
            logger.info(f"""Items saved in DynamoDB {imageAnalyticsTableName} table.""")
    
while 1:
    try:
        logger.info(f"""Job started [{strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())}]""")
        Analyzer().job()
        logger.info(f"""Job finished [{strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())}]""")
        time.sleep(30)
    except:
        raise