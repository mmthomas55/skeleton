from tornado.web import RequestHandler, HTTPError
import logging

class PingHandler(RequestHandler):
    def get(self):
        logging.info("Ping handler")
