import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_iam as iam
from constructs import Construct


class S3Stack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Create public S3
        public_s3 = s3.Bucket(
            self,
            f"{infra_env}-pubilc-s3",
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            public_read_access=True,
        )

        # Add Cors Rule (Public S3)
        public_s3.add_cors_rule(
            allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.POST],
            allowed_origins=["*"],
        )

        # Create Policy_1 (Public S3)
        public_s3_policy_1 = iam.PolicyStatement(
            sid="AllowPublicRead",
            effect=iam.Effect.ALLOW,
            principals=[iam.AnyPrincipal()],
            resources=[public_s3.arn_for_objects("*")],
            actions=["s3:GetObject", "s3:GetObjectVersion"],
        )

        # Add Policy_1 (Public S3)
        public_s3.add_to_resource_policy(public_s3_policy_1)

        # output
        cdk.CfnOutput(
            self,
            "s3-stack-name",
            value=self.artifact_id,
            export_name="s3-stack-name",
        )
