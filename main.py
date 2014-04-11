import curses
from jira_workflow import JiraWorkflow
from github_workflow import GithubWorkflow
from option_handler import main_menu as options
from ui_utils import append_cmd_bar, error_message, show_opening_animation
from constants import KEY_TAB


def main(scr, workflow=None, new=True):
    if new:
        curses.curs_set(0)
        show_opening_animation(scr)
        append_cmd_bar(scr, options)

    if not workflow:
        workflow = JiraWorkflow(scr)

    choice = scr.getch()
    # workflows return false if the route is undefined
    is_recognized_keypress = workflow.route(choice)

    if not is_recognized_keypress:
        if choice == KEY_TAB:
            if 'JiraWorkflow' in repr(workflow):
                workflow = GithubWorkflow(scr)
            else:
                workflow = JiraWorkflow(scr)
            is_new = True
        elif choice == ord('q'):
            exit()
        else:
            is_new = False
            error_message(scr, 'Command not recognized' + str(choice) + ' ' + repr(workflow))

    main(scr, workflow, new=is_new)

curses.wrapper(main)
