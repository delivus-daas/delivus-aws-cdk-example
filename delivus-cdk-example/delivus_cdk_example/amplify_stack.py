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


# Create Redis Subnet Group
redis_subnet_group = cache.CfnSubnetGroup(
    self,
    "infra_env-rediscluster-subnetgroup",
    description="redis subnet group",
    subnet_ids=[cdk.Fn.import_value("private-subnet-1-id")],
    cache_subnet_group_name="infra_env-rediscluster-subnetgroup",
)

# Create Redis Cluster (Clustermode ON)
redis_cluster = cache.CfnReplicationGroup(
    self,
    f"infra_env-app-rediscluster",
    replication_group_description=f"{infra_env} redis(cluster mode on) group",
    cache_node_type="cache.t3.micro",
    cache_parameter_group_name="default.redis5.0.cluster.on",
    security_group_ids=[cdk.Fn.import_value("redis-sg")],
    engine="redis",
    engine_version="5.0.4",
    num_node_groups=1,
    replicas_per_node_group=1,
    cache_subnet_group_name=redis_subnet_group.cache_subnet_group_name,
)

# Create Dependency
# 순서를 꼭 정해줘야 배포 시 에러가 발생하지 않음
redis_cluster.add_depends_on(redis_subnet_group)
