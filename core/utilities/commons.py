import logging


class Status:
    FAIL = 'fail'
    SUCCESS = 'success'
    NULL = 'unset'
    NotFound = 'not found'

    def __init__(self, status_type=None, description=None, id=''):
        self.type = status_type or self.NULL
        self._description = description or 'Nenhuma ação realizada ou o status não foi definido'
        self.id = id

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    def set_status(self, status_type=None, description=None, id=''):

        if status_type in {self.FAIL, self.SUCCESS}:
            self.type = status_type
        else:
            raise ValueError("Status inválido. Use FAIL ou SUCCESS.")
        self.description = description
        self.id = id
        logging.error(description)


