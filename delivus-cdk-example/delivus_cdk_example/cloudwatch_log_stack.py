import aws_cdk as cdk
import aws_cdk.aws_logs as logs
from constructs import Construct


class CloudWatchLogsStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Create Xray Logs (L1)
        xray_cloudwatch_logs = logs.CfnLogGroup(
            self,
            f"{infra_env}-xray-logs",
            log_group_name="/ecs/example/xray",
        )

        # Create API Logs (L2)
        api_logs = logs.LogGroup(
            self,
            f"{infra_env}-api-logs",
            log_group_name="/ecs/example-api",
        )
