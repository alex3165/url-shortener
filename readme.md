# Url shortener (Babylon, Fullstack challenge)

This web service can be deployed to one or many AWS EC2 instance using aws cli on the local machine or from any CI. The service is completely standalone (including it's own dynamoDB) and could also be deployed to many EC2 instances with a load balancer.

It is also possible to deploy the app with Elastic Beanstalk which will create all the resources needed to monitor and auto scale EC2 instance.

DynamoDB is a NoSQL database, it is fully managed by AWS and scale on demand. You can manually increase read and write capacity unit and / or turn on / off auto scaling for dynamoDB too.

In order to scale both the service and the DB we could put a cache in front of the EC2 instances has the service is indempotant it would be good candidate for that

What is left to do:

- Write a script running on a CRON task to remove all url saved in database for more than 2 days using `created_at` field

## Pre-requirements

- Having docker install on your local machine
- Having python 3 and pip 3 installed

## How to start

- Run DynamoDB on your local machine (Docker container)

```
docker pull dwmkerr/dynamodb && docker run -p 8000:8000 dwmkerr/dynamodb
```

- Run the service

Install the dependencies:

```
pip install -r requirements
```

Run the app:

```
python application.py
```
