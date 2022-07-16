import curses
import time

from curses.textpad import Textbox


def show_input_window(stdscr, text, sep=' ', amount=5):
    """
    Show label and field to accept user's input
    """

    input_color = curses.color_pair(3)

    _, xw = stdscr.getmaxyx()

    display_text = '{}{}'.format(text, sep)

    w_pid_input = stdscr.subwin(1, xw, 5, 0)
    w_pid_input.bkgd(' ', input_color)
    w_pid_input.addstr(0, 0, display_text)
    w_pid_input.refresh()

    w_input = w_pid_input.subpad(1, amount + 1, 5, len(display_text))

    box = Textbox(w_input)
    box.edit()

    user_input = box.gather().strip()

    w_pid_input.clear()
    w_pid_input.refresh()

    return user_input


def show_tmp_text(stdscr, text: str = ''):
    """
    Show a dismissable message to the user, it lasts 3 seconds
    """

    input_color = curses.color_pair(3)

    _, xw = stdscr.getmaxyx()

    w_pid_input = stdscr.subwin(1, xw, 5, 0)
    w_pid_input.bkgd(' ', input_color)
    w_pid_input.addstr(0, 0, text[0:xw - 4])
    w_pid_input.refresh()

    wait_clear(w_pid_input)


def wait_clear(window):
    time.sleep(3)
    window.clear()
    window.refresh()
