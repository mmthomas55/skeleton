from tornado.web import RequestHandler
import logging


class PingHandler(RequestHandler):
    def get(self):
        logging.info("Ping handler")
