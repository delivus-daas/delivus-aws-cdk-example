import aws_cdk as cdk
import aws_cdk.aws_amplify as amplify
from constructs import Construct

from .amplify_build_specs import get_build_spec


class AmplifyStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]
        github_token = config["GITHUB_TOKEN"]

        # Create Example App
        example_amplify = amplify.CfnApp(
            self,
            f"{infra_env}-amplify",
            name=f"{infra_env}-fe",
            repository="https://github.com/example/repo",
            oauth_token=github_token,
            build_spec=get_build_spec(),
            environment_variables=[
                amplify.CfnApp.EnvironmentVariableProperty(
                    name="EXAMPLE_ENV",
                    value=f"exmaple",
                ),
            ],
            custom_rules=[
                amplify.CfnApp.CustomRuleProperty(
                    source="/<*>",
                    target="/index.html",
                    status="404",
                ),
            ],
        )

        # Connect Example Branch
        example_amplify_branch = amplify.CfnBranch(
            self,
            f"{infra_env}-seller-amplify-branch",
            app_id=example_amplify.attr_app_id,
            branch_name=infra_env,
            build_spec=get_build_spec(),
        )
