from aws_cdk import Stack
from constructs import Construct
from .iam_role_stack import AppIamRoleStack
from .vpc_subnet_stack import VpcSubnetStack
from .security_group_stack import SecurityGroupStack
from .rds_satck import RdsStack
from .cloudwatch_log_stack import CloudWatchLogsStack
from .bastion_ec2_stack import Ec2Stack
from .alb_target_group_stack import AlbTargetGroupStack
from .s3_stack import S3Stack

# Doesn't run by default (Just example code)
from .amplify_stack import AmplifyStack
from .ecr_stack import EcrStack
from .ecs_stack import EcsStack


class DelivusCdkExampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        config = {
            "INFRA_ENV": "example",
            "KEY_PAIR_NAME": [],
            # "GITHUB_TOKEN": [] -> Use by Amplify
        }

        # The code that defines your stack goes here
        role_stack = AppIamRoleStack(self, "iam_role", config=config)
        vpc_subnet_stack = VpcSubnetStack(self, "vpc", config=config)
        security_group_stack = SecurityGroupStack(self, "security_group", config=config)
        s3_stack = S3Stack(self, "s3", config=config)
        cloud_watch_log_stack = CloudWatchLogsStack(self, "cloudwatch_log_stack", config=config)
        alb_target_group_stack = AlbTargetGroupStack(self, "alb_target_group", config=config)
        bastion_ec2_stack = Ec2Stack(self, "ec2_stack", config=config)
        rds_stack = RdsStack(self, "rds_stack", config=config)
        # amplify_stack = AmplifyStack(self, "amplify_stack", config=config)
        # ecr_stack = EcrStack(self, "ecr_stack", config=config)
        # ecs_stack = EcsStack(self, "ecs_stack", config=config)

        # Stack Execution order
        vpc_subnet_stack.add_dependency(role_stack)
        security_group_stack.add_dependency(vpc_subnet_stack)
        s3_stack.add_dependency(security_group_stack)
        cloud_watch_log_stack.add_dependency(s3_stack)
        alb_target_group_stack.add_dependency(cloud_watch_log_stack)
        bastion_ec2_stack.add_dependency(alb_target_group_stack)
        rds_stack.add_dependency(bastion_ec2_stack)
        # amplify_stack.add_dependency(rds_stack)
        # ecr_stack.add_dependency(amplify_stack)
        # ecs_stack.add_dependency(ecr_stack)
