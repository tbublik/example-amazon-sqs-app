FROM amazonlinux

RUN yum update -y && \
    yum install -y python3-pip python3-dev libXext libSM libXrender

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app
# Set region for all Amazon API commands running inside of container
ENV AWS_DEFAULT_REGION eu-central-1

CMD python3 job.py