# See ./requirements.txt for requirements.
import os

from jira.client import JIRA

from st2reactor.sensor.base import PollingSensor


class JIRASensor(PollingSensor):
    '''
    Sensor will monitor for any new projects created in JIRA and
    emit trigger instance when one is created.
    '''
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(JIRASensor, self).__init__(sensor_service=sensor_service,
                                         config=config,
                                         poll_interval=poll_interval)

        self._jira_url = None
        # The Consumer Key created while setting up the "Incoming Authentication" in
        # JIRA for the Application Link.
        self._jira_client = None
        self._username = ''
        self._password = ''
        self._projects_available = None
        self._poll_interval = 30
        self._project = None
        self._issues_in_project = None
        self._jql_query = None
        self._trigger_name = 'issues_tracker'
        self._trigger_pack = 'jira_basic'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

    def setup(self):
        self._jira_url = self._config['url']
        self._username = self._config['username']
        self._password = self._config['password']
        self._poll_interval = self._config.get('poll_interval', self._poll_interval)

        self._jira_client = JIRA(options={'server': self._jira_url},
                                 basic_auth=(self._username, self._password))
        if self._projects_available is None:
            self._projects_available = set()
            for proj in self._jira_client.projects():
                self._projects_available.add(proj.key)
        self._project = self._config.get('project', None)
        if not self._project or self._project not in self._projects_available:
            raise Exception('Invalid project (%s) to track.' % self._project)
        self._jql_query = 'project=%s' % self._project
        all_issues = self._jira_client.search_issues(self._jql_query, maxResults=None)
        self._issues_in_project = {issue.key: issue for issue in all_issues}

    def poll(self):
        self._detect_new_issues()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _detect_new_issues(self):
        loop = True
        while loop:
            new_issues = self._jira_client.search_issues(self._jql_query, maxResults=50,
                                                         startAt=0)
            for issue in new_issues:
                if issue.key not in self._issues_in_project:
                    self._dispatch_issues_trigger(issue)
                    self._issues_in_project[issue.key] = issue
                else:
                    loop = False  # Hit a task already in issues known. Stop getting issues.
                    break

    def _dispatch_issues_trigger(self, issue):
        trigger = self._trigger_ref
        payload = {}
        payload['issue_name'] = issue.key
        payload['issue_url'] = issue.self
        payload['issue_browse_url'] = self._jira_url + '/browse/' + issue.key
        payload['project'] = self._project
        payload['created'] = issue.raw['fields']['created']
        payload['assignee'] = issue.raw['fields']['assignee']
        payload['fix_versions'] = issue.raw['fields']['fixVersions']
        payload['issue_type'] = issue.raw['fields']['issuetype']['name']
        self._sensor_service.dispatch(trigger, payload)
