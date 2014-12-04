from __future__ import print_function
from rds import RDS
import db_instance_creater
import data_backup_creater


def backup_data(config):
    """
    1. Create an instance from the latest snapshot.
    2. Backup the data to s3 given an instance.
    3. Delete the instance.
    """
    instance_id = db_instance_creater.create_from_latest_snapshot(config)
    print('Created instance', instance_id)

    data_backup_creater.dump_gzip_backkup(instance_id, config)

    print('Deleting instance', instance_id)
    rds = RDS(aws_id=config['aws_access_key_id'],
              aws_secret_key=config['aws_secret_access_key'],
              aws_region=config['aws_region'])
    rds.delete_instance(instance_id)
