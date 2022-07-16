APP_TITLE = ' PROCESS MANAGER by Dario Peña '.ljust(200, ' ')
ID_REGEX = r'^\d{1,5}$'  # Handle up-to 99999 pid/uid
INVALID_PROCESS_ID = 'It looks like the PID is incorrect'
INVALID_USER_ID = 'It looks like the UID is incorrect'
PID_TO_KILL = 'PID to send kill signal [integer]'
PROCESS_COLUMNS = 87
SLEEP_TIMES = [1, 2, 3, 5, 8]
STRING_PAGINATION = 'Page {}/{}'
STRING_PROCESS_ATTRIBUTES_PLACEHOLDER = '{} {} {} {}'
STRING_USER_PLACE_HOLDER = '{} {}'

AVAILABLE_OPERATIONS = '[{}] [{}] [{}]'.format(
    'k)ill process',
    'q)uit process manager',
    's)tart DUMMY process with child',
)

FIELDS_EXPLANATION = '[{}] [{}] [{}] [{}]'.format(
    'ppid=parent process id',
    'pid=process id',
    'uid=user id',
    'command=process script',
)

STRING_PROCESS_HEADER = STRING_PROCESS_ATTRIBUTES_PLACEHOLDER.format(
    'PPID'.ljust(5, ' '),
    'PID'.ljust(5, ' '),
    'USER'.ljust(10, ' '),
    'COMMAND'.ljust(200, ' ')
)
