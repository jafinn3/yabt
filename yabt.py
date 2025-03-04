import os
import yaml
import shutil

def validate_yabt_config(config):
    if 'repositories' not in config:
        return False

    for repo in config['repositories']:
        if 'source_dir' not in config['repositories'][repo]:
            return False
        if 'yabt_dir' not in config['repositories'][repo]:
            return False
        if 'cron' not in config['repositories'][repo]:
            return False

    return True

def get_yabt_config():
    YABT_CONFIG_FILE = "~/.yabt/yabt_config.yaml"
    with open (os.path.expanduser(YABT_CONFIG_FILE)) as f:
        config = yaml.safe_load(f)

    assert(validate_yabt_config(config))
    return config

def init_repo(repo_name, source_dir, yabt_dir, cron):
    if os.path.exists(yabt_dir) and os.listdir(yabt_dir) != []:
        print('[ERROR] yabt_dir already exists')
        exit(1)

    if not os.path.exists(source_dir):
        print('[ERROR] source_dir does not exist')
        exit(1)

    config = get_yabt_config()
    if repo_name in config['repositories']:
        print('[ERROR] repo already exists')
        exit(1)

    config['repositories'][repo_name] = {
        'source_dir': source_dir,
        'yabt_dir': yabt_dir,
        'cron': cron
    }

    with open(os.path.expanduser('~/.yabt/yabt_config.yaml'), 'w') as f:
        yaml.dump(config, f)

    os.makedirs(yabt_dir, exist_ok=True)
