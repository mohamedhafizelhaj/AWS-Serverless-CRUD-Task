from layers.python.shared_resources import json, table, create_response

def handler(event, context):

    taskId = event.get('pathParameters', {}).get('taskId')
    body   = json.loads(event['body'])

    try:
        key = {"taskId": str(taskId)}

        update_expression = "SET "
        expression_names  = {}
        expression_values = {}

        if 'title' in body:
            update_expression += "#title = :new_title"
            expression_names['#title'] = "title"
            expression_values[':new_title'] = body('title')

        if 'description' in body:
            update_expression += "#description = :new_description"
            expression_names['#description'] = "description"
            expression_values[':new_description'] = body('description')

        if 'status' in body:
            update_expression += "#s = :new_status"
            expression_names['#s'] = "status"
            expression_values[':new_status'] = body('status')

        response = table.update_item(
            Key=key, UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW"
        )

        return create_response(200, response["Attributes"])
    
    except Exception as e:
        message = {'error': 'Server Error', 'details': str(e)}
        return create_response(500, message)