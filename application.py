import boto3
import hashlib
import datetime
import os

from boto3.dynamodb.conditions import Key
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

from db import getTable, hasTable, createTable
from utils import validateUrl

SERVER_DNS = os.getenv('SERVER_DNS', 'http://localhost:5000')

application = Flask(__name__)
CORS(application)

if hasTable():
    table = getTable()
else:
    table = createTable()


@application.route('/shorten_url', methods=['POST'])
def shortenUrl():
    body = request.get_json()

    if not validateUrl(body['url']):
        res = {
            'message': 'Invalid url in request body'
        }

        return jsonify(res), 400

    hashObject = hashlib.md5(body['url'].encode())
    urlHash = hashObject.hexdigest()

    if 'truncate' in body:
        urlHash = urlHash[:10]

    table.put_item(
        Item={
            'url_hash': urlHash,
            'url': body['url'],
            'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    res = {
        'id': urlHash,
        'shortened_url': SERVER_DNS + '/' + urlHash
    }

    return jsonify(res), 201


@application.route('/<urlHash>')
def getUrl(urlHash):
    assert urlHash == request.view_args['urlHash']

    response = table.query(
        KeyConditionExpression=Key('url_hash').eq(urlHash)
    )

    if len(response['Items']) < 1:
        res = {
            'message': 'No URL found for given hash'
        }

        return jsonify(res), 400

    url = response['Items'][0]['url']

    return redirect(url, code=302)


if __name__ == '__main__':
    application.run()
