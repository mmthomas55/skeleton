"""
Config Manager
==============

A wrapper for reading values through Vault's API. Will only look for
values that are not found as environment variables.
"""

import os
import logging

import hvac

# Export env variables to mimic envconsul
os.environ['debug'] = 'True'
os.environ['port'] = '80'
os.environ['VAULT_TOKEN'] = 'b930ad4f-444e-8223-f0a1-5b8eb80e238d'


# This can come from an env file or some other constant in the repo
CONFIG = [
    'port',
    'debug',
    'super_secret_token'
]


class ConfigManager(object):
    @classmethod
    def load(cls, env, app):
        return cls(env, app)()


    def __init__(self, env, app):
        """Constructor for Config Manager service.

        Args:
            env (string): Name of the environment (e.g. mthomas, qa)
            app (string): Name of the application (e.g skeleton)
        """

        # Can be switched to TLS with https and use cert
        self.secret_client = hvac.Client(
            url='http://localhost:8200', token=os.environ['VAULT_TOKEN'])
        self.env = env
        self.app = app
        self.domain = '/'.join([app, env])


    def __call__(self):
        """Reads configs from environment variables. If environment variable does
        not exist, asks for it from Vault.

        Returns:
            dict: Config key/value pairs
        """
        config_dict = {}

        for item in CONFIG:
            if item in os.environ:
                config_dict[item] = os.getenv(item)
            else:
                config_dict[item] = self.read_secret(item)

        logging.info(config_dict)
        return config_dict


    def read_secret(self, item):
        """Reads secret by key from Vault.

        Args:
            item (string): Vault key to look for

        Returns:
            string: Value from Vault for the key provided
        """
        prefix = 'secret/%s' % self.domain
        logging.info('Prefix: %s', prefix)

        secret_item = super_secret_value = self.secret_client.read(
                '%s/%s' % (prefix, item))

        # Raise error to prevent app from starting
        if not secret_item:
            logging.error('Not Found: %s', item)
            raise ConfigManagerException('Item Not Found: %s', item)

        logging.info('Secret Found: %s', item)
        return secret_item['data'][item]


class ConfigManagerException(Exception):
    # TODO: error logger
    pass
