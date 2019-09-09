# How to run
```
docker-compose up --build
```
# How to perform load tests
The `./load-tests/` directory contains simple tests to demonstrate Amazon SQS and DynamoDB behavior under load. To run them locally you can run the same Docker image, just make sure to make your AWS credentials available in the container (do not hardcode them and commit to git) and to run container with "./load-tests/<test-name>.py" in the end.
# Infrastructure deployment
Deploy in the sorted order. The `04-resizer-lambda.yaml` is located in the [corresponding](https://github.com/tbublik/example-amazon-s3-lambda-image-resize) repo.