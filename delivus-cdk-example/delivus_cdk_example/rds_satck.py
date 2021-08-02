import aws_cdk as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_ssm as ssm
import aws_cdk.aws_s3 as s3
from constructs import Construct


class RdsStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # env
        infra_env = config["INFRA_ENV"]

        # Managed Role
        rds_role = f"arn:aws:iam::{self.account}:role/aws-service-role/rds.amazonaws.com/AWSServiceRoleForRDS"

        # Pre-create required (AWS SSM)
        ssm_db_password = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "/Secure/DB_PASSWORD",
            version=1,
            parameter_name="/Secure/DB_PASSWORD",
        )
        rds_paasword = ssm_db_password.string_value

        # Create Subnet Group
        rds_subnet_group = rds.CfnDBSubnetGroup(
            self,
            f"{infra_env}-aurora-cluster-subnetgroup",
            db_subnet_group_description=f"aurora cluster subnetgroup",
            subnet_ids=[cdk.Fn.import_value("private-subnet-1-id")],
            db_subnet_group_name=f"{infra_env}-aurora-cluster-subnetgroup",
        )

        # Create DB Cluster Parameter Group
        aurora_rds_cluster_parameter = rds.CfnDBClusterParameterGroup(
            self,
            f"{infra_env}-aurora-cluster-parameter",
            family="aurora-mysql5.7",
            description="aurora 5.7 cluster parameter group",
            parameters={
                "character_set_server": "utf8mb4",
                "character_set_connection": "utf8mb4",
                "character_set_database": "utf8mb4",
                "character_set_filesystem": "utf8mb4",
                "character_set_results": "utf8mb4",
                "character_set_client": "utf8mb4",
                "collation_connection": "utf8mb4_general_ci",
                "collation_server": "utf8mb4_general_ci",
            },
        )

        # Create Aurora Cluster
        aurora_rds_cluster = rds.CfnDBCluster(
            self,
            f"{infra_env}-aurora-cluster",
            associated_roles=[rds.CfnDBCluster.DBClusterRoleProperty(role_arn=rds_role)],
            engine="aurora-mysql",
            engine_mode="provisioned",
            backtrack_window=0,
            backup_retention_period=1,
            db_subnet_group_name=f"{infra_env}-aurora-cluster-subnetgroup",
            db_cluster_parameter_group_name=aurora_rds_cluster_parameter.ref,
            db_cluster_identifier=f"{infra_env}-aurora-cluster",
            master_username="admin",
            master_user_password=rds_paasword,
            port=3306,
            storage_encrypted=False,
            vpc_security_group_ids=[cdk.Fn.import_value("mysql-sg")],
            database_name="example",
        )

        # Create Aurora Instance_1
        aurora_rds_instance_1 = rds.CfnDBInstance(
            self,
            f"{infra_env}-aurora-instance1",
            db_cluster_identifier=aurora_rds_cluster.ref,
            db_instance_class="db.t3.small",
            db_instance_identifier=f"{infra_env}-aurora-instance1",
            engine="aurora-mysql",
        )

        # Create Dependency (Subnet -> Cluster -> Instance)
        aurora_rds_cluster.add_depends_on(rds_subnet_group)
        aurora_rds_cluster.add_depends_on(aurora_rds_cluster_parameter)
        aurora_rds_instance_1.add_depends_on(aurora_rds_cluster)
