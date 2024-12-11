from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    Duration,
    aws_iam as iam,
    aws_apigatewayv2 as apigatewayv2,
    aws_apigatewayv2_integrations as integrations,
    CfnOutput
)
from constructs import Construct
from os import path

class TasksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##########################################
        ##########    DynamoDB Table    ##########
        ##########################################

        dynamodb_table = dynamodb.Table(self,
            'TasksTable',
            table_name='TasksTable',
            partition_key=dynamodb.Attribute(name='taskId', type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST # use on-demand mode, later we can change it to provision if needed
        )

        ##########################################
        ###### A set of lambda functions    ######
        ##########################################

        lambdadir = path.dirname(path.abspath(__file__) + '../../../lambda/')

        # using a lambda layer to reduce the deployment package size of a single function
        shared_resources = _lambda.LayerVersion(
            self, "SharedResourcesLayer", compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            code=_lambda.Code.from_asset(f"{lambdadir}/layers"), layer_version_name="SharedResourcesLayer"
        )

        # Create task
        create_task_role = iam.Role(
            self, "CreateTaskRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="CreateTaskRole"
        )

        create_task = _lambda.Function(
            self, "CreateTask", runtime=_lambda.Runtime.PYTHON_3_12,
            handler="create_task.handler", code=_lambda.Code.from_asset(lambdadir), timeout=Duration.minutes(15),
            role=create_task_role, layers=[shared_resources]
        )

        # Get task
        get_task_role = iam.Role(
            self, "GetTaskRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="GetTaskRole"
        )

        get_task = _lambda.Function(
            self, "GetTask", runtime=_lambda.Runtime.PYTHON_3_12,
            handler="get_task.handler", code=_lambda.Code.from_asset(lambdadir), timeout=Duration.minutes(15),
            role=get_task_role, layers=[shared_resources]
        )

        # Update task
        update_task_role = iam.Role(
            self, "UpdateTaskRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="UpdateTaskRole"
        )

        update_task = _lambda.Function(
            self, "UpdateTask", runtime=_lambda.Runtime.PYTHON_3_12,
            handler="update_task.handler", code=_lambda.Code.from_asset(lambdadir), timeout=Duration.minutes(15),
            role=update_task_role, layers=[shared_resources]
        )

        # Delete task
        delete_task_role = iam.Role(
            self, "DeleteTaskRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="DeleteTaskRole"
        )

        delete_task = _lambda.Function(
            self, "DeleteTask", runtime=_lambda.Runtime.PYTHON_3_12,
            handler="delete_task.handler", code=_lambda.Code.from_asset(lambdadir), timeout=Duration.minutes(15),
            role=delete_task_role, layers=[shared_resources]
        )

        # attach an IAM policy to the functions' roles so they will have permissions to interact with the dynamodb table
        create_task_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:PutItem"],
                resources=[dynamodb_table.table_arn]
            )
        )

        get_task_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:GetItem"],
                resources=[dynamodb_table.table_arn]
            )
        )

        update_task_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:UpdateItem"],
                resources=[dynamodb_table.table_arn]
            )
        )

        delete_task_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:DeleteItem"],
                resources=[dynamodb_table.table_arn]
            )
        )

        ##########################################
        ###########     API Gateway     ##########
        ##########################################

        api = apigatewayv2.HttpApi(self, 'HttpApi')

        api.add_routes(
            path="/tasks",
            methods=[apigatewayv2.HttpMethod.POST],
            integration=integrations.HttpLambdaIntegration(
                'createTask', handler=create_task
            ),
        )

        api.add_routes(
            path="/tasks/{taskId}",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=integrations.HttpLambdaIntegration(
                'getTask', handler=get_task
            )
        )

        api.add_routes(
            path="/tasks/{taskId}",
            methods=[apigatewayv2.HttpMethod.PUT],
            integration=integrations.HttpLambdaIntegration(
                'updateTask', handler=update_task
            )
        )

        api.add_routes(
            path="/tasks/{taskId}",
            methods=[apigatewayv2.HttpMethod.DELETE],
            integration=integrations.HttpLambdaIntegration(
                'deleteTask', handler=delete_task
            )
        )

        CfnOutput(
            self, "APIGatewayUrl",
            value=api.url,
            description="The URL for the API"
        )
