from layers.python.shared_resources import json, table, create_response

def handler(event, context):

    taskId = event.get('pathParameters', {}).get('taskId')

    try:
        key = {"taskId": str(taskId)}
        table.delete_item(Key=key)

        return create_response(204)
    
    except Exception as e:
        message = {'error': 'Server Error', 'details': str(e)}
        return create_response(500, message)