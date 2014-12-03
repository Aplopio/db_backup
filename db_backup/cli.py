import yaml
import click

from db_backup import data_backup


@click.command()
@click.option('--config-file', default='config.yml',
              help="Path to config file.")
def main(config_file):
    with open(config_file) as config_file_p:
        config = yaml.load(config_file_p)
        data_backup.backup_data(config)
