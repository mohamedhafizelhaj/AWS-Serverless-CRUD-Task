import aws_cdk as core
import aws_cdk.assertions as assertions

from tasks.tasks_stack import TasksStack

def test_dynamodb_table_created():
    app = core.App()

    stack = TasksStack(app, "TasksStack")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::DynamoDB::Table", {
        "TableName": "TasksTable",
        "KeySchema": [
            {
                "AttributeName": "taskId",
                "KeyType": "HASH"
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    })

def test_lambda_functions_created():
    app = core.App()

    stack = TasksStack(app, "TasksStack")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::Function", 4)

    # CreateTask
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "create_task.handler",
        "Runtime": "python3.12",
        "Timeout": 900
    })

    # GetTask
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "get_task.handler",
        "Runtime": "python3.12",
        "Timeout": 900
    })

    # UpdateTask
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "update_task.handler",
        "Runtime": "python3.12",
        "Timeout": 900
    })

    # DeleteTask
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "delete_task.handler",
        "Runtime": "python3.12",
        "Timeout": 900
    })

def test_lambda_permissions():
    # assert th
    app = core.App()

    stack = TasksStack(app, "TasksStack")
    template = assertions.Template.from_stack(stack)

    # CreateTask
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": "dynamodb:PutItem",
                    "Effect": "Allow",
                    "Resource": {"Fn::GetAtt": ["TasksTable88911DC5", "Arn"]}
                }
            ]
        },
        "Roles": [{
            "Ref": "CreateTaskRoleF7B76E59"
        }]
    })

    # GetTask
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": "dynamodb:GetItem",
                    "Effect": "Allow",
                    "Resource": {"Fn::GetAtt": ["TasksTable88911DC5", "Arn"]}
                }
            ]
        },
        "Roles": [{
            "Ref": "GetTaskRoleB3C61240"
        }]
    })

    # UpdateTask
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": "dynamodb:UpdateItem",
                    "Effect": "Allow",
                    "Resource": {"Fn::GetAtt": ["TasksTable88911DC5", "Arn"]}
                }
            ]
        },
        "Roles": [{
            "Ref": "UpdateTaskRole46CA3A63"
        }]
    })

    # DeleteTask
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": "dynamodb:DeleteItem",
                    "Effect": "Allow",
                    "Resource": {"Fn::GetAtt": ["TasksTable88911DC5", "Arn"]}
                }
            ]
        },
        "Roles": [{
            "Ref": "DeleteTaskRoleE3F265C1"
        }]
    })

def test_lambda_layer_attached():
    app = core.App()

    stack = TasksStack(app, "TasksStack")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::LayerVersion", 1)

    template.has_resource_properties("AWS::Lambda::Function", {
        "Layers": [{
            "Ref": "SharedResourcesLayer865505F8"
        }]
    })

def test_api_gateway_output():
    app = core.App()

    stack = TasksStack(app, "TasksStack")
    template = assertions.Template.from_stack(stack)

    template.has_output("APIGatewayUrl", {
        "Description": "The URL for the API"
    })
