import aws_cdk as cdk
import aws_cdk.aws_ecr as ecr
from constructs import Construct


class EcrStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Create Example ECR
        ecr_example = ecr.CfnRepository(
            self,
            f"{infra_env}-private-ecr",
            image_tag_mutability="MUTABLE",
            repository_name=f"example-ecr",
        )

        cdk.CfnOutput(
            self,
            "ecr-example-arn",
            value=ecr_example.attr_arn,
            export_name="ecr-example-arn",
        )
