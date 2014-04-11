import thread
import curses
from time import sleep
from math import floor

"""
    append_cmd_bar
"""
def append_cmd_bar(scr, options):
    yx = scr.getmaxyx()
    x = yx[1] - 1
    yx = (yx[0], x)
    bars = []

    for i, option in enumerate(options):
        if len(option['name']) > yx[1]:
            # trim if longer than screen
            option['name'] = option['name'][0:yx[1]]

        if len(bars):
            proposed_string = bars[-1] + ' ' + option['name']
            if len(proposed_string) < yx[1]:
                bars[-1] = proposed_string
            else:
                bars.append(option['name'])
        else:
            proposed_string = option['name']
            bars.append(option['name'])


    for i, bar in enumerate(reversed(bars)):
        scr.addstr(yx[0] - (i + 2), 1, bar, curses.A_BOLD)


"""
    error_message
"""
def error_message(scr, text):
    yx = scr.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    scr.addstr(yx[0]-1, 0, text, curses.color_pair(1))
    scr.refresh()
    def clear_msg(scr, text):
        sleep(2)
        scr.addstr(yx[0]-1, 0, ' ' * len(text))
        scr.refresh()

    thread.start_new_thread(clear_msg, (scr, text))

"""
    write_one_liner
"""
def write_one_liner(scr, y, text):
    yx = scr.getmaxyx()
    if len(text) < yx[1] - 3:
        scr.addstr(y, 2, text)
    else:
        x = yx[1] - 3
        scr.addstr(y, 2, text[0:x-2] + '...')


"""
    show_opening_animation
    desc: simple visual displayed when the app is opened
    params: <curses screen>scr
    returns: None
"""
def show_opening_animation(scr):
    yx = scr.getmaxyx()
    center = [int(floor(i / 2)) for i in yx]

    for i in range(0, center[0]):
        scr.clear()
        scr.addstr(center[0], center[1], 'wf')
        draw_box(scr, center, i)

        if i*2 + 5 <= yx[0]:
            draw_box(scr, center, i+2)

        scr.refresh()
        sleep(.05)

    scr.clear()
    scr.refresh()


def draw_box(scr, center, width):
    for i in range(center[1] - width, center[1] + width):
        scr.addstr(center[0] + width, i, '.')
        scr.addstr(center[0] - width, i, '.')

    for i in range(center[0] - width, center[0] + width):
        scr.addstr(i, center[1] - width, '.')
        scr.addstr(i, center[1] + width, '.')