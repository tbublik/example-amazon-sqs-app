Russian version below / русская версия внизу
# How to run
```
docker-compose up --build
```
# How to perform load tests
The `./load-tests/` directory contains simple tests to demonstrate Amazon SQS and DynamoDB behavior under load. To run them locally you can use many method, including:
- Running in [Pipenv](https://docs.pipenv.org/en/latest/). 
- Running the same Docker image, just make sure to make your AWS credentials available in the container (do not hardcode them and commit to git) and to run container with `docker run -it --rm <image-name>` command while appending `python3 ./load-tests/<test-name>.py` in the end.
# Infrastructure deployment
Deploy in the numerated ascending order. The `04-resizer-lambda.yaml` is located in the [corresponding](https://github.com/tbublik/example-amazon-s3-lambda-image-resize) repo. After the `03` template use the abovementioned repo, then return to the current and deploy `05` template.

# -------------
# Запуск
```
docker-compose up --build
```
# Нагрузочное тестирование
Папка `./load-tests/` содержит тестовые Python скрипты для наглядной демонстрации поведения приложения под нагрузкой в среде Amazon SQS и DynamoDB. Для запуска можно воспользоваться несколькими методами:
- [Pipenv](https://docs.pipenv.org/en/latest/) один из самых простых. 
- Также можно использовать Docker образ из ./Dockerfile. Добавьте в него ваши учетные данные AWS access key и secret key (не записывайте его нигде в коде) и запустите контейнер с `docker run -it --rm <image-name>` добавив команду `python3 ./load-tests/<название-теста>.py` в конце.

# Деплой инфраструктуры
Для деплоя инфраструктуры используйте Amazon CloudFormation шаблоны из папки `./infrastructure`. Деплоить необходимо по возрастающему порядку нумерации. Шаблон `04-resizer-lambda.yaml` отсутствует, так как относится к [другому](https://github.com/tbublik/example-amazon-s3-lambda-image-resize) репозиторию. После `03` шаблона используйте шаблон из вышеуказанного репозитория, затем продолжайте шаблоном `05` из текущего.
