from jira.client import JIRA
from settings import JIRA_NAME, JIRA_PW, JIRA_SERVER
import persistence

class JiraWrapper:
    def __init__(self):
        if not hasattr(self, '_jira'):
            self._jira = JIRA(
                basic_auth=(JIRA_NAME, JIRA_PW),
                options={'server': JIRA_SERVER}
            )
        self._issue = None


    def get_info(self):
        return {
            'ticketname': self._issue.key,
            'reporter': self._issue.fields.reporter.displayName,
            'updated': self._issue.fields.updated,
            'description': self._issue.fields.description,
            'issuetype': self._issue.fields.issuetype,
            'labels': self._issue.fields.labels,
            'priority': self._issue.fields.priority,
            'status': self._issue.fields.status,
            'summary': self._issue.fields.summary,
            'assignee': self._issue.fields.assignee.displayName
        }


    def set_issue(self, issue_str):
        self.issue_str = issue_str
        # change to try/catch
        if persistence.has_ticket(issue_str):
            self._issue = persistence.lookup_ticket(issue_str)
        else:
            self._issue = self._jira.issue(issue_str)
            persistence.store_ticket(self._issue)


    def get_states(self):
        self._states = []

        t = self._jira.transitions(self._issue)
        for i in t:
            self._states.append({i['to']['name'], i['id']})
            print '%s: %s' % (i['id'], i['to']['name'])


    def set_state(self, id):
        self._jira.transition_issue(self._issue, str(id))
        self.get_states()


    def exec_jql(self, jql):
        return self._jira.search_issues(jql)