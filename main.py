import curses
import os
import re
import threading
import time

from constants import (
    APP_TITLE, FIELDS_EXPLANATION, AVAILABLE_OPERATIONS, ID_REGEX,
    INVALID_PROCESS_ID, INVALID_USER_ID, PID_TO_KILL, PROCESS_COLUMNS,
    STRING_PAGINATION, STRING_PROCESS_ATTRIBUTES_PLACEHOLDER,
    STRING_PROCESS_HEADER, STRING_USER_PLACE_HOLDER,
)

from input_handler import (
    show_input_window,
    show_tmp_text
)

from math import ceil

from process_not_found import ProcessError

from processes import (
    create_process_with_child_with_user, get_running_processes, kill_process,
)

from users import (
    current_user, get_user_list
)


# Variables to control navigation over large lists
p_current_page = 0
p_total_pages = 65536
u_current_page = 0
u_total_pages = 65536

# Reference to previous process' screen
w_previous_ps_list = None

# Run indefinitely a threa for querying processes list
loop_for_process = True


def create_process_reader_thread(on_list_updated):
    """
    Spawn a new thread to query the list of processes
    """
    process_thread = threading.Thread(
        target=process_reader,
        args=(on_list_updated,)
    )
    process_thread.setDaemon(True)
    process_thread.start()


def process_reader(on_list_updated):
    """
    Funtion to be called from another thread, in charge of querying processes
    """
    while loop_for_process:
        processes = get_running_processes()
        on_list_updated(processes)
        time.sleep(0.5)


def show_processes(ps_list, stdscr):
    """
    When a new process' list is ready to be displayed, this function must be called
    """

    global p_current_page, p_total_pages
    global w_previous_ps_list

    yw, xw = stdscr.getmaxyx()

    border_and_padding = 2 + 2
    border_lines = 2
    title_lines = 1
    window_lines = yw - 6

    if xw <= PROCESS_COLUMNS:
        w_columns = xw
    else:
        w_columns = xw - 25

    max_processes = window_lines - title_lines - border_lines
    p_total_pages = ceil(len(ps_list) / max_processes)

    if p_current_page >= p_total_pages:
        p_current_page = p_total_pages - 1

    end_position = w_columns - border_and_padding

    if w_previous_ps_list:
        w_previous_ps_list.clear()
        w_previous_ps_list.refresh()

    w_process = stdscr.subwin(window_lines, w_columns, 6, 0)
    w_previous_ps_list = w_process
    w_process.border()

    w_process.addstr(
        1, 2, STRING_PROCESS_HEADER[0:end_position], curses.color_pair(1)
    )
    w_process.refresh()

    actual_page = STRING_PAGINATION.format(p_current_page + 1, p_total_pages)
    w_process.addstr(0, 2, actual_page)
    w_process.refresh()

    start_of_page = p_current_page * max_processes
    end_of_page = start_of_page + max_processes
    processes_sublist = ps_list[start_of_page:end_of_page]

    for index, process in enumerate(processes_sublist):
        uid = process[0]
        pid = process[1]
        ppid = process[2]
        command = process[7]

        if len(command) >= (w_columns - 27):
            command = '...{}'.format(command[-((w_columns - 27) - 3):])

        process_info = STRING_PROCESS_ATTRIBUTES_PLACEHOLDER.format(
            ppid.ljust(5, ' '),
            pid.ljust(5, ' '),
            uid.ljust(10, ' '),
            command.ljust(60, ' ')
        )[0:end_position]

        w_process.addstr(index + 2, 2, process_info)

        w_process.refresh()


def show_kill_command_window(stdscr):
    """
    Initiates the flow to allow user to kill a process
    """

    pid = show_input_window(stdscr, PID_TO_KILL)

    if not re.match(ID_REGEX, pid):
        show_tmp_text(stdscr, INVALID_PROCESS_ID)
        return

    try:
        kill_process(int(pid))

        show_tmp_text(
            stdscr,
            'SIGKILL signal sent to process {}'.format(pid)
        )
    except ProcessError as pnf:
        show_tmp_text(stdscr, str(pnf))
    except Exception as ex:
        show_tmp_text(
            stdscr,
            'Shell command raises exception: {0}'.format(ex)
        )


def on_new_process_list(ps_list, stdscr):
    """
    Callback funtion to perform updates on processes' list
    """

    try:
        show_processes(ps_list, stdscr)
    except Exception as _:
        pass


def show_help_window(stdscr):
    """
    Draw the header view of the UI with important information
    """

    _, xw = stdscr.getmaxyx()
    border_and_padding = 2 + 2
    end_position = xw - border_and_padding

    w_app_header = stdscr.subwin(5, xw, 0, 0)
    w_app_header.border()

    title_decoration = curses.color_pair(1)
    w_app_header.addstr(1, 2, APP_TITLE[0:end_position], title_decoration)
    w_app_header.addstr(2, 2, FIELDS_EXPLANATION[0:end_position])
    w_app_header.addstr(3, 2, AVAILABLE_OPERATIONS[0:end_position])

    w_app_header.refresh()


def show_users_window(stdscr):
    """
    Show users in OS
    """

    global u_current_page
    global u_current_page

    yw, xw = stdscr.getmaxyx()

    if xw <= PROCESS_COLUMNS:
        return

    w_columns = 25
    w_lines = yw - 6

    border_and_padding = 2 + 2
    border_lines = 2

    user_list = get_user_list()
    max_users = w_lines - border_lines
    u_total_pages = ceil(len(user_list) / max_users)

    if u_current_page >= u_total_pages:
        u_current_page = u_total_pages - 1

    end_position = w_columns - border_and_padding

    w_user_list = stdscr.subwin(w_lines, w_columns, 6, xw - 25)

    w_user_list.clear()
    w_user_list.border()

    start_page = u_current_page * max_users
    end_of_page = start_page + max_users
    user_sublist = user_list[start_page:end_of_page]

    user_pagination = STRING_PAGINATION.format(
        u_current_page+1,
        u_total_pages
    )
    user_title = ' Users {} '.format(user_pagination)[0:end_position]
    w_user_list.addstr(0, 1, user_title, curses.color_pair(1))

    yi = 1
    for index, user in enumerate(user_sublist):
        user_line = STRING_USER_PLACE_HOLDER.format(
            str(user.uid).ljust(5, ' '),
            user.name
        )

        y_pos = yi + index

        if current_user().uid != user.uid:
            w_user_list.addstr(y_pos, 2, user_line[0:end_position])
            continue

        current_user_color = curses.color_pair(1)
        w_user_list.addstr(
            y_pos, 2, user_line[0:end_position], current_user_color
        )

    w_user_list.refresh()


def init_colors():
    """
    Prepare colors to be used to add some styles to UI
    """

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)


def handle_kill_process(key_pressed_code, stdscr):
    """
    Handle keyboard input to start killing processes
    """

    if key_pressed_code == ord('k'):
        show_kill_command_window(stdscr)


def handle_process_navigation(key_pressed_code, _):
    """
    Handle keyboard input to navigate in process list
    """

    global p_current_page
    global p_total_pages

    if key_pressed_code == curses.KEY_LEFT:
        p_current_page = max(0, p_current_page - 1)

    if key_pressed_code == curses.KEY_RIGHT:
        p_current_page = min(p_total_pages - 1, p_current_page + 1)


def handle_resize(key_pressed_code, stdscr):
    """
    Handle keyboard input to handle screen resizing
    """

    if key_pressed_code == curses.KEY_RESIZE:
        stdscr.clear()
        stdscr.refresh()

        show_users_window(stdscr)
        show_help_window(stdscr)


def handle_start_processes(key_pressed_code, stdscr):
    if key_pressed_code == ord('s'):
        start_process(stdscr)


def handle_user_navigation(key_pressed_code, stdscr):
    """
    Handle keyboard input to navigate in user list
    """

    global u_current_page
    global u_total_pages

    if key_pressed_code == curses.KEY_DOWN:
        u_current_page = max(0, u_current_page - 1)
        show_users_window(stdscr)

    if key_pressed_code == curses.KEY_UP:
        u_current_page = min(u_total_pages - 1, u_current_page + 1)
        show_users_window(stdscr)


def start_process(stdscr):
    """
    Start a dummy process to show behavior of parent/child processes
    """

    uid = show_input_window(stdscr, 'Type user\'s id to use:')

    if not re.match(ID_REGEX, uid):
        show_tmp_text(stdscr, INVALID_USER_ID)
        return

    #  Transform this UID into a valid integer
    uid = int(uid)

    # We look for a user with the provided uid
    user_found = [user for user in get_user_list() if user.uid == uid]

    # Checking if a valid user was found
    if not len(user_found):
        show_tmp_text(stdscr, 'User no found in OS')
        return

    # Check for permissions
    if not(os.getuid() == 0 or os.getuid() == uid):
        show_tmp_text(
            stdscr,
            'No permissions, try running the app as root/sudo'
        )
        return

    try:
        pid = create_process_with_child_with_user(uid)
        show_tmp_text(
            stdscr,
            'Process started with pid={} and uid={}'.format(pid, uid)
        )
    except Exception as ex:
        show_tmp_text(
            stdscr,
            'Exception starting process: {0}'.format(ex)
        )


def curses_ui(stdscr):
    """
    Prepare UI
    """

    global loop_for_process

    stdscr.clear()

    init_colors()

    show_help_window(stdscr)
    show_users_window(stdscr)

    create_process_reader_thread(
        lambda ps_list: on_new_process_list(ps_list, stdscr)
    )

    while True:
        key_pressed_code = stdscr.getch()

        handle_kill_process(key_pressed_code, stdscr)
        handle_process_navigation(key_pressed_code, stdscr)
        handle_resize(key_pressed_code, stdscr)
        handle_start_processes(key_pressed_code, stdscr)
        handle_user_navigation(key_pressed_code, stdscr)

        if key_pressed_code == ord('q') or key_pressed_code == ord('Q'):
            loop_for_process = False
            break


if __name__ == "__main__":
    """
    App entry point
    """

    curses.wrapper(curses_ui)
