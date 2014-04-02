import curses
from github import Github
from subprocess import call
from settings import GITHUB_USER, GITHUB_PW, REPO_LIST, JIRA_SERVER


def is_keyboard_arrow(key):
    arrow_keys = [curses.KEY_UP, curses.KEY_DOWN]
    if key in arrow_keys:
        return True
    else:
        return False

def launch_jira(ticket):
    call(['open', JIRA_SERVER + 'browse/' + ticket['ticketname']])

def launch_gh(pr):
        api_url = pr.url
        url = api_url.replace('api.', '')
        url = url.replace('repos/', '')
        url = url.replace('pulls', 'pull')
        call(['open', url])

def fetch_prs(on_success=None):
    results = lookup_prs()
    if on_success:
        on_success(results)
    else:
        return results

def lookup_prs():
    repo_list = REPO_LIST
    g = Github(GITHUB_USER, GITHUB_PW)
    result = []
    for repo_name in repo_list:
        repo = g.get_repo(repo_name)

        for pr in repo.get_pulls():
            if pr.user.login == GITHUB_USER:
                result.append(pr)
    return result