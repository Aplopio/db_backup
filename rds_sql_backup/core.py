import rds
import mysql


def get_sql_dumper(db_type):

    if db_type == 'mysql':
        return mysql


def dump_database(db_name, aws_id, aws_secret_key, user, password,
                  tmp_file_loc='/tmp/', source='latest-snapshot',
                  db_type='mysql'):
    """Allows to create a data dump from an rds instance."""
    conn = rds.get_conn(aws_id, aws_secret_key)
    snapshot = rds.get_latest_snapshot(conn, db_name)
    assert snapshot, ("There is no snapshot for this instance. You can "
                      "try `source=new-snapshot` to create a new snapshot and "
                      "then dump that.")
    db_instance = rds.create_instace_from_snapshot(conn, snapshot)
    sql_dumper = get_sql_dumper(db_type)
    sql_dumper.dump(rds.get_host(db_instance), user, password, tmp_file_loc)
    rds.delete_instace(db_instance)
