import yaml
from io import open


class Config:

    def __init__(self, env):
        self._env = env

        config = self._get_config()
        self.client_id = config.get('client_id')
        self.client_secret = config.get('client_secret')
        self.user_agent = config.get('user_agent')

    def _get_config(self):
        with open('./config/config.yml', 'r') as f:
            all_configs = yaml.safe_load(f)
            return all_configs.get(self._env)


config = Config('development')
