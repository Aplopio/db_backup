from datetime import datetime
import subprocess

import wait
from rds import RDS


def dump_gzip_backkup(instance_id, config):
    rds = RDS(aws_id=config['aws_access_key_id'],
              aws_secret_key=config['aws_secret_access_key'],
              aws_region=config['aws_region'])
    instance = rds.get_instance(instance_id)
    host = rds.get_host(instance)
    s3_location = 's3://{}/{}/mysql-{}-{}.bkp.gz'.format(
        config['s3_bucket'], config['s3_prefix'],
        instance_id, datetime.now().strftime('%y-%b-%d-%H-%M-%S'))
    create_backup(host, s3_location, db_user=config['db_user'],
                  db_password=config['db_password'], db_name=config['db_name'])


def create_backup(host, s3_location, db_user, db_password, db_name):
    command_str = ('mysqldump --opt --add-drop-table --max_allowed_packet=256M'
                   ' --single-transaction --order-by-primary'
                   ' -h {host} -u {db_user} -p{db_password} {db_name}'
                   ' | gzip -9 -c | aws s3 cp - {s3_location}').format(
                       host=host, db_user=db_user, db_password=db_password,
                       db_name=db_name, s3_location=s3_location)
    mysql_dump_command = subprocess.Popen(command_str, shell=True)

    wait.wait_for(
        condition=lambda mysql_dump_command: mysql_dump_command.poll() is None,
        args=[mysql_dump_command])