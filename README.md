
# Redshift Benchmark

This CDK project will deploy a clean redshift cluster and a Glue workflow to perform the TPC-DS benchmark test including sequantially run 99 queries and concurrently run 99 queries(10 parallel level). It doesn't include tpcds data. Thus, you need to generate the data first and store it in S3. 


## Prerequisite

* Refer to [CDK website](https://aws.amazon.com/cn/cdk/) for how to install the environment.

* Use TPC-DS generate data and store it in S3 in '|' delimited CSV format

## Deploy Testing Environment

Modify the *app.py* file to set custom paramters

```python
rs_instance_type = "ra3.xlplus" # Redshift instance type
rs_node_count = 2               # Redshift cluster size
rs_username = "XXXX"            # Redshift username
rs_password = "XXXX"            # Redshift user password
tpcds_data_path = 's3://redshift-downloads/TPC-DS/2.13/3TB/'    # TPCDS data path
parallel_level = 10             # concurrent thread count during concurrent query test
num_runs = 1                    # total number of runs
num_files = 99                  # number of sql files(files are under redshift_script/tpcds_queries)
```

Optional: you could use your own SQL files. Just need to put them under redshift_script/tpcds_queries/query[0-9].sql and provide number of total files above

To list current cloudformation stack that could be deployed:

```
$ cdk ls
```

It returns below stacks
```
repository                       # S3 bucket to store assets
vpc-stack                        # A vpc to put Redshift
Redshift-stack                   # Redshift cluster
Glue-redshift-benchmark-workflow # A Glue workflow to perform the benchmark test
```

Use CDK CLI deploy the cloudformations 
```
$ cdk deploy Glue-redshift-benchmark-workflow
```


## Perform Benchmark Test

Go to Glue console -> Workflow, you will see a workflow named 'redshift-benchmark'. Start the workflow and it will perform below tasks:

 * `tpcds-benchmark-create-tables`          Create all tpcds tables
 * `tpcds-benchmark-load-tables`      Use copy command to load data into Redshift tables
 * `tpcds-benchmark-sequential-report`        Do sequential query submit and generate report
 * `tpcds-benchmark-concurrent-report`        Do concurrent query submit and generate report

Above glue jobs can be run individually and manually.

## Check Performance Report

When the Glue workflow completes and succeeds. There are two places you could check the query runtime.

* Job logs of  `tpcds-benchmark-sequential-report`, `tpcds-benchmark-concurrent-report`
* S3 directory of repository cloudformation stack eg. s3://repository-s3assetea84da40-mfflf52ih6b4/report/

## Customize for your own dataset
You could put your own DDL and queries in redshift_scripts/ and replace the TPCDS DDL and queries. And modify the *app.py* parameters `tpcds_data_path` and `num_files` to match your own dataset.
Enjoy!
