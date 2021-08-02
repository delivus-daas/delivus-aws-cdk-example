import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_ec2 as ec2


class SecurityGroupStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        infra_env = config["INFRA_ENV"]

        # Create ALB SG
        alb_sg = ec2.CfnSecurityGroup(
            self,
            f"{infra_env}-alb-sg",
            group_description="alb sg",
            group_name=f"{infra_env}-alb-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=443, to_port=443
                ),
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=80, to_port=80
                ),
            ],
        )

        # Create Bastion SG
        bastion_sg = ec2.CfnSecurityGroup(
            self,
            f"{infra_env}-bastion-sg",
            group_description="bastion sg",
            group_name=f"{infra_env}-bastion-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp", cidr_ip="0.0.0.0/0", from_port=22, to_port=22
                )
            ],
        )

        # Create Aurora SG
        aurora_sg = ec2.CfnSecurityGroup(
            self,
            f"{infra_env}-mysql-sg",
            group_description="mysql sg",
            group_name=f"{infra_env}-mysql-sg",
            vpc_id=cdk.Fn.import_value("vpc-id"),
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    source_security_group_id=bastion_sg.ref,
                    from_port=3306,
                    to_port=3306,
                ),
            ],
        )

        # output
        cdk.CfnOutput(self, "alb-sg", value=alb_sg.ref, export_name="alb-sg")
        cdk.CfnOutput(self, "bastion_sg", value=bastion_sg.ref, export_name="bastion-sg")
        cdk.CfnOutput(self, "mysql-sg", value=aurora_sg.ref, export_name="mysql-sg")
