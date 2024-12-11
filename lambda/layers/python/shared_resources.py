import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("TasksTable")

def create_response(status_code, body):

    return {
        'status_code': status_code,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }