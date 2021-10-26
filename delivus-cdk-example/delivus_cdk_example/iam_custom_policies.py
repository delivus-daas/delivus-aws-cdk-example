import aws_cdk.aws_iam as iam


def get_policy_bastion_instance():
    bastion_Instance = iam.PolicyStatement(
        resources=["*"],
        sid="VisualEditor0",
        actions=["s3:*"],
    )

    return bastion_Instance


def get_policy_ecs_server_task_or_execution_policy():

    # Creating new custom Policies
    ecs_policy = iam.PolicyStatement(
        resources=["*"],
        sid="VisualEditor0",
        actions=[
            "s3:*",
            "ssm:*",
            "cloudwatch:*",
            "kms:*",
            "logs:*",
            "lambda:*",
        ],
    )

    return ecs_policy
