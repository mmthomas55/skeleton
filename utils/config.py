"""
Config Manager
==============

A wrapper for reading values through Vault's API. Will only look for
values that are not found as environment variables. Will unseal Vault
for use and re-seal it on completion.
"""

import os
import logging

import hvac

# Export env variables to mimic envconsul
os.environ['debug'] = 'True'
os.environ['port'] = '80'

# Vault's client token, which can be specific to the app
os.environ['VAULT_TOKEN'] = 'b930ad4f-444e-8223-f0a1-5b8eb80e238d'


# Keys that Vault was unsealed with. Don't ever do this!
KEYS = [
    '0fa78da2342f12ccc23f576cffef40b7f79c240f4ebe88d535f1e88bdf8ddce101',
    'c7c338f2946fe6816b2e635a363daa872c8a21d1fc0e0f806c88b3efd060222902',
    'c556ee13aef5bcf0a7f36cfca04f7dfc15bb81e7bd3a9e16f12610e68d39a3d303',
    '97e6e081b4e3679071cebac06ccdfb9867ec00d42d048923829c02bfabbf202604',
    '957336608e793de1bd13b566fabf2ce35edda0e26c3018b51f32a1b6f6e6a1dc05'
]


# This can come from an env file or some other constant in the repo
APP_CONFIG = [
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
        self.env = env
        self.app = app
        self.domain = '/'.join([app, env])

        # Can be switched to TLS with https and use cert
        self.secret_client = hvac.Client(
            url='http://localhost:8200', token=os.environ['VAULT_TOKEN'])

        if self.secret_client.is_sealed():
            logging.info('Unsealing Vault...')
            self.secret_client.unseal_multi(KEYS[:3])

            logging.info('Vault is successfully unsealed')


    def __call__(self):
        """Reads configs from environment variables. If environment variable does
        not exist, asks for it from Vault. Reseals Vault when finished.

        Returns:
            dict: Config key/value pairs
        """
        config_dict = {}

        for item in APP_CONFIG:
            if item in os.environ:
                config_dict[item] = os.getenv(item)
            else:
                config_dict[item] = self.read_secret(item)

        logging.info(config_dict)

        # Re-seal Vault
        self.secret_client.seal()
        logging.info('Vault is successfully sealed.')

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

        secret_item = self.secret_client.read(
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
