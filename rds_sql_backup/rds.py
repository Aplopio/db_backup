def get_conn(aws_id, aws_secret_key):
    """Get aws rds connection."""


def get_latest_snapshot(conn, db):
    """Takes a db name and gets the latest snapshot for that db."""


def create_new_snapshot(conn, db):
    """Given a db a completely new snapshot is created for it."""


def create_instace_from_snapshot(conn, snapshot):
    """Given a snapshot a new db instance is created from it."""


def delete_instance(db_instance):
    """Given an db_instance delete it."""
