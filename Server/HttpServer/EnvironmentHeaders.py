import os


class ServerEnvironmentVariables(object):
    server_env_vars = {}

    def __init__(self, **kwargs):
        self.server_env_vars.update(**kwargs)

    def set_env_var(self, key, value):
        self.server_env_vars[key] = value

    def get_env_vars(self):
        return self.server_env_vars
