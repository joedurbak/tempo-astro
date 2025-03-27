from tempo.interface import response
from tempo.utils.logging import log_and_print

class BaseCommand(object):
    def __init__(self, arguments, received_message, status, logfile=None, request=None, *args, **kwargs):
        self.__name__ = self.__class__.__name__
        # print(self.__name__)
        self.command_render_dict = {}
        self.response_template = response.response.get(self.__name__, response.base)
        self.response_render_dict = {'command_name': self.__name__}
        self.arguments = arguments
        self.received_message = received_message
        self.logfile = logfile
        self.request = request
        self.status = status

    def print(self, string):
        log_and_print(string, logfile=self.logfile, request=self.request)

    def response(self):
        return self.response_template.format(**self.response_render_dict)

    def parse_arguments(self):
        pass

    def execute_command(self):
        return self.response()

    def generate_save_name(self):
        return self.__name__

