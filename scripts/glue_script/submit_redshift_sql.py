# This is the Glue python-shell script to submit a Redshift SQL script to redshift cluster
# Author : Liulu He
# Version: 1.0

# AWS data wrangler environment preparation. Reference:https://github.com/boto/boto3/issues/2566

import os.path
import subprocess
import sys
import logging
import sys
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv,['dbname',
                                    #'cluster_id',
                                    'host',
                                    'port',
                                    'username',
                                    'password',
                                    'sql_script_bucket',
                                    'sql_script_key',
                                    'role_arn',
                                    'tpcds_root_path'])

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


# Download the sql code from S3 in the repository
import boto3
s3 = boto3.resource('s3')
obj = s3.Object(args['sql_script_bucket'], args['sql_script_key'])
sql_script = obj.get()['Body'].read().decode('utf-8')
# Check if any pass in paramters 
if args['role_arn'] != '':
    sql_script=sql_script.replace('<rs_role_arn>',args['role_arn']).replace('<tpcds_root_path>',args['tpcds_root_path'])


import pg


def get_connection(host,port,db_name,user,password_for_user):
    rs_conn_string = "host=%s port=%s dbname=%s user=%s password=%s" % (
        host, port, db_name, user, password_for_user)

    rs_conn = pg.connect(dbname=rs_conn_string)
    rs_conn.query("set statement_timeout = 1200000")
    return rs_conn


def query(con,statement):
    root.info("Execute SQL %s"%statement)
    res = con.query(statement)
    return res

con1 = get_connection(args['host'],args['port'],args['dbname'],args['username'],args['password'])
res = query(con1,sql_script)

root.info("SQL return is %s"%res)
