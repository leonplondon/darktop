class ProcessError(Exception):
    def __init__(self, pid: int) -> None:
        self.pid = pid

    def __str__(self) -> str:
        return 'An error ocurred or no such process with pid={0}'.format(self.pid)
