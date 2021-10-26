import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_ec2 as ec2


class VpcSubnetStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        infra_env = config["INFRA_ENV"]

        # Create VPC
        vpc = ec2.CfnVPC(
            self,
            f"{infra_env}-vpc",
            cidr_block="172.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )

        # Create subnet_1 (public)
        pulbic_subnet_1 = ec2.CfnSubnet(
            self,
            f"{infra_env}-pulbic-1",
            cidr_block="172.0.0.0/28",
            vpc_id=vpc.ref,
            availability_zone="ap-northeast-2a",
            map_public_ip_on_launch=True,
        )

        # Create subnet_2 (public)
        pulbic_subnet_2 = ec2.CfnSubnet(
            self,
            f"{infra_env}-pulbic-2",
            cidr_block="172.0.0.16/28",
            vpc_id=vpc.ref,
            availability_zone="ap-northeast-2b",
            map_public_ip_on_launch=True,
        )

        # Create subnet_1 (private)
        private_subnet_1 = ec2.CfnSubnet(
            self,
            f"{infra_env}-private-1",
            cidr_block="172.0.0.64/28",
            vpc_id=vpc.ref,
            availability_zone="ap-northeast-2a",
        )

        # Create subnet_2 (private)
        private_subnet_2 = ec2.CfnSubnet(
            self,
            f"{infra_env}-private-2",
            cidr_block="172.0.0.80/28",
            vpc_id=vpc.ref,
            availability_zone="ap-northeast-2b",
        )

        # Create Elastic IP
        eip = ec2.CfnEIP(self, f"{infra_env}-vpc-eip")

        # Create Internet Gateway
        internet_gateway = ec2.CfnInternetGateway(
            self,
            f"{infra_env}-vpc-internetgateway",
        )

        # Attachment Internet Gateway
        attachment_internet_gateway = ec2.CfnVPCGatewayAttachment(
            self,
            f"{infra_env}-attachmentvpc-internetgateway",
            vpc_id=vpc.ref,
            internet_gateway_id=internet_gateway.ref,
        )

        # Create NAT Gateway
        nat_gateway = ec2.CfnNatGateway(
            self,
            f"{infra_env}-vpc-natgateway",
            allocation_id=eip.attr_allocation_id,
            subnet_id=pulbic_subnet_1.ref,
        )

        # Create Route Table + Route
        # public_subnet_1
        route_table_pulbic_subnet_1 = ec2.CfnRouteTable(
            self, f"{infra_env}-vpc-route-table-public-1", vpc_id=vpc.ref
        )
        route_pulbic_subnet_1 = ec2.CfnRoute(
            self,
            f"{infra_env}-vpc-route-public-1",
            route_table_id=route_table_pulbic_subnet_1.ref,
            gateway_id=internet_gateway.ref,
            destination_cidr_block="0.0.0.0/0",
        )
        route_attach_pulbic_subnet_1 = ec2.CfnSubnetRouteTableAssociation(
            self,
            f"{infra_env}-vpc-routeattach-public-1",
            route_table_id=route_table_pulbic_subnet_1.ref,
            subnet_id=pulbic_subnet_1.ref,
        )

        # public_subnet_2
        route_table_pulbic_subnet_2 = ec2.CfnRouteTable(
            self, f"{infra_env}-vpc-route-table-public-2", vpc_id=vpc.ref
        )
        route_pulbic_subnet_2 = ec2.CfnRoute(
            self,
            f"{infra_env}-vpc-route-public-2",
            route_table_id=route_table_pulbic_subnet_2.ref,
            gateway_id=internet_gateway.ref,
            destination_cidr_block="0.0.0.0/0",
        )
        route_attach_pulbic_subnet_2 = ec2.CfnSubnetRouteTableAssociation(
            self,
            f"{infra_env}-vpc-routeattach-public-2",
            route_table_id=route_table_pulbic_subnet_2.ref,
            subnet_id=pulbic_subnet_2.ref,
        )

        # private_subnet_1
        route_table_private_subnet_1 = ec2.CfnRouteTable(
            self, f"{infra_env}-vpc-route-table-private-1", vpc_id=vpc.ref
        )
        route_private_subnet_1 = ec2.CfnRoute(
            self,
            f"{infra_env}-vpc-route-private-1",
            route_table_id=route_table_private_subnet_1.ref,
            gateway_id=internet_gateway.ref,
            destination_cidr_block="0.0.0.0/0",
        )
        route_attach_private_subnet_1 = ec2.CfnSubnetRouteTableAssociation(
            self,
            f"{infra_env}-vpc-routeattach-private-1",
            route_table_id=route_table_private_subnet_1.ref,
            subnet_id=private_subnet_1.ref,
        )

        # private_subnet_2
        route_table_private_subnet_2 = ec2.CfnRouteTable(
            self, f"{infra_env}-vpc-route-table-private-2", vpc_id=vpc.ref
        )
        route_private_subnet_2 = ec2.CfnRoute(
            self,
            f"{infra_env}-vpc-route-private-2",
            route_table_id=route_table_private_subnet_2.ref,
            gateway_id=internet_gateway.ref,
            destination_cidr_block="0.0.0.0/0",
        )
        route_attach_private_subnet_2 = ec2.CfnSubnetRouteTableAssociation(
            self,
            f"{infra_env}-vpc-routeattach-private-2",
            route_table_id=route_table_private_subnet_2.ref,
            subnet_id=private_subnet_2.ref,
        )

        # output
        cdk.CfnOutput(
            self,
            "vpc-id",
            value=vpc.ref,
            export_name="vpc-id",
        )
        cdk.CfnOutput(
            self,
            "pulbic-subnet-1",
            value=pulbic_subnet_1.ref,
            export_name="pulbic-subnet-1-id",
        )
        cdk.CfnOutput(
            self,
            "pulbic-subnet-2",
            value=pulbic_subnet_2.ref,
            export_name="pulbic-subnet-2-id",
        )
        cdk.CfnOutput(
            self,
            "private-subnet-1",
            value=private_subnet_1.ref,
            export_name="private-subnet-1-id",
        )
        cdk.CfnOutput(
            self,
            "private-subnet-2",
            value=private_subnet_2.ref,
            export_name="private-subnet-2-id",
        )
