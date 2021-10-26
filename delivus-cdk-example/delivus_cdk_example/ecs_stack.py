import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_elasticloadbalancingv2 as elb_v2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_logs as logs
import aws_cdk.aws_ssm as ssm
from constructs import Construct


class EcsStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Get VPC
        ecs_vpc = ec2.Vpc.from_vpc_attributes(
            self,
            "ecs_stack_vpc",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            availability_zones=[
                "ap-northeast-2a",
                "ap-northeast-2b",
            ],
        )

        # Get Security Group
        ecs_security_group = ec2.SecurityGroup.from_security_group_id(
            self, "ecs_stack_sg", security_group_id=cdk.Fn.import_value("ecs-sg")
        )

        # Get Private Subnet
        ecs_private_subnet_1 = ec2.Subnet.from_subnet_id(
            self, "ecs_stack_private_subnet_1", subnet_id=cdk.Fn.import_value("private-subnet-1-id")
        )
        ecs_private_subnet_2 = ec2.Subnet.from_subnet_id(
            self, "ecs_stack_private_subnet_2", subnet_id=cdk.Fn.import_value("private-subnet-2-id")
        )

        # Get ALB TargetGroup
        ecs_application_target_group = elb_v2.ApplicationTargetGroup.from_target_group_attributes(
            self,
            "ecs_stack_application_target_group",
            target_group_arn=cdk.Fn.import_value("alb-target-group-arn"),
        )

        # Get ECS Task Role
        ecs_task_role = iam.Role.from_role_arn(
            self,
            "ecs_stack_task_role",
            role_arn=cdk.Fn.import_value("ecs-task-role-arn"),
        )

        # Get ECS Execution Role
        ecs_execution_role = iam.Role.from_role_arn(
            self,
            "ecs_stack_execution_role",
            role_arn=cdk.Fn.import_value("ecs-execution-role-arn"),
        )

        # Get SSM Parameter
        ssm_db_password = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/DB_PASSWORD",
            version=1,
            parameter_name="/DB_PASSWORD",
        )

        # Get ECR
        ecr_example = ecr.Repository.from_repository_attributes(
            self,
            "ecr-example-ecr_uri",
            repository_name="example-ecr",
            repository_arn=cdk.Fn.import_value("ecr-example-arn"),
        )

        # Create ECS Cluster
        example_ecs_cluster = ecs.Cluster(
            self,
            f"{infra_env}-private-ecs-cluster",
            cluster_name=f"{infra_env}-private-ecs-cluster",
            container_insights=True,
            vpc=ecs_vpc,
        )

        # Create ECS Task Definition
        ecs_example_task_definition = ecs.FargateTaskDefinition(
            self,
            f"{infra_env}-private-api-ecs-task",
            cpu=1024,
            memory_limit_mib=2048,
            task_role=ecs_task_role,
            execution_role=ecs_execution_role,
        )

        # Add Ecr Example Container (Task Definition)
        ecs_example_container = ecs_example_task_definition.add_container(
            f"{infra_env}-private-ecs-container",
            image=ecs.ContainerImage.from_registry(f"{ecr_example.repository_uri}"),
            container_name="example-api",
            memory_limit_mib=1024,
            port_mappings=[
                ecs.PortMapping(
                    container_port=3000,
                    host_port=3000,
                )
            ],
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="ecs",
                log_group=logs.LogGroup.from_log_group_name(
                    self, f"{infra_env}-api-loggroup", log_group_name="/ecs/example-api"
                ),
            ),
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "python manage.py check"],
                interval=cdk.Duration.seconds(30),
                retries=5,
                timeout=cdk.Duration.seconds(10),
            ),
            environment={
                "ENV": infra_env,
            },
            secrets={
                "DB_PASSWORD": ecs.Secret.from_ssm_parameter(ssm_db_password),
            },
            docker_labels={"name": "example-api", "env": infra_env},
        )

        # Create ECS Service
        ecs_api_service = ecs.FargateService(
            self,
            f"{infra_env}-private-api-ecs-service",
            task_definition=ecs_example_task_definition,
            cluster=example_ecs_cluster,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[
                    ecs_private_subnet_1,
                    ecs_private_subnet_2,
                ]
            ),
            security_groups=[ecs_security_group],
            service_name=f"{infra_env}-private-api-ecs-service",
            assign_public_ip=True,
        )

        # Add Target Group 80
        ecs_api_service.attach_to_application_target_group(
            target_group=ecs_application_target_group
        )
