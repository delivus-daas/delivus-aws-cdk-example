import aws_cdk as cdk
from constructs import Construct

from .iam_custom_policies import get_policy_ecs_server_task_or_execution_policy
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

        # ECS Task Role
        # ecs_task_role = iam.Role(
        #     self,
        #     f"{infra_env}-app-ecs-task-iam-role",
        #     assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        #     role_name=f"{infra_env}-app-ecs-task-iam-role",
        #     inline_policies=[
        #         iam.PolicyDocument(statements=[get_policy_ecs_server_task_or_execution_policy()])
        #     ],
        #     managed_policies=[
        #         iam.ManagedPolicy.from_aws_managed_policy_name("AWSXRayDaemonWriteAccess")
        #     ],
        # )

        # ECS Excution Role
        # ecs_execution_role = iam.Role(
        #     self,
        #     f"{infra_env}-app-ecs-execution-iam-role",
        #     assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        #     role_name=f"{infra_env}-app-ecs-execution-iam-role",
        #     inline_policies=[
        #         iam.PolicyDocument(statements=[get_policy_ecs_server_task_or_execution_policy()])
        #     ],
        #     managed_policies=[
        #         iam.ManagedPolicy.from_managed_policy_arn(
        #             self,
        #             "ECSTaskExecutionRolePolicy",
        #             managed_policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
        #         )
        #     ],
        # )

        # cdk.CfnOutput(
        #     self,
        #     "ecs-task-role",
        #     value=ecs_task_role.role_arn,
        #     export_name="ecs-task-role-arn",
        # )

        # cdk.CfnOutput(
        #     self,
        #     "ecs-execution-role",
        #     value=ecs_execution_role.role_arn,
        #     export_name="ecs-execution-role-arn",
        # )
