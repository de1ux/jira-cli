from curses.ascii import ctrl
from jira_wrapper import JiraWrapper
from threading import Thread
from settings import REPO_LIST, GITHUB_USER, GITHUB_PW, JIRA_TEAM

def lookup_ticket_by_name(ticket_no, results=None, persistence=None):
    if not persistence:
        persistence = JiraWrapper()
    persistence.set_issue(ticket_no)
    if results:
        results.append(persistence.get_info())
    else:
        return persistence.get_info()

def lookup_in_progress(on_success=None):
    j = JiraWrapper()
    raw = j.exec_jql('project=' + JIRA_TEAM + ' and assignee=currentUser() and status="In Progress"')
    threads, results = ([], [])

    for ticket in raw:
        threads.append(
            Thread(target=lookup_ticket_by_name, args=(ticket, results, j))
        )
        threads[-1].start()
    [t.join() for t in threads]

    if on_success:
        on_success(results)
    else:
        return results

def lookup_in_code_review(on_success=None):
    j = JiraWrapper()
    raw = j.exec_jql('project=' + JIRA_TEAM + ' and assignee=currentUser() and status="Code Review"')
    threads, results = ([], [])

    for ticket in raw:
        threads.append(
            Thread(target=lookup_ticket_by_name, args=(ticket, results, j))
        )
        threads[-1].start()
    [t.join() for t in threads]

    if on_success:
        on_success(results)
    else:
        return results

def lookup_in_todo(on_success=None):
    j = JiraWrapper()
    raw = j.exec_jql('project=' + JIRA_TEAM + ' and assignee=currentUser() and status="New"')
    threads, results = ([], [])

    for ticket in raw:
        threads.append(
            Thread(target=lookup_ticket_by_name, args=(ticket, results, j))
        )
        threads[-1].start()
    [t.join() for t in threads]

    if on_success:
        on_success(results)
    else:
        return results
