#!/usr/bin/env python3
import aws_cdk as cdk

from tasks.tasks_stack import TasksStack

app = cdk.App()
TasksStack(app, "TasksStack")

app.synth()
