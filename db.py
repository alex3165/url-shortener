import boto3
import os

TABLE_NAME = os.getenv('TABLE_NAME', 'urls')
DYNAMODB_URL = os.getenv('DYNAMODB_URL', 'http://localhost:8000')
READ_UNIT = os.getenv('READ_UNIT', 5)
WRITE_UNIT = os.getenv('WRITE_UNIT', 5)

dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_URL)
dynamodb_client = boto3.client('dynamodb', endpoint_url=DYNAMODB_URL)


def hasTable():
    existing_tables = dynamodb_client.list_tables()['TableNames']
    return TABLE_NAME in existing_tables


def createTable():
    return dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'url_hash',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'url',
                'KeyType': 'string'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'url_hash',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'url',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': READ_UNIT,
            'WriteCapacityUnits': WRITE_UNIT
        }
    )


def getTable():
    return dynamodb.Table(TABLE_NAME)
