import aws_cdk.aws_iam as iam


def get_policy_bastion_instance():
    bastion_Instance = iam.PolicyStatement(
        resources=["*"],
        sid="VisualEditor0",
        actions=["s3:*"],
    )

    return bastion_Instance
