#!/usr/bin/env python3
import os
import aws_cdk as cdk
from delivus_cdk_example.delivus_cdk_example_stack import DelivusCdkExampleStack


app = cdk.App()
DelivusCdkExampleStack(
    app,
    "DelivusCdkExampleStack",
)

app.synth()
