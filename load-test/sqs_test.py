import urllib.request
import requests
import boto3
import random

# Obtain Amazon EC2 Public IP address of app instance
app_ip = boto3.client('ec2').describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'app',
            ]
        },
    ],
)

while 1:
    img = requests.get('https://picsum.photos/500/700', stream=True)
    url = f"http://{app_ip['Reservations'][0]['Instances'][0]['PublicIpAddress']}/upload"
    file = {'file': (f'{str(random.randint(1,9999))}.jpg', img.content)}
    r = requests.post(url, files=file)
    print(r.content)