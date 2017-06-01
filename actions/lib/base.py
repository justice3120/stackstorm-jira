from jira import JIRA

#  from st2actions.runners.pythonrunner import Action
__all__ = [
    'BaseJiraAction'
]


class Action(object):
    def __init__(self, config):
        self.config = config


class BaseJiraAction(Action):
    def __init__(self, config):
        super(BaseJiraAction, self).__init__(config=config)
        self._client = self._get_client()

    def _get_client(self):
        config = self.config

        options = {'server': config['url']}

        username = config['username']
        password = config['password']

        client = JIRA(options=options, basic_auth=(username, password))
        return client

    def _get_file_content(self, file_path):
        with open(file_path, 'r') as fp:
            content = fp.read()

        return content
