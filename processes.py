import os
import signal
import subprocess
import sys

from operator import itemgetter

from process_not_found import ProcessError


def get_running_processes():
    cmd_result = subprocess.check_output(
        'ps -Af; exit 0;',
        stderr=subprocess.STDOUT,
        shell=True
    ).splitlines()

    processes = [line.decode().split() for line in cmd_result[1:]]
    return sorted(processes, key=itemgetter(7))


def kill_process(pid):
    parent_error = None
    child_error = None

    try:
        os.killpg(pid, signal.SIGKILL)
        return
    except Exception as ex:
        parent_error = ex

    try:
        os.kill(pid, signal.SIGKILL)
        return
    except Exception as ex:
        child_error = ex

    if child_error or parent_error:
        raise ProcessError(pid)


def create_process_with_child_with_user(uid: int = 0) -> int:
    result = subprocess.Popen(
        [sys.executable, './dummy.py'],
        env={'CUSTOM_UID': str(uid)},
        preexec_fn=os.setsid
    )
    return result.pid
