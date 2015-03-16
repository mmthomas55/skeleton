from skeleton.handlers.ping_handler import PingHandler

def routes():
    return [
        (r"/ping", PingHandler)]
