import aws_cdk as cdk
import aws_cdk.aws_elasticloadbalancingv2 as elb_v2
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class AlbTargetGroupStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        exmaple_vpc = ec2.Vpc.from_vpc_attributes(
            self,
            "example-alb-vpc",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            availability_zones=[
                "ap-northeast-2a",
                "ap-northeast-2b",
            ],
        )

        # Create ALB (API)
        example_api_alb = elb_v2.ApplicationLoadBalancer(
            self,
            f"{infra_env}-api-alb",
            security_group=ec2.SecurityGroup.from_security_group_id(
                self,
                f"example-{infra_env}-api-alb-sg",
                security_group_id=cdk.Fn.import_value("alb-sg"),
            ),
            vpc=exmaple_vpc,
            internet_facing=True,
            load_balancer_name=f"{infra_env}-api-alb",
            vpc_subnets=ec2.SubnetSelection(
                subnets=[
                    ec2.Subnet.from_subnet_attributes(
                        self,
                        f"{infra_env}-api-alb-subnet-1",
                        subnet_id=cdk.Fn.import_value("pulbic-subnet-1-id"),
                    ),
                    ec2.Subnet.from_subnet_attributes(
                        self,
                        f"{infra_env}-api-alb-subnet-2",
                        subnet_id=cdk.Fn.import_value("pulbic-subnet-2-id"),
                    ),
                ]
            ),
        )

        # # Create Listener (API ALB Listener 80)
        # example_api_alb_listener = elb_v2.ApplicationTargetGroup(
        #     self,
        #     f"{infra_env}-api-alb-listener",
        #     port=80,
        #     target_group_name=f"{infra_env}-api-alb-listener",
        #     health_check=elb_v2.HealthCheck(path="/api/healthcheck/"),
        #     vpc=exmaple_vpc,
        #     target_type=elb_v2.TargetType.IP,
        # )

        # # Add 80 Listener (API ALB)
        # exmaple_api_alb_add_listener = example_api_alb.add_listener(
        #     f"{infra_env}-api-alb-add-listener-80",
        #     protocol=elb_v2.ApplicationProtocol.HTTP,
        #     port=80,
        #     default_action=elb_v2.ListenerAction(
        #         action_json=elb_v2.CfnListener.ActionProperty(
        #             type="forward",
        #             target_group_arn=example_api_alb_listener.target_group_arn,
        #         )
        #     ),
        # )

        # Output
        cdk.CfnOutput(
            self,
            "alb-arn",
            value=example_api_alb.load_balancer_arn,
            export_name="alb-arn",
        )
        cdk.CfnOutput(
            self,
            "alb-dns-name",
            value=example_api_alb.load_balancer_dns_name,
            export_name="alb-dns-name",
        )
        # cdk.CfnOutput(
        #     self,
        #     "alb-target-group-arn",
        #     value=example_api_alb_listener.target_group_arn,
        #     export_name="alb-target-group-arn",
        # )
