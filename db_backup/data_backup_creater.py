from __future__ import print_function
from datetime import datetime
import subprocess

import wait
from rds import RDS

command_to_extension = {'gzip': 'gz',
                        'bzip2': 'bz2',
                        'xz': 'xz'}


def dump_gzip_backkup(instance_id, config):
    rds = RDS(aws_id=config['aws_access_key_id'],
              aws_secret_key=config['aws_secret_access_key'],
              aws_region=config['aws_region'])
    instance = rds.get_instance(instance_id)
    host = rds.get_host(instance)
    compress_command = config.get('compress_command', 'gzip')
    assert compress_command in command_to_extension
    s3_location = 's3://{}/{}/mysql-{}.bkp.{}'.format(
        config['s3_bucket'], config['s3_prefix'],
        datetime.now().strftime('%y-%b-%d-%H-%M-%S'),
        command_to_extension[compress_command])
    print('Uploading to', s3_location)
    create_backup(host, s3_location, db_user=config['db_user'],
                  db_password=config['db_password'], db_name=config['db_name'],
                  compress_command=compress_command)


def create_backup(host, s3_location, db_user, db_password, db_name,
                  compress_command='gzip'):
    command_str = ('mysqldump --opt --add-drop-table --max_allowed_packet=256M'
                   ' --single-transaction --order-by-primary'
                   ' -h {host} -u {db_user} -p{db_password} {db_name}'
                   ' | {compress_command} -9c |'
                   ' aws s3 cp - {s3_location}').format(
                       host=host, db_user=db_user, db_password=db_password,
                       db_name=db_name, s3_location=s3_location,
                       compress_command=compress_command)
    mysql_dump_command = subprocess.Popen(command_str, shell=True)

    wait.wait_for(
        condition=lambda mysql_dump_command: mysql_dump_command.poll() is None,
        args=[mysql_dump_command])
