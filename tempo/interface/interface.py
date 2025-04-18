from tempo.gcn.kafka import get_kafka_consumer

class BaseListener(object):
    def __init__(self, logfile=None, request=None, *args, **kwargs):
        pass

    def listen(self):
        pass

    def process_message(self, message):
        pass


class GCNListener(BaseListener):
    def listen(self):
        consumer = get_kafka_consumer()
        while True:
            for message in consumer.consume(timeout=1):
                if message.error():
                    print(message.error())
                    continue
                # Print the topic and message ID
                print(f'topic={message.topic()}, offset={message.offset()}')
                value = message.value()
                print(value.decode('utf8'))


class SlackListener(BaseListener):
    pass


class DiscordListener(BaseListener):
    pass


if __name__ == '__main__':
    listener = GCNListener()
    listener.listen()
