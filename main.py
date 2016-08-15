#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import define, options
from skeleton.routes import routes

from utils.config import ConfigManager

define(
    'env', default='local',
    help='Target environment e.g. mthomas, stg, prod', type=str)
config = None


def get_config(args):
    global config
    if config is None:
        # Get config from conf manager based on provided env
        env = options.env
        logging.info('Loading new config for env: %s', env)
        config = ConfigManager.load(env, 'skeleton')
    return config


class Application(tornado.web.Application):
    def __init__(self):
        handlers = routes()
        tornado.web.Application.__init__(self, handlers, **config)


def main():
    fmt = '%(asctime)s %(levelname)-8.8s %(message)s'
    logging.basicConfig(format=fmt)
    logging.root.setLevel('INFO')

    tornado.options.parse_command_line()

    global config
    config = get_config(options)

    app = Application()
    app.listen(int(config['port']))

    logging.info('Starting skeleton app on port %d', int(config['port']))

    if config['debug']:
        tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
