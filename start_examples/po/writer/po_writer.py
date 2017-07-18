from nilsson.start_examples.po.config_po_states import waiting_new_line, command_channel
from nilsson.start_examples.po.msg_model.msg_collection import MsgCollection
from nilsson.start_examples.po.state_machine_model.controller import Controller
from nilsson.start_examples.po.state_machine_model.state_machine import StateMachine
from nilsson.start_examples.po.utils import join_by_new_line


class PoWriter:

    def __init__(self):
        pass

    @staticmethod
    def new():
        return PoWriter()

    def write_lines(self, msg_collection):
        result = []
        for msg in msg_collection:
            result.append('\n')
            for path in msg.paths:
                result.append('#: {}'.format(path))
            result.append('msgid "{}"'.format(msg.id))
            result.append('msgstr "{}"'.format(msg.str))
        return result
