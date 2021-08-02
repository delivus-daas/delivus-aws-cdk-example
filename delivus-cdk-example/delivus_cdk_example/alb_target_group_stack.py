import aws_cdk as cdk
import aws_cdk.aws_elasticloadbalancingv2 as elb_v2
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class AlbTargetGroupStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        alb_availability_zones = ec2.Vpc.from_vpc_attributes(
            self,
            "alb-availability-zones",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            availability_zones=[
                "ap-northeast-2a",
                "ap-northeast-2b",
                "ap-northeast-2c",
                "ap-northeast-2d",
            ],
        )

        # Create ALB (api)
        example_api_alb = elb_v2.CfnLoadBalancer(
            self,
            f"{infra_env}-api-alb",
            ip_address_type="ipv4",
            name=f"{infra_env}-api-alb",
            scheme="internet-facing",
            security_groups=[cdk.Fn.import_value("alb-sg")],
            subnets=[
                cdk.Fn.import_value("pulbic-subnet-1-id"),
            ],
            type="application",
        )

        # Load ALB Interface (L1 -> L2, IApplicationInterface)
        example_api_alb_interface = (
            elb_v2.ApplicationLoadBalancer.from_application_load_balancer_attributes(
                self,
                f"{infra_env}-api-alb-lookup",
                load_balancer_arn=example_api_alb.ref,
                security_group_id=cdk.Fn.import_value("alb-sg"),
            )
        )

        # Create ALB Listener
        example_api_alb_listener = elb_v2.ApplicationTargetGroup(
            self,
            f"{infra_env}-api-alb-listener",
            port=80,
            target_group_name=f"{infra_env}-api-alb-listener",
            health_check=elb_v2.HealthCheck(path="/api/healthcheck/"),
            vpc=alb_availability_zones,
            target_type=elb_v2.TargetType.IP,
        )

        # Add ALB Listener
        example_api_alb_add_listener = elb_v2.ApplicationListener(
            self,
            f"{infra_env}-api-alb-add-listener",
            load_balancer=example_api_alb_interface,
            default_target_groups=[example_api_alb_listener],
            protocol=elb_v2.ApplicationProtocol.HTTP,
        )

        # Output
        cdk.CfnOutput(self, "alb-arn", value=example_api_alb.ref, export_name="alb-arn")
        cdk.CfnOutput(
            self, "alb-dns-name", value=example_api_alb.attr_dns_name, export_name="alb-dns-name"
        )
        cdk.CfnOutput(
            self,
            "alb-target-group-arn",
            value=example_api_alb_listener.target_group_arn,
            export_name="alb-target-group-arn",
        )
