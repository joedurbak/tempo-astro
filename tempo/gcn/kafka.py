from gcn_kafka import Consumer

from tempo.utils.settings import GCN


class BaseGCNObject(object):
    pass


class PointSourceObject(object):
    pass


class ProbabilityMapObject(object):
    pass


def get_kafka_consumer(topics=GCN['topics'], client_id=GCN['client_id'], client_secret=GCN['client_secret']):
    consumer = Consumer(client_id=client_id, client_secret=client_secret)
    consumer.subscribe(topics)
    return consumer


def parse_voevent_message(message):
    pass


def parse_message(message):
    return
