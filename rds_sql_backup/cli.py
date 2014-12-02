import yaml
import click

from rds_sql_backup import core


@click.command()
@click.option('--config-file', default='config.yml',
              help="Path to config file.")
@click.option('--storage', default='s3',
              help='Storage to use for storing the sql-dump')
def main(config_file, storage):
    with open(config_file) as config_file_p:
        config = yaml.load(config_file_p)
        core.dump_database(rds_db_name=config['rds_instance_id'],
                           aws_id=config['aws_access_key_id'],
                           aws_secret_key=config['aws_secret_access_key'],
                           aws_region=config['aws_region'],
                           db_conf=config['db'])
