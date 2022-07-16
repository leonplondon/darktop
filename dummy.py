import os
import random
import time

from constants import SLEEP_TIMES
from multiprocessing import Process


class OwnershipNoProvidedException(Exception):
    def __init__(self,):
        self.message = 'A uid was not provided to take process ownership'

    def __str__(self):
        return self.message


def child_process():
    sleep_time = random.choice(SLEEP_TIMES)
    time.sleep(sleep_time)

    while True:
        """
        This is a child a process
        """
        time.sleep(random.choice(SLEEP_TIMES))


def create_process():
    p_child = Process(
        target=child_process,
        name='child_process',
    )

    p_child.start()
    p_child.join()


if __name__ == "__main__":
    uid = os.environ.get('CUSTOM_UID')

    if not uid:
        raise OwnershipNoProvidedException()

    uid = int(uid)
    os.setuid(uid)

    create_process()

    while True:
        """
        This is a dummy process, no I/O required, demostrative purpose only
        This is a parent process
        """
        time.sleep(5)
