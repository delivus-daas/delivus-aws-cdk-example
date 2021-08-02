import aws_cdk as cdk
from constructs import Construct
from .iam_custom_policies import get_policy_ecs_server_task_policy
from .iam_custom_policies import get_policy_ecs_execution_policy
from .iam_custom_policies import get_policy_bastion_instance
import aws_cdk.aws_iam as iam


class AppIamRoleStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        infra_env = config["INFRA_ENV"]

        # Create IAM Role (bastions Instance)
        bastion_instance_role = iam.Role(
            self,
            f"{infra_env}-bastion-instance-iam-role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            role_name=f"{infra_env}-bastion-instance-iam-role",
            inline_policies=[iam.PolicyDocument(statements=[get_policy_bastion_instance()])],
        )
