from rds import RDS


def create_from_latest_snapshot(config):
    rds = RDS(aws_id=config['aws_access_key_id'],
              aws_secret_key=config['aws_secret_access_key'],
              aws_region=config['aws_region'])
    snapshot = rds.get_latest_snapshot(
        rds_instance_id=config['rds_instance_id'])
    instance = rds.create_instace_from_snapshot(
        snapshot, config['rds_subnet_group'])
    return instance.id
