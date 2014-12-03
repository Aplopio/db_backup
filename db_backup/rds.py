from __future__ import print_function
from datetime import datetime
from dateutil.parser import parse as dateparse

from boto import rds

import wait
__all__ = ['RDS']

SLEEP_FOR = 5


class RDS(object):

    def __init__(self, aws_id, aws_secret_key, aws_region):
        """Sets aws rds connection."""
        self.conn = rds.connect_to_region(
            aws_region, aws_access_key_id=aws_id,
            aws_secret_access_key=aws_secret_key)

    def get_latest_snapshot(self, rds_instance_id):
        """Takes a db name and gets the latest snapshot for that db."""
        snapshots = self.conn.get_all_dbsnapshots(instance_id=rds_instance_id)
        if not snapshots:
            return None
        snap = max(snapshots,
                   key=lambda x: dateparse(x.snapshot_create_time))
        return snap.id

    def create_new_snapshot(self, db):
        """Given a db a completely new snapshot is created for it."""

    def create_instace_from_snapshot(self, snapshot_id, subnet_group):
        """Given a snapshot a new db instance is created from it."""
        instance_name = "sql-bkp-tmp-{}".format(
            datetime.now().strftime('%y-%b-%d-%H-%M-%S'))
        instance = self.conn.restore_dbinstance_from_dbsnapshot(
            identifier=snapshot_id, instance_id=instance_name,
            instance_class='db.t2.medium', multi_az=False,
            db_subnet_group_name=subnet_group)

        def while_wating(instance, old_state):
            instance.update()
            if instance.status != old_state:
                print()
                print(instance.status)
            return instance, instance.status

        wait.wait_for(
            while_wating=while_wating,
            condition=lambda instance, *args: instance.status != 'available',
            args=[instance, instance.status])
        return instance

    def get_instance(self, db_instance_id):
        """Given a db_instance_id get the db_instance"""
        return self.conn.get_all_dbinstances(db_instance_id)[0]

    def delete_instance(self, db_instance_id):
        """Given a db_instance delete it."""
        self.conn.delete_dbinstance(db_instance_id, skip_final_snapshot=True)

    def get_host(self, db_instance):
        """Given a db_instance return the hostname for it."""
        return db_instance.endpoint[0]
