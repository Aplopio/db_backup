from __future__ import print_function
import time
from datetime import datetime
from dateutil.parser import parse as dateparse

from boto import rds

__all__ = ['get_conn', 'get_latest_snapshot', 'create_new_snapshot',
           'create_instace_from_snapshot', 'delete_instance']

SLEEP_FOR = 5


def get_conn(aws_id, aws_secret_key, aws_region):
    """Get aws rds connection."""
    return rds.connect_to_region(aws_region, aws_access_key_id=aws_id,
                                 aws_secret_access_key=aws_secret_key)


def get_latest_snapshot(conn, db):
    """Takes a db name and gets the latest snapshot for that db."""
    snaps = sorted(conn.get_all_dbsnapshots(instance_id=db), reverse=True,
                   key=lambda x: dateparse(x.snapshot_create_time))
    print(snaps)
    if snaps:
        return snaps[0]


def create_new_snapshot(conn, db):
    """Given a db a completely new snapshot is created for it."""


def create_instace_from_snapshot(conn, snapshot):
    """Given a snapshot a new db instance is created from it."""
    instance_name = "sql-bkp-tmp-{}".format(
        datetime.now().strftime('%y-%b-%d'))
    instance = conn.restore_dbinstance_from_dbsnapshot(
        identifier=snapshot.id, instance_id=instance_name,
        instance_class='db.t2.medium', multi_az=False,
        db_subnet_group_name='accessgroup')
    inst_status = instance.status
    time_taken = 0
    while instance.status != 'available':
        time.sleep(SLEEP_FOR)
        time_taken += SLEEP_FOR
        instance.update()
        print(inst_status)
        if inst_status != instance.status:
            inst_status = instance.status
            print()
            print(inst_status)
        else:
            print('.', sep='', end='')
        if time_taken % 60 == 0:
            print()
            print('Has waited for', time_taken/60, 'm')

    return instance


def delete_instance(db_instance):
    """Given a db_instance delete it."""


def get_host(db_instance):
    """Given a db_instance return the hostname for it."""
    return db_instance.endpoint[0]
