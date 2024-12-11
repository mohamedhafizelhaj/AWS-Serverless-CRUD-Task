import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("TasksTable")

def create_response(status_code, body=None):

    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    if body:
        response['body'] = json.dumps(body)
        
    return response