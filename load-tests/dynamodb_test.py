import boto3
import random
import hashlib
import time
from time import gmtime, strftime

dynamodb = boto3.resource('dynamodb')
imageAnalyticsTableName = boto3.client('ssm').get_parameter(
            Name='imageAnalyticsTable',
            WithDecryption=False
        )['Parameter']['Value']
table = dynamodb.Table(imageAnalyticsTableName)
color_names = ['blue', 'green', 'red']

while 1:
    # Generate fake pixel count
    item = {}
    start = time.time()
    for i in range(len(color_names)):
        if sum(item.values()) < 255:
            if i == len(color_names)-1:
                item[color_names[i]] = 255-sum(item.values())
            else:
                item[color_names[i]] = random.randint(0,255-sum(item.values()))
        else:
            break
    file_content = random.randint(0,99999) # Generate fake file content to hash it and put in DynamoDB
    item['checksum'] = hashlib.md5(str(file_content).encode()).hexdigest()
    response = table.put_item(Item=item, ReturnConsumedCapacity='TOTAL')
    end = time.time()
    print(f"""[{strftime("%H:%M:%S", gmtime())}] Put item {item['checksum']} finished in {end - start} seconds. RetryAttempts {response['ResponseMetadata']['RetryAttempts']}""")