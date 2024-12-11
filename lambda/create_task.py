from layers.python.shared_resources import uuid, json, table, create_response

def validate_input(body):

    required_fields = ['title', 'description', 'status']
    errors = []

    for field in required_fields:
        if field not in body:
            errors.append(f"{field} is required")
    
    return errors

def handler(event, context):

    body   = json.loads(event['body'])
    errors = validate_input(body)
    if errors:
        return create_response(400, {'error': 'Invalid Input', 'details': errors})

    taskId = uuid.uuid4()

    try:
        item = {
            'taskId': str(taskId),
            'title': body['title'],
            'description': body['description'],
            'status': body['status']
        }

        table.put_item(Item=item)
        return create_response(200, item)

    except Exception as e:
        message = {'error': 'Server Error', 'details': str(e)}
        return create_response(500, message)
    