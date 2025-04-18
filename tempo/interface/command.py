import traceback

from tempo.interface import response
from tempo.utils.logging import log_and_print, error_log_and_print
from tempo.utils.files import load_settings
from tempo.utils.status import StatusReadWrite


class ExecutionError(Exception):
    pass


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


class SubmitObservation(BaseCommand):
    def execute_command(self):
        return self.response()


class GenObservation(BaseCommand):
    def execute_command(self):
        return self.response()


class EditObservation(BaseCommand):
    def execute_command(self):
        return self.response()


class Status(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Status, self).__init__(*args, **kwargs)

    def print(self, string):
        _settings = load_settings()
        log_and_print(
            string, logfile=self.logfile, request=self.request, log=_settings['LOGSTATUS'],
            verbose=_settings['PRINTSTATUS']
        )

    def execute_command(self):
        self.print(self.status.get_status_str())
        return self.response()


COMMANDS = {
    'SUBMIT': SubmitObservation,
    'GENERATE': GenObservation,
    'STATUS': Status,
    'EDIT': EditObservation,
}

skip_updates = {'STATUS'}


def execute_command(interface_command='TEST 0', request=None, status=None):
    split_command = interface_command.split()
    command = split_command[0].upper()
    command = command
    if status is None:
        status = StatusReadWrite()
    log_and_print('received command: {}'.format(interface_command), request=request)
    if command not in skip_updates:
        status.update_current_command(command)
    try:
        arguments = split_command[1:]
    except IndexError:
        arguments = []
    try:
        tcs_command = COMMANDS[command](arguments, interface_command, status=status, request=request)
        command_response = tcs_command.execute_command()
        if command not in skip_updates:
            status.update_command_complete()
        return command_response
    except ConnectionAbortedError:
        if command not in skip_updates:
            status.update_command_complete()
        tb = traceback.format_exc()
        raise ConnectionAbortedError(tb)
    except Exception as e:
        if command not in skip_updates:
            status.update_command_complete()
        tb = traceback.format_exc()
        if not load_settings()['ERRORNAK']:
            error_log_and_print('Received message "{}", but generated error'.format(interface_command))
            error_log_and_print(tb)
            return tb
        else:
            raise ExecutionError(e)
