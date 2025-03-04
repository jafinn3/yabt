import os
import yaml
import subprocess
import shutil

CWD = os.getcwd()

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
    YABT_CONFIG_FILE = f'{CWD}/yabt_config.yaml'
    with open (os.path.expanduser(YABT_CONFIG_FILE)) as f:
        config = yaml.safe_load(f)

    assert(validate_yabt_config(config))
    return config

def reset_crons():
    with open(f'{CWD}/yabt_crontab', 'w'):
        pass
    config = get_yabt_config()

    crontab_lines = ''
    for repo in config['repositories']:
        schedule = config['repositories'][repo]['cron']
        source_dir = config['repositories'][repo]['source_dir']
        yabt_dir = config['repositories'][repo]['yabt_dir']
        cmd = f'{CWD}/yabt_backup.sh --source_dir {source_dir} --yabt_dir {yabt_dir} >> {CWD}/cronjob.log 2>&1'
        cron_job = f'{schedule} {cmd}\n'
        crontab_lines += cron_job

    with open(f'{CWD}/yabt_crontab', 'w') as f:
        f.write(cron_job)
    subprocess.run(['crontab', f'{CWD}/yabt_crontab'], check=True)

def init_repo(repo_name, source_dir, yabt_dir, cron):
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

    with open(os.path.expanduser(f'{CWD}/yabt_config.yaml'), 'w') as f:
        yaml.dump(config, f)

    os.makedirs(yabt_dir, exist_ok=True)
    reset_crons()

def delete_repo(repo_name, delete_backups):
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

    with open(os.path.expanduser(f'{CWD}/yabt_config.yaml'), 'w') as f:
        yaml.dump(config, f)

    subprocess.run(['crontab', '-r'], check=True)

init_repo('test', '/tmp/data0', '/tmp/yabt9', '0 0 * * *')
