import rds
import mysql

__all__ = ['dump_database', 'upload_file']


def get_sql_dumper(db_type):

    if db_type == 'mysql':
        return mysql


def dump_database(rds_db_name, aws_id, aws_secret_key, aws_region, db_conf,
                  tmp_file_loc='/tmp/', source='latest-snapshot'):
    """Allows to create a data dump from an rds instance."""
    conn = rds.get_conn(aws_id, aws_secret_key, aws_region)
    snapshot = rds.get_latest_snapshot(conn, rds_db_name)
    assert snapshot, ("There is no snapshot for this instance. You can "
                      "try `source=new-snapshot` to create a new snapshot and "
                      "then dump that.")
    db_instance = rds.create_instace_from_snapshot(conn, snapshot)
    sql_dumper = get_sql_dumper(db_conf.get('type', 'mysql'))
    sql_dump_file = sql_dumper.dump(rds.get_host(db_instance),
                                    db_conf['database'], db_conf['user'],
                                    db_conf['password'], tmp_file_loc)
    rds.delete_instace(db_instance)
    return sql_dump_file


def upload_file(local_file_path, storage, settings):
    """Given a local file path, storage settings,
    the fn copies the files to the storage location."""
