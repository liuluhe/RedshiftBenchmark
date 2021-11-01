#!/usr/bin/env python3


from aws_cdk import (
    aws_ec2 as ec2,
    core,
)
from redshift_benchmark.lib.cdkVPCStack import VPCStack
from redshift_benchmark.lib.cdkRedshiftStack import RedshiftStack
from redshift_benchmark.lib.cdkInitialAssets import S3Assets
from redshift_benchmark.redshiftBenchmarkStack import RedshiftBenchmarkStack



app = core.App()

######################## Parameters that could be customized ###########################################
# Could change to cloudformation parameter by core.CfnParameter(app,"Pass-in-parameters",)
rs_instance_type = "dc2.large"
rs_node_count = 1
rs_username = "awsuser"
rs_password = "Adim1234"
tpcds_data_path = 's3://redshift-downloads/TPC-DS/2.13/3TB/'
parallel_level = 10
num_runs = 1
num_files = 10


#################### Upload scripts to S3 that could be inferred by following tasks ######################
asset = S3Assets(app, "repository",local_directory="scripts")

############ Set up VPC and redshift cluster, redshift cluster will reside in public subnet ##############
vpc_stack = VPCStack(app,"vpc-stack")
redshift_stack = RedshiftStack(app,"Redshift-stack",vpc_stack
    ,ec2_instance_type=rs_instance_type
    ,master_user=rs_username
    ,password=rs_password
    ,node_num=rs_node_count)

# Use glue workflow and jobs to conduct benchmark tasks include parallel query execution and concurrent query execution
benchmark_workflow = RedshiftBenchmarkStack(app,"Glue-redshift-benchmark-workflow"
    ,dbname=redshift_stack.get_cluster.db_name
    ,host=redshift_stack.get_cluster.attr_endpoint_address
    ,port=redshift_stack.get_cluster.attr_endpoint_port
    ,username=redshift_stack.get_cluster.master_username
    ,password=redshift_stack.get_cluster.master_user_password
    ,s3_bucket=asset.get_bucket
    ,rs_role_arn=redshift_stack.get_role_arn
    ,tpcds_root_path=tpcds_data_path
    ,parallel_level=parallel_level
    ,num_runs=num_runs
    ,num_files=num_files
    )
   
app.synth()
