import boto3
import random
import hashlib
import time
from time import gmtime, strftime

dynamodb = boto3.resource("dynamodb")
imageAnalyticsTableName = boto3.client("ssm").get_parameter(
    Name="imageAnalyticsTable", WithDecryption=False
)["Parameter"]["Value"]
table = dynamodb.Table(imageAnalyticsTableName)
color_names = ["blue", "green", "red"]

while 1:
    start = time.time()
    item = {}

    # Generate fake pixel count
    for i in range(len(color_names)):
        item[color_names[i]] = random.randint(0, 255)

    # Generate fake file content to hash it and put in DynamoDB
    file_content = random.randint(0, 99999)
    item["checksum"] = hashlib.md5(str(file_content).encode()).hexdigest()
    response = table.put_item(Item=item)
    end = time.time()
    print(
        f"""[{strftime("%H:%M:%S", gmtime())}] Put item {item['checksum']} finished in {end - start} seconds.
    RetryAttempts: {response['ResponseMetadata']['RetryAttempts']}."""
    )

