from layers.python.shared_resources import json, table, create_response

def handler(event, context):

    taskId = event.get('pathParameters', {}).get('taskId')

    try:
        key = {"taskId": str(taskId)}
        response = table.get_item(Key=key)

        if 'Item' in response:
            return create_response(200, response['Item'])
        else:
            return create_response(404, {'error': 'task not found'})
        
    except Exception as e:
        message = {'error': 'Server Error', 'details': str(e)}
        return create_response(500, message)