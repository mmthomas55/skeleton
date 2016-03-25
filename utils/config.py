import etcd
import logging


# TODO: Hostname should get passed in?

class ConfigManager(object):
    @classmethod
    def load(cls, env, app):
        return cls(env, app)()

    def __init__(self, env, app):
        self.config_client = etcd.Client(
            host='172.17.8.101', port=2379, protocol='http',
            version_prefix='/v2'
        )
        self.env = env
        self.app = app
        self.domain = '/'.join([app, env])

    def __call__(self):
        prefix = "/%s" % self.domain
        logging.info("Prefix: %s", prefix)

        try:
            config = self.config_client.read(prefix, recursive=True)
        except etcd.EtcdKeyNotFound:
            raise ConfigManagerException("Domain Not Found: %s" % self.domain)

        config_dict = {
            result.key.split("%s/" % prefix)[1]: result.value
            for result in config.children
        }
        logging.info(config_dict)
        return config_dict


class ConfigManagerException(Exception):
    # TODO: error logger
    pass
