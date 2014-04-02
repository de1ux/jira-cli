import curses
import thread
from time import sleep

from jira_api import lookup_in_progress, lookup_in_code_review, lookup_in_todo
from ui_utils import write_one_liner
from utils import is_keyboard_arrow, launch_jira
from constants import KEY_ENTER


class JiraWorkflow:
    def __init__(self, scr):
        # Ticket loaders
        self.in_progress_tickets = []
        self.in_code_review_tickets = []
        self.in_todo_tickets = []

        self.scr = scr
        self.base_y = 1
        self.current_selection = 0
        self.loaded = 0

        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        # implement local disk! do not want reloads
        thread.start_new_thread(lookup_in_progress, (self.show_in_progress, ))
        thread.start_new_thread(lookup_in_code_review, (self.show_in_code_review, ))
        thread.start_new_thread(lookup_in_todo, (self.show_in_todo, ))
        thread.start_new_thread(self.draw_selector, ())


    def route(self, choice):
        if is_keyboard_arrow(choice):
            self.update_selection(choice)
        elif choice == KEY_ENTER:
            # yuck. assembly shouldnt be done here
            tickets = self.in_todo_tickets + self.in_progress_tickets + \
                self.in_code_review_tickets
            ticket = tickets[self.current_selection]
            launch_jira(ticket)
        else:
            return False

        return True


    def draw_selector(self):
        # TODO - better blocking mechanism
        while self.loaded != 3:
            sleep(1)

        y = self.current_selection
        adjust = 2
        if y+1 > len(self.in_todo_tickets):
            adjust += 2
        if y+1 > len(self.in_todo_tickets) + len(self.in_progress_tickets):
            adjust += 2

        self.scr.addstr(y + adjust, 1, '>')
        self.scr.refresh()

    # TODO - make shared across GithubWorkflow
    def clear_selector(self):
        y = self.current_selection
        adjust = 2
        if y+1 > len(self.in_todo_tickets):
            adjust += 2
        if y+1 > len(self.in_todo_tickets) + len(self.in_progress_tickets):
            adjust += 2

        self.scr.addstr(y + adjust, 1, ' ')
        self.scr.refresh()


    def update_selection(self, direction):
        self.clear_selector()
        selections = len(self.in_progress_tickets) + len(self.in_todo_tickets) + \
            len(self.in_code_review_tickets)

        def up(self):
            self.current_selection -= 1
            if self.current_selection < 0:
                self.current_selection = selections - 1

        def down(self):
            self.current_selection += 1
            if self.current_selection > selections - 1:
                self.current_selection = 0

        options = {
            curses.KEY_UP: up,
            curses.KEY_DOWN: down,
        }
        options[direction](self)
        self.draw_selector()


    def show_in_progress(self, tickets):
        while self.loaded < 1:
            sleep(.01)

        local_y = self.base_y
        self.base_y += len(tickets) + 2
        self.loaded += 1

        self.scr.addstr(local_y, 2, ' In Progress   ', curses.color_pair(2) + curses.A_UNDERLINE)
        for ticket in tickets:
            local_y += 1
            write_one_liner(self.scr, local_y, ticket['ticketname'] + ': ' + ticket['summary'])

        self.in_progress_tickets = tickets


    def show_in_code_review(self, tickets):
        while self.loaded < 2:
            sleep(.01)

        local_y = self.base_y
        self.base_y += len(tickets) + 2
        self.loaded += 1

        self.scr.addstr(local_y, 2, ' Code Review   ', curses.color_pair(2) + curses.A_UNDERLINE)
        for ticket in tickets:
            local_y += 1
            write_one_liner(self.scr, local_y, ticket['ticketname'] + ': ' + ticket['summary'])

        self.in_code_review_tickets = tickets


    def show_in_todo(self, tickets):
        local_y = self.base_y
        self.base_y += len(tickets) + 2
        self.loaded += 1

        self.scr.addstr(local_y, 2, ' To Do   ', curses.color_pair(2) + curses.A_UNDERLINE)
        for ticket in tickets:
            local_y += 1
            write_one_liner(self.scr, local_y, ticket['ticketname'] + ': ' + ticket['summary'])

        self.in_todo_tickets = tickets
