#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import define, options
from skeleton.routes import routes

define("port", default=999, help="run on the given port", type=int)
define("debug", default=False, help="Run in debug mode to reload on code changes", type=bool)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = routes()
        settings = { "debug": options.debug}

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    fmt = "%(asctime)s %(levelname)-8.8s %(message)s"
    logging.basicConfig(format=fmt)
    logging.root.setLevel("INFO")

    tornado.options.parse_command_line()

    app = Application()
    app.listen(options.port)

    logging.info("Starting skeleton app on port %d" % options.port)

    if options.debug:
        tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
