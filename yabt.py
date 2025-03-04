import os
import yaml
import subprocess
import shutil
import argparse

CWD = os.getcwd()
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def validate_yabt_config(config):
    if 'repositories' not in config.keys():
        return False

    if config['repositories'] == None:
        return True

    for repo in config['repositories']:
        if 'source_dir' not in config['repositories'][repo]:
            return False
        if 'yabt_dir' not in config['repositories'][repo]:
            return False
        if 'cron' not in config['repositories'][repo]:
            return False

    return True

def get_yabt_config():
    YABT_CONFIG_FILE = f'{SCRIPT_DIR}/yabt_config.yaml'
    with open (os.path.expanduser(YABT_CONFIG_FILE)) as f:
        config = yaml.safe_load(f)

    assert(validate_yabt_config(config))
    return config

def reset_crons():
    with open(f'{SCRIPT_DIR}/yabt_crontab', 'w'):
        pass
    config = get_yabt_config()

    crontab_lines = ''
    for repo in config['repositories']:
        schedule = config['repositories'][repo]['cron']
        source_dir = config['repositories'][repo]['source_dir']
        yabt_dir = config['repositories'][repo]['yabt_dir']
        cmd = f'{SCRIPT_DIR}/yabt_backup.sh --source_dir {source_dir} --yabt_dir {yabt_dir} >> {SCRIPT_DIR}/cronjob.log 2>&1'
        cron_job = f'{schedule} {cmd}\n'
        crontab_lines += cron_job

    with open(f'{SCRIPT_DIR}/yabt_crontab', 'w') as f:
        f.write(cron_job)
    subprocess.run(['crontab', f'{SCRIPT_DIR}/yabt_crontab'], check=True)

def init(args):
    repo_name = args.name
    yabt_dir = args.directory
    source_dir = CWD
    cron = args.cron

    if os.path.exists(yabt_dir) and os.listdir(yabt_dir) != []:
        print('[ERROR] yabt_dir already exists')
        exit(1)

    if not os.path.exists(source_dir):
        print('[ERROR] source_dir does not exist')
        exit(1)

    config = get_yabt_config()
    if config['repositories'] is not None and repo_name in config['repositories']:
        print('[ERROR] repo already exists')
        exit(1)

    if config['repositories'] is None:
        config['repositories'] = {}

    config['repositories'][repo_name] = {
        'source_dir': source_dir,
        'yabt_dir': yabt_dir,
        'cron': cron
    }

    with open(os.path.expanduser(f'{SCRIPT_DIR}/yabt_config.yaml'), 'w') as f:
        yaml.dump(config, f)

    os.makedirs(yabt_dir, exist_ok=True)
    reset_crons()

def delete(args):
    repo_name = args.name
    delete_backups = args.delete_backups
    if delete_backups:
        print('[WARNING] This will delete all backups. Proceed? (y/n)')
        answer = input()
        if answer != 'y':
            exit(0)

    config = get_yabt_config()
    if repo_name not in config['repositories']:
        print(f'[ERROR] Trying to delete non-existent repo {repo_name}')
        exit(1)

    if delete_backups:
        shutil.rmtree(config['repositories'][repo_name]['yabt_dir'])

    del config['repositories'][repo_name]

    with open(os.path.expanduser(f'{SCRIPT_DIR}/yabt_config.yaml'), 'w') as f:
        yaml.dump(config, f)

    subprocess.run(['crontab', '-r'], check=True)

def create_parser():
    parser = argparse.ArgumentParser(description="yabt - Yet Another Backup Tool")

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser('init', help="Initialize a backup for the current directory.")
    init_parser.add_argument('name', help="The name of the backup.")
    init_parser.add_argument('directory', help="The directory in which to store the backups.")
    init_parser.add_argument('cron', help="The cron schedule for the backup.")
    init_parser.set_defaults(func=init)

    delete_parser = subparsers.add_parser('delete', help="Removes a directory from YABT tracking.")
    delete_parser.add_argument('name', help="The name of the backup to delete.")
    delete_parser.add_argument('-D', '--delete-backups', dest='delete_backups', action='store_true', help="Deletes all YABT data associated with the directory. WARNING: This will result in data loss.")
    delete_parser.set_defaults(func=delete)

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
