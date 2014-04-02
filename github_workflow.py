import curses
import thread
from utils import fetch_prs, is_keyboard_arrow, launch_gh
from ui_utils import error_message
from constants import KEY_ENTER


class GithubWorkflow:
    def __init__(self, scr):
        self.scr = scr
        self.current_selection = 0
        self.scr.clear()
        thread.start_new_thread(fetch_prs, (self.on_fetch_prs, ))


    def route(self, choice):
        if is_keyboard_arrow(choice):
            self.update_selection(choice)
        elif choice == KEY_ENTER:
            launch_gh(self.prs[self.current_selection])
        else:
            return False

        return True


    def update_selection(self, choice):
        self.clear_selector()
        self.draw_selector(choice)


    def draw_selector(self, choice=None):
        def up(self):
            self.current_selection -= 1
            if self.current_selection == -1:
                self.current_selection = len(self.prs) - 1

        def down(self):
            self.current_selection += 1
            if self.current_selection == len(self.prs):
                self.current_selection = 0

        if choice:
            self.clear_selector()
            options = {
                curses.KEY_UP: up,
                curses.KEY_DOWN: down,
            }
            options[choice](self)

        self.scr.addstr(self.current_selection + 2, 0, '>')


    def clear_selector(self):
        self.scr.addstr(self.current_selection + 2, 0, ' ')


    def draw_prs(self):
        for i, pr in enumerate(self.prs):
            self.scr.addstr(i + 2, 2, pr.title)


    def on_fetch_prs(self, prs):
        self.prs = prs
        self.clear_selector()
        self.draw_prs()
        self.draw_selector()
        self.scr.refresh()
